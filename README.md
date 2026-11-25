# Lectures

Open-Ortho lecture materials on orthodontic software interoperability and biomedical
informatics. This repository is a static website: readers browse lecture catalogs,
open reusable slide decks, and find announcements for dated presentations.

[Visit the published site](https://open-ortho.org/lectures/).

## Work tracking

[GitHub Issues](https://github.com/open-ortho/lectures/issues) is the authoritative
place for planned work, follow-ups, and completion criteria.

## Project Structure

This project contains three types of content:

1. **Presentation slides** under `slides/` are reusable teaching material, built
   with the [reveal.js presentation framework](https://revealjs.com/). A deck owns
   its subject, audience, abstract, slide sequence, speaker notes, and resources.
   A year in an existing folder name does not make its guide the home for event logistics.
2. **Event pages** under `events/` describe one scheduled or past presentation.
   Each is a dated presentation record that points to the slides rather than
   copying them. Its folder owns the announcement title and abstract, speaker
   details, date, time when known, location, optional calendar download, and any
   reservation qualifications. Keep the page after the event so its links and
   presentation history remain available.
3. **Catalog pages** help readers discover courses, decks, and events. The
   [root catalog](index.html) separates dated events, courses, and reusable decks;
   the [Orthodontic Informatics course catalog](slides/orthodontic-informatics/index.html)
   links to individual modules. These are navigation pages, not slide decks or
   authoritative event announcements.

For example, **Biomedical Informatics for Computer Scientists** has one
[reusable deck](slides/2026-cs-club-biomedical-informatics/index.html) and a separate
[December 2, 2026 announcement](events/2026-12-02-biomedical-informatics/index.html).
The root catalog links to both. The deck's presentation history links to its event;
to correct the date or room, edit the event folder, not the deck guide. A later
presentation of the same lecture gets a new event folder that can point to the
same deck. Event records preserve their own announcement and schedule; they do
not freeze the linked deck at its historical revision.

### Catalog sections

The root catalog starts with **Events**, listing dated presentations in descending date order.
Each row links to an announcement, not directly to a deck. Maintain event status
manually: **Scheduled** means a planned presentation; **Presented** records a
confirmed past presentation. No clock or JavaScript changes these labels.
**Courses** links to reusable course catalogs. The remaining audience categories,
**Talks for Clinicians** and **Talks for Developers & Students**, link to reusable
lecture decks and retained archives without attaching dated event logistics to
those rows.

### File map

| File or directory | Responsibility |
| --- | --- |
| [index.html](index.html) | Root catalog: dated events, courses, and reusable lecture categories |
| [slides/2026-cs-club-biomedical-informatics/index.html](slides/2026-cs-club-biomedical-informatics/index.html) | Deck entry point: metadata, theme, and ordered slide references |
| [Deck guide](slides/2026-cs-club-biomedical-informatics/README.md) | Reusable abstract, audience, preview instructions, resources, and presentation-history links |
| [slides/2026-cs-club-biomedical-informatics/slides/](slides/2026-cs-club-biomedical-informatics/slides/) | Individual slide content and speaker notes loaded by that deck |
| [Event page](events/2026-12-02-biomedical-informatics/index.html) | Visible announcement for one presentation, including its slides link |
| [Event guide](events/2026-12-02-biomedical-informatics/README.md) | Authoritative announcement copy, schedule sources, and page/calendar maintenance |
| [Event calendar](events/2026-12-02-biomedical-informatics/biomedical-informatics.ics) | Downloadable calendar entry for that presentation |
| [assets/css/index.css](assets/css/index.css) | Shared dark catalog styling and responsive tables |
| [assets/css/cwru-event.css](assets/css/cwru-event.css) | Shared, opt-in blue-and-white event announcement layout |
| [events/README.md](events/README.md) | Shared event markup, activation, maintenance, and browser checks |
| [dist/](dist/) and [plugin/](plugin/) | Reveal.js runtime and plugins used by slide decks |

## Editing and local preview

The root `index.html` is a catalog, not a slide deck. Edit its table rows to change
navigation, short descriptions, or event links. Edit a deck's own `index.html` for
its metadata, theme, and slide sequence. In the CS deck, `<section>` elements with
`data-external-replace` load the individual HTML files from its `slides/` folder;
edit those files for slide content and notes. Other decks may keep content directly
inside their entry point's `<section>` elements. Consult the relevant deck guide
before changing its structure. Event HTML and calendar files are maintained in
the event folder, as described in the event guide linked above.

From the repository root, run:

```sh
make serve
```

On the machine running the server, open http://127.0.0.1:54385/lectures/ and follow
the catalog links. The server binds to loopback; a browser on another machine
needs an existing forwarding route. Use the server rather than opening HTML files
directly: it preserves the `/lectures/` URL prefix used by shared scripts and styles.
Refresh the browser after an edit.

Run the repository checks from the same directory:

```sh
python3 -m unittest discover -s tests -v
```

These check the implemented slide, event, calendar, and documentation contracts.
Also inspect changed pages and slides in a browser; passing tests do not establish
readability, a room reservation, or a rehearsed delivery duration.

## Adding a lecture or event

1. Decide whether to reuse an existing deck or create a new deck for a different
   subject or audience. For a new deck, create a folder under `slides/` with its
   entry point, content, and guide. Keep the reusable title and abstract together
   with its audience and resources; do not put a presentation's schedule there.
2. For each scheduled or past presentation, create a new event folder under `events/`,
   using a dated name such as `YYYY-MM-DD-topic`. Follow the
   [shared event layout guide](events/README.md): load `../../assets/css/index.css`,
   then `../../assets/css/cwru-event.css`, and add `class="event-page"` to the body. Reuse the markup,
   not a copy of the stylesheet. Copy the selected lecture's title and abstract
   into the new event guide and page; add the speaker, known schedule, location,
   and source or reservation qualifications. Link the page to the selected deck.
3. Create a calendar download only when the event's start/end times and time zone
   are known. Match its title, abstract, location, and published event URL. Give
   the new event its own stable calendar UID; do not reuse a previous event's UID.
   Follow the event guide's UTC, revision timestamp, escaping, line-ending, and
   line-folding requirements. For an unknown historical time, omit the time
   and calendar rather than inventing a schedule.
4. Add the dated event to **Events** in descending date order. Put a course link
   in **Courses** and a reusable standalone deck in the appropriate audience
   category; preserve existing archives. Update a course catalog when relevant.
   Link the event from the deck guide's presentation history rather than
   duplicating its logistics there. For later corrections, update the event
   guide and page together, along with any calendar and affected catalog dates
   or links.
   Synchronize reusable deck text only when the lecture's title or abstract changes,
   not when an event's schedule changes; retain earlier event records.
5. Run the checks and local preview above. Check the catalog-to-event-to-slides
   links and the calendar download, then inspect the announcement and changed
   slides at desktop and smaller browser widths before publishing.

### Adding QR Codes

1. Install `qrencode` with `apt`, `yum`, `brew`, ...
2. `make qrcodes`

### Common Make Targets

- `make` or `make help` shows available targets
- `make serve` runs the local dev server
- `make detect-browser` locates Chrome/Chromium for Mermaid CLI
- `make diagrams` renders Mermaid diagrams
- `make qrcodes` generates QR codes for slide decks
- `make clean` removes generated artifacts

### Mermaid Diagrams (Generated SVGs)

Mermaid diagrams live in `assets/diagrams/` and are rendered to SVGs under
`assets/generated/diagrams/` during build. Each diagram renders to a single
`*.svg` with a fixed white background.

#### Nix + direnv (recommended)

1. Install `nix` and `direnv`
2. Run `direnv allow`
3. On macOS, install Chrome or Chromium and set `PUPPETEER_EXECUTABLE_PATH` to the browser binary
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
- **Index pages**: Use shared CSS file at `assets/css/index.css` for consistent dark theme that complements the slide presentations.
- **Event pages**: Load `assets/css/cwru-event.css` after the catalog stylesheet and opt in
  with `class="event-page"` on the body. It supplies the shared blue-and-white
  masthead, schedule, speaker portrait grouping, abstract, call-to-action links,
  and mobile layout without changing catalogs or decks. Maintain it once; inspect
  every opted-in event when it changes. See [events/README.md](events/README.md).

No template engine or JavaScript is required for the catalogs or event pages;
maintainers edit static HTML and keep the linked event records consistent.

## Deployment

GitHub Pages publishes this repository's static site from the root of the `main` branch.
Changes become eligible for deployment when they are pushed or merged into `main`;
a local commit or a push to a review branch does not update the published site.


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
