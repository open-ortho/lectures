# Orthodontic Informatics — Module 1 event

This folder maintains the announcement and logistics for the November 30 presentation.
The [Module 1 guide](../../slides/orthodontic-informatics/module1/README.md)
maintains the reusable lecture. Follow the [shared event guide](../README.md)
for page styling, local preview, and publication checks.

## Event announcement

**Title:** Data Sharing, Integration, and Transition in Orthodontic Informatics

**Course:** Orthodontic Informatics · Module 1

An introduction to orthodontic informatics for first-year orthodontic residents. Starting with computers as everyday clinical tools, this lecture examines clinical data sharing, repeated manual workarounds, and the difficulty of reusing work across disconnected software. Residents will consider what software integration and transitions between systems require to keep clinical data and the work built on it reusable.

**Speaker:** Toni Magni, Clinical Instructor, Department of Orthodontics,
School of Dental Medicine, Case Western Reserve University; afm@case.edu.

## Logistics and sources

- **When:** Monday, November 30, 2026, 3:00–4:00 p.m. Eastern (EST, UTC−05:00).
- **Audience:** first-year orthodontic residents.
- **Where:** Ortho seminar room, School of Dental Medicine – Orthodontics,
  Case Western Reserve University.

The date, time, audience, and room are user-provided. The
[official orthodontics department page](https://case.edu/dental/departments-programs/orthodontics)
identifies the department, not a reservation or an exact building for this event.
No street address is published because the supplied address was ambiguous.
The abstract draws on Module 1's
[opening tool question](../../slides/orthodontic-informatics/module1/slides/most-used-tool.html),
[data-sharing problem](../../slides/orthodontic-informatics/module1/slides/problem-1.html),
and [work-ownership problem](../../slides/orthodontic-informatics/module1/slides/problem-2.html).

## Maintain this event

Edit [index.html](index.html), the announcement copy above,
[the calendar](orthodontic-informatics-module1.ics), and the page's Google Calendar
link together when the title, abstract, time, or room changes.
Keep the calendar's stable UID; update its UTC
`DTSTAMP`, preserve CRLF endings, escape text, and fold physical lines to at most
75 UTF-8 octets. The scheduled hour is 20:00–21:00 UTC.

The **Add to Google Calendar** link opens a draft with the same event details;
the visitor must save it. Follow the
[shared Google Calendar rules](../README.md#google-calendar-links) when updating
the link, and retain the ICS download for other calendar applications.

The [slide link](../../slides/orthodontic-informatics/module1/) opens the evolving
shared deck, not an immutable capture of the slides delivered at this event.
Keep logistics here and presentation-history links in the deck guide.

The intended public URL is
https://open-ortho.org/lectures/events/2026-11-30-orthodontic-informatics-module1/.
A local edit is not a deployed page. From the repository root, run
`python3 -m unittest discover -s tests -p test_ortho_events.py -v` for copy,
calendar, and link checks; then check the page at wide and narrow browser sizes
using the shared guide. These checks do not confirm a room reservation.
