#!/usr/bin/env python3

from __future__ import annotations

import json
import re
from datetime import date
from html import escape
from pathlib import Path
from typing import Any
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
SITE_BASE_URL = "https://jswachter.github.io"

NOTEBOOKS_DIR = ROOT / "notebooks"
INDEX_PATH = NOTEBOOKS_DIR / "notebook-index.json"
NOTEBOOKS_HTML_PATH = ROOT / "notebooks.html"
SITEMAP_PATH = ROOT / "sitemap.xml"
ROBOTS_PATH = ROOT / "robots.txt"

LIST_START = "<!-- BEGIN AUTO-GENERATED NOTEBOOK LIST -->"
LIST_END = "<!-- END AUTO-GENERATED NOTEBOOK LIST -->"

KEY_VALUE_RE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*)$")
TAG_ITEM_RE = re.compile(r"^\s*-\s*(.+?)\s*$")
FILENAME_DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def parse_frontmatter(text: str) -> tuple[dict[str, Any], list[str]]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, lines

    meta: dict[str, Any] = {}
    tags_list_mode = False
    i = 1
    while i < len(lines) and lines[i].strip() != "---":
        line = lines[i].rstrip()
        match = KEY_VALUE_RE.match(line)
        if match:
            key = match.group(1).strip()
            value = match.group(2).strip()
            if key == "tags" and value == "":
                meta["tags"] = []
                tags_list_mode = True
            else:
                meta[key] = value
                tags_list_mode = False
        else:
            if tags_list_mode:
                tag_match = TAG_ITEM_RE.match(line)
                if tag_match:
                    meta["tags"].append(tag_match.group(1).strip())
                else:
                    tags_list_mode = False
        i += 1

    content_lines = lines[i + 1 :] if i < len(lines) and lines[i].strip() == "---" else lines
    return meta, content_lines


def parse_tags(raw: Any) -> list[str]:
    if isinstance(raw, list):
        candidates = [str(x).strip() for x in raw]
    else:
        text = str(raw or "").strip()
        if not text:
            return []
        if text.startswith("[") and text.endswith("]"):
            text = text[1:-1]
        candidates = [t.strip() for t in text.split(",")]

    seen: set[str] = set()
    tags: list[str] = []
    for tag in candidates:
        if not tag:
            continue
        key = tag.lower()
        if key in seen:
            continue
        seen.add(key)
        tags.append(tag)
    return tags


def derive_title(meta: dict[str, Any], content_lines: list[str], filename: str) -> str:
    title = str(meta.get("title") or "").strip()
    if title:
        return title
    for line in content_lines:
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return filename.replace(".md", "").replace("-", " ").strip() or "(untitled)"


def derive_date(meta: dict[str, Any], filename: str) -> str:
    raw = str(meta.get("date") or "").strip()
    if raw:
        return raw
    match = FILENAME_DATE_RE.match(filename)
    return match.group(1) if match else ""


def derive_summary(content_lines: list[str]) -> str:
    in_code = False
    parts: list[str] = []

    for line in content_lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if not stripped:
            if parts:
                break
            continue
        if stripped.startswith("#"):
            continue
        if stripped.startswith(">"):
            continue

        cleaned = re.sub(r"^[-*]\s+", "", stripped)
        cleaned = re.sub(r"^\d+\.\s+", "", cleaned)
        cleaned = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cleaned)
        parts.append(cleaned)

        if len(" ".join(parts)) > 220:
            break

    summary = re.sub(r"\s+", " ", " ".join(parts)).strip()
    if len(summary) > 180:
        summary = summary[:177].rstrip() + "..."
    return summary


def safe_data_attr(value: str) -> str:
    # Keep dataset attrs predictable: lowercase, commas, and spaces.
    value = re.sub(r"\s+", " ", value).strip().lower()
    value = value.replace('"', "").replace("'", "")
    return value


def url_quote(value: str) -> str:
    return quote(value, safe="")


def build_index_entries() -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for path in NOTEBOOKS_DIR.rglob("*.md"):
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith("notebooks/drafts/"):
            continue
        if path.name.lower() == "readme.md":
            continue

        text = read_text(path)
        meta, content_lines = parse_frontmatter(text)

        title = derive_title(meta, content_lines, path.name)
        date_str = derive_date(meta, path.name)
        tags = parse_tags(meta.get("tags"))
        collection = str(meta.get("collection") or "").strip() or "General"

        summary = str(meta.get("summary") or "").strip()
        if not summary:
            summary = derive_summary(content_lines)

        entries.append(
            {
                "title": title,
                "date": date_str,
                "path": rel,
                "summary": summary,
                "tags": tags,
                "collection": collection,
            }
        )

    def sort_key(e: dict[str, Any]) -> tuple[str, str]:
        date_str = str(e.get("date") or "")
        title = str(e.get("title") or "")
        # Sort later: we reverse date separately.
        return (date_str, title)

    entries.sort(key=sort_key, reverse=True)
    return entries


def write_notebook_index(entries: list[dict[str, Any]]) -> None:
    generated = ""
    for entry in entries:
        date_str = str(entry.get("date") or "")
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_str):
            generated = max(generated, date_str)
    if not generated:
        generated = date.today().isoformat()

    data = {"generated": generated, "entries": entries}
    content = json.dumps(data, indent=4, ensure_ascii=True) + "\n"
    write_text(INDEX_PATH, content)


def build_entry_html(entry: dict[str, Any]) -> str:
    title = str(entry.get("title") or "(untitled)")
    date_str = str(entry.get("date") or "").strip()
    path = str(entry.get("path") or "")
    tags = entry.get("tags") if isinstance(entry.get("tags"), list) else []
    tags = [str(t).strip() for t in tags if str(t).strip()]
    collection = str(entry.get("collection") or "General").strip() or "General"

    tags_lower = ",".join([t.lower() for t in tags])

    meta_parts: list[str] = []
    if date_str:
        meta_parts.append(escape(date_str))

    meta_parts.append(
        f'<a href="notebooks.html?collection={url_quote(collection)}">{escape(collection)}</a>'
    )

    meta_html = " · ".join(meta_parts)

    return (
        f'<div class="entry" data-title="{escape(title)}" data-date="{escape(date_str)}" '
        f'data-collection="{escape(collection)}" data-tags="{escape(tags_lower)}">\n'
        f'    <h3 class="entry-title"><a href="notebook-viewer.html?entry={url_quote(path)}">{escape(title)}</a></h3>\n'
        f'    <p class="entry-meta">{meta_html}</p>\n'
        f"</div>"
    )


def write_notebooks_page_list(entries: list[dict[str, Any]]) -> None:
    html = read_text(NOTEBOOKS_HTML_PATH)
    if LIST_START not in html or LIST_END not in html:
        raise SystemExit(f"Missing list markers in {NOTEBOOKS_HTML_PATH}")

    generated_lines = []
    for entry in entries:
        generated_lines.append(build_entry_html(entry))

    if not generated_lines:
        generated = '            <p style="color: #888;">No notebook entries yet.</p>'
    else:
        indented_blocks = []
        indent = " " * 12
        for block in generated_lines:
            indented_blocks.append("\n".join([indent + line for line in block.splitlines()]))
        generated = "\n\n".join(indented_blocks)

    before, rest = html.split(LIST_START, 1)
    _, after = rest.split(LIST_END, 1)
    updated = before + LIST_START + "\n" + generated + "\n            " + LIST_END + after
    write_text(NOTEBOOKS_HTML_PATH, updated)


def write_sitemap(entries: list[dict[str, Any]]) -> None:
    urls: list[tuple[str, str]] = []
    urls.append((f"{SITE_BASE_URL}/", ""))
    urls.append((f"{SITE_BASE_URL}/index.html", ""))
    urls.append((f"{SITE_BASE_URL}/notebooks.html", ""))
    urls.append((f"{SITE_BASE_URL}/library.html", ""))

    for entry in entries:
        path = str(entry.get("path") or "").lstrip("/")
        if not path:
            continue
        lastmod = str(entry.get("date") or "")
        urls.append((f"{SITE_BASE_URL}/{path}", lastmod))

    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for loc, lastmod in urls:
        lines.append("    <url>")
        lines.append(f"        <loc>{escape(loc)}</loc>")
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", lastmod):
            lines.append(f"        <lastmod>{escape(lastmod)}</lastmod>")
        lines.append("    </url>")
    lines.append("</urlset>")
    write_text(SITEMAP_PATH, "\n".join(lines) + "\n")


def write_robots() -> None:
    lines = [
        "User-agent: *",
        "Allow: /",
        "",
        f"Sitemap: {SITE_BASE_URL}/sitemap.xml",
        "",
    ]
    write_text(ROBOTS_PATH, "\n".join(lines))


def main() -> None:
    entries = build_index_entries()
    write_notebook_index(entries)
    write_notebooks_page_list(entries)
    write_sitemap(entries)
    write_robots()


if __name__ == "__main__":
    main()
