"""Observable delivery contract for the resident lecture, not a clinical validation."""
from html.parser import HTMLParser
from pathlib import Path
import re
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
    def opening_slides(self):
        manifest = MODULE / 'index.html'
        return [local_target(manifest, attrs['data-external-replace'])
                for _, attrs in Elements(manifest.read_text()).elements
                if 'data-external-replace' in attrs]

    def test_first_slide_restores_course_title_and_module_qr_table(self):
        title = self.opening_slides()[0]
        text = title.read_text()
        elements = Elements(text).elements
        self.assertEqual(title.name, 'orthodontic-informatics.html')
        self.assertIn(('table', {'style': 'width:100%;'}), elements)
        self.assertIn(('td', {'style': 'width: 33%;'}), elements)
        self.assertIn(('td', {'style': 'vertical-align: top;'}), elements)
        self.assertIn('<h2 style="margin-top: 0px;">Orthodontic Informatics</h2>', text)
        self.assertIn('<p>Data, Imaging, and Standards in Orthodontic Practice</p>', text)
        self.assertIn('<b>Module 3</b><br />AI and Reusable Clinical Data', text)
        self.assertIn('<em>toni magni, BME - afm@case.edu</em>', text)
        images = [attrs for tag, attrs in elements if tag == 'img']
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0]['src'],
                         '/lectures/slides/orthodontic-informatics/module3/url_qrcode.svg')
        self.assertTrue(images[0].get('alt', '').strip())
        self.assertEqual(images[0]['style'], 'width:100%')

    def test_second_slide_is_outline_before_preserved_hook_and_case(self):
        slides = self.opening_slides()
        self.assertEqual([slide.name for slide in slides[:5]],
                         ['orthodontic-informatics.html', 'outline.html',
                          'hook.html', 'case.html', 'review.html'])
        text = slides[1].read_text()
        self.assertIn('<h2>Outline</h2>', text)
        elements = Elements(text).elements
        self.assertTrue(any(tag == 'ol' for tag, _ in elements))
        self.assertGreaterEqual(sum(tag == 'li' for tag, _ in elements), 5)
        self.assertIn('What would you delegate before the next visit?', slides[2].read_text())
        self.assertIn('One case, one useful output', slides[3].read_text())
        self.assertEqual([int(next(attrs['data-duration'] for tag, attrs in
                                  Elements(slide.read_text()).elements if tag == 'section'))
                          for slide in slides[:5]], [30, 30, 90, 150, 120])

    def test_section_time_labels_are_speaker_notes_only(self):
        label = r'\d+[–-]\d+\s*·\s*[^<]+'
        for slide in self.opening_slides():
            with self.subTest(slide=slide.name):
                text = slide.read_text()
                notes = re.search(r'<aside class="notes">(.*?)</aside>', text, re.S)
                self.assertIsNotNone(notes)
                self.assertRegex(notes.group(1), label)
                visible = text[:notes.start()] + text[notes.end():]
                self.assertNotRegex(visible, label)

    def test_manifest_delivers_timed_lecture_with_notes_and_assets(self):
        manifest = MODULE / 'index.html'
        elements = Elements(manifest.read_text()).elements
        slides = [local_target(manifest, a['data-external-replace'])
                  for _, a in elements if 'data-external-replace' in a]
        self.assertGreaterEqual(len(slides), 20)
        self.assertEqual(len(slides), 26)
        self.assertLessEqual(len(slides), 30)
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
