# Dated lecture events

Each folder under `events/` records one presentation: its announcement, speaker,
date, time, room, and link to a reusable slide deck. Keep event records after the
presentation. A deck's presentation history should link here; the linked slides
can continue to evolve unless the event explicitly links to a versioned snapshot.
The [root catalog](../index.html) lists events separately from courses and decks.

## Use the shared announcement layout

[assets/css/cwru-event.css](../assets/css/cwru-event.css) gives announcements a CWRU-blue masthead, a schedule,
a speaker portrait beside the name, an abstract, and call-to-action links. It uses
a white reading surface and a single-column mobile flow. It requires no JavaScript,
external fonts, or build step. The stylesheet loads no images; portrait URLs belong
in each event's HTML.

For an event at `events/YYYY-MM-DD-topic/index.html`, load the catalog stylesheet
first, then the shared event stylesheet, and opt in on the body:

```html
<link rel="stylesheet" href="../../assets/css/index.css">
<link rel="stylesheet" href="../../assets/css/cwru-event.css">
<body class="event-page">
```

All event rules are scoped to `.event-page`. Merely linking the file does not
change a catalog or deck without that body class. Do not copy `cwru-event.css` into
individual event folders. Changes to the shared file affect every opted-in event;
preview each affected announcement before publishing them.

Start from the [copyable HTML template](../templates/events/cwru-event.html),
not an existing announcement with another event's facts. The template is ordinary
static HTML, not a template engine; no build or JavaScript substitutes its tokens.
Keep these layout responsibilities:

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

From the repository root, replace the example folder name with the event's known
date and topic, then copy the template:

```sh
mkdir -p events/YYYY-MM-DD-topic
cp templates/events/cwru-event.html events/YYYY-MM-DD-topic/index.html
```

1. Replace every `{{PLACEHOLDER}}` manually. Set the title in both `<title>` and
   `<h1>`, and the abstract in both the description metadata and visible section.
   Supply the audience, date at its known precision, institution, country, venue,
   and speaker. Escape HTML special characters in text and attribute values.
   Create an event `README.md` with announcement copy and sources for its logistics.
2. Include only supplied details. If a historical event's time is unknown, omit the time
   and calendar links by deleting the optional time block and both calendar actions.
   For known times, use local ISO timestamps with an explicit UTC offset in
   `datetime`, and show the time zone to readers. Remove unknown portrait or
   affiliation blocks; keep supplied affiliation distinct from hosting claims.
   Resolve portrait and slides paths from the new event folder (`../../assets/`
   and `../../slides/`), not from the template's folder. Enable the commented
   slides action only for an existing deck and remove the unavailable-slides message.
   Enable both calendar actions only after creating that event's own file using
   [Calendar files](#calendar-files). Delete unused actions and every remaining
   placeholder before adding the page to a catalog; never publish a draft example.
3. Add a row to the root catalog's **Events** table in descending date order.
   Display dates there as `YYYY-MM-DD`, and known times in 24-hour format with
   the local UTC offset on each endpoint, for example `15:10-05:00–16:25-05:00`.
   Determine the offset for the event's location and date, including daylight
   saving time where applicable. Preserve month-only precision as `YYYY-MM`
   and omit unknown times rather than inventing a day or zone. The individual event pages
   may use the event locale's date and time format.
   Keep its status explicit: use **Presented** only for a confirmed past
   presentation, and maintain scheduled entries manually. The catalog has no
   automatic clock-based status updates. Put courses in **Courses** and reusable
   decks in their audience categories, without dated logistics in those deck rows.
4. Add the event link to the deck guide's presentation history. For corrections,
   update the event guide, page, calendar when present, and affected catalog
   fields together. Change the reusable deck abstract only if its framing changes,
   not for a room or schedule correction.

## Calendar files

Create a calendar download only when start/end times and time zone are known.
Convert the confirmed local times to UTC for `DTSTART` and `DTEND` (the `Z` suffix);
do not infer a time from a neighboring event or turn an unknown time into an all-day entry.
Match `SUMMARY`, `DESCRIPTION`, `LOCATION`, and `URL` to the published announcement.
Give each new event its own stable `UID`; keep that UID when correcting the same
event. Record the file revision time in a UTC `DTSTAMP` and refresh it on edits.

Use RFC 5545 text escaping: escape backslashes first, then commas as `\,`,
semicolons as `\;`, and embedded newlines as `\n`. Preserve CRLF line endings and
fold each physical line to at most 75 UTF-8 octets, without splitting a UTF-8
character; begin continuation lines with one space. Keep the calendar in its event
folder and link to that local file with the `download` attribute. Check its title,
abstract, times, location, event URL, and downloadable bytes whenever they change.

### Google Calendar links

For every event with an ICS download, also include an **Add to Google Calendar**
link. This link opens a prefilled event draft; the visitor must save the draft in
Google Calendar. It does not subscribe the visitor to future schedule changes.
Keep the ICS download for other calendar applications. Omit both actions when
the start, end, or time zone is unknown; do not turn a date-only historical record
into an all-day calendar event.

Use `https://calendar.google.com/calendar/render` with these URL-encoded query
parameters, then escape query separators as `&amp;` in the HTML `href`:

| Parameter | Value |
| --- | --- |
| `action` | `TEMPLATE` |
| `text` | The ICS `SUMMARY`, with calendar text escapes decoded |
| `dates` | The ICS UTC `DTSTART` and `DTEND`, joined with `/`, such as `20261202T201000Z/20261202T212500Z` |
| `location` | The ICS `LOCATION`, with calendar text escapes decoded |
| `details` | The decoded ICS `DESCRIPTION`, two newlines, and the event's published `URL` |

Use UTC timestamps ending in `Z`; do not also supply a different local time or
zone parameter. When event details change, update the page, guide, ICS file and
Google Calendar URL together. Check the decoded URL fields against the ICS and
the visible schedule. Never add attendees, organizer details or a save operation
to the link. See the [University of Michigan calendar-link guide](https://teamdynamix.umich.edu/TDClient/210/DepressionCenter/KB/Article/13454/How-to-Create-Add-to-Calendar-Links)
for the Google Calendar URL format.

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

Use [Editing and local preview](../README.md#editing-and-local-preview) for
server startup, browser access, and the repository test command. Then check these
event-specific details:

Inspect the root catalog and all announcements affected by shared CSS changes at
desktop and narrow mobile widths. Check keyboard focus, title and paragraph
wrapping, portrait/name grouping, schedule readability, slides links, and any
calendar download. Check for horizontal overflow and failed assets without hiding
content. Passing structural tests does not establish prose comprehension, room
reservation, rendered readability, or a rehearsed lecture duration.
