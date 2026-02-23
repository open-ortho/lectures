# Lectures

ORTHODONTIC SOFTWARE INTEROPERABILITY Lectures

See it live [http://www.open-ortho.org/lectures/](http://www.open-ortho.org/lectures/).

## Project Structure

This project contains two types of content:

1. **Presentation Slides**: Built using the [reveal.js presentation framework](https://revealjs.com/) with a dark theme
2. **Index Pages**: Landing pages that list and describe the presentations, using a shared CSS file for consistent dark styling

### Presentation Slides

The individual presentation slides are built with reveal.js and include:
- Slide content in `index.html` files within each presentation folder
- Dark theme configuration using the reveal.js "night" theme
- Interactive features like speaker notes, slide transitions, and fragment animations

### Index Pages

The index pages provide navigation and description of the presentations:
- Main index at `/index.html` lists all presentation categories
- Module-specific indices (e.g., `/slides/orthodontic-informatics/index.html`) list individual modules
- Both use a shared CSS file at `/assets/css/index.css` for consistent dark theme styling

## How to edit this document

This presentation is written using the [reveal.js presentation framework](https://revealjs.com/).

* Slide content are in the [index.html](./index.html) file. Add and remove slides by adding and removing `<section>` tags.
* Slide configuration is also in the [index.html](./index.html) file.
* The framework is in the [dist](./dist) and [plugin](./plugin) folders.
* Run `make serve`
* View the changes by opening the `http://127.0.0.1:54385/lectures/` file with your browser.

NB: the web server is only there because using absolute paths for common libraries like common.js is the easiest way to deal with using them from different locations. Then the absolute paths would not work locally for development. Hence the development server.

### Adding QR Codes

1. Install `qrencode` with `apt`, `yum`, `brew`, ...
2. `make qrcodes`

### Common Make Targets

- `make` or `make help` shows available targets
- `make serve` runs the local dev server
- `make diagrams` renders Mermaid diagrams
- `make qrcodes` generates QR codes for slide decks

### Mermaid Diagrams (Generated SVGs)

Mermaid diagrams live in `assets/diagrams/` and are rendered to SVGs under
`assets/generated/diagrams/` during build. Each diagram renders to `*.dark.svg` and
`*.light.svg` with a transparent background, so slides can switch by theme.

#### Nix + direnv (recommended)

1. Install `nix` and `direnv`
2. Run `direnv allow`
3. On macOS, install Chrome and set `PUPPETEER_EXECUTABLE_PATH` to the Chrome binary
4. Render diagrams: `make diagrams`

#### Non-Nix

1. Install Node.js 20+
2. Install Chrome or Chromium and set `PUPPETEER_EXECUTABLE_PATH` to the browser binary
3. `npm install`
4. Render diagrams: `make diagrams`

The rendered SVGs are not committed. Run the render step before local preview or
any GitHub Actions deploy step.

### Styling

- **Slides**: Use reveal.js themes (currently "night" theme) configured in each presentation's `index.html`
- **Index pages**: Use shared CSS file at `assets/css/index.css` for consistent dark theme that complements the slide presentations

## Deployment

This project is being hosted as a static site on GitHub Pages from the `main` branch. Committing and pushing to the master branch will deploy the presentation.


## Upgrading Reveal-JS

1. Download latest [zip compiled from github](https://github.com/hakimel/reveal.js/archive/master.zip).
2. Unzip
3. Replace `dist/` and `plugin/` folders with the ones found in the zip archive. Example:

        cd ~/Downloads
        curl -O https://github.com/hakimel/reveal.js/archive/master.zip
        unzip ~/Downloads/master.zip
        cd -
        rsync -av --delete ~/Downloads/reveal.js-master/plugin/ plugin/
        rsync -av --delete ~/Downloads/reveal.js-master/dist/ dist/
