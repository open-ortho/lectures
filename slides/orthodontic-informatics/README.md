# Orthodontic Informatics

This course is an introduction to medical/dental informatics for dental and orthodontic students.

## Goal

The point is not to turn clinicians into software engineers. The goal is to help future providers:

- M1
  - Reduce lock-in risk (including the risk of losing access to patient data). M1
  - Understand the hidden overhead costs of proprietary formats, brittle interfaces, and one-off workflows.
- M2
  - Set reasonable expectations for vendors and integrations.
- M3
  - Identify the role of the provider in informatics: they are not just the consumer (as tends to be the case now), they also need to be the drivers for requirements (M3, when standards and SDOs are covered).
- M4
  - Choose software more intentionally (and choose what to avoid)

The course is organized into four modules, each delivered as a 1h lecture, using its own reveal.js slide deck.

## Modules

- Module 1: Problem framing - why informatics matters, what breaks, and how data sharing fails.
- Module 2: Workflow + infrastructure - how data should flow through a clinic by the means of databases, storage, and interfaces.
- Module 3: Interoperability - proprietary vs open standards, how standards get built, and how the community tests them.
- Module 4 (draft): "What is the best software out there?" - how to evaluate products and vendors to find what is best for you.

## Reusable chapter footer (opt-in)

This custom Reveal.js footer shows the audience only the current chapter: “Introduction”, “Review” or a numbered label derived from the deck's outline. The per-slide `data-chapter` mapping selects that label; it updates on readiness, slide changes and asynchronous external slide loading, including direct links. It is not native Reveal functionality and provides no navigation, menu or timer. Its CSS positions and styles only the footer, using responsive sizing and leaving room for controls and the progress bar; it does not replace the deck theme.

Deck authors can reuse [chapter-nav.js](chapter-nav.js) and [chapter-nav.css](chapter-nav.css), the browser runtime assets in `slides/orthodontic-informatics/`. Only [Module 3](module3/index.html) currently opts in; placing these assets at course level does not enable them in other modules. [chapter-nav.test.cjs](chapter-nav.test.cjs) is a Node.js CommonJS regression test using Module 3 as its explicit fixture, not a script to load in a deck.

To opt a deck in, the author edits that deck's `index.html`; no changes to `common.js`, vendor code or other decks are required. The current implementation requires a flat list of horizontal slides and an ordered outline as the second slide (index 1). Keep its chapter names in audience-facing `ol > li` items, without nested lists or other ordered lists on that slide, because those items supply the footer labels in order.

1. Link `../chapter-nav.css` in the deck's `<head>`.
2. Inside `.reveal`, immediately after the closing `.slides` container, add `<div id="chapter-footer" hidden></div>`. Keeping the footer outside `.slides` prevents Reveal's slide scaling from resizing it.
3. Assign `data-chapter` to each manifest `<section>` placeholder, including references to shared slides. Use `"1"`, `"2"`, etc. for the corresponding outline item; `"introduction"` and `"review"` display the fixed labels “Introduction” and “Review”. Missing or unmatched values hide the footer. Keep these attributes in the manifest, not only in external slide files.
4. After the deck markup, load `<script src="../chapter-nav.js"></script>` immediately **before** the existing `<script src="../common.js"></script>`. The footer script must capture the manifest chapter IDs before the shared loader replaces the placeholders and removes their attributes. It then refreshes the label on Reveal readiness, slide changes and asynchronous slide insertion.

Use [Module 3's manifest](module3/index.html) as the working placement example; retain each deck's own chapter assignments and outline rather than copying Module 3's content. These relative asset paths assume an `index.html` one directory below this course directory. To check the existing implementation from the repository root, run `node --test slides/orthodontic-informatics/chapter-nav.test.cjs` and `python3 -m unittest discover -s tests -p test_module3.py -v`. Those tests cover the opted-in Module 3, not a newly adapted deck: preview that deck separately and check the introduction, review and numbered labels in both navigation directions, including direct links and the shared closing. Moving the assets does not authorize or perform another deck's opt-in.
