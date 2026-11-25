# Biomedical Informatics event page

This static announcement gives computer science students the lecture abstract,
time, location, speaker details, slides, and a downloadable calendar entry. This
folder owns the announcement copy and logistics for this presentation; the
[lecture guide](../../slides/2026-cs-club-biomedical-informatics/README.md)
maintains the reusable abstract, audience, and learning resources. The page requires
no JavaScript, build step, external fonts, or tracking services.

## Announcement copy

The following title and abstract are the authoritative copy for this event's
announcement. Copy them with the event details below when preparing an invitation.

Title:

```text
Biomedical Informatics for Computer Scientists
```

Abstract:

```text
A one-hour introduction to biomedical informatics for computer science students. The lecture connects familiar computing problems to clinical workflows and introduces the standards, software, shared infrastructure, and communities already available in healthcare. The goal is to help future developers recognize when they can build on existing work—and know where to look—rather than reinventing data models, interfaces, or isolated proprietary solutions. Students will leave with starting points for further learning, projects, and research. No medical background is required.
```

Speaker: Toni Magni, Clinical Instructor, Department of Orthodontics,
School of Dental Medicine, Case Western Reserve University; afm@case.edu.
The faculty affiliation is supplied by the speaker. It does not establish
Computer and Data Sciences (CDS) sponsorship or university endorsement of this event.

## Event

Wednesday, December 2, 2026, 3:10–4:25 p.m. Eastern (EST, UTC−05:00),
White 411, Case Western Reserve University. The date and room are user-provided;
the room reservation is not independently verified. The
[official White 411 page](https://case.edu/utech/departments/client-experience/mediavision/technology-enhanced-classroom-tec/list-classrooms/white-411)
provides room information, not a reservation record.

The 75-minute scheduled slot uses the M/W 3:10–4:25 p.m. block in the official
[CWRU teaching grid, effective Fall 2026](https://case.edu/registrar/sites/default/files/2026-02/CWRU%20Teaching%20Grid_fall2026_final_fillable_1.pdf).
The one-hour lecture is intended to fit within that slot; the schedule is not a timed rehearsal
and does not specify an additional agenda.

## Preview and maintain

From the repository root:

```sh
make serve
```

On the server machine, open
http://127.0.0.1:54385/lectures/events/2026-12-02-biomedical-informatics/.
The server binds to loopback; a browser on another machine needs an existing
forwarding route. The published URL is
https://open-ortho.org/lectures/events/2026-12-02-biomedical-informatics/.

Edit [index.html](index.html) for visible content. It loads the shared
[../../assets/css/index.css](../../assets/css/index.css) first, then
[../../assets/css/cwru-event.css](../../assets/css/cwru-event.css) for the shared event palette, typography, layout,
focus states, and mobile flow. The body opts in with `class="event-page"`; all
rules are scoped to `.event-page`, so they do not change the catalog or slides.
See the [shared event layout guide](../README.md) before changing styling used
by multiple announcements.

The announcement uses a blue-and-white academic layout inspired by CWRU's
[color guidance](https://case.edu/brand/visual-identity/color), including current
CWRU Blue `#003071`. Its Arial/system-sans typography follows the
[digital font fallback guidance](https://case.edu/brand/visual-identity/fonts)
without downloading an external font. The
[CDS lecture announcement example](https://engineering.case.edu/sites/default/files/Announcement_Rexford.pdf)
informs the title, speaker, abstract, and logistics hierarchy, not the event's
hosting status. These are design references, not a claim of official CDS hosting,
endorsement, or full brand compliance.

### Keep the announcement consistent

- **Schedule or room changes:** edit the Event section above, the visible page,
  and [calendar file](biomedical-informatics.ics). Update the date and event link
  in the [site catalog](../../index.html) when affected; do not change the deck
  abstract or metadata for logistics-only edits.
- **Title or abstract changes:** edit the announcement copy above, the visible
  page and its metadata, and the calendar's `SUMMARY` or `DESCRIPTION`. If the
  reusable lecture framing changes too, synchronize the
  [deck abstract](../../slides/2026-cs-club-biomedical-informatics/README.md),
  [deck metadata](../../slides/2026-cs-club-biomedical-informatics/index.html),
  and [title slide](../../slides/2026-cs-club-biomedical-informatics/slides/title.html)
  as applicable. Update the catalog title or short description to match the
  lecture; its description is a summary, not a second full announcement abstract.
- **Speaker changes:** update the speaker details above and on the page. Keep
  affiliation separate from any claim about who hosts the event.

This event's calendar uses UTC start/end times of 20:10–21:25 UTC. Follow the
[shared calendar rules](../README.md#calendar-files) when editing its timestamps,
identity, text, or file formatting.

Run the structural and calendar checks from the repository root:

```sh
python3 -m unittest discover -s tests -v
```

These checks verify copy, links, metadata, local assets, and calendar formatting;
responsive readability still needs a browser check. They do not verify the room
reservation or lecture delivery duration.
