"""Observable delivery contract for the resident lecture, not a clinical validation."""
from html.parser import HTMLParser
from pathlib import Path
import unittest
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / 'slides/orthodontic-informatics/module3'


class Elements(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.elements = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))


def local_target(source, url):
    path = unquote(urlsplit(url).path)
    if path.startswith('/lectures/'):
        return ROOT / path.removeprefix('/lectures/')
    return source.parent / path


class Module3Delivery(unittest.TestCase):
    def test_manifest_delivers_timed_lecture_with_notes_and_assets(self):
        manifest = MODULE / 'index.html'
        elements = Elements(manifest.read_text()).elements
        slides = [local_target(manifest, a['data-external-replace'])
                  for _, a in elements if 'data-external-replace' in a]
        self.assertGreaterEqual(len(slides), 20)
        self.assertLessEqual(len(slides), 25)
        self.assertEqual(len(slides), len(set(slides)))
        duration = 0
        for source in [manifest, *slides]:
            with self.subTest(source=source.name):
                self.assertTrue(source.is_file(), str(source))
                text = source.read_text()
                parsed = Elements(text).elements
                for tag, attrs in parsed:
                    for key in ('src', 'href'):
                        url = attrs.get(key, '')
                        if url and not urlsplit(url).scheme and not url.startswith('#'):
                            self.assertTrue(local_target(source, url).exists(), (source, url))
                    if tag == 'img':
                        self.assertTrue(attrs.get('alt', '').strip(), str(source))
                if source == manifest:
                    continue
                sections = [a for tag, a in parsed if tag == 'section']
                self.assertEqual(len(sections), 1)
                duration += int(sections[0]['data-duration'])
                self.assertTrue(any(tag == 'aside' and 'notes' in a.get('class', '').split()
                                    for tag, a in parsed), str(source))
                self.assertNotIn('<script', text.lower())
        self.assertEqual(duration, 60 * 60)
        self.assertEqual(set(MODULE.joinpath('slides').glob('*.html')), set(slides))


if __name__ == '__main__':
    unittest.main()
