#!/usr/bin/env python3
"""
Fetch Zotero group/collection items and commit a compact JSON snapshot for GitHub Pages.

This is intentionally stdlib-only so it can run in GitHub Actions without installs.
"""

from __future__ import annotations

import datetime
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ZOTERO_CONFIG_PATH = ROOT / "zotero-config.js"

DEFAULT_OUTPUT_PATH = ROOT / "zotero" / "library-items.json"

GROUP_RE = re.compile(r"\bgroupId\s*:\s*['\"]([^'\"]+)['\"]")
COLLECTION_RE = re.compile(r"\bcollectionKey\s*:\s*['\"]([^'\"]+)['\"]")
STYLE_RE = re.compile(r"\bstyle\s*:\s*['\"]([^'\"]+)['\"]")


def utc_now_iso() -> str:
    return (
        datetime.datetime.now(datetime.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_defaults_from_config(path: Path) -> dict[str, str]:
    text = read_text(path)
    group = (GROUP_RE.search(text).group(1) if GROUP_RE.search(text) else "").strip()
    collection = (COLLECTION_RE.search(text).group(1) if COLLECTION_RE.search(text) else "").strip()
    style = (STYLE_RE.search(text).group(1) if STYLE_RE.search(text) else "").strip()
    return {"group_id": group, "collection_key": collection, "style": style}


def is_valid_group_id(value: str) -> bool:
    return bool(re.fullmatch(r"\d+", (value or "").strip()))


def is_valid_collection_key(value: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9]{8}", (value or "").strip()))


def build_collections_url(group_id: str, start: int, limit: int) -> str:
    base = f"https://api.zotero.org/groups/{urllib.parse.quote(group_id)}/collections"
    qs = {
        "v": "3",
        "format": "json",
        "limit": str(limit),
        "start": str(start),
    }
    return f"{base}?{urllib.parse.urlencode(qs)}"


def build_collection_items_url(group_id: str, collection_key: str, style: str, start: int, limit: int) -> str:
    base = f"https://api.zotero.org/groups/{urllib.parse.quote(group_id)}/collections/{urllib.parse.quote(collection_key)}/items/top"
    qs = {
        "v": "3",
        "format": "json",
        "include": "data,bib",
        "style": style,
        "linkwrap": "1",
        "limit": str(limit),
        "start": str(start),
    }
    return f"{base}?{urllib.parse.urlencode(qs)}"


def fetch_json(url: str, api_key: str = "", timeout_s: int = 30) -> Any:
    headers = {
        "User-Agent": "jswachter.github.io zotero snapshot updater",
        "Accept": "application/json",
    }
    if api_key:
        headers["Zotero-API-Key"] = api_key
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout_s) as resp:
        raw = resp.read()
    return json.loads(raw.decode("utf-8"))


KEEP_DATA_FIELDS = {
    "title",
    "creators",
    "date",
    "tags",
    "DOI",
    "doi",
    "url",
    "collections",
}


def compact_item(raw: dict[str, Any]) -> dict[str, Any]:
    data = raw.get("data") if isinstance(raw.get("data"), dict) else {}
    compact_data: dict[str, Any] = {}
    for k in KEEP_DATA_FIELDS:
        if k in data:
            compact_data[k] = data.get(k)

    out: dict[str, Any] = {
        "key": raw.get("key"),
        "data": compact_data,
    }

    if "version" in raw:
        out["version"] = raw.get("version")
    if isinstance(raw.get("bib"), str):
        out["bib"] = raw.get("bib")
    if isinstance(raw.get("links"), dict):
        out["links"] = raw.get("links")

    return out


def compact_collection(raw: dict[str, Any]) -> dict[str, Any]:
    data = raw.get("data") if isinstance(raw.get("data"), dict) else {}
    meta = raw.get("meta") if isinstance(raw.get("meta"), dict) else {}
    return {
        "key": raw.get("key"),
        "name": data.get("name"),
        "parentCollection": data.get("parentCollection"),
        "numCollections": meta.get("numCollections", 0),
        "numItems": meta.get("numItems", 0),
    }


def fetch_paginated(url_builder: Any, api_key: str, page_size: int = 100) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    start = 0

    while True:
        url = url_builder(start, page_size)
        batch = fetch_json(url, api_key=api_key)

        if not isinstance(batch, list) or not batch:
            break

        for raw in batch:
            if isinstance(raw, dict):
                results.append(raw)

        if len(batch) < page_size:
            break

        start += len(batch)
        time.sleep(0.25)

    return results


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=4, ensure_ascii=False)
        f.write("\n")


def main() -> int:
    try:
        defaults = parse_defaults_from_config(ZOTERO_CONFIG_PATH)
    except FileNotFoundError:
        print(f"error: missing {ZOTERO_CONFIG_PATH}", file=sys.stderr)
        return 2

    group_id = (os.environ.get("ZOTERO_GROUP_ID") or defaults.get("group_id") or "").strip()
    collection_key = (os.environ.get("ZOTERO_COLLECTION_KEY") or defaults.get("collection_key") or "").strip()
    style = (os.environ.get("ZOTERO_STYLE") or defaults.get("style") or "apa").strip()

    if not is_valid_group_id(group_id):
        print("error: missing/invalid Zotero group id (ZOTERO_GROUP_ID or zotero-config.js)", file=sys.stderr)
        return 2
    if not is_valid_collection_key(collection_key):
        print("error: missing/invalid Zotero collection key (ZOTERO_COLLECTION_KEY or zotero-config.js)", file=sys.stderr)
        return 2
    if not style:
        print("error: missing Zotero style (ZOTERO_STYLE or zotero-config.js)", file=sys.stderr)
        return 2

    api_key = (os.environ.get("ZOTERO_API_KEY") or "").strip()
    output_path = Path(os.environ.get("ZOTERO_OUTPUT_PATH") or str(DEFAULT_OUTPUT_PATH))
    if not output_path.is_absolute():
        output_path = (ROOT / output_path).resolve()

    try:
        raw_collections = fetch_paginated(
            lambda start, limit: build_collections_url(group_id=group_id, start=start, limit=limit),
            api_key=api_key,
        )
    except urllib.error.HTTPError as exc:
        detail = ""
        try:
            detail = exc.read().decode("utf-8", errors="replace")
        except Exception:
            detail = ""
        print(f"error: Zotero API error ({exc.code}) {detail}".strip(), file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"error: Zotero API request failed: {exc}", file=sys.stderr)
        return 1

    child_collections: list[dict[str, Any]] = []
    for raw in raw_collections:
        data = raw.get("data") if isinstance(raw.get("data"), dict) else {}
        if data.get("deleted"):
            continue
        if str(data.get("parentCollection") or "") != collection_key:
            continue
        if not raw.get("key"):
            continue
        child_collections.append(compact_collection(raw))

    child_collections.sort(key=lambda c: str(c.get("name") or "").lower())

    collection_items: dict[str, list[dict[str, Any]]] = {}
    items_by_key: dict[str, dict[str, Any]] = {}

    try:
        for collection in child_collections:
            child_key = str(collection.get("key") or "").strip()
            if not child_key:
                continue

            raw_items = fetch_paginated(
                lambda start, limit, key=child_key: build_collection_items_url(
                    group_id=group_id,
                    collection_key=key,
                    style=style,
                    start=start,
                    limit=limit,
                ),
                api_key=api_key,
            )

            compact_items = []
            for raw in raw_items:
                if not raw.get("key"):
                    continue
                item = compact_item(raw)
                compact_items.append(item)
                items_by_key[str(raw.get("key"))] = item

            collection_items[child_key] = compact_items
    except urllib.error.HTTPError as exc:
        detail = ""
        try:
            detail = exc.read().decode("utf-8", errors="replace")
        except Exception:
            detail = ""
        print(f"error: Zotero API error ({exc.code}) {detail}".strip(), file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"error: Zotero API request failed: {exc}", file=sys.stderr)
        return 1

    items = list(items_by_key.values())

    payload: dict[str, Any] = {
        "updated_at": utc_now_iso(),
        "source": {
            "group_id": group_id,
            "collection_key": collection_key,
            "style": style,
            "endpoint": "https://api.zotero.org/groups/{group_id}/collections/{collection_key}/items/top",
            "collections_endpoint": "https://api.zotero.org/groups/{group_id}/collections",
        },
        "collections": child_collections,
        "collection_items": collection_items,
        "items": items,
    }

    write_json(output_path, payload)
    print(f"wrote {output_path} ({len(items)} items across {len(child_collections)} collections)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
