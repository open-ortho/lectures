---
# lectures-2g3g
title: Reframe in AI terms
status: todo
type: task
priority: normal
created_at: 2026-09-28T04:28:34Z
updated_at: 2026-09-28T09:29:36Z
---

Today, people are mainly interested in AI, AI is the hype, the buzzword. People
hear it from places, don't really get it, and are blown away by it. My
presentation for doctors is really hard to raise interest without any AI. Since
there is a strong connection between interoperability and AI, which i was giving
for granted, this should be emphasized and clarified and used to hook the
audience.

One possible hook/abstract could be something like: "Everyone is talking about
AI these days, ai for this, ai for that, add it in this product, how do i use to
achieve that, all application level. But nobody is talking about the foundation
of it, not the math/statistics behind LLM, but the importance of structured
data. Just like you can't do much when everything is a mess, so can't the AI,
and it has to spend enormous amount of time cleaning up the mess first. This is
what i will talk about, how to avoid the mess which you currently have, and how
to clean it up, s.t. using AI will then be orders of magnitude more
powerful/genrate more useufl data."

Once i have an abstract, we can draft out the plan for how to reframe the
orthodontic-informatics course.

## Abstract

**Proposed title:** Before AI Can Help Your Practice, Your Data Has to Work

AI promises to help orthodontists make sense of clinical information, follow treatment progress, and support decisions. But what happens when diagnoses, medical histories, treatment notes, encounters, and images are scattered across systems, inconsistently recorded, or disconnected from the right patient and time point? This course follows a patient's clinical record through an orthodontic practice to show why these everyday problems matter for both care and AI. You'll learn how clinical data is captured and exchanged, what standards can make possible, and how to test a vendor's claims rather than take them on faith. You won't need to build an AI model: you'll leave knowing what to ask for so your practice's data remains usable, portable, and ready for future tools.

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

L'intelligenza artificiale promette di aiutare gli ortodontisti a interpretare i dati clinici, seguire l'evoluzione dei trattamenti e supportare le decisioni. Ma cosa succede se diagnosi, anamnesi, note di trattamento, visite e immagini sono sparse tra sistemi diversi, registrate in modo incoerente o non collegate al paziente e al momento giusti? Questo corso segue la cartella clinica di un paziente attraverso uno studio ortodontico per mostrare perché questi problemi quotidiani contano sia per la cura sia per l'IA. Scoprirai come vengono raccolti e scambiati i dati clinici, che cosa rendono possibile gli standard e come verificare concretamente le promesse dei fornitori. Non dovrai sviluppare un modello di IA: imparerai quali domande porre affinché i dati del tuo studio restino utilizzabili, trasferibili e pronti per gli strumenti futuri.

### Sintesi dei moduli

1. **La promessa e l'ostacolo (M1):** Perché l'IA fatica a usare in modo affidabile i dati clinici che già abbiamo? Mostrare una cartella in cui anamnesi, diagnosi, visite, note di trattamento e immagini sono sparse o mal collegate. La foto di una radiografia rimane un esempio efficace, ma non rappresenta tutto il problema.
2. **Seguire il percorso dei dati del paziente (M2):** Come diventano le informazioni raccolte durante le visite una storia clinica utilizzabile nel tempo? Seguire un unico caso attraverso persone, flussi di lavoro, database, archivi e interfacce, includendo anamnesi, diagnosi, note, trattamenti e immagini.
3. **Far comunicare i sistemi (M3):** Come può uno strumento ricevere il contesto clinico giusto e restituire il risultato al paziente e alla visita corretti? Confrontare integrazioni proprietarie e standard aperti; distinguere una compatibilità dimostrata da una soltanto dichiarata. DICOM è l'esempio per le immagini, non per tutti i dati clinici.
4. **Acquistare sulla base di prove, non di promesse (M4):** Come valutare un prodotto con IA, o qualsiasi software clinico? Mettere alla prova esportazione, importazione e integrazione; esaminare contratto, archivio e segnali d'allarme. Chiedere quali dati clinici servono, come i risultati si collegano al paziente e alle visite pertinenti e come recuperare l'intera cartella e i risultati.
