"""CS lecture framing/resource contract; not a rehearsal or publication approval.

Run from the repository root: python3 -m unittest discover -s tests -v
External slide assets resolve against the deck URL, as they do in Reveal.
"""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DECK = ROOT / 'slides/2026-cs-club-biomedical-informatics'
TITLE = 'Biomedical Informatics for Computer Scientists'
DESCRIPTION = (
    'A one-hour introduction to biomedical informatics for computer science students. '
    'Explore how computing shapes healthcare through clinical data, software systems, '
    'interoperability, standards, and shared infrastructure. The lecture connects '
    'familiar computer science problems to clinical workflows and introduces existing '
    'tools, communities, and learning resources, with routes into projects and research. '
    'No medical background is required; the goal is to discover the field and its '
    'opportunities, not master every technical detail.'
)
ORIGINAL_SLIDES = [
    'title', 'names-are-messy', 'fast-heuristics', 'problems', 'wasted-resources',
    'common-infrastructure', 'prototype-tools', 'resources', 'dicom', 'dicom-iods-mwl',
    'dicom-browsers', 'weasis-horos', 'dicom-machine-readable', 'hl7v2', 'hl7v3',
    'fhir', 'fhir-ig', 'snomed', 'dcmtk', 'dcm4che', 'openehr',
]


class Node:
    def __init__(self, tag='', attrs=()):
        self.tag = tag
        self.attrs = dict(attrs)
        self.children = []

    def all(self, tag=None):
        for child in self.children:
            if isinstance(child, Node):
                if tag is None or child.tag == tag:
                    yield child
                yield from child.all(tag)

    def text(self, exclude_notes=False):
        if exclude_notes and 'notes' in self.attrs.get('class', '').split():
            return ''
        return ''.join(child.text(exclude_notes) if isinstance(child, Node) else child
                       for child in self.children)


class Document(HTMLParser):
    VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link',
            'meta', 'param', 'source', 'track', 'wbr'}

    def __init__(self, text):
        super().__init__()
        self.root = Node()
        self.stack = [self.root]
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in self.VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID:
            self.stack.pop()

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                self.stack = self.stack[:index]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def parsed(path):
    return Document(path.read_text()).root


def normalized(node, exclude_notes=False):
    return ' '.join(node.text(exclude_notes).split())


def manifest():
    return [node.attrs['data-external-replace']
            for node in parsed(DECK / 'index.html').all('section')
            if 'data-external-replace' in node.attrs]


class CSLecture(unittest.TestCase):
    def test_approved_title_aligns_browser_opening_and_catalog(self):
        self.assertEqual(normalized(next(parsed(DECK / 'index.html').all('title'))), TITLE)
        first = DECK / manifest()[0]
        self.assertEqual(first, DECK / 'slides/title.html')
        self.assertEqual(normalized(next(parsed(first).all('h2'))), TITLE)
        links = [node for node in parsed(ROOT / 'index.html').all('a')
                 if node.attrs.get('href') ==
                 'slides/2026-cs-club-biomedical-informatics/index.html']
        self.assertEqual([normalized(node) for node in links], [TITLE])

    def test_opening_preserves_qr_presenter_layout_subtitle_and_audience(self):
        opening = parsed(DECK / manifest()[0])
        self.assertEqual(next(opening.all('table')).attrs['style'], 'width:100%;')
        cells = list(opening.all('td'))
        self.assertEqual(cells[0].attrs['style'], 'width: 33%;')
        self.assertEqual(cells[1].attrs['style'], 'vertical-align: top;')
        qr = next(opening.all('img'))
        self.assertEqual(qr.attrs['src'], 'url_qrcode.svg')
        self.assertEqual(qr.attrs['style'], 'width:100%')
        self.assertTrue(qr.attrs.get('alt'))
        self.assertTrue((DECK / qr.attrs['src']).is_file())
        self.assertIn('Data, Systems, Standards, and Infrastructure in Healthcare',
                      normalized(opening, True))
        self.assertIn('For Computer Science Students', normalized(opening, True))
        self.assertIn('toni magni, BME - afm@case.edu', normalized(opening, True))
        notes = [node for node in opening.all('aside')
                 if 'notes' in node.attrs.get('class', '').split()]
        self.assertEqual(len(notes), 1)
        self.assertIn('No medical background', normalized(notes[0]))
        self.assertIn('orientation', normalized(notes[0]).lower())

    def test_booking_description_is_exact_in_metadata_and_copy_ready_readme(self):
        descriptions = [node.attrs.get('content')
                        for node in parsed(DECK / 'index.html').all('meta')
                        if node.attrs.get('name') == 'description']
        self.assertEqual(descriptions, [DESCRIPTION])
        readme = DECK / 'README.md'
        self.assertTrue(readme.is_file(), 'Missing deck README with booking copy')
        text = readme.read_text()
        self.assertIn(f'```text\n{TITLE}\n```', text)
        self.assertIn(f'```text\n{DESCRIPTION}\n```', text)
        for phrase in ('computer science students', 'orientation', '60-minute',
                       'not been rehearsed', 'not been rewritten',
                       'python3 -m unittest discover -s tests -v', 'make serve',
                       'http://127.0.0.1:54385/lectures/slides/'
                       '2026-cs-club-biomedical-informatics/'):
            self.assertIn(phrase, text)

    def test_catalog_description_names_audience_without_booking_length(self):
        rows = [row for row in parsed(ROOT / 'index.html').all('tr')
                if any(a.attrs.get('href') ==
                       'slides/2026-cs-club-biomedical-informatics/index.html'
                       for a in row.all('a'))]
        self.assertEqual(len(rows), 1)
        description = normalized(list(rows[0].all('td'))[1])
        self.assertIn('computer science students', description)
        self.assertLess(len(description), len(DESCRIPTION))

    def test_existing_slide_order_is_preserved_without_chapter_footer(self):
        references = manifest()
        originals = [f'slides/{name}.html' for name in ORIGINAL_SLIDES]
        self.assertEqual([ref for ref in references if ref in originals], originals)
        self.assertEqual(len(references), len(set(references)))
        entry = (DECK / 'index.html').read_text()
        self.assertNotIn('chapter-nav', entry)
        self.assertNotIn('chapter-footer', entry)

    def test_two_further_learning_slides_follow_last_technical_slide(self):
        references = manifest()
        self.assertEqual(references, [f'slides/{name}.html' for name in ORIGINAL_SLIDES] + [
            'slides/further-learning-course.html', 'slides/further-learning-books.html'])
        self.assertEqual(set(DECK.joinpath('slides').glob('*.html')),
                         {DECK / ref for ref in references})
        self.assertEqual(normalized(next(parsed(DECK / 'slides/resources.html').all('h2'))),
                         'Resources')

    def test_optional_course_provides_official_links_and_prerequisite_context(self):
        source = DECK / 'slides/further-learning-course.html'
        self.assertTrue(source.is_file(), 'Missing audience-facing course follow-up')
        slide = parsed(source)
        self.assertEqual({node.attrs['href'] for node in slide.all('a')}, {
            'https://omscs.gatech.edu/cs-6440-intro-health-informatics',
            'https://omscs.gatech.edu/cs-6440-intro-health-informatics-course-videos',
        })
        visible = normalized(slide, True)
        for phrase in ('Georgia Tech', 'CS 6440', 'Jon Duke', 'Elizabeth Shivers',
                       'basic CS', 'programming', 'No health-informatics background',
                       'full course', 'orientation talk', 'Optional', 'not prerequisites'):
            self.assertIn(phrase, visible)

    def test_optional_books_provide_authors_years_scope_and_exact_links(self):
        source = DECK / 'slides/further-learning-books.html'
        self.assertTrue(source.is_file(), 'Missing audience-facing books follow-up')
        slide = parsed(source)
        self.assertEqual({node.attrs['href'] for node in slide.all('a')}, {
            'https://books.google.com/books/about/Hacking_Healthcare.html?id=8ZBxeohRSXoC',
            'https://link.springer.com/book/10.1007/978-3-030-91563-6',
        })
        visible = normalized(slide, True)
        for phrase in ('Hacking Healthcare', 'Fred Trotter', 'David Uhlman',
                       'O’Reilly', '2011', 'US-focused', 'dated', 'not current policy',
                       'Health Informatics on FHIR', 'Mark L. Braunstein',
                       '2nd ed.', '2022', 'Springer', 'interoperable apps',
                       'API ecosystem', 'CS/IT', 'not the whole field',
                       'Optional', 'not prerequisites'):
            self.assertIn(phrase, visible)

    def test_new_learning_slides_have_short_bold_keyed_presenter_cues(self):
        for name in ('further-learning-course', 'further-learning-books'):
            source = DECK / f'slides/{name}.html'
            with self.subTest(slide=name):
                self.assertTrue(source.is_file(), f'Missing {source.name}')
                slide = parsed(source)
                self.assertEqual(len(list(slide.all('section'))), 1)
                self.assertLessEqual(len(normalized(next(slide.all('h2')))), 35)
                notes = [n for n in slide.all('aside')
                         if 'notes' in n.attrs.get('class', '').split()]
                self.assertEqual(len(notes), 1)
                cues = list(notes[0].all('li'))
                self.assertGreaterEqual(len(cues), 2)
                self.assertLessEqual(len(cues), 4)
                for cue in cues:
                    key = list(cue.all('strong'))
                    self.assertEqual(len(key), 1)
                    self.assertLess(len(normalized(key[0])), len(normalized(cue)))
                    self.assertLessEqual(len(normalized(cue)), 210)

    def test_further_learning_readme_links_explain_optional_scope_and_evidence(self):
        text = (DECK / 'README.md').read_text()
        for phrase in ('## Further learning', 'Optional follow-up', 'not prerequisites',
                       'full course', 'basic CS', 'programming',
                       'No health-informatics background',
                       'US-focused', 'dated', 'not current policy', 'CS/IT',
                       'not the whole field', 'not watched', 'not read',
                       'https://omscs.gatech.edu/cs-6440-intro-health-informatics',
                       'https://omscs.gatech.edu/cs-6440-intro-health-informatics-course-videos',
                       'https://books.google.com/books/about/Hacking_Healthcare.html?id=8ZBxeohRSXoC',
                       'https://link.springer.com/book/10.1007/978-3-030-91563-6'):
            self.assertIn(phrase, text)
        for url in re.findall(r'\]\(([^)]+)\)', text):
            if not urlsplit(url).scheme:
                self.assertTrue((DECK / unquote(urlsplit(url).path)).exists(), url)

    def test_manifest_and_slide_assets_resolve_against_the_deck_url(self):
        references = manifest()
        for source in [DECK / 'index.html', *(DECK / ref for ref in references)]:
            with self.subTest(source=source.name):
                self.assertTrue(source.is_file(), str(source))
                for node in parsed(source).all():
                    for attribute in ('src', 'href', 'data-external-replace',
                                      'data-background-image'):
                        url = node.attrs.get(attribute, '')
                        parts = urlsplit(url)
                        if not url or parts.scheme or parts.netloc or url.startswith('#'):
                            continue
                        path = unquote(parts.path)
                        if path.startswith('/lectures/'):
                            target = ROOT / path.removeprefix('/lectures/')
                        else:
                            target = DECK / path
                        self.assertTrue(target.exists(), (source.name, url))
                    if node.tag == 'img':
                        self.assertTrue(node.attrs.get('alt', '').strip(), source.name)


if __name__ == '__main__':
    unittest.main()
