# Agent Guide for open-ortho/lectures

This repository hosts static reveal.js-based lecture slides and index pages for
the Open-Ortho lectures site.

## Quick Start

- Primary content is in HTML files under `index.html` and `slides/**/index.html`.
- Static assets live in `assets/`.
- reveal.js vendor files live in `dist/` and `plugin/`.

## Build, Lint, Test

There is no traditional build or test pipeline in this repo. The workflow is
editing HTML/CSS/JS directly and previewing through the local server.

### Local Dev Server

- Run: `./serve.py`
- Or: `python3 serve.py`
- Open: `http://127.0.0.1:54385/lectures/`

The server exists because slides use absolute `/lectures/...` paths that do not
work with plain `file://` opens.

### Single-Slide / Single-Presentation Preview

- Run the server, then open a specific deck:
  - Example: `http://127.0.0.1:54385/lectures/slides/orthodontic-informatics/module1/`
- For index pages:
  - Example: `http://127.0.0.1:54385/lectures/index.html`

### Linting

- No lint config or tooling is present.
- Use editor/IDE HTML/CSS validation as needed.

### Tests

- No automated tests are configured.
- “Single test” equivalent is manual verification in a browser for the specific
  slide deck or index page you edited.

### QR Code Generation

- Generates `url_qrcode.svg` for every slide deck.
- Requires `qrencode`.
- Run: `make qrcodes`

## Repository Structure

- `index.html` – main site landing page (dark theme).
- `assets/css/index.css` – shared styling for index pages.
- `slides/**/index.html` – reveal.js deck entry files (slide manifest/order).
- `slides/**/slides/*.html` – one file per slide (HTML source of truth).
- `slides/orthodontic-informatics/common.js` – shared reveal.js loader.
- `plugin/external/external.js` – custom Reveal plugin for external slide loading.
- `dist/`, `plugin/` – vendored reveal.js runtime.

## Vendor / Generated Assets

- Treat `dist/` and most of `plugin/` as vendored. Do not hand-edit vendored files.
- Exception: `plugin/external/external.js` is project-maintained custom code.
- Upgrades follow the process in `README.md` using reveal.js zip contents.

## Code Style Guidelines

This repo is small and mostly static. Follow existing conventions rather than
introducing new tooling.

### HTML (Index Pages)

- Use the shared CSS: `<link rel="stylesheet" href="assets/css/index.css">`.
- Keep the dark theme and typography consistent with `assets/css/index.css`.
- Use semantic structure: `h1`, `p`, `table`, and descriptive link text.
- Prefer relative paths on index pages (e.g., `assets/`, `slides/`).
- Keep footer content consistent with existing pages.

### HTML (Slides)

- Author slides in HTML (not Markdown) for maximum layout/control flexibility.
- One-file-per-slide approach:
  - Put each slide in `slides/**/slides/<slug>.html` as a full `<section>...</section>`.
  - In `slides/**/index.html`, keep ordered placeholders:
    - `<section data-external-replace="slides/<slug>.html"></section>`
  - Prefer `data-external-replace` (not `data-external`) to avoid nested `<section>` blank-slide issues.
- Use absolute `/lectures/...` paths for slide assets and reveal.js files.
- Use the night theme and highlight theme consistent with existing decks.
- Use `alt` text for images; keep it descriptive but concise.
- Use reveal.js features as in existing slides:
  - `class="fragment"` for staged bullet points.
  - `data-auto-animate` for animated transitions.
  - `<aside class="notes">` for speaker notes.

### CSS

- Index page styles live in `assets/css/index.css` and are shared.
- Preserve the dark palette, spacing, and typography.
- Favor small, incremental changes rather than reworking the theme.

### JavaScript

- Minimal vanilla JS only; no bundling or frameworks.
- Use `const`/`let` appropriately.
- Follow existing indentation (4 spaces) and simple, linear flow.
- Error handling is basic `console.error` logging, as in `common.js`.

### Formatting & Whitespace

- HTML indentation varies in legacy files; follow the file’s existing style.
- CSS uses 4-space indentation.
- JS uses 4-space indentation.
- Keep line wrapping modest; avoid reformatting unrelated lines.

### Naming Conventions

- Filenames: lowercase with hyphens (e.g., `2024-aao-vendors-meeting`).
- Slide modules: `module1`, `module2`, etc.
- Slide filenames: abbreviated title-based slugs from the slide heading (`<h2>`, fallback `<h3>`), lowercase hyphenated.
- Image assets: descriptive names, existing files are mixed case; avoid renames
  unless necessary to prevent broken links.

### Imports / Asset Paths

- Slides: prefer absolute `/lectures/...` paths so they work on the local server
  and GitHub Pages.
- Index pages: use relative paths since they are at the repo root or module root.
- Keep reveal.js includes aligned with current deck templates.
- If a slide file moves under `slides/**/slides/`, fix local relative assets accordingly
  (example: `url_qrcode.svg` becomes `../url_qrcode.svg`).

### Reveal Loader Customizations

- `slides/orthodontic-informatics/common.js` is intentionally customized:
  - Scripts are loaded sequentially (not `Promise.all`) to ensure Reveal is ready before plugin init.
  - Loads `/lectures/plugin/external/external.js`.
  - Registers `RevealExternal` in `Reveal.initialize({ plugins: [...] })`.
- `plugin/external/external.js` is a Reveal 4-compatible adaptation of the external loader plugin.
- Rationale: HTML was chosen over Markdown because it provides more flexibility for complex slide content; extra authoring complexity is acceptable and handled by LLM-assisted workflows.

### Reveal.js Upgrade Watchouts

- Upgrading reveal.js can break external loading if plugin APIs change.
- Re-check these integration points after upgrade:
  - `RevealExternal` registration still works in `plugins: [...]`.
  - Plugin methods used by custom external loader (`init(reveal)`, `getConfig()`, `getRevealElement()`, `sync()`, `setState()`) are still valid.
  - Script paths/names in `common.js` still match upgraded reveal distribution.
- Do not overwrite `plugin/external/external.js` during vendor refresh.
- Manual regression check required for every upgraded module deck:
  - No blank slides
  - No console errors (especially Reveal/plugin init errors)
  - External slide files load and render in order

### Error Handling

- Use simple logging for client-side JS errors; no UI error overlays are used.
- For missing assets, rely on browser console and network inspector.

## Content Editing Tips

- Add slides by inserting new `<section>` blocks.
- Use concise slide titles (`<h2>`) and short bullet lists.
- When adding images, verify the path works from the `/lectures/` base.
- If a slide needs inline layout tweaks, keep inline styles minimal.

## Deployment Notes

- Site is hosted on GitHub Pages from the `main` branch.
- Pushing updates to `main` is the deployment mechanism.

## Cursor / Copilot Rules

- No `.cursor/rules/`, `.cursorrules`, or `.github/copilot-instructions.md`
  were found in this repository at the time of writing.
