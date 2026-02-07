#!/usr/bin/env python3
"""
Fetch Goodreads shelf RSS feeds and commit JSON snapshots for use on GitHub Pages.

This is intentionally stdlib-only so it can run in GitHub Actions without installs.
"""

from __future__ import annotations

import datetime
import gzip
import html
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser


SHELVES = ("currently-reading", "to-read", "read")
DEFAULT_QUOTES_MAX_PAGES = 50


def utc_now_iso() -> str:
    return (
        datetime.datetime.now(datetime.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def localname(tag: str) -> str:
    if not tag:
        return ""
    if tag.startswith("{"):
        return tag.split("}", 1)[1]
    return tag


def safe_text(value: str | None) -> str:
    return (value or "").strip()


def build_text_map(item: ET.Element) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for el in item.iter():
        name = localname(el.tag)
        if not name:
            continue
        text = safe_text(el.text)
        if not text:
            continue
        out.setdefault(name, []).append(text)
    return out


def first_text(text_map: dict[str, list[str]], *names: str) -> str:
    for name in names:
        values = text_map.get(name)
        if values:
            return values[0]
    return ""


def fetch_bytes(url: str, timeout_s: int = 30) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "jswachter.github.io goodreads snapshot updater",
            "Accept": "application/rss+xml, application/xml;q=0.9, text/xml;q=0.8, */*;q=0.1",
            "Accept-Encoding": "gzip",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout_s) as resp:
        data = resp.read()
        encoding = (resp.headers.get("Content-Encoding") or "").lower()
        if "gzip" in encoding:
            data = gzip.decompress(data)
        return data


def parse_rss_items(xml_bytes: bytes) -> list[ET.Element]:
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError as exc:
        preview = xml_bytes[:200].decode("utf-8", errors="replace")
        raise ValueError(f"Response was not valid XML. Preview: {preview!r}") from exc

    root_name = localname(root.tag)
    if root_name not in {"rss", "RDF"}:
        raise ValueError(f"Unexpected XML root tag: {root.tag!r}")

    channel = None
    for el in root.iter():
        if localname(el.tag) == "channel":
            channel = el
            break
    if channel is None:
        raise ValueError("No <channel> element found in RSS.")

    items: list[ET.Element] = []
    for el in channel.iter():
        if localname(el.tag) == "item":
            items.append(el)
    return items


def build_rss_url(
    user_id: str, shelf: str, page: int, per_page: int, rss_key: str
) -> str:
    qs: dict[str, str] = {
        "shelf": shelf,
        "page": str(page),
        "per_page": str(per_page),
        "sort": "date_added",
        "order": "d",
    }
    if rss_key:
        qs["key"] = rss_key
    return (
        f"https://www.goodreads.com/review/list_rss/{urllib.parse.quote(user_id)}?"
        f"{urllib.parse.urlencode(qs)}"
    )


def item_from_rss(item_el: ET.Element) -> dict[str, str]:
    m = build_text_map(item_el)

    book_id = first_text(m, "book_id", "bookId", "bookid")
    link = first_text(m, "link")

    # Goodreads feeds typically include both <title> and a book-specific title field.
    title = first_text(m, "book_title", "booktitle", "title")
    author_name = first_text(m, "author_name", "book_author", "bookauthor", "creator", "author")

    # Image URLs may vary by feed version.
    book_small_image_url = first_text(
        m,
        "book_small_image_url",
        "book_small_image",
        "small_image_url",
        "small_image",
    )
    book_image_url = first_text(
        m,
        "book_image_url",
        "book_image",
        "image_url",
        "image",
    )
    book_medium_image_url = first_text(m, "book_medium_image_url", "book_medium_image", "medium_image_url")
    book_large_image_url = first_text(m, "book_large_image_url", "book_large_image", "large_image_url")

    # ISBN can show up in a couple of different fields; keep one output field.
    isbn = first_text(m, "isbn13", "isbn", "book_isbn", "book_isbn13")

    out: dict[str, str] = {
        "book_id": book_id,
        "title": title,
        "author_name": author_name,
        "link": link,
        "book_small_image_url": book_small_image_url,
        "book_image_url": book_image_url,
        "book_medium_image_url": book_medium_image_url,
        "book_large_image_url": book_large_image_url,
        "isbn": isbn,
        "user_rating": first_text(m, "user_rating"),
        "user_read_at": first_text(m, "user_read_at", "read_at"),
        "user_date_added": first_text(m, "user_date_added", "date_added"),
        "user_shelves": first_text(m, "user_shelves", "shelves"),
        "user_review": first_text(m, "user_review", "review"),
        "average_rating": first_text(m, "average_rating"),
        "book_published": first_text(m, "book_published", "published"),
        "pubDate": first_text(m, "pubDate"),
        "guid": first_text(m, "guid"),
    }

    return out


def fetch_shelf(
    user_id: str, shelf: str, per_page: int, max_pages: int, rss_key: str
) -> list[dict[str, str]]:
    seen: set[str] = set()
    out: list[dict[str, str]] = []

    for page in range(1, max_pages + 1):
        url = build_rss_url(user_id=user_id, shelf=shelf, page=page, per_page=per_page, rss_key=rss_key)
        xml_bytes = fetch_bytes(url)
        items = parse_rss_items(xml_bytes)

        if not items:
            break

        for item_el in items:
            item = item_from_rss(item_el)
            key = item.get("book_id") or item.get("link") or item.get("guid") or ""
            if not key:
                key = f"{item.get('title','')}|{item.get('author_name','')}"
            if key in seen:
                continue
            seen.add(key)
            out.append(item)

        # Be polite to Goodreads.
        time.sleep(0.5)

    return out


def write_json(path: str, payload: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=4, ensure_ascii=False)
        f.write("\n")


def build_quotes_url(profile_slug: str, page: int) -> str:
    qs: dict[str, str] = {"page": str(page), "sort": "date_added"}
    return (
        f"https://www.goodreads.com/quotes/list/{urllib.parse.quote(profile_slug)}?"
        f"{urllib.parse.urlencode(qs)}"
    )


class QuotesListParser(HTMLParser):
    """Extract raw quote blocks from Goodreads /quotes/list/<profile_slug> pages."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._in_quote_text = False
        self._quote_div_depth = 0
        self._current_parts: list[str] = []
        self.quote_blocks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "div":
            attr_map = dict(attrs)
            class_attr = safe_text(attr_map.get("class"))
            classes = {c for c in class_attr.split(" ") if c}
            if "quoteText" in classes:
                self._in_quote_text = True
                self._quote_div_depth = 1
                self._current_parts = []
                return
            if self._in_quote_text:
                self._quote_div_depth += 1
                return

        if self._in_quote_text and tag == "br":
            self._current_parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if not self._in_quote_text:
            return
        if tag != "div":
            return
        self._quote_div_depth -= 1
        if self._quote_div_depth > 0:
            return

        raw = "".join(self._current_parts)
        self.quote_blocks.append(raw)
        self._in_quote_text = False
        self._quote_div_depth = 0
        self._current_parts = []

    def handle_data(self, data: str) -> None:
        if self._in_quote_text and data:
            self._current_parts.append(data)


_ATTR_PREFIXES = ("―", "—", "--", "-")


def parse_quote_block(raw: str) -> dict[str, object] | None:
    cleaned = html.unescape(raw).replace("\r", "\n").replace("\u00a0", " ")
    lines = [ln.strip() for ln in cleaned.split("\n")]
    lines = [ln for ln in lines if ln]
    if not lines:
        return None

    attribution = ""
    quote_lines = lines[:]

    for i in range(len(lines) - 1, -1, -1):
        line = lines[i]
        if line in _ATTR_PREFIXES:
            if i + 1 < len(lines):
                attribution = lines[i + 1].lstrip("".join(_ATTR_PREFIXES)).strip()
                quote_lines = lines[:i]
            break
        if line.startswith(_ATTR_PREFIXES):
            attribution = line.lstrip("".join(_ATTR_PREFIXES)).strip()
            quote_lines = lines[:i]
            break

    quote_text = " ".join(quote_lines).strip()
    quote_text = re.sub(r"\s+", " ", quote_text).strip()
    if not quote_text:
        return None

    out: dict[str, object] = {"text": quote_text}
    if attribution:
        out["attribution"] = attribution
    return out


def parse_quotes_html(html_bytes: bytes) -> list[dict[str, object]]:
    doc = html_bytes.decode("utf-8", errors="replace")
    parser = QuotesListParser()
    parser.feed(doc)
    parser.close()

    out: list[dict[str, object]] = []
    for raw in parser.quote_blocks:
        item = parse_quote_block(raw)
        if item:
            out.append(item)
    return out


def fetch_quotes(profile_slug: str, max_pages: int) -> list[dict[str, object]]:
    seen: set[str] = set()
    out: list[dict[str, object]] = []

    for page in range(1, max_pages + 1):
        url = build_quotes_url(profile_slug=profile_slug, page=page)
        html_bytes = fetch_bytes(url)
        items = parse_quotes_html(html_bytes)

        if not items:
            break

        for item in items:
            key = f"{item.get('text','')}|{item.get('attribution','')}"
            if key in seen:
                continue
            seen.add(key)
            out.append(item)

        # Be polite to Goodreads.
        time.sleep(0.5)

    return out


def main() -> int:
    user_id = os.getenv("GOODREADS_USER_ID", "98490343").strip()
    user_slug = os.getenv("GOODREADS_USER_SLUG", "jonatan").strip()
    rss_key = os.getenv("GOODREADS_RSS_KEY", "").strip()
    profile_slug = os.getenv("GOODREADS_PROFILE_SLUG", "").strip()
    per_page_raw = os.getenv("GOODREADS_PER_PAGE", "100").strip()
    max_pages_raw = os.getenv("GOODREADS_MAX_PAGES", "50").strip()
    quotes_max_pages_raw = os.getenv("GOODREADS_QUOTES_MAX_PAGES", "").strip()

    try:
        per_page = int(per_page_raw)
        max_pages = int(max_pages_raw)
    except ValueError:
        print("GOODREADS_PER_PAGE and GOODREADS_MAX_PAGES must be integers.", file=sys.stderr)
        return 2

    if not user_id:
        print("GOODREADS_USER_ID is required.", file=sys.stderr)
        return 2

    if quotes_max_pages_raw:
        try:
            quotes_max_pages = int(quotes_max_pages_raw)
        except ValueError:
            print("GOODREADS_QUOTES_MAX_PAGES must be an integer.", file=sys.stderr)
            return 2
    else:
        quotes_max_pages = DEFAULT_QUOTES_MAX_PAGES

    if not profile_slug and user_slug:
        profile_slug = f"{user_id}-{user_slug}"

    generated_at = utc_now_iso()
    any_written = False

    for shelf in SHELVES:
        try:
            items = fetch_shelf(
                user_id=user_id,
                shelf=shelf,
                per_page=per_page,
                max_pages=max_pages,
                rss_key=rss_key,
            )
        except Exception as exc:
            print(f"Failed to fetch shelf {shelf!r}: {exc}", file=sys.stderr)
            return 1

        payload = {
            "generated_at": generated_at,
            "user": {"id": user_id, "slug": user_slug},
            "shelf": shelf,
            "items": items,
        }

        out_path = os.path.join("goodreads", "shelves", f"{shelf}.json")
        write_json(out_path, payload)
        any_written = True

    if profile_slug:
        try:
            quotes = fetch_quotes(profile_slug=profile_slug, max_pages=quotes_max_pages)
        except Exception as exc:
            # Keep shelf snapshots updating even if Goodreads quote pages change.
            print(f"Failed to fetch quotes: {exc}", file=sys.stderr)
        else:
            payload = {
                "generated_at": generated_at,
                "user": {"id": user_id, "slug": user_slug, "profile_slug": profile_slug},
                "quotes": quotes,
            }
            write_json(os.path.join("goodreads", "quotes.json"), payload)
            any_written = True

    if not any_written:
        print("No shelves were written.", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
