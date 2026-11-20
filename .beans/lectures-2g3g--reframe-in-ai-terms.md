---
# lectures-2g3g
title: Reframe in AI terms
status: in-progress
type: task
priority: normal
created_at: 2026-09-28T04:28:34Z
updated_at: 2026-11-20T04:19:19Z
---

Today, people are mainly interested in AI, AI is the hype, the buzzword. People
hear it from places, don't really get it, and are blown away by it. My
presentation for doctors is really hard to raise interest without any AI. Since
there is a strong connection between interoperability and AI, which i was giving
for granted, this should be emphasized and clarified and used to hook the
audience.

## Abstract

**Proposed title:** Before AI Can Help Your Practice, Your Data Has to Work

Start with a useful ambition: delegate work such as preparing a treatment presentation, capturing patient history, preparing treatment consent forms, organizing photos and scans, or opening clinical apps and uploading aligner records. These are illustrative teaching tasks, not demonstrated top priorities for residents or deployed clinical automation. When we copy notes, label images, reconcile dates and reformat information before feeding it to AI, we are doing the adapting ourselves. Clinical software should preserve meaningful records and normalize reusable context for export and authorized retrieval/exchange, so clinicians and permitted tools do not repeatedly rebuild the same input. This course explains what must survive that exchange and how to ask for evidence that it works. Standards support reuse; they do not guarantee compatible systems, safe access or correct AI results.

**M3 implementation:** The approved [60-minute direction](../slides/orthodontic-informatics/module3/PLAN.md) is implemented in 27 slides for second-year orthodontic residents: 26 module-local slides plus the unchanged shared Open-Ortho closing. Title → outline → M1/M2 prerequisite review precedes the delegation menu and synthetic Patient 18 (P-18) case. The menu motivates a contrast between manual preparation and connected, authorized reuse, not a single summary task. The current ending is three recap slides followed by an M4 preview, not an exercise or homework. [PR #4](https://github.com/open-ortho/lectures/pull/4) is open at `630ab442b8f5e487f624d3851cd38b1ea80a983f`, not merged. Current implementation and verification are recorded below. Human final content review, lecturer-led timed rehearsal and the broader M1/M2/M4 reframe remain outstanding; this bean stays in progress.

## Plan

### Core argument

AI can use unstructured data, just as a clinician can infer meaning from a messy chart. But if patient identity, visit date, diagnoses, history, treatment events, image metadata, or provenance has to be inferred afresh every time a record is used, each use incurs inference cost and a chance of error. Put reliable structure at the source, preserve it when exchanging data, and validate it where appropriate; then AI can spend its effort on the clinical task instead of repeatedly reconstructing the basics. Standards do not make AI unnecessary, nor do they guarantee correct results. They make routine data exchange and reuse more reliable and testable.

### Four-module narrative

1. **The promise and the bottleneck (M1):** Why can't AI reliably use the clinical records we already have? Bring the existing AI and Research question near the opening. Show a patient record whose history, diagnoses, visits, treatment notes, and imaging are scattered or poorly linked. The phone photo of an X-ray remains one vivid example, not the whole problem. Establish consequences for care as well as AI.
2. **Follow the patient's data (M2):** How does information from an encounter become a usable longitudinal record? Teach actors, workflow, databases, storage, and interfaces through one patient journey; include notes, diagnoses, history, treatment events, and imaging, showing where identity, time, and context are captured or lost.
3. **Make systems work together (M3):** How could a tool receive the right clinical context and return a result to the right patient and encounter? Contrast proprietary interfaces with open standards; connect standards development and connectathons to verifying real interoperability, not merely claimed support. DICOM is the imaging example, not a catch-all for clinical data.
4. **Buy for evidence, not promises (M4):** How do I evaluate an AI-enabled product or any clinical software? Use the existing evaluation framework, export/import demo, contract, archive, and red flags. Ask which clinical data and identifiers the tool needs, how outputs link to the patient and relevant encounters, and how the complete record and results can be retrieved.

### Opening and recurring example

After the title, outline and M1/M2 prerequisite review, introduce fictional Patient 18 (P-18) and ask what residents would delegate: prepare the treatment presentation; capture patient history; prepare treatment consent forms; select, orient and import photos and scans; open clinical apps and upload aligner records. Reveal one task at a time, then map the same five tasks to their required records and access. Ask separately how AI would obtain those records and why the clinician would trust them.

The recurring principle is manual preparation versus connected reuse: when the clinician repeatedly collects, reformats and explains the same records, the clinician is the adapter. Preserve meaningful source records and normalized reusable context so authorized software can retrieve what a task needs without rebuilding the input each time. Revisit that principle across the modules. The presenter’s actual email workflow supplies the nonclinical before/after example; the clinical tasks remain proposed teaching scenarios, with clinician responsibility and permission boundaries intact.

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

Partiamo da un obiettivo utile: delegare attività come preparare la presentazione del trattamento, raccogliere l’anamnesi, predisporre i moduli di consenso al trattamento, organizzare fotografie e scansioni oppure aprire le applicazioni cliniche e caricare i documenti per gli allineatori. Sono esempi didattici, non priorità principali dimostrate per gli specializzandi né automazioni cliniche già operative. Quando copiamo note, etichettiamo immagini, riconciliamo date e riformattiamo informazioni prima di passarle all'IA, siamo noi a fare da adattatori tra i sistemi. Il software clinico dovrebbe conservare informazioni significative e normalizzare il contesto riutilizzabile per l'esportazione e il recupero/scambio autorizzato, affinché clinici e strumenti autorizzati non debbano ricostruire ogni volta gli stessi dati di ingresso. Il corso spiega che cosa deve sopravvivere allo scambio e quali prove chiedere per verificarlo. Gli standard favoriscono il riuso, ma non garantiscono compatibilità, accesso sicuro o risultati corretti dell'IA.

**Implementazione M3:** La [direzione approvata da 60 minuti](../slides/orthodontic-informatics/module3/PLAN.md) è implementata in 27 slide per specializzandi del secondo anno: 26 slide locali al modulo più la chiusura condivisa Open-Ortho, invariata. Titolo → programma → ripasso dei prerequisiti M1/M2 precedono le attività da delegare e il caso sintetico Patient 18 (P-18). Le attività introducono il confronto tra preparazione manuale e riuso tramite sistemi collegati e autorizzati, non un unico compito di sintesi. La conclusione comprende tre slide di riepilogo e un’anteprima di M4, senza esercizio né compiti a casa. La [PR #4](https://github.com/open-ortho/lectures/pull/4) è aperta sul commit `630ab442b8f5e487f624d3851cd38b1ea80a983f`, non integrata nel ramo principale. I 17 test Python e i 4 test Node passano; le revisioni indipendenti della comprensibilità, con citazioni dei passaggi, e i successivi controlli tecnici/browser delle parti modificate sono stati superati. Restano la revisione finale dei contenuti da parte del docente, la prova cronometrata e la riformulazione più ampia di M1/M2/M4; questa attività resta in corso. La verifica indipendente di questo aggiornamento del registro precede la sua pubblicazione.

### Sintesi dei moduli

1. **La promessa e l'ostacolo (M1):** Perché l'IA fatica a usare in modo affidabile i dati clinici che già abbiamo? Mostrare una cartella in cui anamnesi, diagnosi, visite, note di trattamento e immagini sono sparse o mal collegate. La foto di una radiografia rimane un esempio efficace, ma non rappresenta tutto il problema.
2. **Seguire il percorso dei dati del paziente (M2):** Come diventano le informazioni raccolte durante le visite una storia clinica utilizzabile nel tempo? Seguire un unico caso attraverso persone, flussi di lavoro, database, archivi e interfacce, includendo anamnesi, diagnosi, note, trattamenti e immagini.
3. **Far comunicare i sistemi (M3):** Come può uno strumento ricevere il contesto clinico giusto e restituire il risultato al paziente e alla visita corretti? Confrontare integrazioni proprietarie e standard aperti; distinguere una compatibilità dimostrata da una soltanto dichiarata. DICOM è l'esempio per le immagini, non per tutti i dati clinici.
4. **Acquistare sulla base di prove, non di promesse (M4):** Come valutare un prodotto con IA, o qualsiasi software clinico? Mettere alla prova esportazione, importazione e integrazione; esaminare contratto, archivio e segnali d'allarme. Chiedere quali dati clinici servono, come i risultati si collegano al paziente e alle visite pertinenti e come recuperare l'intera cartella e i risultati.

## Current M3 implementation and verification

### Implemented content

- **Opening and navigation:** 27 manifest entries, comprising 26 module-local slides and the existing shared Open-Ortho closing. The scheduled total is 60 minutes, not a completed rehearsal. Title, outline and M1/M2 prerequisite review precede the task menu and P-18 input requirements. A module-local footer shows the current chapter; its six numbered labels come from the outline. Introduction and Review are separate footer labels. Delivery timings remain in speaker notes only.
- **Email story and access:** the presenter contrasts copying email into AI chat and copying its answer back with tools that read email, compose replies and save drafts. A manual-transfer illustration accompanies the story. Matching traditional/agentic diagrams show the same mailbox boundary; the agentic SVG is reused as foreground and background artwork, with the human operating the outer harness and the model inside it. The diagram’s limited Model Context Protocol (MCP) path authenticates with the human account: filtering limits that path, not the account’s rights through other clients. This illustrative alternative is distinct from the presenter’s actual filtered tools plus separately permissioned agent accounts. The model receives tools, not raw credentials; sending is not claimed.
- **Clinical reuse:** the proposed clinical analogy preserves identity, encounter, dates, units, source records, provenance and uncertainty. Normalization makes context reusable without overwriting originals. Authorized retrieval, a reviewable result and any separately authorized future writeback remain distinct. The standalone review-before-writeback and meaning-versus-tool-access slides were removed, with time reassigned to adjacent slides; the underlying safety boundaries remain.
- **Integration and standards:** the vendor table defines provider/consumer roles and compares design, implementation and maintenance for the same exchange. Shared standards permit one reusable implementation per product with compatible partners, not one universal program or zero mapping/testing work. The nine-stage U-shaped process shows doctors leading stages 1–2 with developer advice, standards experts leading 3–6 with optional doctor review, developers leading 7–8 with optional doctor review, and stage 9 as a joint outcome. Amendment is conditional; testing feedback returns to profile/implementation work.
- **Testing evidence and conclusion:** both Connectathon photographs appear together. Public lookup links distinguish tested Connectathon capabilities from vendor-declared Product Registry support; the suggested agent lookup requests exact product/version matches, citations and unknowns, not a completed investigation. Three recap slides cover the possible AI benefits of structured/normalized data and interconnection with trust/access controls; DICOM, HL7 FHIR and IHE profiles; and clinicians’ contribution to testable requirements and implementation testing. M4 is a preview, not homework. There is no paired exercise, despite retained legacy filenames for two recap slides.

### Verified state and limits

- Local HEAD and the open PR #4 head match `630ab442b8f5e487f624d3851cd38b1ea80a983f`; PR state is OPEN and `mergedAt` is null. This record update does not merge or publish the lecture.
- Re-run for this tracker reconciliation: `python3 -B -m unittest discover -s tests -p test_module3.py -v` passes all 17 tests; `node --test slides/orthodontic-informatics/chapter-nav.test.cjs` passes all 4 tests. Coverage includes the 27-entry manifest, local assets/links, notes, scheduled duration, opening order, shared closing, chapter assignments and navigation, diagram boundaries and removed slides.
- Prior fresh-context, passage-cited comprehension reviews and subsequent separate technical/browser checks passed for the changed lecture surfaces. Those completed checks are not pending. They do not establish human final content acceptance, a rehearsed 60-minute delivery or a deployed clinical workflow. The updated Bean prose passed its focused fresh-context, passage-cited comprehension review and subsequent technical check against the implementation and PR state.
- The [module guide](../slides/orthodontic-informatics/module3/README.md) and [approved plan](../slides/orthodontic-informatics/module3/PLAN.md) supply the delivery map and teaching direction. Their older summary-hook and pending-review wording, and the outline note about repairing a proposal, predate the latest task-menu/recap revisions; they do not supersede the current state recorded here. This tracker-only update does not edit those sources.
- The personal email account is attributed firsthand experience, not an independently audited deployment. No patient-data upload, deployed clinical integration, live clinical writeback, autonomous treatment decision, measured AI benefit or completed four-module reframe is claimed.

## Remaining acceptance

- [x] Updated Bean prose: focused fresh-context comprehension review and separate technical verification completed; bookkeeping is ready to accompany PR #4.
- [ ] Lecturer: perform final human content/clinical-relevance review of the current M3 deck and a timed rehearsal; revise delivery if needed. Scheduled minutes and browser checks do not satisfy this acceptance.
- [ ] Implement and verify the broader AI/interoperability reframe in M1, M2 and M4 against the retained four-module plan. Current M3 implementation does not complete that course-wide scope.
