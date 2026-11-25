"""Public archive timings, handwritten independently of the pages under test.

No private correspondence or research inventory is needed to run these checks.
October's two shared slots are not assignments to individual resident years.
"""
from datetime import datetime, timezone
from pathlib import Path
import unittest
from zoneinfo import ZoneInfo

from test_cs_lecture import normalized, parsed

ROOT = Path(__file__).resolve().parents[1]
# Event folder: date, local zone, separately recorded scheduled intervals.
TIMINGS = {
    '2022-09-14-case-interoperability': (
        '2022-09-14', 'America/New_York', (('13:00', '14:00'),)),
    '2023-02-ferrara-interoperability': ('2023-02', 'Europe/Rome', ()),
    '2023-03-24-case-orthodontic-informatics': (
        '2023-03-24', 'America/New_York', (('10:00', '12:00'),)),
    '2023-03-27-harvard-interoperability': (
        '2023-03-27', 'America/New_York', (('10:00', '12:00'),)),
    '2023-10-11-case-orthodontic-informatics': (
        '2023-10-11', 'America/New_York', (('13:00', '14:00'),)),
    '2024-03-15-case-orthodontic-informatics': (
        '2024-03-15', 'America/New_York', (('13:00', '14:00'),)),
    '2024-10-11-case-orthodontic-informatics-year1': (
        '2024-10-11', 'America/New_York', (('13:00', '14:00'), ('14:00', '15:00'))),
    '2024-10-11-case-orthodontic-informatics-year2': (
        '2024-10-11', 'America/New_York', (('13:00', '14:00'), ('14:00', '15:00'))),
    '2025-01-21-aao-soe-informatics-education': (
        '2025-01-21', 'America/Chicago', (('19:00', '20:15'),)),
    '2025-02-18-aao-soe-informatics-standards': (
        '2025-02-18', 'America/Chicago', (('19:00', '20:15'),)),
    '2025-10-10-case-orthodontic-informatics': (
        '2025-10-10', 'America/New_York', (('13:00', '14:00'),)),
    '2025-11-12-trieste-clinical-informatics': (
        '2025-11-12', 'Europe/Rome', (('14:15',),)),
    '2026-02-23-case-orthodontic-informatics': (
        '2026-02-23', 'America/New_York', (('13:00', '14:00'),)),
    '2026-02-24-case-orthodontic-informatics': (
        '2026-02-24', 'America/New_York', (('13:00', '14:00'),)),
    # Preserve the already published, lecturer-confirmed one-hour presentation.
    '2026-11-20-orthodontic-informatics-module3': (
        '2026-11-20', 'America/New_York', (('10:00', '11:00'),)),
}


def catalog_rows():
    table = next(n for n in parsed(ROOT / 'index.html').all('table')
                 if n.attrs.get('id') == 'events')
    return {next(row.all('a')).attrs['href']: row
            for row in next(table.all('tbody')).all('tr')}


class ArchiveTiming(unittest.TestCase):
    def test_all_fifteen_records_have_exact_local_endpoints_in_both_locations(self):
        self.assertEqual(len(TIMINGS), 15)
        rows = catalog_rows()
        for folder, (date, zone, intervals) in TIMINGS.items():
            expected = [date]
            expected.extend(datetime.fromisoformat(f'{date}T{clock}').replace(
                tzinfo=ZoneInfo(zone)).isoformat(timespec='seconds')
                for interval in intervals for clock in interval)
            page = parsed(ROOT / 'events' / folder / 'index.html')
            row = rows[f'events/{folder}/']
            for location, node in (('event', page), ('catalog', next(row.all('td')))):
                with self.subTest(event=folder, location=location):
                    times = list(node.all('time'))
                    self.assertEqual([n.attrs['datetime'] for n in times], expected)
                    for time_node, timestamp in zip(times[1:], expected[1:]):
                        instant = datetime.fromisoformat(timestamp)
                        # Check the local offset and UTC instant, not only wall time.
                        actual = datetime.fromisoformat(time_node.attrs['datetime'])
                        self.assertEqual(actual.utcoffset(), instant.utcoffset())
                        self.assertEqual(actual.astimezone(timezone.utc),
                                         instant.astimezone(timezone.utc))
                        if location == 'catalog':
                            self.assertEqual(normalized(time_node),
                                             timestamp[11:16] + timestamp[-6:])
            self.assertEqual(normalized(list(row.all('td'))[-1]), 'Presented')

    def test_new_schedules_use_local_display_without_claiming_actual_duration(self):
        for folder, (date, zone, intervals) in TIMINGS.items():
            if not intervals or date in ('2026-11-20', '2025-11-12'):
                continue
            with self.subTest(event=folder):
                page = parsed(ROOT / 'events' / folder / 'index.html')
                self.assertIn('Scheduled time', [normalized(n) for n in page.all('dt')])
                displayed = [normalized(n) for n in page.all('dd')
                             if 'event-time' in n.attrs.get('class', '').split()]
                if zone == 'America/Chicago':
                    self.assertEqual(displayed, ['7:00–8:15 p.m. Central'])
                    self.assertIn('CST (UTC−06:00)', normalized(page))
                elif date in ('2023-03-24', '2023-03-27'):
                    self.assertEqual(displayed, ['10:00 a.m.–12:00 p.m. Eastern'])
                elif date == '2024-10-11':
                    self.assertEqual(displayed, ['1:00–2:00 p.m. Eastern',
                                                 '2:00–3:00 p.m. Eastern'])
                else:
                    self.assertEqual(displayed, ['1:00–2:00 p.m. Eastern'])
                if zone == 'America/New_York':
                    self.assertIn('EST (UTC−05:00)' if date.startswith('2026-02')
                                  else 'EDT (UTC−04:00)', normalized(page))

    def test_october_shared_schedule_does_not_assign_or_combine_cohort_slots(self):
        rows = catalog_rows()
        for year in (1, 2):
            folder = f'2024-10-11-case-orthodontic-informatics-year{year}'
            page = parsed(ROOT / 'events' / folder / 'index.html')
            cell = next(rows[f'events/{folder}/'].all('td'))
            for location, node in (('event', page), ('catalog', cell)):
                with self.subTest(year=year, location=location):
                    self.assertIn('Shared schedule:', normalized(node))
                    self.assertIn('One-hour session;', normalized(node))
            self.assertIn('One-hour session; resident-year time slot not recorded.',
                          normalized(page))
            self.assertIn('One-hour session; cohort slot not recorded.', normalized(cell))
            # Separate containers retain the two one-hour intervals, not 1–3 p.m.
            self.assertEqual([len(list(n.all('time'))) for n in page.all('dd')
                              if 'event-time' in n.attrs.get('class', '').split()], [2, 2])

    def test_trieste_has_an_approximate_start_only_and_localized_date(self):
        folder = '2025-11-12-trieste-clinical-informatics'
        page = parsed(ROOT / 'events' / folder / 'index.html')
        self.assertEqual(normalized(next(page.all('time'))), '12 novembre 2025')
        self.assertIn('Scheduled time', [normalized(n) for n in page.all('dt')])
        self.assertIn('Circa 14:15 CET (UTC+01:00); fine non indicata.', normalized(page))
        self.assertIn('Venue', [normalized(n) for n in page.all('dt')])
        self.assertIn('Aula 4', [normalized(n) for n in page.all('dd')])
        cell = next(catalog_rows()[f'events/{folder}/'].all('td'))
        self.assertIn('Approx. 14:15+01:00', normalized(cell))
        self.assertIn('End not recorded.', normalized(cell))
        self.assertNotIn('18:00', normalized(page))

    def test_past_timing_does_not_add_calendars_or_scripts(self):
        self.assertEqual(sorted(str(p.relative_to(ROOT)) for p in (ROOT / 'events').rglob('*.ics')),
                         ['events/2026-11-30-orthodontic-informatics-module1/orthodontic-informatics-module1.ics',
                          'events/2026-12-02-biomedical-informatics/biomedical-informatics.ics'])
        for folder in TIMINGS:
            page = parsed(ROOT / 'events' / folder / 'index.html')
            self.assertEqual(list(page.all('script')), [])
            self.assertFalse(any('calendar.google.com' in n.attrs['href'] or
                                 n.attrs['href'].endswith('.ics') for n in page.all('a')))

    def test_ferrara_retains_duration_without_an_exact_day_or_clock_time(self):
        folder = '2023-02-ferrara-interoperability'
        page = parsed(ROOT / 'events' / folder / 'index.html')
        row = catalog_rows()[f'events/{folder}/']
        self.assertIn('3 ore', normalized(page))
        self.assertIn('3-hour course', normalized(row))
        for node in (page, row):
            self.assertEqual([n.attrs['datetime'] for n in node.all('time')], ['2023-02'])
        self.assertIn('Presentation date not recorded.', normalized(row))


if __name__ == '__main__':
    unittest.main()
