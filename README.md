## Hi there 👋

<!--
**jswachter/jswachter** is a ✨ _special_ ✨ repository because its `README.md` (this file) appears on your GitHub profile.

Here are some ideas to get you started:

- 🔭 I’m currently working on ...
- 🌱 I’m currently learning ...
- 👯 I’m looking to collaborate on ...
- 🤔 I’m looking for help with ...
- 💬 Ask me about ...
- 📫 How to reach me: ...
- 😄 Pronouns: ...
- ⚡ Fun fact: ...
-->

## Notebook footnotes

Use standard Markdown footnote references and definitions in notebook entries:

```markdown
A sentence with an aside.[^aside]

[^aside]: The aside can include links, emphasis, and the same math syntax as the notebook.
```

Indent additional paragraphs in a definition by four spaces. Notes are numbered
in reading order, with links to the note and back to its reference. At screen widths
of 1280px and above, notes sit in the right margin beside their first reference;
on smaller screens and in print, they remain at the end. Closely spaced margin
notes stack without overlapping. The viewer uses `marked-footnote` for parsing
and `scripts/notebook-sidenotes.js` for placement, keeping a single copy of each note.

## Notebook references

The same margin layout supports the bibliography format used by the MSc thesis:

```markdown
A citation [1](#ref-example).

## References

1. <a id="ref-example"></a> Author (2026). *Title*. [Source](https://example.com).
```

A `References` or `Bibliography` heading immediately followed by an ordered list
is recognized when every entry has a `ref-` anchor and is cited in the text. Each
entry sits beside its first citation on wide screens and remains in the numbered
bibliography on smaller screens and in print. Repeated citations share one entry,
with a return link to each citation. References and footnotes share collision
handling so they can appear together in the same margin. Other bibliography
formats keep their existing layout.
