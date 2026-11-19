# Orthodontic Informatics — Module 3

## Make clinical context reusable

This implemented 24-slide lecture is designed for second-year orthodontic residents in a 60-minute session, including discussion and a paired exercise. Residents start with a useful ambition—having a tool prepare a source-linked visit brief—and identify what clinical software must expose so another authorized tool can reuse the records without repeated manual assembly. No programming knowledge is required.

The presenter contrasts copying email into AI chat and copying the answer back with agents reading email, composing replies and saving drafts through selected tools. The lecture then moves explicitly to a proposed clinical analogy: products exchange records through permitted interfaces using independently restricted identities. The clinical case T-017 is synthetic; the deck does not demonstrate a deployed clinical integration or use patient data.

## Learning objectives

By the end, residents should be able to:

1. Explain how manual preparation for AI can make the clinician perform work that clinical software should make reusable.
2. Identify what clinical software must make available so another authorized tool can use its data without the clinician manually collecting, reformatting, and explaining the records each time.
3. Compare integration using vendor-specific interfaces with integration using shared open clinical standards, without assuming that either approach guarantees compatibility, safety or clinical accuracy.
4. Describe the different jobs of clinical data standards, an AI harness and MCP, and identify where access must be enforced.
5. Turn a clinical need into an exchange requirement and explain how standards development and Connectathons help test it, while leaving local workflow validation necessary.

## Delivery map

| Time | Slides | Teaching question |
| --- | --- | --- |
| 0–7 | 1–3 | What would you delegate, and what would the tool need? |
| 7–15 | 4–6 | Who did the adapting in the email workflow? |
| 15–27 | 7–11 | What context and permissions must survive clinical exchange? |
| 27–39 | 12–16 | How do vendor-specific and shared-standard integration compare? |
| 39–49 | 17–20 | How do clinicians shape requirements and test implementations? |
| 49–56 | 21–22 | Can you repair a flawed exchange proposal? |
| 56–60 | 23–24 | What evidence questions go to M4? |

Each slide contains a section time block, a `data-duration` value in seconds and delivery notes. Reveal fragments stage comparisons and discussion. Notes include prompts, transitions, exercise timing and relevant sources. The four-minute paired exercise asks residents to identify missing clinical context, excessive permissions and one observable acceptance test; the debrief takes three minutes.

## Scope and limits

The deck preserves patient/encounter identity, dates, units, originals, provenance and uncertainty as requirements. It distinguishes portable export, authorized retrieval and returning a reviewable result without making these implementation stages the main learning goal. Read-only retrieval precedes a draft; clinician review and separately authorized writeback are distinct steps.

DICOM supplies the imaging example; applicable HL7 standards, including FHIR, address wider clinical/administrative exchange. Versions, profiles, terminology and actual supported operations matter. A harness connects a model to tools; MCP exposes selected operations but does not replace clinical meaning or resource-side permission enforcement. Filtered tools and independently restricted accounts are complementary controls. Connectathons provide bounded exchange-testing evidence, not universal certification or a guarantee of safe AI.

M1 supplies the problem framing; M2 supplies actors, storage and interfaces. M3 turns clinical needs into exchange requirements. M4 applies those requirements to product demonstrations, contracts and archive control. The broader four-module reframe remains incomplete. See the [approved direction and its proposal provenance](PLAN.md) and the [course overview](../README.md).

## Open and check the deck

- [Slide manifest](index.html): order and local slide references.
- From the repository root, run `python3 serve.py`, then open `http://127.0.0.1:54385/lectures/slides/orthodontic-informatics/module3/`.
- From the repository root, run `python3 -m unittest discover -s tests -p test_module3.py -v` to check the manifest, local assets/links, slide notes and total scheduled duration with the standard library HTML parser.

The 24-slide deck passed independent, passage-cited comprehension review and separate technical checks, including unit tests and local links. All 24 slides loaded in real Chromium without JavaScript or HTTP failures; the exercise and comparison were fully visible after style-only layout fixes. The implementation is verified for PR review, not clinical deployment or measured benefits. A lecturer-led timed rehearsal remains pending; these checks do not establish clinical correctness or a rehearsed 60-minute delivery.

## Sources for the clinical exchange concepts

- [DICOM standard and conformance documents](https://www.dicomstandard.org/current)
- [HL7 FHIR overview](https://hl7.org/fhir/summary.html) and [profiles / implementation guides](https://hl7.org/fhir/profiling.html)
- [MCP architecture](https://modelcontextprotocol.io/docs/learn/architecture)
- [IHE background](https://www.ihe.net/about_ihe/) and [Connectathon testing scope](https://www.ihe.net/testing/connectathon/)
