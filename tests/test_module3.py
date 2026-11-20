"""Observable delivery contract for the resident lecture, not a clinical validation."""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET
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


class VisibleListItems(HTMLParser):
    """Read audience list text while leaving speaker-note lists unrestricted."""

    def __init__(self, text):
        super().__init__()
        self.items = []
        self.notes_depth = 0
        self.item = None
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        if tag == 'aside' and (self.notes_depth or
                               'notes' in dict(attrs).get('class', '').split()):
            self.notes_depth += 1
        if not self.notes_depth and tag == 'li':
            self.item = []

    def handle_endtag(self, tag):
        if self.notes_depth:
            if tag == 'aside':
                self.notes_depth -= 1
            return
        if tag == 'li' and self.item is not None:
            self.items.append(' '.join(''.join(self.item).split()))
            self.item = None

    def handle_data(self, data):
        if not self.notes_depth and self.item is not None:
            self.item.append(data)


def visible_list_items(text):
    return VisibleListItems(text).items


def local_target(source, url):
    path = unquote(urlsplit(url).path)
    if path.startswith('/lectures/'):
        return ROOT / path.removeprefix('/lectures/')
    return source.parent / path


class Module3Delivery(unittest.TestCase):
    def diagram(self, name):
        source = MODULE / 'slides' / name
        text = source.read_text()
        if name == 'agentic-email.html':
            images = [attrs for tag, attrs in Elements(text).elements if tag == 'img']
            self.assertEqual(len(images), 1)
            self.assertEqual(images[0]['src'], '/lectures/assets/img/agentic-email.svg')
            self.assertTrue(images[0].get('alt', '').strip())
            self.assertEqual(images[0]['style'], 'width:100%')
            self.assertNotIn('<svg', text)
            return ET.fromstring(local_target(source, images[0]['src']).read_text())
        return ET.fromstring(re.search(r'<svg\b.*?</svg>', text, re.S).group())

    def test_agentic_diagram_is_one_shared_accessible_image_and_two_backgrounds(self):
        asset = ROOT / 'assets/img/agentic-email.svg'
        self.assertTrue(asset.is_file(), 'Missing shared agentic email diagram')
        svg = self.diagram('agentic-email.html')
        self.assertEqual(svg.get('viewBox'), '0 0 1400 460')
        description = next(n.text for n in svg if n.tag.split('}')[-1] == 'desc')
        image = next(attrs for tag, attrs in Elements(
            (MODULE / 'slides/agentic-email.html').read_text()).elements if tag == 'img')
        self.assertEqual(image['alt'], description)
        for name in ('harness-mcp.html', 'independent-permissions.html'):
            with self.subTest(slide=name):
                source = MODULE / 'slides' / name
                text = source.read_text()
                section = next(attrs for tag, attrs in Elements(text).elements if tag == 'section')
                self.assertEqual(section['data-background-image'],
                                 '/lectures/assets/img/agentic-email.svg')
                self.assertEqual(local_target(source, section['data-background-image']), asset)
                self.assertEqual(section['data-background-opacity'], '0.2')
                self.assertEqual(section['data-background-size'], 'contain')
                self.assertNotIn('<svg', text)

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

    def test_outline_then_prerequisite_review_before_preserved_hook_and_case(self):
        slides = self.opening_slides()
        self.assertEqual([slide.name for slide in slides[:5]],
                         ['orthodontic-informatics.html', 'outline.html',
                          'review.html', 'hook.html', 'case.html'])
        text = slides[1].read_text()
        self.assertIn('<h2>Outline</h2>', text)
        elements = Elements(text).elements
        self.assertTrue(any(tag == 'ol' for tag, _ in elements))
        self.assertEqual(visible_list_items(text), [
            'Delegate to AI',
            'How I use AI',
            'Reusable clinical context, permissions and review',
            'Integration using vendor-specific interfaces versus shared standards',
            'Clinician requirements and Connectathon testing',
            'Case exercise, takeaways and questions for Module 4',
        ])
        self.assertIn('<h2>Review</h2>', slides[2].read_text())
        self.assertIn('What would you delegate to AI?', slides[3].read_text())
        self.assertIn('P-18: what would AI need?', slides[4].read_text())
        self.assertEqual([int(next(attrs['data-duration'] for tag, attrs in
                                  Elements(slide.read_text()).elements if tag == 'section'))
                          for slide in slides[:5]], [30, 30, 120, 90, 150])

    def test_visible_agenda_parser_excludes_note_bullets_not_other_asides(self):
        text = '''<ol><li>Delegate to <strong>AI</strong></li></ol>
            <aside class="presenter notes"><ul><li>Presenter reminder</li></ul></aside>
            <aside><ul><li>Visible supporting item</li></ul></aside>
            <ol><li>How I use AI</li></ol>'''
        self.assertEqual(visible_list_items(text), [
            'Delegate to AI', 'Visible supporting item', 'How I use AI'])

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

    def test_email_diagrams_compare_clients_at_the_same_mailbox_auth_boundary(self):
        slides = self.opening_slides()
        self.assertEqual([s.name for s in slides[5:10]], [
            'email-story.html', 'traditional-email.html', 'agentic-email.html',
            'harness-mcp.html', 'independent-permissions.html'])
        diagrams = []
        for name, client, account in [
                ('traditional-email.html', 'mail-client', 'Human account'),
                ('agentic-email.html', 'mcp-server', 'Human email account')]:
            with self.subTest(slide=name):
                text = (MODULE / 'slides' / name).read_text()
                svg = self.diagram(name)
                self.assertEqual(svg.get('role'), 'img')
                nodes = {node.get('data-component', node.get('id')): node
                         for node in svg.iter() if node.get('id')}
                for ref in svg.get('aria-labelledby', '').split():
                    self.assertTrue(''.join(nodes[ref].itertext()).strip())
                self.assertTrue(svg.get('aria-labelledby'))
                for tag in ('title', 'desc'):
                    self.assertTrue(any(n.tag.split('}')[-1] == tag for n in svg))
                boundary = nodes['mailbox-auth']
                imap = nodes['imap-service']
                self.assertEqual(boundary.get('x1'), boundary.get('x2'))
                imap_right = float(imap.get('x')) + float(imap.get('width'))
                self.assertGreater(float(boundary.get('x1')), imap_right)
                self.assertLess(float(boundary.get('x1')), float(nodes[client].get('x')))
                self.assertTrue(boundary.get('stroke-dasharray'))
                self.assertIn(client, nodes)
                labels = ' '.join(svg.itertext())
                self.assertIn(account, labels)
                for label in ('MBOX', 'IMAP', 'mailbox data', 'requests'):
                    self.assertIn(label, labels)
                for forbidden in ('<script', '<image', '<foreignObject', '<pattern'):
                    self.assertNotIn(forbidden, text)
                    self.assertNotIn(forbidden, ET.tostring(svg, encoding='unicode').replace('ns0:', ''))
                diagrams.append(nodes)
        self.assertEqual(len(diagrams), 2, 'Both diagrams must satisfy the shared boundary contract')
        for component in ('mailbox-store', 'imap-service', 'mailbox-auth'):
            for attr in ('x', 'y', 'width', 'height', 'x1', 'x2', 'y1', 'y2',
                         'fill', 'stroke', 'stroke-width', 'stroke-dasharray'):
                self.assertEqual(diagrams[0][component].get(attr),
                                 diagrams[1][component].get(attr))
        agent = (MODULE / 'slides/agentic-email.html').read_text()
        self.assertIn('The MCP server authenticates to the mail service;', agent)
        for phrase in ('Model Context Protocol', 'model does not receive raw credentials',
                       'tool filtering', 'resource-side', 'additional authentication'):
            self.assertIn(phrase, agent)
        traditional = (MODULE / 'slides/traditional-email.html').read_text()
        for phrase in ('Webmail (GMail, ...)', 'Mail app (Apple Mail, Thunderbird, ...)', 'Gmail', 'illustrative',
                       'not a claim about Gmail', 'Internet Message Access Protocol'):
            self.assertIn(phrase, traditional)

    def test_email_diagrams_show_a_human_operating_the_client_or_outer_harness(self):
        diagrams = []
        for name, interface in [('traditional-email.html', 'mail-client'),
                                ('agentic-email.html', 'harness')]:
            with self.subTest(slide=name):
                text = (MODULE / 'slides' / name).read_text()
                svg = self.diagram(name)
                nodes = {n.get('data-component'): n for n in svg.iter()
                         if n.get('data-component')}
                self.assertIn('human', nodes)
                self.assertIn('laptop', nodes)
                self.assertIn('envelope', nodes)
                self.assertIn('Human', ''.join(nodes['human'].itertext()))
                link = nodes['human-interface']
                self.assertEqual(link.get('data-from'), 'human')
                self.assertEqual(link.get('data-to'), interface)
                self.assertTrue(link.get('marker-start'))
                self.assertTrue(link.get('marker-end'))
                diagrams.append(nodes)
        self.assertEqual(len(diagrams), 2, 'Both diagrams must contain the human interface')
        for component in ('human', 'laptop', 'envelope'):
            self.assertEqual(ET.tostring(diagrams[0][component]),
                             ET.tostring(diagrams[1][component]))
        agent = diagrams[1]
        self.assertIn(agent['model'], list(agent['harness'].iter()))
        self.assertNotIn(agent['human'], list(agent['harness'].iter()))
        self.assertEqual(agent['tool-requests'].get('data-from'), 'model')
        self.assertEqual(agent['tool-requests'].get('data-to'), 'mcp-server')
        self.assertEqual(agent['tool-requests'].get('data-executor'), 'harness')
        self.assertTrue(agent['tool-requests'].get('marker-start'))
        self.assertTrue(agent['tool-requests'].get('marker-end'))
        notes = (MODULE / 'slides/agentic-email.html').read_text()
        self.assertIn('The human controls the harness, not the model directly.', notes)
        self.assertIn('not a direct model network connection', notes)

    def test_agent_email_limits_tools_not_the_underlying_human_account(self):
        text = (MODULE / 'slides/agentic-email.html').read_text()
        svg = self.diagram('agentic-email.html')
        labels = ' '.join(' '.join(svg.itertext()).split())
        for phrase in ('Human email account', 'Limited MCP server', 'Read', 'Compose', 'Save drafts', 'No send tool'):
            self.assertIn(phrase, labels)
        self.assertNotIn('Agent’s own restricted email account', text)
        for phrase in ('filter limits this tool path, not the account itself',
                       'restricted or unrestricted', 'not equivalent to independent least-privilege'):
            self.assertIn(phrase, text)

    def test_manifest_removes_writeback_slide_without_a_replacement(self):
        slides = self.opening_slides()
        self.assertEqual(len(slides), 27)
        self.assertNotIn('review-before-writeback.html', [slide.name for slide in slides])
        self.assertFalse((MODULE / 'slides/review-before-writeback.html').exists())
        self.assertEqual([slide.name for slide in slides[13:15]], [
            'exchange-operations.html', 'proprietary-based-interoperability.html'])

    def test_delivery_maps_match_the_27_slide_section_boundaries(self):
        guide = (MODULE / 'README.md').read_text()
        plan = (MODULE / 'PLAN.md').read_text()
        for time, minutes, slides in [
                ('0–7', 7, '1–5'), ('7–15', 8, '6–10'),
                ('15–27', 12, '11–14'), ('27–39', 12, '15–19'),
                ('39–49', 10, '20–23'), ('49–56', 7, '24–25'),
                ('56–60', 4, '26–27')]:
            with self.subTest(time=time):
                self.assertIn(f'| {time} | {slides} |', guide)
                self.assertIn(f'| {time} | {minutes} | {slides} |', plan)
        self.assertIn('| **Total** | **60** | **27** |', plan)
        for document in (guide, plan):
            self.assertNotIn('28-slide', document)
            self.assertNotIn('28 slides', document)

    def test_removed_duration_is_assigned_to_preceding_exchange_slide(self):
        text = (MODULE / 'slides/exchange-operations.html').read_text()
        section = next(attrs for tag, attrs in Elements(text).elements if tag == 'section')
        self.assertEqual(int(section['data-duration']), 240)

    def test_manifest_delivers_timed_lecture_with_notes_and_assets(self):
        manifest = MODULE / 'index.html'
        elements = Elements(manifest.read_text()).elements
        slides = [local_target(manifest, a['data-external-replace'])
                  for _, a in elements if 'data-external-replace' in a]
        self.assertGreaterEqual(len(slides), 20)
        self.assertEqual(len(slides), 27)
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
