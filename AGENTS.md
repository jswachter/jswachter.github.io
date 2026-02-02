# Repository Guidelines

This repository hosts a static, personal portfolio site for GitHub Pages. Keep changes focused, readable, and easy to preview locally.

## Project Structure & Module Organization
- `index.html` is the main portfolio page with inline CSS in a `<style>` block.
- `notebooks.html` and `notebook-viewer.html` provide a notebook index and viewer.
- `notebooks/` stores Markdown notes plus `notebook-index.json`; drafts live under `notebooks/drafts/`.
- `images/` and `pdfs/` hold media referenced by the HTML pages.

## Build, Test, and Development Commands
- No build step is required; the site is plain HTML/CSS.
- Local preview (recommended):
  - `python3 -m http.server` then open `http://localhost:8000/index.html`.
- You can also open HTML files directly in a browser for quick checks.

## Coding Style & Naming Conventions
- Use 4-space indentation in HTML/CSS to match existing files.
- Keep CSS minimal and colocated in each HTML file’s `<style>` block unless a shared stylesheet is introduced.
- Prefer `kebab-case` for CSS class names (e.g., `image-row`, `profile-image`).
- Notebook filenames use date-prefixed slugs, e.g., `2025-10-02-autoformalization-agents.md`.

## Testing Guidelines
- There is no automated test suite.
- Manually verify:
  - Pages render correctly on desktop and mobile widths (notably the 600px breakpoint).
  - Links to `images/` and `pdfs/` resolve and open in new tabs where expected.
  - Notebook listings and `notebook-viewer.html` can load entries from `notebooks/notebook-index.json`.

## Commit & Pull Request Guidelines
- Commit messages in history are short, lowercase, and descriptive (e.g., “mobile scroll snap”). Follow that pattern.
- Do not mention AI tools or Claude Code in commit messages.
- Create a commit after even minor changes so history stays granular.
- PRs should include a clear summary and note affected pages; add screenshots for any visual or layout changes.

## Deployment Notes
- The site is deployed via GitHub Pages from the `main` branch. Merged changes to `main` publish automatically.
