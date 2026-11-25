---
# lectures-z4rn
title: Prepare biomedical informatics lecture for CS students
status: in-progress
type: task
priority: normal
tags:
    - cs-lecture
created_at: 2026-11-21T00:59:49Z
updated_at: 2026-11-25T01:45:45Z
---

## Purpose
Prepare a one-hour introductory survey of biomedical informatics for computer-science students: awareness, orientation and interest rather than proficiency or recall of every detail. Introduce the clinical problems, established resources and communities, and opportunities to contribute from the computing side.

## Agreed direction
- Address people with computing knowledge, not clinicians learning computing.
- Title for this revision: “Biomedical Informatics for Computer Scientists”. Both the booking description and catalog entry must explicitly name computer science students.
- Show the breadth of the field and its existing infrastructure, not only medical AI. Students should leave knowing that the field exists, how their skills relate, and where to explore next.

## Required resource addition
Add Georgia Tech CS 6440: Introduction to Health Informatics to the lecture’s further-learning resources, with both links:
- Course: https://omscs.gatech.edu/cs-6440-intro-health-informatics
- Public lecture-video index: https://omscs.gatech.edu/cs-6440-intro-health-informatics-course-videos

The official course description requires a basic CS/programming background and no previous health-informatics knowledge. This is a strong audience match and a full-course follow-up, not a replacement for the one-hour talk. The description and video index have been inspected; the full video series has not been watched.

## Required book resources
Include both previously recommended books in the lecture’s further-reading resources:
- Fred Trotter and David Uhlman, *Hacking Healthcare: A Guide to Standards, Workflows, and Meaningful Use* (O’Reilly, 2011). Computing/IT practitioners entering healthcare; useful for workflows and domain differences. US-focused and dated: not a current policy or technology reference. https://books.google.com/books/about/Hacking_Healthcare.html?id=8ZBxeohRSXoC
- Mark L. Braunstein, *Health Informatics on FHIR: How HL7’s API Is Transforming Healthcare*, second edition (Springer, 2022). Healthcare applications, interoperability, FHIR and SMART on FHIR; explicitly includes CS/IT professionals among its mixed audience. https://link.springer.com/book/10.1007/978-3-030-91563-6

Descriptions and contents were inspected, not the books in full. Present these as optional follow-up reading, not prerequisites for the one-hour lecture.

## Acceptance
- [x] Identify the existing CS-audience deck and update its title and framing for computing students.
- [x] Include the Georgia Tech course and video index in audience-visible further-learning resources.
- [x] Include both books above in audience-visible further-reading resources, with author, edition/year, links and scope/age caveats.
- [ ] Organize the one-hour talk as a broad field tour with concrete problems, existing infrastructure and entry points; do not require retention of every resource name.
- [ ] Review the revised content and verify resource links and slide rendering before delivery.

## Status
The focused revision on branch `docs/cs-informatics-introduction` updates the existing deck at `slides/2026-cs-club-biomedical-informatics/`: consistent title and computer science audience, copy-ready room-booking description in the deck README, and Georgia Tech/book resource slides. There are 23 slides; the 20 original technical slide files and their order are unchanged. This revision does not rewrite the technical body or enable chapter footers.

Verification: fresh-context passage-cited comprehension review passed; separate checks passed 29 Python tests and 4 Node tests. The title and new resource slides render without overflow or broken images at 1440×1000 and 1280×720; no page or HTTP errors occurred while loading the deck. All four resource destination pages were reachable and their relevant descriptions were checked. Existing technical slides 6–7 have reported viewport overflow and remain to be polished. A one-hour delivery remains an unrehearsed target; lecturer acceptance, broader narrative work and final whole-deck readiness remain outstanding. This work is separate from the orthodontic M1–M4 reframe tracked in lectures-2g3g.

Proposed in PR #5: https://github.com/open-ortho/lectures/pull/5 (open; not merged).

## Event landing page
- Organizer reports a room for Wednesday, December 2, 2026, White 411 at Case Western Reserve University.
- CWRU’s official Fall 2026 teaching grid lists the M/W class slot as 3:10–4:25 p.m. Eastern, not 3:00–4:30 with hidden buffer time. This verifies the standard slot, not the individual reservation. Source: https://case.edu/registrar/sites/default/files/2026-02/CWRU%20Teaching%20Grid_fall2026_final_fillable_1.pdf
- [x] Add a responsive static announcement at `events/2026-12-02-biomedical-informatics/` with the maintained title, revised reuse-focused abstract, date/time/place, calendar download and slides link.
- [x] Reconcile booking copy and deck metadata with the revised abstract, and link the event from the site catalog.
- [x] Verify prose, mobile/desktop rendering, links and calendar dates before pushing to PR #5.
Event-page verification: prose comprehension completed; catalog synchronization added to maintenance instructions. The organizer’s room information is accepted as supplied; the official grid confirms the standard time only. All 32 Python tests and 4 Node tests pass. Chromium at widths 1440/768/390/320 found no horizontal overflow, page/network errors; focus outline and calendar download passed. Desktop/mobile screenshots were inspected. Calendar UTC 20:10–21:25 matches Cleveland 15:10–16:25 on December 2. Page/abstract changes are prepared for PR #5; merging/deployment is not authorized. Legacy root README catalog/deployment wording findings are pre-existing and outside this change.

## PR #5 review follow-up
Human review https://github.com/open-ortho/lectures/pull/5#pullrequestreview-6048829310 requests documenting reusable decks versus dated events in the main README and restyling the announcement from actual CWRU computer-science lecture references, with CWRU colors and the presenter’s affiliation: Clinical Instructor, Department of Orthodontics, School of Dental Medicine. Inline comments additionally request replacing “Booking copy” wording and moving schedule/reservation text out of the reusable deck guide. Implemented in separate tested commits: `58f4390` replaces “Booking copy” with the reusable abstract; `14030d4` moves announcement copy/logistics into the event guide; `c592a00` explains slides/events/catalogs and corrects editing/deployment guidance; `8a7d70f` redesigns the page from inspected CWRU CS announcement/web references and current brand colors, with the confirmed faculty affiliation. Fresh-context passage-cited comprehension passed, followed by 39 Python and 4 Node tests and Chromium checks at widths 1440/768/390/320. Focus, calendar download, exact times, and desktop/mobile readability passed. Calendar bytes, reusable slide sources and shared catalog CSS are unchanged. Publication and contextual replies follow; human threads will remain unresolved unless the reviewer resolves them.

## Events and courses catalog expansion
Implemented a distinct Events section alongside Courses on the root catalog, and promoted the CWRU event stylesheet to `events/event.css` for all three announcements. Add Module 1 for first-year orthodontic residents on Monday, November 30, 2026, 15:00–16:00 Eastern in the Ortho seminar room, and a presented Module 3 record for second-year residents on Friday, November 20, 2026 in the back seminar room; both at Case School of Dental Medicine – Orthodontics. The organizer confirmed Module 3 ran 10:00–11:00 Eastern on November 20; the event page, catalog and event guide record that time. The past presentation record has no calendar download. The organizer mentioned Carnegie Road; official CWRU sources list a Cornell Road research campus, so no street address is asserted pending clarification. New events link to reusable module decks, not slide copies.
The catalog/shared-style/new-session revision passed fresh-context prose comprehension, followed by 51 Python and 4 Node tests. Independent Chromium checks covered the catalog and all three announcements at 1440/768/390/320 pixels with no horizontal overflow, broken images or page/network errors; focus and both calendar downloads passed. Shared CSS runtime rules are identical to the previous event-local stylesheet, and slide sources are unchanged. The event records point to evolving module decks, not immutable delivery snapshots. Prepared for publication to PR #5; no merge/deployment authorized.
