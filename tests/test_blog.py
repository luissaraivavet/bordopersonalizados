"""Verificações básicas do blog editorial sem dependências externas."""
import json
import re
import xml.etree.ElementTree as ET
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
                if href.startswith("/blog/") and not href.endswith((".css", ".xml")):
                    path = href.split("#")[0].split("?")[0].lstrip("/")
                    self.assertTrue((ROOT / path / "index.html").is_file(), f"{page}: {href}")

    def test_estrutura_seo_e_autoria(self):
        pages = [BLOG / "index.html"] + [BLOG / slug / "index.html" for slug in ARTIGOS]
        pages.append(BLOG / "como-selecionamos" / "index.html")
        for page in pages:
            with self.subTest(page=page):
                html = page.read_text(encoding="utf-8")
                title = re.search(r"<title>([^<]+)</title>", html)
                self.assertIsNotNone(title)
                self.assertLessEqual(len(title.group(1)), 65)
                canonical = re.search(r'<link rel="canonical" href="([^"]+)"', html)
                self.assertIsNotNone(canonical)
                expected = "https://bordopersonalizados.com.br/" + str(page.parent.relative_to(ROOT)).replace("\\", "/") + "/"
                self.assertEqual(canonical.group(1), expected)
                scripts = re.findall(r'<script type="application/ld\+json">([\s\S]*?)</script>', html)
                self.assertEqual(len(scripts), 1)
                structured = json.loads(scripts[0])
                graph = structured.get("@graph", [])
                types = {node.get("@type") for node in graph}
                self.assertIn("BreadcrumbList", types)
                self.assertTrue("BlogPosting" in types or "CollectionPage" in types or "AboutPage" in types)
                self.assertIn('href="/blog/feed.xml"', html)

    def test_feed_e_sitemap_validos(self):
        rss = ET.parse(BLOG / "feed.xml").getroot()
        self.assertEqual(len(rss.findall("./channel/item")), 4)
        sitemap = ET.parse(ROOT / "sitemap.xml").getroot()
        urls = [elem.text for elem in sitemap.iter() if elem.tag.endswith("loc")]
        self.assertEqual(len(urls), len(set(urls)))
        self.assertIn("https://bordopersonalizados.com.br/blog/como-selecionamos/", urls)

    def test_pesquisa_produto_rastreavel_e_nao_publicada(self):
        dossier = json.loads((ROOT / "content" / "afiliados-rascunho-arvore.json").read_text(encoding="utf-8"))
        catalogo = json.loads((ROOT / "content" / "afiliados-links.json").read_text(encoding="utf-8"))
        original = next(item for item in catalogo["links"]
                        if item["slug"] == dossier["slug"])
        self.assertEqual(dossier["url_afiliado"], original["url_afiliado"])
        self.assertEqual(dossier["caracteristicas"]["altura_cm"], 210)
        self.assertEqual(dossier["caracteristicas"]["largura_maxima_cm"], 105)
        self.assertEqual(dossier["painel_avaliacoes"]["total_avaliacoes"], 333)
        self.assertEqual(dossier["painel_avaliacoes"]["total_comentarios_visiveis_indicados"], 150)
        self.assertTrue(dossier["procedencia"]["fonte_primaria"].startswith("https://www.mercadolivre.com.br/"))
        self.assertFalse(dossier["revisado"])
        self.assertFalse(dossier["publicar_no_site"])
        self.assertFalse(dossier["painel_avaliacoes"]["fotos_de_compradores_baixadas"])
        artigo = (BLOG / "arvore-de-natal-180-ou-210" / "index.html").read_text(encoding="utf-8")
        self.assertIn("600 galhos", artigo)
        self.assertIn("333 avaliações e 150 comentários", artigo)
        self.assertIn("Não incluídos", artigo)
        self.assertIn("A Bordô não realizou teste físico", artigo)

    def test_previa_nao_indexavel(self):
        preview = ROOT / "preview"
        for html_file in preview.rglob("index.html"):
            with self.subTest(page=html_file):
                html = html_file.read_text(encoding="utf-8")
                self.assertIn('content="noindex,nofollow"', html)

    def test_navegacao_e_sitemap(self):
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        self.assertIn('href="/blog/"', home)
        for slug in [""] + [s + "/" for s in ARTIGOS] + ["como-selecionamos/"]:
            self.assertIn("https://bordopersonalizados.com.br/blog/" + slug, sitemap)

if __name__ == "__main__":
    unittest.main()
