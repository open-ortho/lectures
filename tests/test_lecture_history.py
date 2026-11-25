"""Public history contracts using a handwritten, sanitized fixture only.

Run from the repository root: python3 -m unittest discover -s tests -v
No private attachment or local research file is needed to run these checks.
"""
from collections import Counter
import json
from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urlsplit

from test_cs_lecture import normalized, parsed

ROOT = Path(__file__).resolve().parents[1]
# Stable event identifiers are not email or calendar identifiers.
EXPECTED_DATES = {
    'case-2022-09-14': '2022-09-14',
    'ferrara-2023-02': '2023-02',
    'case-2023-03-24': '2023-03-24',
    'harvard-2023-03-27': '2023-03-27',
    'case-2023-10-11': '2023-10-11',
    'case-2024-03-15': '2024-03-15',
    'case-2024-10-11-year1': '2024-10-11',
    'case-2024-10-11-year2': '2024-10-11',
    'aao-soe-2025-01-21': '2025-01-21',
    'aao-soe-2025-02-18': '2025-02-18',
    'case-2025-10-10': '2025-10-10',
    'trieste-2025-11-12': '2025-11-12',
    'case-2026-02-23': '2026-02-23',
    'case-2026-02-24': '2026-02-24',
    'case-2026-11-20': '2026-11-20',
}


def history():
    return json.loads((ROOT / 'events/history.json').read_text())


class LectureHistory(unittest.TestCase):
    def test_inventory_keeps_all_fifteen_distinct_supplied_records(self):
        path = ROOT / 'events/history.json'
        self.assertTrue(path.is_file(), 'Publish a sanitized history inventory')
        data = history()
        self.assertEqual(data['source'], 'Organizer-supplied history')
        records = data['records']
        self.assertEqual(len(records), 15)
        self.assertEqual({r['source_id']: r['date'] for r in records}, EXPECTED_DATES)
        self.assertEqual(len({r['event_path'] for r in records}), 15)
        self.assertEqual(Counter(r['material_status'] for r in records),
                         {'provisional': 13, 'course-family': 1, 'confirmed': 1})
        self.assertEqual(Counter(r['delivery_status'] for r in records),
                         {'Presented': 6, 'Scheduled; delivery unconfirmed': 9})
        self.assertEqual([r['date'] for r in records], sorted(EXPECTED_DATES.values()))

    def test_new_pages_expose_historical_uncertainty_and_resolve_local_assets(self):
        for record in history()['records']:
            if record['source_id'] == 'case-2026-11-20':
                continue
            with self.subTest(source_id=record['source_id']):
                source = ROOT / record['event_path']
                self.assertTrue(source.is_file(), 'Each additional record needs an event page')
                page = parsed(source)
                self.assertEqual(normalized(next(page.all('h1'))), record['display_title'])
                self.assertEqual(normalized(next(page.all('title'))), record['display_title'])
                self.assertEqual(next(page.all('body')).attrs.get('class'), 'event-page')
                text = normalized(page)
                for value in (record['institution'], record['audience'], record['delivery_status'],
                              'Time not recorded in this archive', 'About this record'):
                    self.assertIn(value, text)
                self.assertEqual([n.attrs['datetime'] for n in page.all('time')], [record['date']])
                self.assertEqual(list(page.all('script')), [])
                portrait = list(page.all('img'))
                self.assertEqual(len(portrait), 1)
                self.assertEqual(portrait[0].attrs['src'], '../../assets/img/amagni.jpeg')
                self.assertEqual(portrait[0].attrs['alt'], 'Toni Magni')
                self.assertEqual((portrait[0].attrs['width'], portrait[0].attrs['height']), ('80', '80'))
                styles = [n.attrs['href'] for n in page.all('link') if n.attrs.get('rel') == 'stylesheet']
                self.assertEqual(styles, ['../../assets/css/index.css', '../event.css'])
                for node in page.all():
                    for key in ('href', 'src'):
                        if key not in node.attrs:
                            continue
                        url = urlsplit(node.attrs[key])
                        self.assertNotIn(url.scheme, ('mailto', 'tel'))
                        if not url.scheme and not url.netloc:
                            self.assertTrue((source.parent / unquote(url.path)).exists(), node.attrs[key])
                links = [(n.attrs['href'], normalized(n)) for n in page.all('a')]
                if record['material_status'] == 'provisional':
                    self.assertIn(('../../' + record['material_path'], 'View candidate slides'), links)
                    self.assertIn('Provisional material match — awaiting review. These current slides are a possible match, not a verified historical version.', text)
                else:
                    self.assertIn(('../../' + record['material_path'], 'View referenced course'), links)
                    self.assertIn('Specific modules are not established', text)
                if record['title_status'] == 'descriptive':
                    self.assertIn('Descriptive title; original title not established.', text)
                self.assertNotRegex(text, r'Clinical Instructor|Faculty lecture|Sole presenter|Hosted by|Co-presenter')
                self.assertEqual(list(source.parent.glob('*.ics')), [])
        ferrara = next(r for r in history()['records'] if r['source_id'] == 'ferrara-2023-02')
        self.assertEqual(ferrara['event_path'], 'events/2023-02-ferrara-interoperability/index.html')
        self.assertIn('February 2023 (planned month; actual date unconfirmed)',
                      normalized(parsed(ROOT / ferrara['event_path'])))

    def test_public_inventory_uses_only_sanitized_fields_and_stable_statuses(self):
        allowed = {'source_id', 'date', 'date_precision', 'date_note', 'institution',
                   'audience', 'display_title', 'title_status', 'delivery_status',
                   'material_path', 'material_status', 'confidence', 'rationale', 'event_path'}
        confirmed = {'ferrara-2023-02', 'harvard-2023-03-27',
                     'case-2024-10-11-year1', 'case-2024-10-11-year2',
                     'trieste-2025-11-12', 'case-2026-11-20'}
        paths = {
            'case-2022-09-14': 'slides/2022-orthostudents/index.html',
            'ferrara-2023-02': 'slides/2023-orthostudents/index.html',
            'case-2023-03-24': 'slides/2023-orthostudents/index.html',
            'harvard-2023-03-27': 'slides/2023-orthostudents/index.html',
            'case-2023-10-11': 'slides/2023-orthostudents/index.html',
            'case-2024-03-15': 'slides/2023-orthostudents/index.html',
            'case-2024-10-11-year1': 'slides/orthodontic-informatics/module1/index.html',
            'case-2024-10-11-year2': 'slides/orthodontic-informatics/module3/index.html',
            'aao-soe-2025-01-21': 'slides/orthodontic-informatics/module1/index.html',
            'aao-soe-2025-02-18': 'slides/2023-orthostudents/index.html',
            'case-2025-10-10': 'slides/orthodontic-informatics/module1/index.html',
            'trieste-2025-11-12': 'slides/orthodontic-informatics/index.html',
            'case-2026-02-23': 'slides/orthodontic-informatics/module2/index.html',
            'case-2026-02-24': 'slides/orthodontic-informatics/module4/index.html',
            'case-2026-11-20': 'slides/orthodontic-informatics/module3/index.html',
        }
        for row in history()['records']:
            with self.subTest(source_id=row['source_id']):
                self.assertEqual(set(row), allowed)
                expected_delivery = ('Presented' if row['source_id'] in confirmed
                                     else 'Scheduled; delivery unconfirmed')
                self.assertEqual(row['delivery_status'], expected_delivery)
                self.assertEqual(row['material_path'], paths[row['source_id']])
                self.assertTrue((ROOT / row['material_path']).is_file())
                self.assertIn(row['confidence'], {'low', 'medium', 'high'})
                self.assertEqual(row['date_precision'], 'month' if row['source_id'] == 'ferrara-2023-02' else 'day')
                self.assertRegex(row['date'], r'^\d{4}-\d{2}$' if row['date_precision'] == 'month' else r'^\d{4}-\d{2}-\d{2}$')
                self.assertEqual(list((ROOT / row['event_path']).parent.glob('*.ics')), [])
        data = history()
        self.assertEqual(set(data), {'schema_version', 'source', 'description', 'records'})
        added = [ROOT / r['event_path'] for r in data['records'] if r['source_id'] != 'case-2026-11-20']
        public_files = [ROOT / 'events/history.json', ROOT / 'events/history-review.md', *added]
        for source in public_files:
            text = source.read_text()
            with self.subTest(source=str(source.relative_to(ROOT))):
                self.assertNotRegex(text, r'(?i)[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}|mailto:|Message-ID:|In-Reply-To:|References:\s*<|BEGIN:VCALENDAR|calendar_event_ids|email_sources|research_coverage|/home/agent/|attachment:|\b(?:From|To|Cc|Bcc):')
        current = next(r for r in data['records'] if r['source_id'] == 'case-2026-11-20')
        self.assertEqual(current['display_title'], 'AI and Reusable Clinical Data')
        self.assertEqual(current['material_status'], 'confirmed')
        self.assertEqual(current['event_path'], 'events/2026-11-20-orthodontic-informatics-module3/index.html')
        trieste = next(r for r in data['records'] if r['source_id'] == 'trieste-2025-11-12')
        self.assertEqual(trieste['material_status'], 'course-family')

    def test_review_guide_explains_matches_and_links_each_record(self):
        source = ROOT / 'events/history-review.md'
        self.assertTrue(source.is_file(), 'Give maintainers a public history review guide')
        text = source.read_text()
        for phrase in ('13 provisional', 'Two known course associations', 'not exhaustive',
                       'Organizer-supplied history', 'date_precision', 'title_status',
                       'delivery_status', 'material_status', 'confidence', 'rationale',
                       'source_id', 'event_path', 'material_path', 'date_note',
                       'display_title', 'institution', 'audience', 'history.json',
                       'manually', 'No calendar', 'actual date unconfirmed'):
            self.assertIn(phrase, text)
        for row in history()['records']:
            self.assertIn(row['source_id'], text)
            self.assertIn(row['event_path'].removeprefix('events/'), text)
        for url in re.findall(r'\]\(([^)]+)\)', text):
            parts = urlsplit(url)
            if not parts.scheme and not parts.netloc:
                self.assertTrue((source.parent / unquote(parts.path)).exists(), url)
        events_guide = (ROOT / 'events/README.md').read_text()
        self.assertIn('history-review.md', events_guide)
        self.assertIn('history.json', events_guide)


if __name__ == '__main__':
    unittest.main()
