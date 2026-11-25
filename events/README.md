# Dated lecture events

Each folder under `events/` records one presentation: its announcement, speaker,
date, time, room, and link to a reusable slide deck. Keep event records after the
presentation. A deck's presentation history should link here; the linked slides
can continue to evolve unless the event explicitly links to a versioned snapshot.
The [root catalog](../index.html) lists events separately from courses and decks.

## Use the shared announcement layout

[events/event.css](event.css) gives announcements a CWRU-blue masthead, a schedule,
a speaker portrait beside the name, an abstract, and call-to-action links. It uses
a white reading surface and a single-column mobile flow. It requires no JavaScript,
external fonts, or build step. The stylesheet loads no images; portrait URLs belong
in each event's HTML.

For an event at `events/YYYY-MM-DD-topic/index.html`, load the catalog stylesheet
first, then the shared event stylesheet, and opt in on the body:

```html
<link rel="stylesheet" href="../../assets/css/index.css">
<link rel="stylesheet" href="../event.css">
<body class="event-page">
```

All event rules are scoped to `.event-page`. Merely linking the file does not
change a catalog or deck without that body class. Do not copy `event.css` into
individual event folders. Changes to the shared file affect every opted-in event;
preview each affected announcement before publishing them.

Use the [CS event page](2026-12-02-biomedical-informatics/index.html) as a markup
example and its [maintenance guide](2026-12-02-biomedical-informatics/README.md)
for announcement and calendar editing details. Keep these layout responsibilities:

| Class | Content and behavior |
| --- | --- |
| `event-shell` | Centers the page content with responsive side margins |
| `event-nav` | Breadcrumb back to the root catalog |
| `event-masthead` | Blue title area with an audience label |
| `event-schedule` | A definition list of date, time, and location |
| `event-actions` | Slides and optional calendar links; `event-primary` marks the main action |
| `event-content` | Speaker and reading columns, stacked on mobile |
| `event-speaker-heading` | Portrait and speaker name kept together |
| `event-abstract` | Labelled abstract section with readable paragraph widths |
| `event-footer` | Closing navigation or project identity |

Supply meaningful portrait alternative text, explicit image dimensions, labelled
sections, and a single page title. Keep speaker affiliation separate from hosting
or sponsorship claims. Reuse existing local portraits rather than duplicating them.

## Add or correct an event

1. Create a dated folder with `index.html` and `README.md`. Link to the selected
   deck rather than copying slides. Maintain the event's announcement copy and
   the sources for its logistics in that folder's guide.
2. Include only supplied details. If a historical event's time is unknown, omit the time
   and calendar download. Add a calendar
   only when its start/end times and time zone are known. For calendars, follow
   the existing event guide's stable UID, UTC, revision timestamp, escaping,
   CRLF line-ending, and 75-octet line-folding instructions.
3. Add a row to the root catalog's **Events** table in descending date order.
   Keep its status explicit: use **Presented** only for a confirmed past
   presentation, and maintain scheduled entries manually. The catalog has no
   automatic clock-based status updates. Put courses in **Courses** and reusable
   decks in their audience categories, without dated logistics in those deck rows.
4. Add the event link to the deck guide's presentation history. For corrections,
   update the event guide, page, calendar when present, and affected catalog
   fields together. Change the reusable deck abstract only if its framing changes,
   not for a room or schedule correction.

## Maintain past presentations

Keep event records after the presentation so readers can find its date, institution,
country, audience, speaker, and slides. Maintain the event HTML and its root catalog
row together; the archive is edited manually. Existing archived records use this
shared guide rather than separate per-event READMEs.

- Preserve established titles, event URLs, and separate records for distinct cohorts.
- Keep the precision of the supplied date. Ferrara uses `2023-02` and
  “February 2023 (planned month)”; its presentation date is not recorded. Do not
  turn a planned month into a delivery date or add a day. Omit unknown times and calendars.
- Use **Presented** for past presentations and include the institution's country.
- Link **View slides** to the current deck, or **View course** to the course index.
  Slides may be updated after the presentation. A dated event record does not
  freeze the linked deck.
- When slides are unavailable, omit the slides link and say
  “Slides are not yet available.”
- Keep the lecture description about its known subject and audience. Do not infer
  additional topics from the linked deck or add a historical speaker affiliation
  from the speaker's current role.
- Publish event facts, not correspondence, personal contact lists, or private logistics.
- For a correction, update the event page, catalog row, any calendar, and affected
  deck presentation-history links, then run the checks below.

## Preview and check

From the repository root, run `make serve`. On that server machine, open
http://127.0.0.1:54385/lectures/ and follow the event links. A browser on another
machine needs an existing forwarding route because the server binds to loopback.
Run the structural checks from the same directory:

```sh
python3 -m unittest discover -s tests -v
```

Inspect the root catalog and all announcements affected by shared CSS changes at
desktop and narrow mobile widths. Check keyboard focus, title and paragraph
wrapping, portrait/name grouping, schedule readability, slides links, and any
calendar download. Check for horizontal overflow and failed assets without hiding
content. Passing structural tests does not establish prose comprehension, room
reservation, rendered readability, or a rehearsed lecture duration.
