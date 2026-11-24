"""Maintainer documentation boundaries and local links; not prose approval.

Run from the repository root: python3 -m unittest discover -s tests -v
"""
from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urlsplit

from test_cs_lecture import normalized, parsed

ROOT = Path(__file__).resolve().parents[1]
DECK = ROOT / 'slides/2026-cs-club-biomedical-informatics'
EVENT = ROOT / 'events/2026-12-02-biomedical-informatics'
GUIDES = (ROOT / 'README.md', DECK / 'README.md', EVENT / 'README.md')


class Documentation(unittest.TestCase):
    def test_root_explains_reusable_slides_dated_events_and_catalogs(self):
        text = GUIDES[0].read_text()
        for phrase in ('three types of content', '**Presentation slides**',
                       '**Event pages**', '**Catalog pages**', 'reusable',
                       'dated presentation record', 'points to the slides',
                       '## Adding a lecture or event', 'reuse an existing deck',
                       'new deck', 'new event folder', 'title and abstract',
                       'calendar', 'presentation history',
                       'edit the event folder', 'not the deck guide'):
            self.assertIn(phrase, text)
        for target in ('slides/2026-cs-club-biomedical-informatics/README.md',
                       'events/2026-12-02-biomedical-informatics/README.md',
                       'events/2026-12-02-biomedical-informatics/index.html',
                       'events/2026-12-02-biomedical-informatics/biomedical-informatics.ics',
                       'slides/orthodontic-informatics/index.html', 'index.html'):
            self.assertRegex(text, r'\]\((?:\./)?' + re.escape(target) + r'\)')
        catalog = parsed(ROOT / 'index.html')
        hrefs = {n.attrs.get('href') for n in catalog.all('a')}
        self.assertIn('slides/2026-cs-club-biomedical-informatics/index.html', hrefs)
        self.assertIn('events/2026-12-02-biomedical-informatics/', hrefs)
        self.assertIn('Biomedical Informatics for Computer Scientists', normalized(catalog))

    def test_root_editing_instructions_match_catalog_manifest_and_preview(self):
        text = GUIDES[0].read_text()
        self.assertIn('root `index.html` is a catalog, not a slide deck', text)
        self.assertIn('data-external-replace', text)
        self.assertIn('make serve', text)
        self.assertIn('http://127.0.0.1:54385/lectures/', text)
        self.assertIn('python3 -m unittest discover -s tests -v', text)
        self.assertNotIn('Slide content are in the [index.html](./index.html)', text)
        self.assertEqual(list(parsed(ROOT / 'index.html').all('section')), [])
        self.assertTrue(any('data-external-replace' in node.attrs
                            for node in parsed(DECK / 'index.html').all('section')))
        server = (ROOT / 'serve.py').read_text()
        self.assertIn('PORT = 54385', server)
        self.assertIn('BIND = "127.0.0.1"', server)
        self.assertIn('BASE = "/lectures"', server)
        self.assertIn('python3 serve.py', (ROOT / 'Makefile').read_text())

    def test_deployment_names_main_without_a_competing_master_instruction(self):
        text = GUIDES[0].read_text()
        deployment = text.split('## Deployment\n', 1)[1].split('\n## ', 1)[0]
        self.assertIn('GitHub Pages', deployment)
        self.assertIn('`main` branch', deployment)
        self.assertNotIn('master', deployment)

    def test_guide_relative_links_resolve_from_each_document_directory(self):
        for source in GUIDES:
            for url in re.findall(r'\]\(([^)]+)\)', source.read_text()):
                with self.subTest(source=str(source.relative_to(ROOT)), url=url):
                    parts = urlsplit(url)
                    if parts.scheme or parts.netloc:
                        continue
                    target = source.parent / unquote(parts.path) if parts.path else source
                    self.assertTrue(target.exists(), str(target))
                    if parts.fragment and target.suffix == '.md':
                        headings = re.findall(r'^#{1,6}\s+(.+)$', target.read_text(), re.M)
                        anchors = {re.sub(r'[^\w\- ]', '', h.lower()).replace(' ', '-')
                                   for h in headings}
                        self.assertIn(unquote(parts.fragment), anchors)


if __name__ == '__main__':
    unittest.main()
