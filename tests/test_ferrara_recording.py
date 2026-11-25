"""Ferrara's recording supplements the course record without inventing a date."""
from pathlib import Path
import unittest

from test_cs_lecture import normalized, parsed

ROOT = Path(__file__).resolve().parents[1]
FOLDER = '2023-02-ferrara-interoperability'
TITLE = 'Dov\'è il bottone "Esporta Tutto"?'
AUDIENCE = 'First- and second-year orthodontic residents'
VIDEO = 'https://www.youtube.com/watch?v=QygXAt2kt7Q'


class FerraraRecording(unittest.TestCase):
    def test_recording_title_audience_and_duration_are_public_event_details(self):
        page = parsed(ROOT / 'events' / FOLDER / 'index.html')
        self.assertEqual(normalized(next(page.all('title'))), TITLE)
        self.assertEqual([normalized(node) for node in page.all('h1')], [TITLE])
        self.assertIn(AUDIENCE, normalized(page))
        self.assertIn('3 ore', normalized(page))
        self.assertIn('Registrazione: 3 ore, 7 minuti e 8 secondi.', normalized(page))
        self.assertIn(VIDEO, [node.attrs['href'] for node in page.all('a')])
        self.assertIn('Guarda la registrazione', [normalized(node) for node in page.all('a')])
        self.assertEqual([node.attrs['datetime'] for node in page.all('time')], ['2023-02'])
        self.assertEqual(normalized(next(page.all('time'))), 'febbraio 2023 (mese previsto)')
        self.assertIn('Data della presentazione non registrata.', normalized(page))
        self.assertNotIn('2023-02-13', (ROOT / 'events' / FOLDER / 'index.html').read_text())
        self.assertFalse(any('ACT-12.4.1' in node.attrs.get('href', '') for node in page.all('a')))
        self.assertEqual(list(page.all('iframe')), [])
        self.assertEqual(list(page.all('script')), [])

    def test_main_catalog_uses_recording_title_but_retains_month_precision(self):
        page = parsed(ROOT / 'index.html')
        row = next(row for row in page.all('tr') if any(
            node.attrs.get('href') == f'events/{FOLDER}/' for node in row.all('a')))
        self.assertEqual(normalized(next(row.all('a'))), TITLE)
        self.assertIn(AUDIENCE, normalized(row))
        self.assertIn('3-hour course', normalized(row))
        self.assertEqual([node.attrs['datetime'] for node in row.all('time')], ['2023-02'])
        self.assertIn('Presentation date not recorded.', normalized(row))


if __name__ == '__main__':
    unittest.main()
