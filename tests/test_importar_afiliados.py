"""Testes do importador de afiliados sem conexão com o Mercado Livre."""
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "scripts" / "importar_afiliados.py"
spec = importlib.util.spec_from_file_location("importar_afiliados", MODULE)
importador = importlib.util.module_from_spec(spec)
spec.loader.exec_module(importador)

LINK = (
    "https://www.mercadolivre.com.br/p/MLB54646018"
    "?matt_tool=38524122&pdp_filters=item_id:MLB4263473855"
    "&ua=referencia#origin=share"
)


class TestImportarAfiliados(unittest.TestCase):
    def test_preserva_url_original_e_ids(self):
        self.assertEqual(importador.validate_affiliate_url(LINK), LINK)
        self.assertEqual(
            importador.product_ids(LINK),
            {"id_catalogo": "MLB54646018", "id_anuncio": "MLB4263473855"},
        )
        item = importador.product_ids("https://produto.mercadolivre.com.br/MLB-4263473855-item-_JM")
        self.assertEqual(item["id_anuncio"], "MLB4263473855")

    def test_rejeita_hosts_nao_confiaveis_e_urls_sem_produto(self):
        for url in (
            "http://www.mercadolivre.com.br/p/MLB54646018",
            "https://www.mercadolivre.com.br.evil.test/p/MLB54646018",
            "https://localhost/p/MLB54646018",
            "https://www.mercadolivre.com.br/",
            "https://user:pass@www.mercadolivre.com.br/p/MLB54646018",
        ):
            with self.subTest(url=url), self.assertRaises(ValueError):
                importador.validate_affiliate_url(url)

    def test_formatacao_de_precos(self):
        cases = {
            "R$ 1.234,56": "1234.56",
            "1200.99": "1200.99",
            "0": "0.00",
            "999,90": "999.90",
        }
        for sample, expected in cases.items():
            self.assertEqual(importador.number_string(sample), expected)
        self.assertIsNone(importador.number_string("sem preço"))
        self.assertIsNone(importador.number_string("-5"))

    def test_entrada_catalogo(self):
        entries = importador.load_links(ROOT / "content" / "afiliados-links.json")
        self.assertTrue(entries)
        self.assertEqual(entries[0][0], "arvore-de-natal-210-600-galhos")
        self.assertEqual(entries[0][1], importador.validate_affiliate_url(entries[0][1]))

    def test_fixture_sem_rede_com_scrapling(self):
        try:
            from scrapling import Selector
        except ImportError:
            self.skipTest("Scrapling opcional não instalado no ambiente de testes")
        fixture = ROOT / "tests" / "fixtures" / "anuncio_afiliado_exemplo.html"
        page = Selector(fixture.read_text(encoding="utf-8"), url=LINK)
        result = importador.parse_page(page, LINK, "teste")
        self.assertEqual(result["status"], "revisar")
        self.assertEqual(result["titulo"], "Árvore de Natal de Teste")
        self.assertEqual(result["preco_brl"], "145.90")
        self.assertEqual(result["vendedor"], "Loja de Teste")
        self.assertEqual(result["marca"], "Marca de Exemplo")
        self.assertEqual(result["avaliacao"], "4.50")
        self.assertEqual(result["quantidade_avaliacoes"], "10")
        self.assertEqual(result["caracteristicas"]["Altura"], "2,10 m")
        self.assertTrue(result["imagens"])
        self.assertFalse(result["publicar_no_site"])
        self.assertFalse(result["revisado"])


if __name__ == "__main__":
    unittest.main()
