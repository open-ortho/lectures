"""Regression checks for reusable course navigation and catalog date display."""
from datetime import datetime
from pathlib import Path
import unittest
from zoneinfo import ZoneInfo

from test_cs_lecture import normalized, parsed

ROOT = Path(__file__).resolve().parents[1]


class ReviewCatalog(unittest.TestCase):
    def test_guide_documents_main_catalog_iso_display(self):
        guide = (ROOT / 'events/README.md').read_text()
        for phrase in ('YYYY-MM-DD', '24-hour', '15:10-05:00',
                       'local UTC offset', 'YYYY-MM', 'individual event pages'):
            self.assertIn(phrase, guide)

    def test_course_catalog_has_modules_without_dated_presentations(self):
        page = parsed(ROOT / 'slides/orthodontic-informatics/index.html')
        self.assertNotIn('Presentations', [normalized(n) for n in page.all('h2')])
        self.assertFalse(any(n.attrs.get('aria-labelledby') == 'presentations-heading'
                             for n in page.all('section')))
        self.assertEqual([n.attrs['href'] for n in page.all('a')], [
            './module1/index.html', './module2/index.html',
            './module3/index.html', './module4/index.html',
            'https://open-ortho.org', 'https://www.antoniomagni.com',
            'https://opensource.org/licenses/MIT',
        ])
        self.assertEqual(len(list(page.all('table'))), 1)
        self.assertEqual(list(page.all('script')), [])

    def test_event_dates_display_iso_at_the_recorded_precision(self):
        table = next(n for n in parsed(ROOT / 'index.html').all('table')
                     if n.attrs.get('id') == 'events')
        rows = list(next(table.all('tbody')).all('tr'))
        self.assertEqual(len(rows), 17)
        known_times = {
            '2026-12-02': ('America/New_York', ('15:10', '16:25')),
            '2026-11-30': ('America/New_York', ('15:00', '16:00')),
            '2026-11-20': ('America/New_York', ('10:00', '11:00')),
            '2026-02-24': ('America/New_York', ('13:00', '14:00')),
            '2026-02-23': ('America/New_York', ('13:00', '14:00')),
            '2025-11-12': ('Europe/Rome', ('14:15',)),
            '2025-10-10': ('America/New_York', ('13:00', '14:00')),
            '2025-02-18': ('America/Chicago', ('19:00', '20:15')),
            '2025-01-21': ('America/Chicago', ('19:00', '20:15')),
            # Both cohorts show the shared slots; neither is assigned an order.
            '2024-10-11': ('America/New_York', ('13:00', '14:00', '14:00', '15:00')),
            '2024-03-15': ('America/New_York', ('13:00', '14:00')),
            '2023-10-11': ('America/New_York', ('13:00', '14:00')),
            '2023-03-27': ('America/New_York', ('10:00', '12:00')),
            '2023-03-24': ('America/New_York', ('10:00', '12:00')),
            '2022-09-14': ('America/New_York', ('13:00', '14:00')),
        }
        for row in rows:
            cell = next(row.all('td'))
            date_node, *time_nodes = cell.all('time')
            date = date_node.attrs['datetime']
            with self.subTest(date=date):
                self.assertRegex(date, r'^\d{4}-\d{2}(?:-\d{2})?$')
                self.assertEqual(normalized(date_node), date)
                if date in known_times:
                    expected = []
                    zone, clocks = known_times[date]
                    for time in clocks:
                        local = datetime.fromisoformat(f'{date}T{time}').replace(
                            tzinfo=ZoneInfo(zone))
                        expected.append(local.isoformat(timespec='seconds'))
                    self.assertEqual([n.attrs['datetime'] for n in time_nodes], expected)
                    self.assertEqual([normalized(n) for n in time_nodes],
                                     [value[11:16] + value[-6:] for value in expected])
                    displayed = [normalized(n) for n in time_nodes]
                    if date == '2024-10-11':
                        self.assertEqual(normalized(cell), date + ' Shared schedule: ' +
                                         '–'.join(displayed[:2]) + ' ' +
                                         '–'.join(displayed[2:]) +
                                         ' One-hour session; cohort slot not recorded.')
                    elif date == '2025-11-12':
                        self.assertEqual(normalized(cell),
                                         date + ' Approx. ' + displayed[0] + ' End not recorded.')
                    else:
                        self.assertEqual(normalized(cell), date + ' ' + '–'.join(displayed))
                elif len(date) == 7:
                    self.assertEqual(date, '2023-02')
                    self.assertEqual(time_nodes, [])
                    self.assertEqual(normalized(cell),
                                     '2023-02 (planned month) Presentation date not recorded.')
                else:
                    self.fail(f'Event date missing from timing expectations: {date}')


if __name__ == '__main__':
    unittest.main()
