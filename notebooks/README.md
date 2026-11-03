# Publishing notebooks

Write notes as date-prefixed Markdown files in this directory. Use the same title
in frontmatter and the first Markdown heading so the listing, browser tab, and
article agree:

```markdown
---
title: A note title
date: 2026-11-03
collection: AI
---

# A note title

The note starts here.
```

Choose a broad collection: `AI`, `Mathematics`, or `Finance`. Tags are optional and
are not displayed on articles; existing tags remain for compatibility with tag
filter URLs. An optional `summary:` overrides the generated opening-paragraph
summary in the machine-readable index.

After adding or updating a note, run `python3 scripts/generate_notebook_index.py`
from the repository root. Commit the generated index, notebook listing, and any
sitemap changes with the note. Files under `drafts/` are excluded from the index.
