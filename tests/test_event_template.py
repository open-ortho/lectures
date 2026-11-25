"""Copyable event markup; synthetic examples live only in scratch directories."""
from datetime import datetime
from pathlib import Path
import os
import re
import shutil
import tempfile
import unittest
from urllib.parse import urlsplit

from test_cs_lecture import normalized, parsed

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / 'templates/events/cwru-event.html'


class EventTemplate(unittest.TestCase):
    def test_template_is_static_copyable_markup_not_an_event_instance(self):
        self.assertTrue(TEMPLATE.is_file(), 'Provide a neutral HTML template to copy')
        text = TEMPLATE.read_text()
        page = parsed(TEMPLATE)
        self.assertTrue(text.startswith('<!--'))
        for phrase in ('events/YYYY-MM-DD-topic/index.html', 'Replace every',
                       'delete optional', 'YYYY-MM-DDTHH:MM:SS±HH:MM'):
            self.assertIn(phrase, text)
        for token in ('TITLE', 'ABSTRACT', 'DATE_ISO', 'DATE_DISPLAY', 'START_ISO',
                      'END_ISO', 'START_DISPLAY', 'END_DISPLAY', 'TIME_ZONE',
                      'INSTITUTION', 'COUNTRY', 'LOCATION', 'AUDIENCE',
                      'SPEAKER_NAME', 'PORTRAIT_PATH', 'AFFILIATION'):
            self.assertIn('{{' + token + '}}', text)
        self.assertEqual(len(list(page.all('h1'))), 1)
        self.assertEqual(normalized(next(page.all('title'))), '{{TITLE}}')
        self.assertEqual(normalized(next(page.all('h1'))), '{{TITLE}}')
        self.assertEqual([n.attrs['href'] for n in page.all('link')
                          if n.attrs.get('rel') == 'stylesheet'],
                         ['../../assets/css/index.css', '../../assets/css/cwru-event.css'])
        self.assertEqual(next(page.all('body')).attrs['class'], 'event-page')
        self.assertEqual(list(page.all('script')), [])
        self.assertEqual(list(page.all('iframe')), [])
        self.assertEqual(list(page.all('style')), [])
        self.assertFalse(any(n.attrs.get('href', '').endswith('.ics') for n in page.all('a')))
        self.assertNotIn('Toni Magni', text)
        self.assertNotIn('2026-12-02', text)

    def test_copy_substitution_resolves_assets_from_a_new_event_folder(self):
        self.assertTrue(TEMPLATE.is_file(), 'Provide the template before testing copies')
        with tempfile.TemporaryDirectory(dir=os.environ['TMPDIR']) as scratch:
            site = Path(scratch)
            shutil.copytree(ROOT / 'assets', site / 'assets')
            target = site / 'events/2099-01-02-synthetic-example/index.html'
            target.parent.mkdir(parents=True)
            shutil.copyfile(TEMPLATE, target)
            text = target.read_text()
            # Unknown optional fields are removed, not published with guessed values.
            text = re.sub(r'<!-- OPTIONAL TIME START -->.*?<!-- OPTIONAL TIME END -->',
                          '', text, flags=re.S)
            text = re.sub(r'<!-- OPTIONAL PORTRAIT START -->.*?<!-- OPTIONAL PORTRAIT END -->',
                          '', text, flags=re.S)
            text = re.sub(r'<!-- OPTIONAL AFFILIATION START -->.*?<!-- OPTIONAL AFFILIATION END -->',
                          '', text, flags=re.S)
            # Optional actions are inert HTML comments until real destinations exist.
            text = re.sub(r'<!-- OPTIONAL ACTIONS START.*?OPTIONAL ACTIONS END -->',
                          '', text, flags=re.S)
            values = dict(TITLE='Synthetic example', ABSTRACT='A test-only abstract.',
                          DATE_ISO='2099-01-02', DATE_DISPLAY='January 2, 2099',
                          INSTITUTION='Example institution', COUNTRY='Example country',
                          LOCATION='Example venue', AUDIENCE='Example audience',
                          SPEAKER_NAME='Example speaker')
            for key, value in values.items():
                text = text.replace('{{' + key + '}}', value)
            text = re.sub(r'<!--.*?-->', '', text, flags=re.S)
            target.write_text(text)
            self.assertNotRegex(text, r'\{\{[A-Z_]+\}\}')
            page = parsed(target)
            self.assertEqual(normalized(next(page.all('title'))), 'Synthetic example')
            self.assertEqual([n.attrs['datetime'] for n in page.all('time')], ['2099-01-02'])
            for node in page.all():
                self.assertFalse(any(k.startswith('on') for k in node.attrs))
                for attr in ('href', 'src'):
                    url = node.attrs.get(attr, '')
                    if url and not urlsplit(url).scheme and not url.startswith('#'):
                        self.assertTrue((target.parent / url).exists(), url)
            self.assertEqual(list(page.all('img')), [])
            self.assertFalse(any('download' in n.attrs for n in page.all('a')))
            self.assertNotIn('2099-01-02-synthetic-example', (ROOT / 'index.html').read_text())

    def test_shared_guide_owns_template_recipe_and_calendar_rules(self):
        guide = (ROOT / 'events/README.md').read_text()
        self.assertIn('../templates/events/cwru-event.html', guide)
        self.assertIn('mkdir -p events/YYYY-MM-DD-topic', guide)
        self.assertIn('cp templates/events/cwru-event.html events/YYYY-MM-DD-topic/index.html', guide)
        self.assertNotIn('as a markup', guide)
        for phrase in ('stable', 'UID', 'DTSTAMP', 'UTC', 'CRLF', '75 UTF-8 octets',
                       'escape', 'start/end times', 'time zone'):
            self.assertIn(phrase, guide)
        self.assertIn('templates/events/cwru-event.html', (ROOT / 'README.md').read_text())
        instance = (ROOT / 'events/2026-12-02-biomedical-informatics/README.md').read_text()
        self.assertIn('../README.md#calendar-files', instance)
        self.assertNotIn('75 UTF-8 octets', instance)


if __name__ == '__main__':
    unittest.main()
