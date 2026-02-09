#!/usr/bin/env python3

"""
Temporary helper: convert a LaTeX thesis introduction chapter to Markdown and
write it into an existing notebook file (preserving YAML frontmatter).

Notes:
- This is a best-effort converter intended for thesis prose + AMS math.
- Display-math environments (align/equation/...) are converted to $$ blocks.
- Labels are stripped from math blocks because most Markdown math renderers
  (e.g. KaTeX) do not support \\label.
"""

from __future__ import annotations

import argparse
import re
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


HEADING_RULES: list[tuple[re.Pattern[str], str]] = [
    # We embed the thesis intro inside a notebook that already has an H1, so
    # LaTeX \chapter becomes Markdown H2.
    (re.compile(r"^\\chapter\{([^}]*)\}.*$", re.MULTILINE), r"## \1"),
    (re.compile(r"^\\section\{([^}]*)\}\s*$", re.MULTILINE), r"### \1"),
    (re.compile(r"^\\subsection\{([^}]*)\}\s*$", re.MULTILINE), r"#### \1"),
    (re.compile(r"^\\subsubsection\{([^}]*)\}\s*$", re.MULTILINE), r"##### \1"),
]


INLINE_RULES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"~\\cite\{"), r" \\cite{"),
    (re.compile(r"\\textbf\{([^}]*)\}"), r"**\1**"),
    (re.compile(r"\\emph\{([^}]*)\}"), r"*\1*"),
    (re.compile(r"\\textit\{([^}]*)\}"), r"*\1*"),
]


THEOREM_BLOCK_RE = re.compile(
    r"(?m)^[ \t]*\\begin\{theorem\}\s*(?P<body>.*?)(?:\n[ \t]*)?\\end\{theorem\}\s*$",
    re.DOTALL | re.MULTILINE,
)

LABEL_CMD_RE = re.compile(r"\\label\{[^}]*\}")
COMMENT_ENV_RE = re.compile(
    r"\\begin\s*\{comment\}.*?\\end\s*\{comment\}",
    re.DOTALL | re.IGNORECASE,
)


def split_frontmatter(text: str) -> tuple[str, str]:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return "", text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            fm = "".join(lines[: i + 1])
            rest = "".join(lines[i + 1 :])
            return fm, rest
    return "", text


def strip_tex_comments(text: str) -> str:
    out_lines: list[str] = []
    for line in text.splitlines():
        if not line:
            out_lines.append(line)
            continue
        # Drop full-line comments; keep inline % since it may appear in text.
        if line.lstrip().startswith("%"):
            continue
        out_lines.append(line)
    return "\n".join(out_lines) + ("\n" if text.endswith("\n") else "")


def strip_comment_environments(text: str) -> str:
    # Remove blocks guarded by the comment environment (from the comment package).
    # Important: these blocks should not appear in the generated notebook.
    return COMMENT_ENV_RE.sub("", text)


def convert_display_math_envs(tex: str) -> str:
    envs = [
        "align",
        "align*",
        "equation",
        "equation*",
        "gather",
        "gather*",
        "multline",
        "multline*",
    ]

    def repl(match: re.Match[str]) -> str:
        env = match.group("env")
        body = match.group("body")
        body = textwrap.dedent(body)
        body = LABEL_CMD_RE.sub("", body)
        body = "\n".join([line.rstrip() for line in body.splitlines()]).strip("\n")

        # Prefer aligned for broad renderer support when the source was align.
        if env in ("align", "align*"):
            body = "\\begin{aligned}\n" + body.strip() + "\n\\end{aligned}"

        return "\n$$\n" + body.strip() + "\n$$\n"

    env_alt = "|".join(re.escape(e) for e in envs)
    pattern = re.compile(
        rf"\\begin\{{(?P<env>{env_alt})\}}(?P<body>.*?)\\end\{{(?P=env)\}}",
        re.DOTALL,
    )
    return pattern.sub(repl, tex)


def convert_theorems(tex: str) -> str:
    def repl(match: re.Match[str]) -> str:
        body = match.group("body")
        body = textwrap.dedent(body).strip()
        body = LABEL_CMD_RE.sub("", body).strip()
        # LaTeX sources often indent theorem bodies; in Markdown that becomes a code block.
        body = re.sub(r"(?m)^[ \t]+", "", body).strip()
        if not body:
            return "**Theorem.**\n"
        return f"**Theorem.**\n\n{body}\n"

    return THEOREM_BLOCK_RE.sub(repl, tex)


def convert_headings(tex: str) -> str:
    for pattern, repl in HEADING_RULES:
        tex = pattern.sub(repl, tex)
    return tex


def apply_inline_rules(tex: str) -> str:
    for pattern, repl in INLINE_RULES:
        tex = pattern.sub(repl, tex)
    return tex


def normalize_whitespace(tex: str) -> str:
    # Remove remaining \label commands (outside math too).
    tex = LABEL_CMD_RE.sub("", tex)
    # Avoid accidental indented-code blocks from LaTeX formatting.
    tex = re.sub(r"(?m)^[ \t]{4,}", "", tex)
    # Collapse excessive blank lines a bit.
    tex = re.sub(r"\n{4,}", "\n\n\n", tex)
    return tex.strip() + "\n"


def convert_tex_to_markdown(tex: str) -> str:
    tex = strip_tex_comments(tex)
    tex = strip_comment_environments(tex)
    tex = convert_display_math_envs(tex)
    tex = convert_theorems(tex)
    tex = convert_headings(tex)
    tex = apply_inline_rules(tex)
    tex = normalize_whitespace(tex)
    return tex


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tex", required=True, help="Path to the LaTeX .tex file to convert")
    parser.add_argument(
        "--notebook",
        default=str(ROOT / "notebooks" / "2026-02-09-msc-thesis-introduction.md"),
        help="Notebook Markdown file to write into (frontmatter preserved)",
    )
    args = parser.parse_args()

    tex_path = Path(args.tex).expanduser().resolve()
    nb_path = Path(args.notebook).expanduser().resolve()

    tex = tex_path.read_text(encoding="utf-8")
    md_body = convert_tex_to_markdown(tex)

    nb_text = nb_path.read_text(encoding="utf-8")
    frontmatter, _ = split_frontmatter(nb_text)
    if not frontmatter:
        raise SystemExit(f"Notebook missing YAML frontmatter: {nb_path}")

    new_nb = frontmatter
    new_nb += "\n# MSc thesis introduction\n\n"
    new_nb += md_body

    nb_path.write_text(new_nb, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
