# Agent Guide for open-ortho/lectures

This repository hosts static reveal.js-based lecture slides and index pages for
the Open-Ortho lectures site.

## Quick Start

- Slide decks live under `slides/**/index.html`.
- Individual slides are in `slides/**/slides/*.html`.
- Shared assets live in `assets/`.
- reveal.js vendor files live in `dist/` and `plugin/`.

## Build, Lint, Test

There is no traditional build or test pipeline. Workflow is edit + browser
preview.

### Local Dev Server

- Run: `make serve` (or `python3 serve.py`)
- Open: `http://127.0.0.1:54385/lectures/`

The server exists because slides use absolute `/lectures/...` paths that do not
work with `file://`.

### Single-Deck Preview ("single test")

- Run the server, then open a specific deck:
  - Example: `http://127.0.0.1:54385/lectures/slides/orthodontic-informatics/module2/`
- For index pages:
  - Example: `http://127.0.0.1:54385/lectures/index.html`

### Mermaid Diagrams

- Source: `assets/diagrams/*.mmd`
- Output: `assets/generated/diagrams/*.svg`
- Render: `make diagrams`
- Clean: `make clean`

Diagram authoring notes:

- Use YAML frontmatter (`---` with `config:`) to control Mermaid look/theme.
- Keep diagrams as plain Mermaid `.mmd` files (one diagram per file).
- Outputs are SVG only; no PNG generation.
- Avoid post-processing generated SVGs; regenerate from `.mmd` instead.
- Background is fixed in Makefile; keep diagram styling inside frontmatter.

Mermaid CLI uses a headless browser. Set `PUPPETEER_EXECUTABLE_PATH` to a
Chrome/Chromium binary if auto-detection fails. You can check detection with:

- `make detect-browser`

Rendering uses a fixed white background via Makefile options. Styling should be
defined in Mermaid frontmatter (`config:` block) inside each `.mmd`.

### QR Codes

- Generates `url_qrcode.svg` for every slide deck.
- Requires `qrencode`.
- Run: `make qrcodes`

### Linting

- No lint configuration present.
- Use editor/IDE HTML/CSS validation as needed.

### Tests

- No automated tests are configured.
- “Single test” is manual verification in a browser for the specific deck or
  index page you edited.

## Repository Structure

- `index.html` – main site landing page (dark theme).
- `assets/css/index.css` – shared styling for index pages.
- `slides/**/index.html` – reveal.js deck entry files (slide manifest/order).
- `slides/**/slides/*.html` – one file per slide (HTML source of truth).
- `slides/orthodontic-informatics/common.js` – shared reveal.js loader.
- `plugin/external/external.js` – custom Reveal plugin for external slide loading.
- `dist/`, `plugin/` – vendored reveal.js runtime.

## Vendor / Generated Assets

- Treat `dist/` and most of `plugin/` as vendored. Do not hand-edit.
- Exception: `plugin/external/external.js` is project-maintained.
- Generated diagrams live in `assets/generated/diagrams/` (not committed).

## Code Style Guidelines

Follow existing conventions and avoid large reformatting changes.

### HTML (Index Pages)

- Use the shared CSS: `<link rel="stylesheet" href="assets/css/index.css">`.
- Preserve the dark theme and typography from `assets/css/index.css`.
- Use semantic structure: `h1`, `p`, `table`, and descriptive link text.
- Prefer relative paths on index pages (e.g., `assets/`, `slides/`).

### HTML (Slides)

- Author slides in HTML (not Markdown) for layout control.
- One-file-per-slide:
  - `slides/**/slides/<slug>.html` contains a full `<section>...</section>`.
  - `slides/**/index.html` references it with:
    - `<section data-external-replace="slides/<slug>.html"></section>`
- Use absolute `/lectures/...` paths for slide assets and reveal.js files.
- Use `alt` text for images; keep it concise.
- Use reveal.js features as in existing slides:
  - `class="fragment"` for staged bullets
  - `data-auto-animate` for transitions
  - `<aside class="notes">` for speaker notes

### CSS

- Index page styles live in `assets/css/index.css`.
- Preserve the dark palette, spacing, and typography.
- Prefer incremental edits over theme rewrites.

### JavaScript

- Minimal vanilla JS only; no bundling or frameworks.
- Use `const`/`let`; no TypeScript.
- Keep indentation at 4 spaces.
- Error handling is simple `console.error` logging as used in `common.js`.

### Formatting & Whitespace

- HTML indentation varies in legacy files; follow the file’s existing style.
- CSS uses 4-space indentation.
- Keep line wrapping modest; avoid reformatting unrelated lines.

### Naming Conventions

- Filenames: lowercase with hyphens (e.g., `2024-aao-vendors-meeting`).
- Slide modules: `module1`, `module2`, etc.
- Slide filenames: lowercase hyphenated slugs from the slide title.
- Image assets: descriptive names; avoid renames unless necessary.

### Imports / Asset Paths

- Slides: use absolute `/lectures/...` paths.
- Index pages: use relative paths.
- If a slide moves, fix relative asset references (e.g., `../url_qrcode.svg`).

### Error Handling

- Use simple logging for client-side JS errors.
- For missing assets, rely on browser console/network inspector.

## Reveal Loader Customizations

- `slides/orthodontic-informatics/common.js` loads scripts sequentially to ensure
  Reveal is ready before plugins initialize.
- Loads `/lectures/plugin/external/external.js` and registers `RevealExternal`.
- `plugin/external/external.js` is a Reveal 4-compatible adaptation of the
  external loader plugin.

## Reveal.js Upgrade Watchouts

- Upgrades can break external loading. Re-check:
  - `RevealExternal` registration in `plugins: [...]`.
  - Plugin APIs used by external loader (`init`, `getConfig`, `getRevealElement`,
    `sync`, `setState`).
  - Script paths/names in `common.js`.
- Do not overwrite `plugin/external/external.js` during vendor refresh.

## Content Editing Tips

- Keep slide titles concise (`<h2>`), bullets short.
- Verify image paths under `/lectures/`.
- Use inline styles sparingly and only when needed.

## Deployment Notes

- Hosted on GitHub Pages from the `main` branch.
- Pushing to `main` deploys.

## Cursor / Copilot Rules

- No `.cursor/rules/`, `.cursorrules`, or `.github/copilot-instructions.md`
  were found at the time of writing.
