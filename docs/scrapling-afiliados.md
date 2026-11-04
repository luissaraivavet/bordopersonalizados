# Bordô · Importador de produtos do Mercado Livre com Scrapling

**Não exige API para começar.** O importador aceita links de afiliado e tenta consultar a ficha pública do anúncio com Scrapling, sem login, quando permitido e tecnicamente acessível. Preserva a URL de afiliado original, faz apenas uma tentativa e não contorna bloqueios.

O Mercado Livre pode impedir consultas automatizadas, e suas condições de uso podem restringir scraping mesmo de dados públicos. Por isso, o modo público verifica robots.txt e retorna `bloqueado` se não houver acesso permitido. Não há promessa de raspagem invisível nem de coleta completa.

## Comando rápido, sem API

Na pasta do repositório:

```powershell
py -m pip install -r scripts/requirements-scrapling.txt
py scripts/importar_afiliados.py --modo publico
```

O primeiro link da árvore de Natal já está cadastrado em `content/afiliados-links.json`. O resultado é salvo em `.bordo-scraping/resultados.json`, pasta ignorada pelo Git.

## Dados extraídos, quando disponíveis

Título, marca, modelo, preço e moeda, preço anterior, identificadores MLB, condição, status, imagens do produto, descrição, características, variações, vendedor, avaliações e metadados do anúncio. Se a fonte não apresentar um dado verificável, ele permanece vazio, sem valores inventados. Preço e estoque são temporários, e frete e entrega dependem da localidade do comprador.

**Não copie automaticamente textos e fotografias de terceiros para publicar.** Use os dados como fonte de pesquisa para uma descrição editorial original e confirme direitos de uso de imagens.

## Se o Mercado Livre bloquear

Não há mecanismo infalível de scraping. Para não depender somente de acesso direto ao HTML, preparei uma ficha de produto com informações encontradas em uma consulta pública:

`content/afiliados-rascunho-arvore.json`

Esse rascunho contém as medidas, características e a URL de afiliado fornecida originalmente; não inventa preços nem fotos, e está marcado como **não aprovado para publicação**. Ele não deve ser confundido com extração ao vivo pelo Scrapling.

## Adicionar outros links

Edite `content/afiliados-links.json` e acrescente um objeto para cada URL válida:

```json
{
  "links": [
    {
      "slug": "arvore-de-natal-210-600-galhos",
      "url_afiliado": "https://www.mercadolivre.com.br/p/MLB54646018?matt_tool=38524122&pdp_filters=item_id:MLB4263473855"
    }
  ]
}
```

O exemplo é abreviado. **Não encurte nem modifique os links reais de afiliado no arquivo.** O código preserva os parâmetros completos.

## Outros modos, opcionais

Se você obtiver um token OAuth válido no futuro, poderá usar a API oficial:

```powershell
$env:MELI_ACCESS_TOKEN = "TOKEN_APENAS_NO_SEU_COMPUTADOR"
py scripts/importar_afiliados.py --modo api
```

Também é possível processar uma página HTML local obtida por meios autorizados, sem acessar a internet:

```powershell
py scripts/importar_afiliados.py --fixture tests/fixtures/anuncio_afiliado_exemplo.html
```

A página de exemplo é **sintética**, não corresponde ao anúncio real.

## Segurança e aprovação

- Nenhum token, cookie ou informação privada deve ser armazenado no repositório.
- O código não altera o catálogo de bordados nem o carrinho.
- Todos os registros começam com `revisado: false` e `publicar_no_site: false`.
- Cada informação comercial precisa ser conferida antes de aparecer em uma página pública.
- A regra contratual do Mercado Livre para coleta automatizada precisa ser respeitada.

## Estado

O modo sem API foi implementado na branch de revisão e os testes automatizados estão configurados no GitHub Actions. A extração direta por um serviço de scraping foi tentada nesta conversa, mas não conseguiu acessar o anúncio. A ficha pública disponível é um **rascunho de pesquisa**, não uma importação completa e em tempo real.
