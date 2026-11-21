"""Gera o feed do catalogo da Meta (Loja do Instagram/Facebook) a partir de content/site.json.

Uso: python scripts/gerar_catalogo_meta.py

Saidas:
- catalogo-meta.csv na raiz, servido em https://bordopersonalizados.com.br/catalogo-meta.csv
- assets/catalogo/<id>.jpg, porque o catalogo da Meta nao aceita as imagens .webp do site

No Commerce Manager, a fonte de dados aponta para a URL do CSV com atualizacao diaria.
Rode de novo sempre que produtos forem publicados ou alterados pelo painel. Exige Pillow.
"""
import csv
import io
import json
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SITE = 'https://bordopersonalizados.com.br'
FEED = ROOT / 'catalogo-meta.csv'
IMAGES = ROOT / 'assets' / 'catalogo'
FIELDS = ['id', 'title', 'description', 'availability', 'condition', 'price', 'link',
          'image_link', 'brand', 'product_type', 'google_product_category']
# Categorias do Google: 5645 = acessorios de cabelo; 1253 = brinquedos de pelucia.
CATEGORY = {'colinho': '1253'}


def jpg(product):
    target = IMAGES / f"{product['id']}.jpg"
    source = ROOT / product['image']
    if not target.exists() or target.stat().st_mtime < source.stat().st_mtime:
        image = Image.open(source).convert('RGB')
        image.thumbnail((1200, 1500))
        image.save(target, 'JPEG', quality=88, optimize=True, progressive=True)
    return f"{SITE}/assets/catalogo/{target.name}"


def rows(content):
    collections = {c['id']: c for c in content['collections'] if c.get('published')}
    for product in content['products']:
        collection = collections.get(product['collection'])
        if not product.get('published') or not collection or product.get('price') is None:
            continue  # "Sob consulta" e ocultos ficam fora: a Meta exige preco.
        yield {
            'id': product['id'],
            'title': product['title'][:150],
            'description': product['description'][:5000],
            'availability': 'in stock',
            'condition': 'new',
            'price': f"{product['price']:.2f} BRL",
            'link': f"{SITE}/#{product['collection']}",
            'image_link': jpg(product),
            'brand': 'Bordô',
            'product_type': collection['name'],
            'google_product_category': CATEGORY.get(product['collection'], '5645'),
        }


def main():
    content = json.loads((ROOT / 'content' / 'site.json').read_text(encoding='utf-8'))
    IMAGES.mkdir(exist_ok=True)
    out = io.StringIO()
    writer = csv.DictWriter(out, fieldnames=FIELDS, lineterminator='\n')
    writer.writeheader()
    total = 0
    for row in rows(content):
        writer.writerow(row)
        total += 1
    FEED.write_text(out.getvalue(), encoding='utf-8')
    print(f'{FEED.name}: {total} produtos')
    return 0


if __name__ == '__main__':
    sys.exit(main())
