#!/usr/bin/env python3

"""
Temporary helper: append a "References" section to a notebook Markdown file by
matching \\cite{...} keys to entries in a BibTeX file.

Idempotent: overwrites the block between BEGIN/END markers.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

BEGIN = "<!-- BEGIN AUTO-GENERATED REFERENCES -->"
END = "<!-- END AUTO-GENERATED REFERENCES -->"

CITE_RE = re.compile(r"\\cite[a-zA-Z]*\{([^}]+)\}")
ENTRY_START_RE = re.compile(r"^\s*@\w+\s*\{\s*([^,\s]+)\s*,", re.MULTILINE)


def split_frontmatter(text: str) -> tuple[str, str]:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return "", text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "".join(lines[: i + 1]), "".join(lines[i + 1 :])
    return "", text


def strip_existing_block(body: str) -> str:
    if BEGIN not in body or END not in body:
        return body
    before, rest = body.split(BEGIN, 1)
    _, after = rest.split(END, 1)
    # Keep a single blank line where the block used to be.
    return before.rstrip() + "\n\n" + after.lstrip()


def extract_cite_keys(text: str) -> list[str]:
    keys: list[str] = []
    seen: set[str] = set()
    for m in CITE_RE.finditer(text):
        raw = m.group(1)
        for key in raw.split(","):
            k = key.strip()
            if not k or k in seen:
                continue
            seen.add(k)
            keys.append(k)
    return keys


def _read_balanced_value(s: str, i: int) -> tuple[str, int]:
    # Reads either { ... } or " ... " value from s starting at i.
    n = len(s)
    while i < n and s[i].isspace():
        i += 1
    if i >= n:
        return "", i

    if s[i] == "{":
        depth = 0
        start = i + 1
        i += 1
        while i < n:
            ch = s[i]
            if ch == "{":
                depth += 1
            elif ch == "}":
                if depth == 0:
                    return s[start:i], i + 1
                depth -= 1
            i += 1
        return s[start:], n

    if s[i] == '"':
        start = i + 1
        i += 1
        while i < n:
            ch = s[i]
            if ch == '"' and s[i - 1] != "\\":
                return s[start:i], i + 1
            i += 1
        return s[start:], n

    # Bareword until comma/newline/brace.
    start = i
    while i < n and s[i] not in ",\n}":
        i += 1
    return s[start:i].strip(), i


def parse_bibtex_entries(text: str) -> dict[str, dict[str, str]]:
    # Very small BibTeX parser: good enough for typical refs.bib.
    entries: dict[str, dict[str, str]] = {}
    starts = [(m.start(), m.group(1)) for m in ENTRY_START_RE.finditer(text)]
    if not starts:
        return entries

    for idx, (pos, key) in enumerate(starts):
        end = starts[idx + 1][0] if idx + 1 < len(starts) else len(text)
        chunk = text[pos:end]
        fields: dict[str, str] = {}

        # Move to after the entry key comma.
        header = ENTRY_START_RE.search(chunk)
        if not header:
            continue
        i = header.end()
        n = len(chunk)

        while i < n:
            # Find field name
            while i < n and chunk[i] not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
                if chunk[i] == "}":
                    i = n
                    break
                i += 1
            if i >= n:
                break
            name_start = i
            while i < n and (chunk[i].isalnum() or chunk[i] in "_-"):
                i += 1
            field_name = chunk[name_start:i].strip().lower()
            if not field_name:
                continue

            # Seek '='
            while i < n and chunk[i] != "=":
                if chunk[i] == "}":
                    i = n
                    break
                i += 1
            if i >= n:
                break
            i += 1  # skip '='

            value, i = _read_balanced_value(chunk, i)
            value = re.sub(r"\s+", " ", value).strip()
            if value:
                fields[field_name] = value

            # Move to next field delimiter
            while i < n and chunk[i] not in ",}":
                i += 1
            if i < n and chunk[i] == ",":
                i += 1
                continue
            if i < n and chunk[i] == "}":
                break

        entries[key] = fields

    return entries


def format_reference(key: str, fields: dict[str, str]) -> str:
    author = fields.get("author") or fields.get("editor") or ""
    title = fields.get("title") or ""
    year = fields.get("year") or fields.get("date") or ""
    container = fields.get("journal") or fields.get("booktitle") or fields.get("publisher") or ""
    doi = fields.get("doi") or ""
    url = fields.get("url") or ""

    parts: list[str] = []
    head = []
    if author:
        head.append(author)
    if year:
        head.append(f"({year})")
    if head:
        parts.append(" ".join(head) + ".")
    if title:
        parts.append(f"*{title}*.")
    if container:
        parts.append(f"{container}.")
    if doi:
        parts.append(f"DOI: `{doi}`.")
    if url:
        parts.append(f"URL: `{url}`.")

    if not parts:
        return f"`{key}`"
    # Always include the cite key at the end for traceability.
    parts.append(f"Key: `{key}`.")
    return " ".join(parts)


def build_references_block(cite_keys: list[str], entries: dict[str, dict[str, str]]) -> str:
    lines: list[str] = []
    lines.append(BEGIN)
    lines.append("")
    lines.append("## References")
    lines.append("")

    if not cite_keys:
        lines.append("_No citations found in this notebook._")
        lines.append("")
        lines.append(END)
        return "\n".join(lines) + "\n"

    missing: list[str] = []
    for i, key in enumerate(cite_keys, start=1):
        fields = entries.get(key)
        if not fields:
            missing.append(key)
            lines.append(f"{i}. Missing BibTeX entry for `{key}`.")
            continue
        lines.append(f"{i}. {format_reference(key, fields)}")

    if missing:
        lines.append("")
        lines.append("Missing keys:")
        lines.append("")
        lines.append(", ".join([f"`{k}`" for k in missing]))

    lines.append("")
    lines.append(END)
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--notebook",
        default=str(ROOT / "notebooks" / "2026-02-09-msc-thesis-introduction.md"),
        help="Notebook Markdown file to update",
    )
    parser.add_argument(
        "--bib",
        default="/Users/jonatanwachter/MSc/MScThesis/thesis_template/refs.bib",
        help="BibTeX file (refs.bib)",
    )
    args = parser.parse_args()

    nb_path = Path(args.notebook).expanduser().resolve()
    bib_path = Path(args.bib).expanduser().resolve()

    nb_text = nb_path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(nb_text)
    if not fm:
        raise SystemExit(f"Notebook missing YAML frontmatter: {nb_path}")

    body_no_block = strip_existing_block(body)
    cite_keys = extract_cite_keys(body_no_block)

    bib_text = bib_path.read_text(encoding="utf-8", errors="replace")
    bib_entries = parse_bibtex_entries(bib_text)

    block = build_references_block(cite_keys, bib_entries)
    new_body = body_no_block.rstrip() + "\n\n" + block
    # Preserve the notebook's conventional single blank line after frontmatter.
    # (Other notes in this repo use: frontmatter, blank line, then H1.)
    nb_path.write_text(fm + new_body, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
