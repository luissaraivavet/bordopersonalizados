#!/usr/bin/env python3
"""Importação revisável de anúncios do Mercado Livre usando Scrapling.

Não publica produtos. Não tenta contornar autenticação, CAPTCHA, bloqueios
ou regras de robots.txt. Execute localmente com URLs autorizadas.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlsplit
from urllib.request import Request, urlopen
from urllib.robotparser import RobotFileParser

ALLOWED_HOSTS = {"mercadolivre.com.br", "www.mercadolivre.com.br", "produto.mercadolivre.com.br"}
USER_AGENT = "BordoCuradoriaBot/1.0 (+https://bordopersonalizados.com.br/)"
ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LINKS = ROOT / "content" / "afiliados-links.json"
DEFAULT_OUTPUT = ROOT / ".bordo-scraping" / "resultados.json"
PRODUCT_PATH = re.compile(r"(?i)(?:/p/MLB\d+|/MLB-\d+)")
IDENTIFIER = re.compile(r"^MLB\d+$", re.I)
MAX_DESCRIPTION = 22000
MAX_GALLERY = 30


def validate_affiliate_url(value: str) -> str:
    if not isinstance(value, str) or len(value) > 4000:
        raise ValueError("Link de afiliado inválido ou excessivamente longo.")
    parsed = urlsplit(value.strip())
    if parsed.scheme != "https" or parsed.hostname not in ALLOWED_HOSTS:
        raise ValueError("Somente URLs HTTPS de anúncios do Mercado Livre Brasil são aceitas.")
    if parsed.username or parsed.password or parsed.port not in (None, 443):
        raise ValueError("Credenciais ou porta não permitidas na URL.")
    if not PRODUCT_PATH.search(parsed.path):
        raise ValueError("URL sem identificador de anúncio ou catálogo MLB.")
    return value.strip()


def product_ids(url: str) -> dict:
    parsed = urlsplit(url)
    match = re.search(r"/p/(MLB\d+)", parsed.path, re.I)
    item = re.search(r"/MLB-(\d+)", parsed.path, re.I)
    query = parse_qs(parsed.query)
    filter_value = (query.get("pdp_filters") or [""])[0]
    filt = re.search(r"item_id:(MLB\d+)", filter_value, re.I)
    return {
        "id_catalogo": match.group(1).upper() if match else None,
        "id_anuncio": (filt.group(1).upper() if filt else ("MLB" + item.group(1) if item else None)),
    }


def clean(value, limit=MAX_DESCRIPTION):
    if value is None:
        return None
    text = re.sub(r"\s+", " ", str(value)).strip()
    return text[:limit] if text else None


def first(page, selectors):
    for selector in selectors:
        try:
            found = page.css(selector).get()
            value = clean(found)
            if value:
                return value
        except (AttributeError, KeyError, ValueError):
            continue
    return None


def all_values(page, selectors, limit=MAX_GALLERY):
    results, seen = [], set()
    for selector in selectors:
        try:
            candidates = page.css(selector).getall()
        except (AttributeError, KeyError, ValueError):
            continue
        for val in candidates:
            v = clean(val, 4000)
            if v and v not in seen:
                results.append(v)
                seen.add(v)
                if len(results) >= limit:
                    return results
    return results


def jsonld_nodes(page):
    # JSON-LD pode superar 4 KB. Ler o script inteiro, sem truncar JSON.
    try:
        blocks = page.css("script[type='application/ld+json']::text").getall()[:100]
    except (AttributeError, KeyError, ValueError):
        blocks = []
    nodes = []
    for block in blocks:
        try:
            obj = json.loads(block)
        except (TypeError, ValueError):
            continue
        stack = [obj]
        while stack:
            entry = stack.pop()
            if isinstance(entry, list):
                stack.extend(entry)
            elif isinstance(entry, dict):
                nodes.append(entry)
                if isinstance(entry.get("@graph"), (dict, list)):
                    stack.append(entry["@graph"])
    return nodes


def product_node(page):
    for node in jsonld_nodes(page):
        types = node.get("@type", [])
        if isinstance(types, str):
            types = [types]
        if any(str(t).lower().endswith("product") for t in types):
            return node
    return {}


def as_dict(obj):
    if isinstance(obj, dict):
        return obj
    if isinstance(obj, list):
        return next((x for x in obj if isinstance(x, dict)), {})
    return {}


def name_of(obj):
    if isinstance(obj, str):
        return clean(obj, 400)
    if isinstance(obj, dict):
        return clean(obj.get("name"), 400)
    return None


def number_string(value):
    if value is None:
        return None
    try:
        if isinstance(value, (float, int, Decimal)):
            result = Decimal(str(value))
        else:
            raw = re.sub(r"[^\d,.-]", "", str(value))
            if not raw:
                return None
            if "," in raw and "." in raw:
                raw = raw.replace(".", "").replace(",", ".") if raw.rfind(",") > raw.rfind(".") else raw.replace(",", "")
            elif "," in raw:
                raw = raw.replace(",", ".")
            result = Decimal(raw)
        if not result.is_finite() or result < 0:
            return None
        return str(result.quantize(Decimal("0.01")))
    except (InvalidOperation, ValueError):
        return None


def product_images(product, page):
    images = product.get("image", [])
    if isinstance(images, str):
        images = [images]
    if isinstance(images, dict):
        images = [images]
    candidates = []
    for item in images if isinstance(images, list) else []:
        src = item.get("url") or item.get("contentUrl") if isinstance(item, dict) else item
        if src:
            candidates.append(src)
    candidates.extend(all_values(page, [
        "meta[property='og:image']::attr(content)",
        ".ui-pdp-gallery__figure img::attr(data-zoom)",
        ".ui-pdp-gallery__figure img::attr(src)",
        "figure.ui-pdp-gallery__figure img::attr(src)",
    ], limit=MAX_GALLERY))
    seen, output = set(), []
    for src in candidates:
        s = clean(src, 2000)
        if not s or not s.startswith("https://") or s in seen:
            continue
        host = urlsplit(s).hostname or ""
        if host not in ("http2.mlstatic.com", "http2.mercadolivre.com", "http2.mlstatic.com.br"):
            continue
        seen.add(s)
        output.append(s)
        if len(output) == MAX_GALLERY:
            break
    return output


def attribute_table(page):
    table = {}
    selectors = [
        ".ui-pdp-specs__table tr",
        ".ui-vpp-striped-specs__table tr",
        "table.andes-table tr",
        ".ui-pdp-specs tr",
    ]
    for selector in selectors:
        try:
            rows = page.css(selector)
        except (AttributeError, KeyError, ValueError):
            continue
        for row in rows:
            try:
                key = clean(row.css("th::text").get(), 120) or clean(row.css("td:first-child::text").get(), 120)
                value = clean(row.css("td:last-child::text").get(), 500)
            except (AttributeError, KeyError, ValueError):
                continue
            if key and value and key != value and len(table) < 100:
                table.setdefault(key, value)
    return table


def description(page, product):
    candidate = clean(product.get("description"))
    if candidate:
        return candidate
    for selector in (".ui-pdp-description__content", ".ui-pdp-description", ".ui-vpp-description__content"):
        try:
            elements = page.css(selector)
            if elements:
                texts = elements[0].xpath(".//text()").getall()
                text = clean(" ".join(str(x) for x in texts))
                if text:
                    return text
        except (AttributeError, KeyError, ValueError):
            continue
    return None


def parse_page(page, affiliate_url: str, slug: str):
    """Extrai campos públicos identificáveis; nunca inventa valores ausentes."""
    product = product_node(page)
    offer = as_dict(product.get("offers"))
    rating = as_dict(product.get("aggregateRating"))
    ids = product_ids(affiliate_url)
    title = clean(product.get("name"), 350) or first(page, [
        "h1.ui-pdp-title::text", "meta[property='og:title']::attr(content)", "h1::text"
    ])
    displayed_price = number_string(offer.get("price"))
    if displayed_price is None:
        amount = first(page, [".ui-pdp-price__second-line .andes-money-amount__fraction::text",
                              ".ui-pdp-price .andes-money-amount__fraction::text"])
        cents = first(page, [".ui-pdp-price__second-line .andes-money-amount__cents::text"])
        if amount:
            displayed_price = number_string(amount.replace(".", "") + ("." + cents if cents else ""))
    visible_description = description(page, product)
    image_urls = product_images(product, page)
    seller = name_of(offer.get("seller")) or first(page, [".ui-pdp-seller__header__title::text"])
    status = "revisar" if title else "inacessivel"
    warnings = []
    if not title:
        warnings.append("Página sem título verificável; pode estar bloqueada, vazia ou alterada.")
    if not displayed_price:
        warnings.append("Preço não encontrado; consultar anúncio antes de divulgar qualquer valor.")
    if not visible_description:
        warnings.append("Descrição não encontrada na fonte acessível.")
    if not image_urls:
        warnings.append("Não foram obtidas imagens de produto verificáveis.")
    return {
        "slug": slug,
        "status": status,
        "capturado_em": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "url_afiliado": affiliate_url,
        "url_resposta": str(getattr(page, "url", affiliate_url)),
        **ids,
        "titulo": title,
        "marca": name_of(product.get("brand")),
        "modelo": clean(product.get("model"), 250),
        "categoria": clean(product.get("category"), 300),
        "sku": clean(product.get("sku") or product.get("productID"), 200),
        "preco_brl": displayed_price if (offer.get("priceCurrency") or "BRL") == "BRL" else None,
        "moeda": clean(offer.get("priceCurrency")) or ("BRL" if displayed_price else None),
        "preco_original_brl": None,
        "disponibilidade": clean(offer.get("availability"), 200),
        "condicao": clean(offer.get("itemCondition"), 200),
        "vendedor": seller,
        "avaliacao": number_string(rating.get("ratingValue")),
        "quantidade_avaliacoes": rating.get("reviewCount") or rating.get("ratingCount"),
        "imagens": image_urls,
        "descricao_publica": visible_description,
        "caracteristicas": attribute_table(page),
        "variacoes": product.get("hasVariant", []) if isinstance(product.get("hasVariant", []), list) else [],
        "frete": None,
        "prazo_entrega": None,
        "observacoes": warnings,
        "revisado": False,
        "publicar_no_site": False,
    }


def robots_permits(url: str):
    parsed = urlsplit(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    try:
        req = Request(robots_url, headers={"User-Agent": USER_AGENT, "Accept": "text/plain"})
        with urlopen(req, timeout=12) as response:
            body = response.read(1024 * 512).decode("utf-8", "replace")
    except HTTPError as exc:
        if exc.code in (404, 410):
            return True, "robots.txt inexistente"
        return False, f"robots.txt não acessível (HTTP {exc.code})"
    except (URLError, OSError, TimeoutError) as exc:
        return False, f"Não foi possível consultar robots.txt ({type(exc).__name__})"
    parser = RobotFileParser()
    parser.parse(body.splitlines())
    return parser.can_fetch(USER_AGENT, url), "Política robots.txt verificada"


def load_links(path: Path):
    source = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(source, dict):
        source = source.get("links")
    if not isinstance(source, list) or not source:
        raise ValueError("O arquivo deve conter uma lista não vazia sob a chave links.")
    output, slugs = [], set()
    for item in source:
        if not isinstance(item, dict):
            raise ValueError("Cada entrada deve ser um objeto com slug e url_afiliado.")
        slug = item.get("slug")
        if not isinstance(slug, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
            raise ValueError(f"Slug inválido: {slug!r}")
        if slug in slugs:
            raise ValueError(f"Slug duplicado: {slug}")
        slugs.add(slug)
        raw = item.get("url_afiliado") or item.get("affiliate_url")
        url = validate_affiliate_url(raw)
        output.append((slug, url))
    return output


def import_one(slug, url, fixture=None):
    if fixture:
        from scrapling import Selector
        page = Selector(fixture.read_text(encoding="utf-8"), url=url)
        result = parse_page(page, url, slug)
        result["origem"] = "fixture_local"
        return result
    allowed, explanation = robots_permits(url)
    if not allowed:
        return {"slug": slug, "url_afiliado": url, "status": "bloqueado",
                "erro": explanation, "publicar_no_site": False}
    from scrapling.fetchers import Fetcher
    try:
        page = Fetcher.get(url, timeout=25, retries=1, stealthy_headers=False,
                           follow_redirects="safe", headers={
                               "User-Agent": USER_AGENT, "Accept-Language": "pt-BR,pt;q=0.9"})
        if getattr(page, "status", 0) != 200:
            raise RuntimeError(f"HTTP {getattr(page, 'status', 'desconhecido')}")
        final_url = str(getattr(page, "url", url))
        validate_affiliate_url(final_url)
        result = parse_page(page, url, slug)
        result["origem"] = "scrapling_fetcher"
        return result
    except Exception as exc:  # falha de transporte/parser deve afetar apenas este item
        return {"slug": slug, "url_afiliado": url, "status": "inacessivel",
                "erro": f"{type(exc).__name__}: {str(exc)[:180]}", "publicar_no_site": False}


def main(argv=None):
    parser = argparse.ArgumentParser(description="Importação revisável de anúncios Mercado Livre por Scrapling")
    parser.add_argument("--links", type=Path, default=DEFAULT_LINKS, help="Arquivo JSON de links")
    parser.add_argument("--saida", type=Path, default=DEFAULT_OUTPUT, help="JSON de saída para revisão")
    parser.add_argument("--fixture", type=Path, help="HTML local para teste de um único link, sem rede")
    parser.add_argument("--intervalo", type=float, default=3.0, help="Pausa entre anúncios (mínimo 2 s)")
    args = parser.parse_args(argv)
    if not args.fixture and args.intervalo < 2.0:
        parser.error("Use intervalo mínimo de 2 segundos entre requisições.")
    try:
        links = load_links(args.links)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    if args.fixture and len(links) != 1:
        parser.error("--fixture exige um arquivo JSON com apenas um produto.")
    try:
        import scrapling  # noqa: F401  (pré-checagem amigável)
    except ImportError:
        parser.error('Instale a dependência: python -m pip install "scrapling>=0.5,<0.6"')
    results = []
    for index, (slug, url) in enumerate(links):
        if index and not args.fixture:
            time.sleep(args.intervalo)
        result = import_one(slug, url, fixture=args.fixture)
        results.append(result)
        print(f"{slug}: {result['status']}")
    args.saida.parent.mkdir(parents=True, exist_ok=True)
    output = {"gerado_em": datetime.now(timezone.utc).isoformat(timespec="seconds"),
              "ferramenta": "Scrapling", "publicado": False, "quantidade": len(results),
              "produtos": results}
    tmp = args.saida.with_suffix(args.saida.suffix + ".tmp")
    tmp.write_text(json.dumps(output, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    tmp.replace(args.saida)
    print(f"Arquivo para revisão: {args.saida}")
    print("Nenhum item foi automaticamente publicado na Bordô.")
    return 0 if all(r["status"] == "revisar" for r in results) else 2


if __name__ == "__main__":
    sys.exit(main())
