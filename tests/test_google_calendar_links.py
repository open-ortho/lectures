"""Google Calendar drafts match each downloadable event without saving it."""
from datetime import datetime, timezone
from pathlib import Path
import re
import unittest
from urllib.parse import parse_qs, urlsplit

from test_cs_lecture import normalized, parsed

ROOT = Path(__file__).resolve().parents[1]


def calendar_text(value):
    return re.sub(r'\\([\\,;nN])',
                  lambda match: '\n' if match[1].lower() == 'n' else match[1], value)


class GoogleCalendarLinks(unittest.TestCase):
    def test_template_and_guides_offer_both_calendar_choices(self):
        template = (ROOT / 'templates/events/cwru-event.html').read_text()
        self.assertIn('href="{{GOOGLE_CALENDAR_URL}}">Add to Google Calendar', template)
        guide = (ROOT / 'events/README.md').read_text()
        for phrase in ('### Google Calendar links', 'action', 'TEMPLATE', 'dates',
                       'details', 'location', 'visitor must save', '&amp;'):
            self.assertIn(phrase, guide)
        for directory in ('2026-11-30-orthodontic-informatics-module1',
                          '2026-12-02-biomedical-informatics'):
            guide = (ROOT / 'events' / directory / 'README.md').read_text()
            self.assertIn('../README.md#google-calendar-links', guide)
            self.assertIn('Google Calendar', guide)

    def test_google_draft_matches_every_downloadable_calendar(self):
        calendars = sorted((ROOT / 'events').glob('*/*.ics'))
        self.assertEqual(len(calendars), 2)
        for calendar in calendars:
            with self.subTest(event=calendar.parent.name):
                content = re.sub(r'\r\n[ \t]', '', calendar.read_bytes().decode())
                fields = dict(line.split(':', 1) for line in content.split('\r\n')
                              if ':' in line)
                page = parsed(calendar.parent / 'index.html')
                links = [node for node in page.all('a')
                         if normalized(node) == 'Add to Google Calendar']
                self.assertEqual(len(links), 1, 'Offer Google Calendar beside the ICS')
                url = urlsplit(links[0].attrs['href'])
                self.assertEqual((url.scheme, url.netloc, url.path),
                                 ('https', 'calendar.google.com', '/calendar/render'))
                query = parse_qs(url.query, strict_parsing=True)
                self.assertEqual(set(query), {'action', 'text', 'dates', 'details', 'location'})
                self.assertTrue(all(len(values) == 1 for values in query.values()))
                self.assertEqual(query['action'], ['TEMPLATE'])
                self.assertEqual(query['text'], [calendar_text(fields['SUMMARY'])])
                self.assertEqual(query['location'], [calendar_text(fields['LOCATION'])])
                self.assertEqual(query['details'],
                                 [calendar_text(fields['DESCRIPTION']) + '\n\n' + fields['URL']])
                self.assertEqual(query['dates'], [fields['DTSTART'] + '/' + fields['DTEND']])
                instants = [datetime.strptime(value, '%Y%m%dT%H%M%SZ').replace(tzinfo=timezone.utc)
                            for value in query['dates'][0].split('/')]
                page_times = [datetime.fromisoformat(node.attrs['datetime'])
                              for node in page.all('time') if 'T' in node.attrs['datetime']]
                self.assertEqual(instants, [value.astimezone(timezone.utc) for value in page_times])
                self.assertTrue(any('download' in node.attrs and
                                    node.attrs.get('href') == calendar.name
                                    for node in page.all('a')))

    def test_pages_without_calendars_do_not_invent_google_drafts(self):
        for source in (ROOT / 'events').glob('*/index.html'):
            if list(source.parent.glob('*.ics')):
                continue
            self.assertFalse(any('calendar.google.com' in node.attrs.get('href', '')
                                 for node in parsed(source).all('a')), source)


if __name__ == '__main__':
    unittest.main()
