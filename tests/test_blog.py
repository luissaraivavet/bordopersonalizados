"""Verificações básicas do blog editorial sem dependências externas."""
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOG = ROOT / "blog"
ARTIGOS = [
    "arvore-de-natal-elegante-gastando-pouco",
    "arvore-de-natal-180-ou-210",
    "quantos-metros-de-pisca-pisca",
    "decoracao-de-natal-crista",
]

class LinksParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.h1 = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "h1":
            self.h1 += 1
        if tag == "a":
            self.links.append(attrs)


class TestBlog(unittest.TestCase):
    def test_paginas_tem_metadados_e_um_titulo(self):
        pages = [BLOG / "index.html"] + [BLOG / slug / "index.html" for slug in ARTIGOS]
        for page in pages:
            with self.subTest(page=page):
                html = page.read_text(encoding="utf-8")
                p = LinksParser()
                p.feed(html)
                self.assertEqual(p.h1, 1)
                self.assertIn('rel="canonical"', html)
                self.assertIn('application/ld+json', html)
                self.assertIn('name="description"', html)
                self.assertIn('/assets/brand-logo.png', html)
                self.assertIn('href="/blog/estilos.css"', html)
                self.assertIn('</html>', html)
                for link in p.links:
                    if "mercadolivre.com.br" in link.get("href", ""):
                        self.assertIn("sponsored", link.get("rel", ""))
                        self.assertIn("nofollow", link.get("rel", ""))
                        self.assertIn("Publicidade", html)

    def test_links_locais_essenciais_existem(self):
        pages = [BLOG / "index.html"] + [BLOG / slug / "index.html" for slug in ARTIGOS]
        for page in pages:
            p = LinksParser()
            p.feed(page.read_text(encoding="utf-8"))
            for link in p.links:
                href = link.get("href", "")
                if href.startswith("/blog/") and not href.startswith("/blog/estilos.css"):
                    path = href.split("#")[0].split("?")[0].lstrip("/")
                    self.assertTrue((ROOT / path / "index.html").is_file(), f"{page}: {href}")

    def test_navegacao_e_sitemap(self):
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        self.assertIn('href="/blog/"', home)
        for slug in [""] + [s + "/" for s in ARTIGOS]:
            self.assertIn("https://bordopersonalizados.com.br/blog/" + slug, sitemap)

if __name__ == "__main__":
    unittest.main()
