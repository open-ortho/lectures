---
# lectures-z4rn
title: Prepare biomedical informatics lecture for CS students
status: in-progress
type: task
priority: normal
tags:
    - cs-lecture
created_at: 2026-11-21T00:59:49Z
updated_at: 2026-11-21T01:55:43Z
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
