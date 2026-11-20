# Orthodontic Informatics — Module 3

## Make clinical context reusable

This implemented 27-slide lecture is designed for second-year orthodontic residents in a 60-minute session, including discussion and a three-slide takeaway summary. After the course title and section outline, residents briefly recall Modules 1–2 before considering a useful ambition—having a tool prepare a source-linked visit brief—and a synthetic case. They identify what clinical software must expose so another authorized tool can reuse the records without repeated manual assembly. No programming knowledge is required.

The presenter contrasts copying email into AI chat and copying the answer back with agents reading email, composing replies and saving drafts through selected tools. Two matching diagrams compare a mail client with a Model Context Protocol (MCP) tool server and harness/model at the same client-facing Internet Message Access Protocol (IMAP) mailbox-authentication edge. MBOX, a mailbox file format, is illustrative storage, not a claim about Gmail or all providers; Gmail is only a familiar webmail example. The agentic diagram illustrates a limited MCP server authenticating with the human’s email account: its tool filter restricts that path, not the account itself. The presenter’s own separate-agent-account setup is discussed separately. The model receives tools, not raw credentials. This highlighted boundary is mailbox authentication only, not every security layer. The lecture then moves explicitly to a proposed clinical analogy: products exchange records through permitted interfaces using independently restricted identities. The clinical case P-18 is synthetic; the deck does not demonstrate a deployed clinical integration or use patient data.

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
| 0–7 | 1–5 | What would you delegate, and what would the tool need? |
| 7–15 | 6–10 | Who did the adapting in the email workflow? |
| 15–27 | 11–14 | What context and permissions must survive clinical exchange? |
| 27–39 | 15–18 | How do vendor-specific and shared-standard integration compare? |
| 39–49 | 19–22 | How do clinicians shape requirements and test implementations? |
| 49–56 | 23–24 | What should connected AI reuse, and which standards support exchange? |
| 56–60 | 25–27 | What is the clinician's role? Preview M4 and close with Open-Ortho. |

Each of the 26 module-local slides contains its section time range and section name in speaker notes only, plus a `data-duration` value in seconds and delivery notes. Slide 27 reuses the unchanged [shared Open-Ortho closing](../open-ortho-org.html), exactly as Modules 1, 2 and 4 do; it has no separate duration or notes. The final four minutes cover slide 25, “Takeaways: your role”, slide 26, “Next: choosing clinical software”, and this shared closing. Showing the closing is included in the existing two-minute [Module 4 handoff](slides/m4-handoff.html) allocation, not added to the hour. The Open-Ortho presenter cues remain in that handoff’s notes. Timing labels are not shown on the main slides. The opening allocates 30 seconds each to the title and outline, 120 seconds to review, 90 seconds to the hook and 150 seconds to the synthetic case; the email section allocates 90 seconds each to the story, traditional diagram and agentic diagram, 120 seconds to harness/MCP, and 90 seconds to complementary permissions. Its total remains eight minutes. The clinical-context section schedules four minutes for slide 14, “What must the software make available?”, including the two minutes reassigned from the removed standalone review-before-writeback slide. Slide 18 ([“Supports FHIR” is the start of a question](slides/open-standards-based-interoperability-2.html)) is allocated four minutes, including the two minutes reassigned from the removed “A tool connection is not a clinical agreement” slide; section boundaries remain unchanged. Reveal fragments stage comparisons and discussion. Notes include prompts, transitions and relevant sources. Slides 23–25 summarize connected AI and reusable context, the complementary roles of DICOM, HL7 FHIR and IHE profiles, and clinician participation in requirements and implementation testing. Their allocations remain four, three and two minutes respectively; there is no paired exercise.

## Audience chapter footer

Every slide has one small, left-aligned chapter label at the bottom of the viewport, including the title, outline, review and shared closing. It shows only the current chapter, not timings or the full outline. These audience chapters are separate from the scheduled delivery blocks above:

| Slides | Footer label |
| --- | --- |
| 1–2 | Introduction |
| 3 | Review |
| 4–5 | 1. Delegate to AI |
| 6–10 | 2. How I use AI |
| 11–14 | 3. Applying AI to clinical workflows |
| 15–16 | 4. Vendor-specific vs shared-standards communications |
| 17–22 | 5. Current clinical informatics standards |
| 23–27 | 6. Takeaways |

The [manifest](index.html) assigns chapter IDs with `data-chapter`. The module-local [script](chapter-nav.js) snapshots those IDs before external slide replacement discards the placeholder attributes, then reads the six chapter names from the [outline](slides/outline.html), the single source for their wording. One overlay sits outside the scaled `.slides` container; [module-local CSS](chapter-nav.css) keeps its font small and leaves space for controls and the progress bar. The script refreshes on Reveal readiness, slide changes and asynchronous slide insertion. Neither the shared loader nor the shared closing source is changed.

## Scope and limits

The deck preserves patient/encounter identity, dates, units, originals, provenance and uncertainty as requirements. It distinguishes portable export, authorized retrieval and returning a reviewable result without making these implementation stages the main learning goal. Read-only retrieval precedes a draft; clinician review and separately authorized writeback are distinct steps.

DICOM supplies the imaging example; applicable HL7 standards, including FHIR, address wider clinical/administrative exchange. Versions, profiles, terminology and actual supported operations matter. A harness connects a model to tools; MCP exposes selected operations but does not replace clinical meaning or resource-side permission enforcement. Filtered tools and independently restricted accounts are complementary controls. Connectathons provide bounded exchange-testing evidence, not universal certification or a guarantee of safe AI.

M1 supplies the problem framing; M2 supplies actors, storage and interfaces. M3 turns clinical needs into exchange requirements. M4 applies those requirements to product demonstrations, contracts and archive control. The broader four-module reframe remains incomplete. See the [approved direction and its proposal provenance](PLAN.md) and the [course overview](../README.md).

## Open and check the deck

- [Slide manifest](index.html): order, module-local slides and the shared closing reference.
- From the repository root, run `python3 serve.py`, then open `http://127.0.0.1:54385/lectures/slides/orthodontic-informatics/module3/`.
- From the repository root, run `python3 -m unittest discover -s tests -p test_module3.py -v` to check the manifest, local assets/links, slide notes, chapter assignments and total scheduled duration with the standard library HTML parser.
- Run `node --test slides/orthodontic-informatics/module3/chapter-nav.test.cjs` to check chapter updates on readiness, forward/backward navigation, late Reveal loading and asynchronous external slide replacement without additional dependencies.

The earlier deck passed independent presenter-note comprehension review and Chromium checks. The current structural tests cover all 27 slide references, local assets, the 60-minute scheduled duration and notes-only timing on module-local slides. They retain the shared closing’s existing missing-alt exception only for its baseline QR image; module-local images still require alt text. The restored closing and revised delivery map still need independent comprehension review followed by a browser check. A lecturer-led timed rehearsal remains pending; technical checks do not establish clinical correctness or a rehearsed 60-minute delivery.

## Sources for the clinical exchange concepts

- [DICOM standard and conformance documents](https://www.dicomstandard.org/current)
- [HL7 FHIR overview](https://hl7.org/fhir/summary.html) and [profiles / implementation guides](https://hl7.org/fhir/profiling.html)
- [MCP architecture](https://modelcontextprotocol.io/docs/learn/architecture)
- [IHE background](https://www.ihe.net/about_ihe/) and [Connectathon testing scope](https://www.ihe.net/testing/connectathon/)
