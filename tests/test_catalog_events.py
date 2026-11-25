"""Catalog navigation and content boundaries; rendered readability is separate.

Run from the repository root: python3 -m unittest discover -s tests -v
"""
from pathlib import Path
from test_lecture_history import ARCHIVE
import unittest

from test_cs_lecture import TITLE, normalized, parsed

ROOT = Path(__file__).resolve().parents[1]
EVENTS = [
    ('2026-12-02', 'events/2026-12-02-biomedical-informatics/', TITLE, 'Scheduled'),
    ('2026-11-30', 'events/2026-11-30-orthodontic-informatics-module1/',
     'Data Sharing, Integration, and Transition in Orthodontic Informatics', 'Scheduled'),
    ('2026-11-20', 'events/2026-11-20-orthodontic-informatics-module3/',
     'AI and Reusable Clinical Data', 'Presented'),
]


class CatalogEvents(unittest.TestCase):
    def test_catalog_lists_dated_events_separately_from_courses_and_decks(self):
        page = parsed(ROOT / 'index.html')
        self.assertEqual(normalized(next(page.all('title'))), 'Open-Ortho Lectures')
        self.assertEqual([normalized(n) for n in page.all('h1')], ['Open-Ortho Lectures'])
        self.assertEqual([normalized(n) for n in page.all('h2')], [
            'Events', 'Courses', 'Talks for Clinicians', 'Talks for Developers & Students'])
        table = next((n for n in page.all('table') if n.attrs.get('id') == 'events'), None)
        self.assertIsNotNone(table, 'Give dated presentations their own Events table')
        rows = list(next(table.all('tbody')).all('tr'))
        self.assertEqual(len(rows), 17)
        for row, (date, url, title, status) in zip(rows[:3], EVENTS, strict=True):
            with self.subTest(date=date):
                self.assertEqual([n.attrs['datetime'] for n in row.all('time')],
                                 [date, *{
                                     '2026-12-02': ['2026-12-02T15:10:00-05:00', '2026-12-02T16:25:00-05:00'],
                                     '2026-11-30': ['2026-11-30T15:00:00-05:00', '2026-11-30T16:00:00-05:00'],
                                     '2026-11-20': ['2026-11-20T10:00:00-05:00', '2026-11-20T11:00:00-05:00'],
                                 }[date]])
                self.assertIn((url, title), [(n.attrs['href'], normalized(n)) for n in row.all('a')])
                self.assertEqual(normalized(list(row.all('td'))[-1]), status)
        courses = next((n for n in page.all('table') if n.attrs.get('id') == 'courses'), None)
        self.assertIsNotNone(courses)
        self.assertEqual([n.attrs['href'] for n in courses.all('a')],
                         ['slides/orthodontic-informatics/'])
        for other in page.all('table'):
            if other is not table:
                self.assertFalse(any(n.attrs['href'].startswith('events/') for n in other.all('a')))
        self.assertEqual(list(page.all('script')), [])

    def test_catalog_has_scoped_mobile_wrapping_without_hiding_content(self):
        page = parsed(ROOT / 'index.html')
        self.assertIn('lecture-catalog', next(page.all('body')).attrs.get('class', '').split())
        css = (ROOT / 'assets/css/index.css').read_text()
        self.assertIn('@media (max-width: 600px)', css)
        self.assertIn('.lecture-catalog table', css)
        self.assertIn('table-layout: fixed', css)
        self.assertIn('overflow-wrap: anywhere', css)
        self.assertIn('content: attr(data-label)', css)
        for table in page.all('table'):
            headers = [normalized(n) for n in table.all('th')]
            for row in next(table.all('tbody')).all('tr'):
                self.assertEqual([n.attrs.get('data-label') for n in row.all('td')], headers)
        self.assertNotRegex(css, r'overflow-x:\s*hidden|display:\s*none')

    def test_event_rows_keep_known_logistics_without_inventing_historical_time(self):
        page = parsed(ROOT / 'index.html')
        table = next((n for n in page.all('table') if n.attrs.get('id') == 'events'), None)
        self.assertIsNotNone(table, 'Missing Events table')
        rows = list(next(table.all('tbody')).all('tr'))
        cs, first_year, second_year = [normalized(row) for row in rows[:3]]
        for phrase in ('2026-12-02', '15:10-05:00–16:25-05:00', 'White 411',
                       'computer science students'):
            self.assertIn(phrase, cs)
        for phrase in ('2026-11-30', '15:00-05:00–16:00-05:00',
                       'first-year orthodontic residents', 'Orthodontics seminar room',
                       'School of Dental Medicine', 'Case Western Reserve University'):
            self.assertIn(phrase, first_year)
        for phrase in ('2026-11-20', '10:00-05:00–11:00-05:00',
                       'second-year orthodontic residents', 'Back seminar room',
                       'School of Dental Medicine', 'Case Western Reserve University'):
            self.assertIn(phrase, second_year)
        self.assertNotIn('Time not recorded', second_year)
        self.assertNotRegex(first_year + second_year, r'\b\d{3,5}\s+\w+\s+(Street|Road|Avenue)\b')

    def test_catalog_adds_all_history_without_duplicates_or_precision_loss(self):
        table = next(n for n in parsed(ROOT / 'index.html').all('table')
                     if n.attrs.get('id') == 'events')
        rows = list(next(table.all('tbody')).all('tr'))
        self.assertEqual(len(rows), 17)
        urls = [next(row.all('a')).attrs['href'] for row in rows]
        self.assertEqual(len(set(urls)), 17)
        dates = [next(row.all('time')).attrs['datetime'] for row in rows]
        self.assertEqual(dates, sorted(dates, reverse=True))
        expected = sorted(((key, row) for key, row in ARCHIVE.items()
                           if key != 'case-2026-11-20'),
                          key=lambda item: (item[1][0], item[0]), reverse=True)
        self.assertEqual(len(expected), 14)
        for row, (key, (date, folder, title, institution, audience, _)) in zip(rows[3:], expected, strict=True):
            with self.subTest(event=key):
                self.assertEqual(next(row.all('time')).attrs['datetime'], date)
                self.assertEqual(next(row.all('a')).attrs['href'], f'events/{folder}/')
                self.assertEqual(normalized(next(row.all('a'))), title)
                self.assertEqual(normalized(list(row.all('td'))[-1]), 'Presented')
                for value in (audience, institution):
                    self.assertIn(value, normalized(row))
                self.assertNotIn('Time not recorded', normalized(row))
        cohort_urls = [url for url in urls if '2024-10-11' in url]
        self.assertEqual(len(cohort_urls), 2)
        self.assertTrue(any('-year1/' in url for url in cohort_urls))
        self.assertTrue(any('-year2/' in url for url in cohort_urls))
        ferrara = next(row for row in rows if 'ferrara' in next(row.all('a')).attrs['href'])
        self.assertIn('2023-02 (planned month)', normalized(ferrara))

    def test_all_historical_rows_are_presented_and_all_event_institutions_name_countries(self):
        table = next(n for n in parsed(ROOT / 'index.html').all('table')
                     if n.attrs.get('id') == 'events')
        rows = list(next(table.all('tbody')).all('tr'))
        self.assertEqual(len(rows), 17)
        for index, row in enumerate(rows):
            with self.subTest(index=index):
                self.assertEqual(normalized(list(row.all('td'))[-1]),
                                 'Scheduled' if index < 2 else 'Presented')
                url = next(row.all('a')).attrs['href']
                institution = ('Universita di Ferrara, Italy' if 'ferrara' in url else
                               'Universita degli Studi di Trieste, Italy' if 'trieste' in url else
                               'Harvard School of Dental Medicine, USA' if 'harvard' in url else
                               'American Association of Orthodontists, Society of Educators, USA' if 'aao-soe' in url else
                               'Case Western Reserve University, USA')
                self.assertIn(institution, normalized(row))

    def test_reusable_catalog_entries_preserve_existing_destinations_and_descriptions(self):
        page = parsed(ROOT / 'index.html')
        expected = {
            'slides/orthodontic-informatics/': 'Comprehensive course covering the fundamentals of orthodontic informatics and digital workflows',
            'slides/2024-aao-vendors-meeting/index.html': 'Presentation delivered at the American Association of Orthodontists vendors meeting in 2024',
            'slides/2023-orthostudents/index.html': 'Educational lecture focused on software interoperability for orthodontic residents',
            'slides/2022-aao-bot/index.html': 'Strategic presentation delivered to the AAO Board of Trustees on orthodontic software standards',
            'slides/2022-orthostudents/index.html': 'Specialized lecture for Case Western Reserve University orthodontic residents on digital orthodontics',
            'slides/2026-cs-club-biomedical-informatics/index.html': 'A one-hour introduction to healthcare data, systems, standards, and opportunities for computer science students',
        }
        for url, description in expected.items():
            rows = [row for row in page.all('tr') if any(n.attrs['href'] == url for n in row.all('a'))]
            self.assertEqual(len(rows), 1, url)
            self.assertEqual(normalized(list(rows[0].all('td'))[-1]), description)
            self.assertEqual([n.attrs['href'] for n in rows[0].all('a')], [url])
        hrefs = {n.attrs['href'] for n in page.all('a')}
        for url in ('https://open-ortho.org', 'https://www.antoniomagni.com',
                    'https://opensource.org/licenses/MIT'):
            self.assertIn(url, hrefs)


if __name__ == '__main__':
    unittest.main()
