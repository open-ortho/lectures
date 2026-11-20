# M3: approved teaching direction and implementation map

## Status and provenance

This document began as the high-level proposal for a 60-minute lecture for second-year orthodontic residents. That teaching direction has been approved for slide implementation. The [current deck](index.html) now implements it in 27 slides; the [module guide](README.md) describes delivery. The former proposal-only approval gate is superseded, not an outstanding request for authorization to author slides.

Approval concerns the lecture argument and content. It does not approve a live clinical integration, patient-data upload or writeback. The current 27-slide deck has passed independent presenter-note comprehension review, followed by structural and Chromium checks. It retains the standard opening, short notes with bold concepts and notes-only timing, and removes the standalone review-before-writeback slide. The broader four-module reframe remains in progress, and a lecturer-led timed rehearsal remains pending. The [course overview](../README.md) still describes the broader course.

## Central argument

Start with the useful ambition of delegating preparation of a source-linked visit brief. This is an illustrative teaching task, not an established top priority for this resident cohort. When a clinician selects notes, labels images, resolves dates and reformats records before giving them to AI, the clinician is acting as the adapter between systems. Software should preserve meaningful records and reusable context so authorized tools do not repeatedly need the same human reconstruction. AI can interpret free text and images; structured context reduces avoidable reconstruction but does not prove clinical correctness.

## Learning objectives

1. Explain how manual preparation for AI can make the clinician perform work that clinical software should make reusable.
2. Identify what clinical software must make available so another authorized tool can use its data without the clinician manually collecting, reformatting, and explaining the records each time.
3. Compare integration using vendor-specific interfaces with integration using shared open clinical standards, without assuming that either approach guarantees compatibility, safety or clinical accuracy.
4. Describe the different jobs of clinical data standards, an AI harness and MCP, and identify where access must be enforced.
5. Turn a clinical need into an exchange requirement and explain how standards development and Connectathons help test it, while leaving local workflow validation necessary.

## Implemented 60-minute structure

The allocations include discussion and transitions; individual slides carry scheduled durations in seconds. Slide 14, “What must the software make available?”, is allocated four minutes, including the two minutes reassigned from the removed standalone review-before-writeback slide. Section time boundaries remain unchanged.

| Time | Minutes | Slides | Section |
| --- | ---: | --- | --- |
| 0–7 | 7 | 1–5 | Course title; outline; recall M1/M2; useful delegation; synthetic P-18 case |
| 7–15 | 8 | 6–10 | Presenter email story; matching traditional/agentic email diagrams; harness/MCP; complementary access limits |
| 15–27 | 12 | 11–14 | Clinical analogy; reusable context; normalization; exchange capabilities and reviewable results |
| 27–39 | 12 | 15–19 | Equivalent integration approaches; standards scope; profiles; meaning versus tools |
| 39–49 | 10 | 20–23 | Clinician requirements; standards development; bounded Connectathon testing |
| 49–56 | 7 | 24–25 | Paired case exercise and debrief |
| 56–60 | 4 | 26–27 | Recap and evidence questions for M4 |
| **Total** | **60** | **27** | |

## Presenter story and clinical analogy

The presenter supplied the nonclinical email account: before, copying an email into an AI chat and copying the generated answer back; now, agents use tools to read email, compose replies and save drafts. The harness is the software surrounding the model that connects it to tools and manages interaction. Filtered and modified Model Context Protocol (MCP) servers expose selected operations. Agents have their own accounts, separate from the human account, with independently restricted permissions on underlying resources. Tool filtering and resource-side permissions serve complementary purposes. This story claims neither sending nor measured time savings. Slides 7–8 compare illustrative MBOX storage served by IMAP to a human mail client, then to an MCP server connected to the harness/model. The same dashed line marks the client-facing IMAP mailbox-authentication edge: the human account in both diagrams. In the second, the MCP server exposes only selected tools; that limits this path, not the underlying account. This alternative is distinct from the presenter’s separate-agent-account setup. The model does not receive raw credentials. MBOX is not universal provider storage, and Gmail is only a familiar webmail example, not the deployment shown. Other authentication may exist; these are not complete security diagrams.

The explicit transition on slide 11 separates that account from a proposed clinical scenario, not a deployed integration. Copying screenshots from one product and re-entering information in another is contrasted with products requesting records through application programming interfaces (APIs). Each consuming product uses its own restricted identity, independently configured from other products and the human. The synthetic P-18 case illustrates requirements; it is not a captured clinical result.

## Exchange and review boundaries

- **Export:** a portable record another system can interpret, not merely an available download.
- **Authorized retrieval:** minimum necessary context through a permitted interface under restricted credentials, not automatic access to every record.
- **Result return:** a source-linked draft associated with the relevant patient and encounter, showing omissions and uncertainty, not an automatically accepted chart entry.

Preserve identity, encounter, dates and time context, values, units, method, originals and provenance. Normalization makes representations consistent; it must not silently overwrite source material. Flag uncertain matches and missing information instead of inventing them. Keep links from derived results to sources.

The conceptual flow is source → access-enforcing service → permitted retrieval → harness/model → reviewable draft → clinician review → separately authorized writeback, if a future workflow permits it. Start with read-only retrieval. Services and credential configuration outside the model enforce access and retain audit records. Exported copies also need access and handling controls.

## Standards and clinician participation

Integration using vendor-specific interfaces and integration using shared open clinical standards are compared against the same task and evidence questions. Either can be well maintained or fail in implementation; shared specifications can reduce repeated work but do not guarantee cost, upgrade stability, compatibility or safety.

DICOM covers imaging and related information/services, not every clinical fact. HL7 develops healthcare exchange standards, including FHIR. Applicable versions, profiles, implementation guidance, terminology and supported operations determine what an implementation can actually exchange. MCP standardizes tool access, not clinical semantics or identity reconciliation. Neither a clinical standard nor MCP makes AI output correct by itself.

Clinicians state use cases and failure conditions. Standards experts and implementers check gaps, develop corrections or guidance and test implementations. The former historical timeline is replaced with this collaboration model; unsupported launch dates are not retained. Connectathons test selected implementations, roles and defined transactions. Participation or a passed test is not universal certification, local acceptance or validation of an AI interpretation. The existing IHE North America photo illustrates the testing setting, not a test of our case.

## Resident application and course boundary

Pairs inspect a deliberately flawed exchange proposal: missing date/units, an uncertain encounter, absent history, the clinician's full-access login and unreviewed chart writeback. They produce a missing-context finding, a permission finding and one testable requirement. The debrief turns these into observable behaviors, such as flagging an omitted unit instead of guessing.

M1 establishes why reuse matters; M2 supplies topology and flow. M3 asks what meaning and permissions must cross those boundaries, and how clinicians shape and test the agreement. M4 evaluates products, contracts and archives using the resulting evidence questions. This lecture is not a deployment tutorial, a procurement workshop or an authorization for autonomous treatment decisions.
