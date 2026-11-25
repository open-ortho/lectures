"""Regression checks for reusable course navigation and catalog date display."""
from pathlib import Path
import unittest

from test_cs_lecture import normalized, parsed

ROOT = Path(__file__).resolve().parents[1]


class ReviewCatalog(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
