"""Reader-facing lecture archive acceptance using handwritten public facts.

Run from the repository root: python3 -m unittest discover -s tests -v
The fixture needs no private correspondence or separate research inventory.
"""
from collections import Counter
from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urlsplit

from test_cs_lecture import normalized, parsed

ROOT = Path(__file__).resolve().parents[1]
CASE = 'Case Western Reserve University, USA'
SOE = 'American Association of Orthodontists, Society of Educators, USA'
COURSE_TITLE = 'Orthodontic Informatics: Data, Imaging, and Standards in Orthodontic Practice'
# ID: date, event folder, title, institution, audience, material route.
# These facts are independent of the HTML under test.
ARCHIVE = {
    'case-2022-09-14': (
        '2022-09-14', '2022-09-14-case-interoperability',
        'Interoperability in orthodontic practice', CASE,
        'Case Western Reserve University orthodontics group',
        'slides/2022-orthostudents/index.html'),
    'ferrara-2023-02': (
        '2023-02', '2023-02-ferrara-interoperability',
        'Open standards and clinical-data interoperability in orthodontics',
        'Universita di Ferrara, Italy', 'Orthodontic school / orthodontics trainees',
        'slides/2023-orthostudents/index.html'),
    'case-2023-03-24': (
        '2023-03-24', '2023-03-24-case-orthodontic-informatics',
        'Orthodontic informatics lecture', CASE, 'CWRU Orthodontics',
        'slides/2023-orthostudents/index.html'),
    'harvard-2023-03-27': (
        '2023-03-27', '2023-03-27-harvard-interoperability',
        'Interoperability in orthodontic practice', 'Harvard School of Dental Medicine, USA',
        'Orthodontic school audience at Harvard School of Dental Medicine',
        'slides/2023-orthostudents/index.html'),
    'case-2023-10-11': (
        '2023-10-11', '2023-10-11-case-orthodontic-informatics',
        'Orthodontic informatics lecture', CASE, 'CWRU Orthodontics',
        'slides/2023-orthostudents/index.html'),
    'case-2024-03-15': (
        '2024-03-15', '2024-03-15-case-orthodontic-informatics',
        'Orthodontic informatics lecture', CASE, 'CWRU Orthodontics',
        'slides/2023-orthostudents/index.html'),
    'case-2024-10-11-year1': (
        '2024-10-11', '2024-10-11-case-orthodontic-informatics-year1',
        COURSE_TITLE, CASE, 'First-year orthodontic residents',
        'slides/orthodontic-informatics/module1/index.html'),
    'case-2024-10-11-year2': (
        '2024-10-11', '2024-10-11-case-orthodontic-informatics-year2',
        COURSE_TITLE, CASE, 'Second-year orthodontic residents',
        'slides/orthodontic-informatics/module3/index.html'),
    'aao-soe-2025-01-21': (
        '2025-01-21', '2025-01-21-aao-soe-informatics-education',
        'Integrating Clinical Informatics into Orthodontic Education', SOE,
        'Orthodontic educators; AAO Society of Educators webinar audience',
        'slides/orthodontic-informatics/module1/index.html'),
    'aao-soe-2025-02-18': (
        '2025-02-18', '2025-02-18-aao-soe-informatics-standards',
        'Integrating Clinical Informatics and Standards', SOE,
        'Orthodontic educators; AAO Society of Educators webinar audience', None),
    'case-2025-10-10': (
        '2025-10-10', '2025-10-10-case-orthodontic-informatics',
        'Orthodontic informatics for second-year residents', CASE,
        'Second-year orthodontic residents',
        'slides/orthodontic-informatics/module1/index.html'),
    'trieste-2025-11-12': (
        '2025-11-12', '2025-11-12-trieste-clinical-informatics',
        'Clinical informatics and interoperability in dental practice',
        'Universita degli Studi di Trieste, Italy',
        'Orthodontic residents across all three years, with additional clinicians from maxillofacial surgery and odontostomatology invited',
        'slides/orthodontic-informatics/index.html'),
    'case-2026-02-23': (
        '2026-02-23', '2026-02-23-case-orthodontic-informatics',
        'Orthodontic informatics — Class of 2028', CASE, 'Class of 2028',
        'slides/orthodontic-informatics/module2/index.html'),
    'case-2026-02-24': (
        '2026-02-24', '2026-02-24-case-orthodontic-informatics',
        'Orthodontic informatics — Class of 2027', CASE, 'Class of 2027',
        'slides/orthodontic-informatics/module4/index.html'),
    'case-2026-11-20': (
        '2026-11-20', '2026-11-20-orthodontic-informatics-module3',
        'AI and Reusable Clinical Data', CASE, 'second-year orthodontic residents',
        'slides/orthodontic-informatics/module3/'),
}
IMPORTED = {key: row for key, row in ARCHIVE.items() if key != 'case-2026-11-20'}


class PublicLectureArchive(unittest.TestCase):
    def test_all_fifteen_presentations_keep_their_routes_titles_dates_and_links(self):
        self.assertEqual(len(ARCHIVE), 15)
        self.assertEqual(len({row[1] for row in ARCHIVE.values()}), 15)
        catalog = parsed(ROOT / 'index.html')
        table = next(n for n in catalog.all('table') if n.attrs.get('id') == 'events')
        rows = list(next(table.all('tbody')).all('tr'))
        self.assertEqual(len(rows), 17)
        self.assertEqual(Counter(normalized(list(row.all('td'))[-1]) for row in rows),
                         {'Presented': 15, 'Scheduled': 2})
        for key, (date, folder, title, institution, audience, material) in ARCHIVE.items():
            with self.subTest(event=key):
                source = ROOT / 'events' / folder / 'index.html'
                page = parsed(source)
                self.assertEqual([normalized(n) for n in page.all('h1')], [title])
                self.assertEqual(normalized(next(page.all('title'))), title)
                self.assertEqual(next(page.all('time')).attrs['datetime'], date)
                self.assertIn('Presented', normalized(page))
                self.assertIn(institution.removesuffix(', USA') if key == 'case-2026-11-20'
                              else institution, normalized(page))
                self.assertIn(audience, normalized(page))
                matching = [row for row in rows if any(
                    n.attrs['href'] == f'events/{folder}/' for n in row.all('a'))]
                self.assertEqual(len(matching), 1)
                row = matching[0]
                self.assertEqual(normalized(next(row.all('a'))), title)
                self.assertEqual(next(row.all('time')).attrs['datetime'], date)
                self.assertEqual(normalized(list(row.all('td'))[-1]), 'Presented')
                self.assertIn(institution, normalized(row))
                self.assertIn(audience, normalized(row))
                links = [(n.attrs['href'], normalized(n)) for n in page.all('a')]
                if material:
                    label = ('View current slides' if key == 'case-2026-11-20' else
                             'View course' if key == 'trieste-2025-11-12' else 'View slides')
                    self.assertIn(('../../' + material, label), links)
                    self.assertTrue((ROOT / material).exists())
                else:
                    self.assertIn('Slides are not yet available.', normalized(page))
                    self.assertFalse(any('slides/' in href for href, _ in links))
                    self.assertFalse(any('event-actions' in n.attrs.get('class', '').split()
                                         for n in page.all('div')))

    def test_public_pages_are_final_lecture_pages_not_research_workflows(self):
        for source in [ROOT / 'index.html', *sorted((ROOT / 'events').glob('*/index.html'))]:
            with self.subTest(page=str(source.relative_to(ROOT))):
                text = normalized(parsed(source))
                self.assertNotRegex(text, r'(?i)confidence|accepted by (?:the )?lecturer|history review|candidate|provisional|pending identification|identification is pending')
                self.assertNotRegex(text, r'(?i)material (?:association|identity|acceptance|match)|organizer-supplied history|original title not established|original title and topic not established|historical slide version|immutable historical|Time not recorded|About this record|source attribution|privacy audit')
        self.assertIn('Dated presentations, newest first. Open an event for details and slides.',
                      normalized(parsed(ROOT / 'index.html')))
        for key, row in IMPORTED.items():
            with self.subTest(event=key):
                page = parsed(ROOT / 'events' / row[1] / 'index.html')
                self.assertIn('Date', [normalized(n) for n in page.all('dt')])
                self.assertIn('Status', [normalized(n) for n in page.all('dt')])
                self.assertIn('About the lecture', [normalized(n) for n in page.all('h2')])
                self.assertEqual([n.attrs['datetime'] for n in page.all('time')], [row[0]])
                self.assertNotRegex(normalized(page), r'(?i)unverified|not established|accepted|confirm(?:ed|ation)|rationale|not a verified|may have been used|another agent')
                self.assertEqual(list((ROOT / 'events' / row[1]).glob('*.ics')), [])
        ferrara = parsed(ROOT / 'events/2023-02-ferrara-interoperability/index.html')
        self.assertEqual(normalized(next(ferrara.all('time'))), 'February 2023 (planned month)')
        self.assertNotRegex(normalized(ferrara), r'February \d{1,2}, 2023')

    def test_archive_pages_keep_accessible_portraits_styles_and_local_destinations(self):
        for key, row in ARCHIVE.items():
            with self.subTest(event=key):
                source = ROOT / 'events' / row[1] / 'index.html'
                page = parsed(source)
                self.assertEqual(next(page.all('body')).attrs.get('class'), 'event-page')
                self.assertEqual(list(page.all('script')), [])
                portraits = list(page.all('img'))
                self.assertEqual(len(portraits), 1)
                self.assertEqual(portraits[0].attrs, {
                    'src': '../../assets/img/amagni.jpeg', 'alt': 'Toni Magni',
                    'width': '80', 'height': '80'})
                grouping = next(n for n in page.all('div')
                                if 'event-speaker-heading' in n.attrs.get('class', '').split())
                self.assertIn('Toni Magni', normalized(grouping))
                self.assertEqual(len(list(grouping.all('img'))), 1)
                self.assertEqual([n.attrs['href'] for n in page.all('link')
                                  if n.attrs.get('rel') == 'stylesheet'],
                                 ['../../assets/css/index.css', '../../assets/css/cwru-event.css'])
                for node in page.all():
                    for attr in ('href', 'src'):
                        if attr not in node.attrs:
                            continue
                        url = urlsplit(node.attrs[attr])
                        if key in IMPORTED:
                            self.assertNotIn(url.scheme, ('mailto', 'tel'))
                        if not url.scheme and not url.netloc:
                            self.assertTrue((source.parent / unquote(url.path)).exists(), node.attrs[attr])

    def test_private_correspondence_does_not_leak_into_imported_pages_or_fixture(self):
        for source in [Path(__file__), *(ROOT / 'events' / row[1] / 'index.html'
                                         for row in IMPORTED.values())]:
            with self.subTest(file=str(source.relative_to(ROOT))):
                text = source.read_text().split('class PublicLectureArchive', 1)[0] if source == Path(__file__) else source.read_text()
                self.assertNotRegex(text, r'(?i)[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}|Message-ID:|In-Reply-To:|References:\s*<|BEGIN:VCALENDAR|calendar_event_ids|email_sources|research_coverage|/home/agent/|attachment:|\b(?:From|To|Cc|Bcc):')

    def test_research_artifacts_are_not_publishable_and_guide_owns_archive_maintenance(self):
        for name in ('history' + '.json', 'history' + '-review.md'):
            self.assertFalse((ROOT / 'events' / name).exists())
        guide = (ROOT / 'events/README.md').read_text()
        self.assertIn('## Maintain past presentations', guide)
        for phrase in ('Keep event records after', 'current deck', 'country',
                       'Slides are not yet available.', 'planned month'):
            self.assertIn(phrase, guide)
        for source in (ROOT / 'README.md', ROOT / 'events/README.md'):
            self.assertNotRegex(source.read_text(), r'(?i)history\.json|history-review|candidate|confidence|material identity|review notes')
        for source in [ROOT / 'index.html', *sorted((ROOT / 'events').glob('*/index.html'))]:
            self.assertFalse(any('history' in n.attrs['href'] for n in parsed(source).all('a')))


if __name__ == '__main__':
    unittest.main()
