# Proposed M3 reframe: from feeding AI to reusable clinical exchange

## Purpose and status

This is a high-level proposal for a 60-minute lecture for second-year orthodontic residents. It reframes Module 3 (M3) around a practical ambition: delegate a useful task without repeatedly assembling and explaining the same clinical information. Preparing a case for the next visit is an illustrative teaching task, not a demonstrated top priority for residents or a validated clinical AI application.

**Central argument:** when a clinician copies notes, labels images, resolves dates and reformats information before giving it to an AI tool, the clinician is acting as the adapter between systems. That preparation can hide the underlying data problem. Clinical software should preserve meaningful records, normalize reusable context and support export and authorized retrieval/exchange, so clinicians and permitted tools can reuse the information without repeating the same manual preparation. AI can interpret free text and images; structured context reduces avoidable reconstruction but does not establish clinical correctness.

The [current deck](index.html) is unchanged. This proposal requests approval of the teaching argument, section structure and boundaries before slide implementation. It does not approve a live clinical integration, patient-data upload or writeback. The broader four-module course reframe and slide implementation remain unfinished; this document does not replace the [current course description](../README.md).

## Learning objectives

By the end of the proposed lecture, residents should be able to:

1. Explain how manual preparation for AI can make the clinician perform work that clinical software should make reusable.
2. Distinguish three operations from one another: exporting a portable copy of clinical records, retrieving records from the source system under limited authorization, and returning a reviewable result. Explain what clinical context must be preserved in each operation.
3. Compare integration using vendor-specific interfaces with integration using shared open clinical standards, without assuming that either approach guarantees compatibility, safety or clinical accuracy.
4. Describe the different jobs of clinical data standards, an AI harness and MCP, and identify where access must be enforced.
5. Turn a clinical need into an exchange requirement and explain how standards development and Connectathons help test it, while leaving local workflow validation necessary.

## Proposed 60-minute structure

The allocation includes discussion and transitions; it is a section plan, not a slide-by-slide script.

| Time | Minutes | Section and resident-facing question | Teaching outcome |
| --- | ---: | --- | --- |
| 0–7 | 7 | **Start with useful delegation.** What would you want a tool to prepare before a visit, and what would it need? | Introduce case preparation using synthetic or appropriately deidentified teaching records. Identify history, diagnoses, notes, encounters and images without asserting that the task is residents' main pain point. |
| 7–15 | 8 | **Who is doing the adapting?** What did the human already select, label and reconcile before AI saw the case? | Contrast manual feeding with reuse through permitted system operations. Use the presenter's bounded personal story, below, without implying a completed clinical integration. |
| 15–27 | 12 | **Make context reusable.** What must survive movement between systems? | Separate export, retrieval and result return; preserve identity, time, meaning, originals and provenance. Draw a controlled exchange, not universal model access. |
| 27–39 | 12 | **Choose an exchange contract.** What changes when two vendors integrate using vendor-specific interfaces rather than shared open clinical standards? | Compare these two integration approaches; distinguish clinical meaning from tool access. Explain the roles and limits of DICOM, HL7/FHIR and MCP at a conceptual level. |
| 39–49 | 10 | **Clinicians help define what gets exchanged.** Who specifies the clinical need and tests implementations? | Follow a requirement through standards development, implementation guidance and Connectathon testing; compress the historical timeline into brief context. |
| 49–56 | 7 | **Apply the argument.** Can a second authorized tool reuse the case without the clinician rebuilding it? | Residents identify missing context, excessive permissions and unreviewed output in a proposed teaching exchange; distinguish a testable requirement from a vendor claim. |
| 56–60 | 4 | **Synthesis and handoff.** What would count as evidence when choosing software? | Check objectives and hand evaluation questions to M4; do not run a procurement workshop here. |
| **Total** | **60** | | |

## Personal story: presenter-supplied evidence, not a clinical success claim

The presenter has described current efforts using an AI harness and setting up MCPs with appropriate access, with powerful capabilities. Use this experience to make the change in interaction concrete, not to claim completed integrations, measured time savings or real patient access.

Begin with the desired task and what the presenter previously had to hand over manually. Then explain how software can connect a model to selected tools: an **AI harness** is the surrounding software that connects the model to tools and manages their interaction. **Model Context Protocol (MCP)** is a protocol for exposing tool operations to such software; it is not a clinical semantic standard, a source of permission by itself or an automatic safety guarantee.

Before writing slides, the presenter must supply:

- **Actual before:** one real, nonclinical example of what was copied, reformatted or selected manually.
- **Actual current state:** what has genuinely been configured, what is still being set up and which tool operations, if any, have actually been exercised. Describe the intended change separately from demonstrated behavior.
- **Permissions and limits:** which system enforces access, which operations and data are allowed, which are excluded, and what requires human approval.
- **Evidence choice:** a verbal account or sanitized teaching reconstruction. A screenshot is optional only if it exists and can be safely shared; do not manufacture one or imply that a reconstruction is a captured result.

Exclude secrets, private identifiers and real patient data. Transition explicitly: “This is my experience with general-purpose tools. The following clinical example is a proposed teaching scenario, not an integration I have deployed.” No clinical performance or time-saving estimate is implied.

## Reusable exchange and controlled access

Use one teaching case across three distinct operations:

1. **Export:** clinical software produces a portable record for use elsewhere. A file download alone does not prove a complete or meaningful export. Specify the included records and metadata and how another system can interpret them.
2. **Authorized retrieval:** a tool requests the minimum necessary context through an interface under limited credentials and permissions. Retrieval may avoid repeated manual uploads, but does not automatically normalize records, grant access or return a result to the record.
3. **Return a reviewable result:** the tool provides a draft linked to the relevant teaching patient, encounter and source information, with uncertainty and omissions visible. A clinician reviews it before any writeback. Producing a response in a chat window is not the same as storing an approved clinical result.

Normalization means making reusable representations consistent, not discarding or silently rewriting source material. Retain original notes and images alongside normalized values, patient and encounter identity, dates and time context, units, metadata and provenance (where information came from and what transformations were applied). Flag uncertain matches and missing information for review instead of inventing them. Retain the link from a derived summary back to its sources.

The teaching flow is: source clinical system → access-enforcing service/interface → permitted retrieval operation → harness/model → reviewable draft → clinician review → separately authorized writeback, if a future workflow permits it. The model must not decide its own access rights. Services and credential configuration outside the model enforce minimum necessary access, limited operations and audit records. Begin with read-only retrieval; neither unrestricted access to all systems nor automatic writeback is the proposed destination. Exported copies also require appropriate handling and access controls.

Standards address different parts of this flow. DICOM (Digital Imaging and Communications in Medicine) is an imaging example, not a representation of every clinical fact. HL7 (Health Level Seven) develops healthcare exchange standards; FHIR (Fast Healthcare Interoperability Resources) is one of them. Their applicable versions, profiles, terminology and actual supported operations matter. MCP exposes tool operations; it does not replace clinical data semantics, reconcile identity or make a clinical system compatible by itself. Standards can support reuse, but do not guarantee that two implementations work together, that access is safe or that an AI result is correct.

## Current-to-proposed section map

The current manifest is [module3/index.html](index.html); the entries below name existing source files, not implemented changes.

| Current material | Proposed treatment |
| --- | --- |
| `orthodontic-informatics.html`, `outline.html` | Reframe the introduction around useful delegation and the clinician-as-adapter contrast. Replace the apologetic “less exciting” framing with a concrete clinical purpose. |
| `review.html` | Short recall of M1's problem and M2's actors, storage and interfaces; do not reteach clinic topology. |
| `proprietary-based-interoperability.html` and `-2.html` | Retain private interfaces and bridge maintenance. Use the case to ask who documents, maintains and permits exchange; avoid categorical claims that every proprietary integration is opaque or unsustainable. |
| `open-standards-based-interoperability.html` and `-2.html` | Retain shared contracts and reusable tooling. Qualify cost, upgrade stability and compatibility as things to test, not guaranteed benefits. Place the clinical-standard/tool-access distinction here. |
| `standards-development-process.html` | Retain clinician-defined requirements, gap analysis, corrections, implementation guidance and testing. Illustrate one requirement: retain patient, encounter, date, units and source links in a reusable case record. |
| `what-going-on.html` | Shorten the timeline to brief ecosystem context, not a date-memorization exercise. Verify any retained historical claims during later slide drafting. |
| `connectathons.html`, `connectathons-2.html` | Retain community testing. Explain what participating implementations tested; do not equate event participation with universal conformance, safe AI or validated local clinical use. |
| Shared `../open-ortho-org.html` close | Preserve the community/participation connection and hand off to M4. No shared-file edit is proposed in this documentation stage. |
| No current dedicated section | Add the bounded personal story, three-operation exchange distinction, access controls and resident application exercise in a later approved slide implementation. |

## Boundaries across the course

- **M1 — Why:** establish the useful clinical ambition and the cost of repeatedly reconstructing context. M3 recalls this argument rather than repeating the entire problem catalogue.
- **M2 — Topology and flow:** explain actors, workflow, databases, storage and interfaces. M3 assumes those building blocks and asks what information and permissions must cross their boundaries.
- **M3 — Reusable exchange with controlled access:** compare exchange approaches, retain clinical meaning, distinguish tool operations from clinical standards, and show how clinicians shape requirements and testing.
- **M4 — Prove and buy:** evaluate products, demonstrate export/import, scrutinize contracts and archives, and test vendor claims. M3 produces questions and acceptance requirements; M4 applies the procurement framework.

This is not a tutorial for deploying MCP servers, writing interfaces, training models or making autonomous treatment decisions. Any future demonstration must use synthetic or appropriately deidentified teaching data and a separately reviewed setup, not live patient uploads.

## Approval criteria before slide implementation

Approve or revise the high-level proposal only when:

- The delegation ambition leads the lecture, and manual feeding versus reusable authorized retrieval/exchange is the single central contrast.
- The section allocation fits 60 minutes and the objectives suit second-year orthodontic residents without requiring programming knowledge.
- The presenter confirms the actual story details and limits; all unspecified evidence remains a slot, not a factual claim.
- Export, retrieval, result return and human-reviewed writeback remain distinct, with originals and clinically meaningful metadata preserved.
- The comparison of integration using vendor-specific interfaces with integration using shared open clinical standards, clinician requirements, standards development and Connectathons remain substantive; the timeline is shortened.
- The harness/MCP distinction and external permission enforcement are clear, with no promise that standards ensure safe or correct AI.
- The M1–M4 boundaries are accepted, and any later slide work is explicitly authorized as a separate implementation stage.

Approval of this plan would settle the proposed teaching direction, not certify a clinical workflow or declare the broader course reframe complete.
