"""Static event contract; browser layout and reservation are separate checks.

Run from the repository root: python3 -m unittest discover -s tests -v
"""
from datetime import datetime, timedelta, timezone
from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urlsplit

from test_cs_lecture import DESCRIPTION, TITLE, normalized, parsed

ROOT = Path(__file__).resolve().parents[1]
EVENT = ROOT / 'events/2026-12-02-biomedical-informatics'
ROOM_URL = ('https://case.edu/utech/departments/client-experience/mediavision/'
            'technology-enhanced-classroom-tec/list-classrooms/white-411')
GRID_URL = ('https://case.edu/registrar/sites/default/files/2026-02/'
            'CWRU%20Teaching%20Grid_fall2026_final_fillable_1.pdf')


class CSEvent(unittest.TestCase):
    def test_event_provides_exact_abstract_and_actionable_static_details(self):
        source = EVENT / 'index.html'
        self.assertTrue(source.is_file(), 'Missing static event landing page')
        page = parsed(source)
        self.assertEqual(normalized(next(page.all('title'))), TITLE)
        self.assertEqual([normalized(n) for n in page.all('h1')], [TITLE])
        self.assertEqual(next(page.all('html')).attrs['lang'], 'en')
        self.assertEqual(len(list(page.all('main'))), 1)
        self.assertTrue(any(n.attrs.get('name') == 'viewport' for n in page.all('meta')))
        abstract = next(n for n in page.all('section') if n.attrs.get('id') == 'abstract')
        self.assertEqual(' '.join(normalized(n) for n in abstract.all('p')), DESCRIPTION)
        self.assertEqual([n.attrs['content'] for n in page.all('meta')
                          if n.attrs.get('name') == 'description'], [DESCRIPTION])
        visible = normalized(next(page.all('body')))
        for phrase in ('Know what exists before you build.', 'Wednesday',
                       'December 2, 2026', '3:10', '4:25', 'p.m.', 'Eastern',
                       'EST', 'UTC−05:00', '75-minute', 'White 411',
                       'Case Western Reserve University', 'Toni Magni'):
            self.assertIn(phrase, visible)
        self.assertEqual({n.attrs['datetime'] for n in page.all('time')}, {
            '2026-12-02', '2026-12-02T15:10:00-05:00', '2026-12-02T16:25:00-05:00'})
        links = {normalized(n): n.attrs['href'] for n in page.all('a')}
        self.assertEqual(links['View slides'], '../../slides/2026-cs-club-biomedical-informatics/')
        self.assertIn('../../', links.values())
        self.assertIn(ROOM_URL, links.values())
        self.assertNotRegex(visible.lower(), r'confirmed|register now|free food|zoom')
        self.assertEqual(list(page.all('script')), [])
        self.assertEqual(list(page.all('iframe')), [])
        styles = [n.attrs['href'] for n in page.all('link')
                  if n.attrs.get('rel') == 'stylesheet']
        self.assertEqual(styles, ['../../assets/css/index.css', '../../assets/css/cwru-event.css'])
        self.assertIn('event-page', next(page.all('body')).attrs['class'].split())
        for node in page.all():
            self.assertFalse(any(key.startswith('on') for key in node.attrs))
            for attr in ('href', 'src'):
                url = node.attrs.get(attr, '')
                parts = urlsplit(url)
                if not url or parts.scheme or parts.netloc or url.startswith('#'):
                    continue
                self.assertTrue((EVENT / unquote(parts.path)).exists(), url)
        css = (ROOT / 'assets/css/cwru-event.css').read_text()
        self.assertNotRegex(css, r'@import|url\(|gradient\(')
        self.assertIn('@media', css)
        self.assertIn(':focus-visible', css)
        self.assertNotRegex(css, r'overflow-x:\s*hidden')
        # Every ordinary CSS rule is scoped to opted-in events, never the catalog.
        rules = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
        for selector in re.findall(r'([^{}]+)\{', rules):
            if selector.strip().startswith('@'):
                continue
            for part in selector.split(','):
                self.assertIn('.event-page', part)


    def test_event_is_discoverable_and_maintainer_guides_explain_sources(self):
        catalog = parsed(ROOT / 'index.html')
        rows = [row for row in catalog.all('tr') if any(
            n.attrs.get('href') == 'slides/2026-cs-club-biomedical-informatics/index.html'
            for n in row.all('a'))]
        self.assertEqual(len(rows), 1)
        self.assertEqual([n.attrs.get('href') for n in rows[0].all('a')],
                         ['slides/2026-cs-club-biomedical-informatics/index.html'])
        events = next((n for n in catalog.all('table') if n.attrs.get('id') == 'events'), None)
        self.assertIsNotNone(events, 'Keep dated event discovery in the Events table')
        self.assertIn(('Biomedical Informatics for Computer Scientists',
                       'events/2026-12-02-biomedical-informatics/'),
                      [(normalized(n), n.attrs.get('href')) for n in events.all('a')])
        deck_readme = (ROOT / 'slides/2026-cs-club-biomedical-informatics/README.md').read_text()
        self.assertNotIn('60-minute session', deck_readme)
        event_readme = EVENT / 'README.md'
        self.assertTrue(event_readme.is_file(), 'Missing event maintenance guide')
        self.assertIn('## Presentation history', deck_readme)
        self.assertIn('../../events/2026-12-02-biomedical-informatics/', deck_readme)
        for phrase in ('## Event', 'December 2, 2026', '3:10', '4:25',
                       'EST', 'UTC', '75-minute', 'White 411', 'reservation',
                       'scheduled slot', GRID_URL, ROOM_URL):
            self.assertNotIn(phrase, deck_readme)
        self.assertIn('60-minute lecture is a delivery goal', deck_readme)
        event_text = event_readme.read_text()
        for phrase in ('## Event', 'December 2, 2026', '3:10–4:25 p.m.',
                       'EST', 'UTC−05:00', '75-minute', 'White 411',
                       'user-provided', 'not independently verified', GRID_URL):
            self.assertIn(phrase, event_text)
        self.assertIn('## Announcement copy', event_text)
        self.assertIn('authoritative', event_text)
        self.assertIn(f'```text\n{TITLE}\n```', event_text)
        self.assertIn(f'```text\n{DESCRIPTION}\n```', event_text)
        for phrase in ('Schedule or room changes', 'do not change the deck',
                       'Title or abstract changes', 'deck abstract', 'deck metadata',
                       'site catalog', 'biomedical-informatics.ics'):
            self.assertIn(phrase, event_text)
        self.assertNotIn('deck booking copy', event_text)
        for phrase in ('http://127.0.0.1:54385/lectures/events/2026-12-02-biomedical-informatics/',
                       'make serve', 'python3 -m unittest discover -s tests -v',
                       '../../assets/css/index.css', '../../assets/css/cwru-event.css', 'palette',
                       'typography', 'layout', 'one-hour lecture', 'not a timed rehearsal'):
            self.assertIn(phrase, event_text)
        for directory, text in ((EVENT, event_text),
                                (ROOT / 'slides/2026-cs-club-biomedical-informatics', deck_readme)):
            for url in re.findall(r'\]\(([^)]+)\)', text):
                parts = urlsplit(url)
                if not parts.scheme and not parts.netloc:
                    self.assertTrue((directory / unquote(parts.path)).exists(), url)

    def test_calendar_download_is_folded_escaped_utc_and_matches_event(self):
        page = parsed(EVENT / 'index.html')
        links = [n for n in page.all('a') if normalized(n) == 'Add to calendar']
        self.assertEqual(len(links), 1)
        self.assertIn('download', links[0].attrs)
        calendar = EVENT / links[0].attrs['href']
        self.assertTrue(calendar.is_file(), 'Missing downloadable calendar file')
        data = calendar.read_bytes()
        self.assertTrue(data.endswith(b'\r\n'))
        self.assertNotIn(b'\n', data.replace(b'\r\n', b''))
        physical = data.split(b'\r\n')[:-1]
        self.assertTrue(all(len(line) <= 75 for line in physical))
        self.assertTrue(any(line.startswith(b' ') for line in physical))
        text = re.sub(r'\r\n[ \t]', '', data.decode('utf-8'))
        lines = text.split('\r\n')
        self.assertEqual(lines.count('BEGIN:VEVENT'), 1)
        self.assertEqual(lines[0], 'BEGIN:VCALENDAR')
        self.assertEqual(lines[-2], 'END:VCALENDAR')
        values = dict(line.split(':', 1) for line in lines if ':' in line)
        self.assertEqual(values['VERSION'], '2.0')
        self.assertIn('PRODID', values)
        self.assertEqual(values['UID'], '20261202-biomedical-informatics@open-ortho.org')
        self.assertEqual(values['SUMMARY'], TITLE)
        self.assertEqual(values['DTSTART'], '20261202T201000Z')
        self.assertEqual(values['DTEND'], '20261202T212500Z')
        start = datetime.strptime(values['DTSTART'], '%Y%m%dT%H%M%SZ')
        end = datetime.strptime(values['DTEND'], '%Y%m%dT%H%M%SZ')
        self.assertEqual(end - start, timedelta(minutes=75))
        self.assertEqual(start.strftime('%A'), 'Wednesday')
        stamp = datetime.strptime(values['DTSTAMP'], '%Y%m%dT%H%M%SZ').replace(tzinfo=timezone.utc)
        self.assertLessEqual(stamp, datetime.now(timezone.utc))
        self.assertGreaterEqual(stamp, datetime(2026, 11, 24, tzinfo=timezone.utc))
        self.assertEqual(values['LOCATION'], 'White 411\\, Case Western Reserve University')
        self.assertEqual(values['URL'],
                         'https://open-ortho.org/lectures/events/2026-12-02-biomedical-informatics/')
        # RFC 5545 TEXT commas/semicolons/newlines must be escaped, not removed.
        desc = values['DESCRIPTION']
        self.assertNotRegex(desc, r'(?<!\\)[,;]')
        self.assertEqual(desc.replace('\\n', '\n').replace('\\,', ',')
                         .replace('\\;', ';').replace('\\\\', '\\'), DESCRIPTION)
        self.assertNotIn('STATUS', values)  # No independently verified reservation.
        self.assertNotIn('ORGANIZER', values)
        self.assertNotIn('ATTENDEE', values)


if __name__ == '__main__':
    unittest.main()
