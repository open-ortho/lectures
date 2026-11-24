# Biomedical Informatics for Computer Scientists

## Abstract

A one-hour introduction to biomedical informatics for computer science students. The lecture connects familiar computing problems to clinical workflows and introduces the standards, software, shared infrastructure, and communities already available in healthcare. The goal is to help future developers recognize when they can build on existing work—and know where to look—rather than reinventing data models, interfaces, or isolated proprietary solutions. Students will leave with starting points for further learning, projects, and research. No medical background is required.

## Event

[Event details](../../events/2026-12-02-biomedical-informatics/): Wednesday,
December 2, 2026, 3:10–4:25 p.m. Eastern (EST, UTC−05:00), White 411,
Case Western Reserve University. The date and room are user-provided; the room
reservation is not independently verified.

The 75-minute scheduled slot follows the M/W 3:10–4:25 p.m. block in the official
[CWRU teaching grid, effective Fall 2026](https://case.edu/registrar/sites/default/files/2026-02/CWRU%20Teaching%20Grid_fall2026_final_fillable_1.pdf).
That grid establishes a standard time block, not a room reservation. The one-hour
lecture is intended to fit within this scheduled slot; it is not a timed rehearsal
or a separate agenda. See the [event maintenance guide](../../events/2026-12-02-biomedical-informatics/README.md)
for the page and calendar files.

## Audience and purpose

This is a field-orientation lecture for computer science students who know basic
computing concepts but need no medical background. The goal is to recognize how
familiar CS problems appear in clinical workflows, discover existing infrastructure
and communities, and find a route into projects or research—not to master every
standard or acronym.

The 60-minute lecture is a delivery goal within the 75-minute scheduled slot.
This deck has not been rehearsed to verify that it fits that duration. The existing
technical body has not been rewritten or broadly reordered for this framing change;
it remains focused on clinical data,
systems, interoperability, standards, and reusable tools rather than the whole
biomedical-informatics field.

## Preview and checks

From the repository root, run:

```sh
make serve
```

On the machine running the server, open the
[local deck preview](http://127.0.0.1:54385/lectures/slides/2026-cs-club-biomedical-informatics/).
The server binds to loopback; a browser on another machine needs an existing
forwarding route. Refresh after editing [the manifest](index.html) or its slide files.

Run the Python checks from the repository root:

```sh
python3 -m unittest discover -s tests -v
```

These checks cover framing, resource links, and slide/asset structure; they do not
establish rendered readability or a timed delivery fit.

## Further learning

Optional follow-up resources, not prerequisites for this lecture:

- **[Georgia Tech CS 6440: Intro to Health Informatics](https://omscs.gatech.edu/cs-6440-intro-health-informatics)**
  (Jon Duke and Elizabeth Shivers, OMSCS): a full course with labs and a project,
  not a substitute for this one-hour orientation. It assumes basic CS and
  programming proficiency. No health-informatics background is required. The
  official [course videos](https://omscs.gatech.edu/cs-6440-intro-health-informatics-course-videos)
  include Introduction, EHRs, and Data Standards as possible starting points.
- **[Hacking Healthcare](https://books.google.com/books/about/Hacking_Healthcare.html?id=8ZBxeohRSXoC)**
  — Fred Trotter and David Uhlman, O’Reilly, 2011. A bridge from IT to clinical
  workflows and healthcare organizations. US-focused and dated: useful context,
  not current policy guidance.
- **[Health Informatics on FHIR](https://link.springer.com/book/10.1007/978-3-030-91563-6)**
  — Mark L. Braunstein, Springer, 2nd edition, 2022. Healthcare use cases through
  interoperable apps and the API ecosystem for a mixed clinical and CS/IT audience;
  not the whole field of biomedical informatics.

These suggestions are based on the official course description/video index and
book descriptions, contents, and bibliographic listings. The videos were not watched
in full and the books were not read in full for this update. A public listing or
preview is not a promise of unrestricted access to the complete content.