---
# lectures-2g3g
title: Reframe in AI terms
status: in-progress
type: task
priority: normal
created_at: 2026-09-28T04:28:34Z
updated_at: 2026-11-19T22:12:26Z
---

Today, people are mainly interested in AI, AI is the hype, the buzzword. People
hear it from places, don't really get it, and are blown away by it. My
presentation for doctors is really hard to raise interest without any AI. Since
there is a strong connection between interoperability and AI, which i was giving
for granted, this should be emphasized and clarified and used to hook the
audience.

## Abstract

**Proposed title:** Before AI Can Help Your Practice, Your Data Has to Work

Start with a useful ambition: delegate a task such as preparing a case for the next visit. This is an illustrative teaching task, not a demonstrated top priority for residents. When we copy notes, label images, reconcile dates and reformat information before feeding it to AI, we are doing the adapting ourselves. Clinical software should preserve meaningful records and normalize reusable context for export and authorized retrieval/exchange, so clinicians and permitted tools do not repeatedly rebuild the same input. This course explains what must survive that exchange and how to ask for evidence that it works. Standards support reuse; they do not guarantee compatible systems, safe access or correct AI results.

**M3 implementation:** The approved [60-minute direction](../slides/orthodontic-informatics/module3/PLAN.md) is implemented in 26 HTML slides for second-year orthodontic residents. The deck includes the bounded email story, synthetic clinical case, exchange/access requirements, equivalent integration comparison, clinician-led requirements, Connectathon limits and paired exercise. For the earlier 24-slide revision, independent passage-cited comprehension review of all 24 slides and separate technical checks passed; all 24 slides loaded in real Chromium without JavaScript or HTTP failures. The earlier revision was verified for PR review; the restored 26-slide revision requires fresh independent comprehension review followed by a separate technical/browser check; lecturer-led timed rehearsal remains pending. The broader four-module reframe is incomplete; this bean remains in progress.

## Plan

### Core argument

AI can use unstructured data, just as a clinician can infer meaning from a messy chart. But if patient identity, visit date, diagnoses, history, treatment events, image metadata, or provenance has to be inferred afresh every time a record is used, each use incurs inference cost and a chance of error. Put reliable structure at the source, preserve it when exchanging data, and validate it where appropriate; then AI can spend its effort on the clinical task instead of repeatedly reconstructing the basics. Standards do not make AI unnecessary, nor do they guarantee correct results. They make routine data exchange and reuse more reliable and testable.

### Four-module narrative

1. **The promise and the bottleneck (M1):** Why can't AI reliably use the clinical records we already have? Bring the existing AI and Research question near the opening. Show a patient record whose history, diagnoses, visits, treatment notes, and imaging are scattered or poorly linked. The phone photo of an X-ray remains one vivid example, not the whole problem. Establish consequences for care as well as AI.
2. **Follow the patient's data (M2):** How does information from an encounter become a usable longitudinal record? Teach actors, workflow, databases, storage, and interfaces through one patient journey; include notes, diagnoses, history, treatment events, and imaging, showing where identity, time, and context are captured or lost.
3. **Make systems work together (M3):** How could a tool receive the right clinical context and return a result to the right patient and encounter? Contrast proprietary interfaces with open standards; connect standards development and connectathons to verifying real interoperability, not merely claimed support. DICOM is the imaging example, not a catch-all for clinical data.
4. **Buy for evidence, not promises (M4):** How do I evaluate an AI-enabled product or any clinical software? Use the existing evaluation framework, export/import demo, contract, archive, and red flags. Ask which clinical data and identifiers the tool needs, how outputs link to the patient and relevant encounters, and how the complete record and results can be retrieved.

### Opening and recurring example

Start with a clinician who wants an AI tool to summarize a patient's treatment trajectory and help prepare the next visit. Relevant information spans medical history, diagnoses, treatment notes, encounter dates, images, and changes over time, recorded in different places and sometimes with inconsistent identifiers or terminology. Ask: what does the tool actually receive, what must it infer, and how would its answer be checked and returned to the clinical workflow? Revisit the same case in each module, resolving one obstacle at a time. Sell the clinical ambition first, reveal the data bottleneck, then teach the existing informatics content as the way through it.

### Possible slide: But can't AI just fix messy data?

Show two paths for repeated use of the same record:

- **Infer every time:** reconstruct patient, visit date, diagnoses, relevant history, treatment events, and imaging context from scattered notes or exports; repeat for each downstream system or task. Flexible, but recurrent cost and uncertain matches must be checked.
- **Preserve and exchange the essentials:** capture identifiers, encounters, diagnoses, and other reusable context in appropriate structured fields; keep original notes and imaging data with their metadata, and exchange them through applicable standards. AI can still interpret free text and images, but need not keep guessing basic facts.

Speaker line: 'AI can help us clean up yesterday's mess. It should not be our plan for creating tomorrow's records.' Avoid claiming AI cannot work with unstructured data, that every inference is wrong, that standards eliminate validation, or that cleanup is always a one-time operation. The relevant distinction is repeated probabilistic reconstruction versus reliable, reusable clinical context.

### Research anchors for the later slide draft

- DICOM describes medical images and their related information and outlines how AI-generated imaging objects should retain appropriate identifiers and metadata: https://www.dicomstandard.org/about and https://www.dicomstandard.org/ai
- WHO health-AI guidance emphasizes responsible deployment and governance: https://www.who.int/publications/i/item/9789240029200
- NIST AI Risk Management Framework frames AI as a system to evaluate and manage, not a substitute for dependable workflows: https://www.nist.gov/itl/ai-risk-management-framework



## Versione italiana

### Titolo proposto

**L'IA può aiutare il tuo studio. I tuoi dati sono pronti?**

### Abstract

Partiamo da un obiettivo utile: delegare un compito, per esempio preparare un caso prima della visita successiva. È un esempio didattico, non una priorità principale dimostrata per gli specializzandi. Quando copiamo note, etichettiamo immagini, riconciliamo date e riformattiamo informazioni prima di passarle all'IA, siamo noi a fare da adattatori tra i sistemi. Il software clinico dovrebbe conservare informazioni significative e normalizzare il contesto riutilizzabile per l'esportazione e il recupero/scambio autorizzato, affinché clinici e strumenti autorizzati non debbano ricostruire ogni volta gli stessi dati di ingresso. Il corso spiega che cosa deve sopravvivere allo scambio e quali prove chiedere per verificarlo. Gli standard favoriscono il riuso, ma non garantiscono compatibilità, accesso sicuro o risultati corretti dell'IA.

**Implementazione M3:** La [direzione approvata da 60 minuti](../slides/orthodontic-informatics/module3/PLAN.md) è implementata in 26 slide HTML per specializzandi del secondo anno. Per la precedente revisione da 24 slide, la revisione indipendente della comprensibilità di tutte le 24 slide, con citazioni dei passaggi, e i controlli tecnici separati sono superati; tutte le 24 slide si sono caricate in Chromium reale senza errori JavaScript o HTTP. La precedente revisione era verificata per la PR; la versione ripristinata da 26 slide richiede una nuova revisione indipendente della comprensibilità seguita da controlli tecnici/browser separati; resta da svolgere una prova cronometrata del docente. La riformulazione dei quattro moduli rimane incompleta; questa attività resta in corso.

### Sintesi dei moduli

1. **La promessa e l'ostacolo (M1):** Perché l'IA fatica a usare in modo affidabile i dati clinici che già abbiamo? Mostrare una cartella in cui anamnesi, diagnosi, visite, note di trattamento e immagini sono sparse o mal collegate. La foto di una radiografia rimane un esempio efficace, ma non rappresenta tutto il problema.
2. **Seguire il percorso dei dati del paziente (M2):** Come diventano le informazioni raccolte durante le visite una storia clinica utilizzabile nel tempo? Seguire un unico caso attraverso persone, flussi di lavoro, database, archivi e interfacce, includendo anamnesi, diagnosi, note, trattamenti e immagini.
3. **Far comunicare i sistemi (M3):** Come può uno strumento ricevere il contesto clinico giusto e restituire il risultato al paziente e alla visita corretti? Confrontare integrazioni proprietarie e standard aperti; distinguere una compatibilità dimostrata da una soltanto dichiarata. DICOM è l'esempio per le immagini, non per tutti i dati clinici.
4. **Acquistare sulla base di prove, non di promesse (M4):** Come valutare un prodotto con IA, o qualsiasi software clinico? Mettere alla prova esportazione, importazione e integrazione; esaminare contratto, archivio e segnali d'allarme. Chiedere quali dati clinici servono, come i risultati si collegano al paziente e alle visite pertinenti e come recuperare l'intera cartella e i risultati.



### M3 implementation verification

- TDD: `python3 -m unittest discover -s tests -p test_module3.py -v` first failed against the old manifest: `AssertionError: 12 not greater than or equal to 20`. After implementation the same test passed (`Ran 1 test`, `OK`).
- Standard-library HTMLParser checks 26 unique local slide references, one section and speaker notes per slide, no slide scripts, existing local links/assets with image alt text, no orphan slide files, and scheduled durations totaling 3,600 seconds.
- `git diff --check`, module Markdown relative-link/whitespace checks including new files, and `beans check` passed. Entry-page asset links were corrected locally to `/lectures/...`; the shared runtime/theme/assets are unchanged.
- Sources retrieved for implementation: DICOM current standard, HL7 FHIR summary/profiling, MCP architecture and IHE background/Connectathon scope. This is author source checking, not independent technical acceptance.
- Independent fresh-context, passage-cited comprehension review passed for all 24 slides; the separate technical review passed unit tests, local-link checks and Beans validation. Parent-run real Chromium loaded all 24 slides without JavaScript or HTTP failures. Five style-only layout fixes were verified to preserve semantics; the latest screenshots show the exercise and comparison fully visible.
- The earlier 24-slide M3 implementation was verified for PR review. Lecturer-led timed rehearsal remains pending, and the broader four-module course remains in progress. No clinical integration, sending, patient upload, live writeback, measured benefits or completed four-module course is claimed. No commit or push performed; publication remains parent-owned.

### PR4 title, outline and notes-only timing correction

- Restored the M2/M4 course-title table convention with the QR code in the left 33% column, Module 3 subtitle AI and Reusable Clinical Data, and original speaker format. The second slide is an actual Outline; hook and synthetic case are preserved as slides 3–4. Review is slide 5.
- The deck now has 26 slides within a maximum of 30. The first five durations are 30/30/90/150/120 seconds; other durations remain unchanged, preserving 3,600 seconds. README/PLAN ranges shift by two; the first section is slides 1–5.
- Every section time range and section name is in speaker notes only, not visible main-slide content. Actual titles and meaningful synthetic-case labels remain unchanged. No shared runtime or other module changed.
- TDD red: four tests ran and failed as expected (27 failure reports: missing title table, 24 rather than 26 slides, missing opening order, and 24 missing notes-only section labels). Green evidence follows after execution. Fresh-context passage-cited comprehension review and a subsequent separate technical/browser check are parent-owned and pending; the author does not self-approve. No commit or push.


- Correction green: `python3 -B -m unittest discover -s tests -p test_module3.py -v` passed all four tests. The 26-slide manifest totals 3,600 seconds, with 26 notes-only timing labels and all local references/alt text/notes validated. Exact-content comparison confirms the 24 original slides differ only by the requested timing-label move and the two opening duration changes. Module/Bean relative Markdown links, `git diff --check`, and `beans check` passed. Independent comprehension and subsequent technical/browser acceptance remain pending with the parent.

### Corrected 26-slide revision acceptance

Fresh-context comprehension passed for the restored title, outline and notes-only labels. Separate technical checks passed all four regression tests, links, duration and whitespace. Chromium loaded all 26 slides without JavaScript or HTTP errors; title and outline screenshots confirm the standard QR/course layout, visible roadmap and absence of audience-facing timing labels. Scheduled duration remains 3,600 seconds. Timed lecturer rehearsal and broader course work remain unfinished.
