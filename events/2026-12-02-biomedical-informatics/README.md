# Biomedical Informatics event page

This static page gives computer science students the lecture abstract, time,
location, slides, and a downloadable calendar entry. It requires no JavaScript,
build step, external fonts, or tracking services.

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

Edit [index.html](index.html) for visible content. The shared
[../../assets/css/index.css](../../assets/css/index.css) supplies the dark palette,
base typography, and link styles. [event.css](event.css) adds the event layout,
editorial headline, amber accent, focus states, and mobile flow; every rule is
scoped to `.event-page`, so it does not change the catalog or slides.

If the abstract or schedule changes, update the page, [calendar file](biomedical-informatics.ics),
and the [deck booking copy](../../slides/2026-cs-club-biomedical-informatics/README.md)
and [deck metadata](../../slides/2026-cs-club-biomedical-informatics/index.html)
together, including the dated event link in the [site catalog](../../index.html).
The calendar uses UTC start/end times (20:10–21:25 UTC), a stable event
UID, and a UTC `DTSTAMP` recording the file revision time. Keep that UID on edits;
refresh `DTSTAMP`, preserve CRLF line endings, escape calendar text, and fold lines
to at most 75 UTF-8 octets as required by RFC 5545.

Run the structural and calendar checks from the repository root:

```sh
python3 -m unittest discover -s tests -v
```

These checks verify copy, links, metadata, local assets, and calendar formatting;
responsive readability still needs a browser check. They do not verify the room
reservation or lecture delivery duration.
