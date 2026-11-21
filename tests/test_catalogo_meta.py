import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CatalogoMetaTests(unittest.TestCase):
    """O feed da Loja do Instagram precisa acompanhar content/site.json."""

    def setUp(self):
        self.content = json.loads((ROOT / 'content' / 'site.json').read_text(encoding='utf-8'))
        with open(ROOT / 'catalogo-meta.csv', encoding='utf-8', newline='') as f:
            self.rows = list(csv.DictReader(f))

    def test_feed_matches_published_priced_products(self):
        live = {c['id'] for c in self.content['collections'] if c.get('published')}
        expected = {p['id'] for p in self.content['products']
                    if p.get('published') and p['collection'] in live and p.get('price') is not None}
        self.assertEqual({r['id'] for r in self.rows}, expected,
                         'Rode python scripts/gerar_catalogo_meta.py depois de mudar o catalogo.')

    def test_rows_meet_meta_requirements(self):
        prices = {p['id']: p['price'] for p in self.content['products']}
        for row in self.rows:
            with self.subTest(row['id']):
                self.assertRegex(row['price'], r'^\d+\.\d{2} BRL$')
                self.assertAlmostEqual(float(row['price'].split()[0]), prices[row['id']])
                self.assertTrue(row['link'].startswith('https://bordopersonalizados.com.br/'))
                image = re.sub(r'^https://bordopersonalizados\.com\.br/', '', row['image_link'])
                self.assertTrue(image.endswith('.jpg') and (ROOT / image).is_file(), image)
                self.assertLessEqual(len(row['title']), 150)
                self.assertTrue(row['description'] and row['brand'])


if __name__ == '__main__':
    unittest.main()
