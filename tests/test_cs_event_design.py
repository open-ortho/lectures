"""Faculty affiliation and local CWRU-inspired announcement styling.

These source checks do not replace fresh-reader or rendered-browser review.
Run from the repository root: python3 -m unittest discover -s tests -v
"""
from pathlib import Path
import unittest

from test_cs_lecture import normalized, parsed

ROOT = Path(__file__).resolve().parents[1]
EVENT = ROOT / 'events/2026-12-02-biomedical-informatics'


class CSEventDesign(unittest.TestCase):
    def test_event_layout_is_shared_not_copied(self):
        self.assertTrue((ROOT / 'assets/css/cwru-event.css').is_file(),
                        'Store the opt-in CWRU event theme with shared CSS assets')
        self.assertFalse((EVENT / 'event.css').exists(),
                         'Do not leave a duplicate per-event stylesheet')

    def test_speaker_has_explicit_faculty_role_and_complete_affiliation(self):
        page = parsed(EVENT / 'index.html')
        speaker = next((n for n in page.all('section')
                        if n.attrs.get('aria-labelledby') == 'speaker-heading'), None)
        self.assertIsNotNone(speaker, 'Give the speaker a labelled affiliation section')
        text = normalized(speaker)
        for phrase in ('Toni Magni', 'Clinical Instructor',
                       'Department of Orthodontics', 'School of Dental Medicine',
                       'Case Western Reserve University'):
            self.assertIn(phrase, text)
        self.assertIn(('afm@case.edu', 'mailto:afm@case.edu'),
                      [(normalized(n), n.attrs.get('href')) for n in page.all('a')])
        visible = normalized(next(page.all('body'))).lower()
        self.assertNotRegex(visible, r'distinguished|hosted by|sponsored by|endorsed by')
        portraits = list(speaker.all('img'))
        self.assertEqual(len(portraits), 1)
        self.assertEqual(portraits[0].attrs['src'], '../../assets/img/amagni.jpeg')
        self.assertEqual(portraits[0].attrs['alt'], 'Toni Magni')
        self.assertEqual(list(page.all('img')), portraits)

    def test_announcement_uses_local_current_brand_palette_and_system_font(self):
        css = (ROOT / 'assets/css/cwru-event.css').read_text()
        self.assertIn('#003071', css.lower(), 'Use the current CWRU blue')
        self.assertIn('#d3d3d3', css.lower())
        self.assertIn('#ffffff', css.lower())
        self.assertRegex(css, r'font-family:\s*Arial,\s*Helvetica,\s*sans-serif')
        self.assertRegex(css, r'background(?:-color)?:\s*(?:#ffffff|var\(--event-paper\))')
        self.assertIn('color-scheme: light', css)
        self.assertNotRegex(css, r'@import|url\(|gradient\(|box-shadow:|Georgia')
        self.assertTrue(css.startswith('/*'), 'Explain the event-only styling capability')
        page = parsed(EVENT / 'index.html')
        headings = [normalized(n) for n in page.all('h2')]
        self.assertIn('Abstract', headings)
        masthead = next((n for n in page.all('header')
                         if 'event-masthead' in n.attrs.get('class', '').split()), None)
        self.assertIsNotNone(masthead, 'Give the lecture a broad academic masthead')
        self.assertEqual(len(list(masthead.all('h1'))), 1)

    def test_page_keeps_its_static_local_asset_contract(self):
        page = parsed(EVENT / 'index.html')
        self.assertEqual(list(page.all('script')), [])
        self.assertEqual(list(page.all('iframe')), [])
        styles = [n.attrs['href'] for n in page.all('link')
                  if n.attrs.get('rel') == 'stylesheet']
        self.assertEqual(styles, ['../../assets/css/index.css', '../../assets/css/cwru-event.css'])
        self.assertNotRegex((ROOT / 'assets/css/cwru-event.css').read_text(), r'@font-face|https?://')
        for n in page.all():
            self.assertFalse(any(attr.startswith('on') for attr in n.attrs))


if __name__ == '__main__':
    unittest.main()
