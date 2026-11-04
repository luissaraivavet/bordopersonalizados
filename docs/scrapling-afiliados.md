# Importador de produtos afiliados da Bordô

Integração opcional com [Scrapling](https://github.com/D4Vinci/Scrapling), independente do site público e do carrinho. O importador **não publica** automaticamente nada na Bordô.

## Por que não raspar o site do Mercado Livre?

A [cláusula 7.6 do programa de desenvolvedores](https://developers.mercadolivre.com.br/pt_br/termos-e-condicoes) proíbe robôs, spiders e scraping do site/conteúdo. Para proteger a operação de afiliados, este código **não coleta diretamente páginas do Mercado Livre por scraping**, nem tenta transpor CAPTCHA, login, bloqueios ou proteções.

O importador possui dois caminhos legítimos:

1. **API oficial, recomendada:** usa o `Fetcher` do Scrapling como cliente HTTP autorizado com token OAuth para consultar os endpoints de itens e descrições da API Mercado Livre, conforme [documentação de busca de itens](https://developers.mercadolivre.com.br/pt_br/itens-e-buscas).
2. **HTML local autorizado:** usa o `Selector` do Scrapling para extrair dados de um documento HTML obtido com permissão do titular dos direitos; não faz requisições ao site.

## Campos coletados

Quando a fonte os oferece: título, URLs originais, identificadores MLB de catálogo e anúncio, preço e preço anterior, moeda, condição, status, características, marca, modelo, SKU, categoria, descrição, fotografias, variações, disponibilidade informada, dados de envio não personalizados, número de unidades indicado pela API e identificação do vendedor.

**O JSON local também preserva a resposta bruta autorizada da API** em `dados_brutos_api`, permitindo revisar outros campos sem perder informação. Os campos incompletos permanecem vazios; o sistema não estima preço, frete, CEP, parcelamento, reputação, dados de clientes ou comissão.

Itens de terceiros podem exigir permissões específicas. Nem todo endpoint está disponível em todas as contas e produtos. Disponibilidade e preço podem mudar imediatamente após a consulta.

## Instalação Windows

Abra o terminal na pasta do repositório da Bordô:

```powershell
py -m pip install -r scripts/requirements-scrapling.txt
```

Configure um **token OAuth válido** do Mercado Livre em variável de ambiente no seu computador, conforme o fluxo oficial do programa de desenvolvedores. Por exemplo, em uma sessão do PowerShell:

```powershell
$env:MELI_ACCESS_TOKEN = "COLE_AQUI_O_TOKEN_APENAS_NO_SEU_COMPUTADOR"
py scripts/importar_afiliados.py
```

Não publique o token no GitHub, no HTML, nos screenshots ou no chat. O script não obtém nem renova tokens automaticamente.

## Como adicionar vários anúncios

O arquivo `content/afiliados-links.json` contém o link original da árvore de Natal informado pelo proprietário. Inclua novos objetos na lista:

```json
{
  "links": [
    {
      "slug": "arvore-de-natal-210-600-galhos",
      "url_afiliado": "https://www.mercadolivre.com.br/p/MLB54646018?matt_tool=38524122&pdp_filters=item_id:MLB4263473855"
    },
    {
      "slug": "outro-produto",
      "url_afiliado": "https://produto.mercadolivre.com.br/MLB-1234567890-exemplo-_JM"
    }
  ]
}
```

Exemplos de links acima são simplificados: no arquivo de produção, **preserve a URL completa fornecida pelo programa de afiliados**, incluindo parâmetros de atribuição. O exemplo `MLB-1234567890` é fictício e deve ser substituído.

O importador extrai `MLB4263473855` do filtro do link da árvore e consulta esse identificador pela API. Em URLs de catálogo sem item específico, será necessário um link que identifique o anúncio, não só a ficha do produto.

## Saída

A execução cria o arquivo local:

```text
.bordo-scraping/resultados.json
```

Ele contém `produtos[]` com valores, imagens, características e `dados_brutos_api`. A pasta é ignorada pelo Git, para evitar publicar conteúdo externo ou dados de conta por engano.

Todos os produtos permanecem com `revisado: false` e `publicar_no_site: false`. O blog, a loja e o carrinho continuam intactos.

Estados possíveis:
- `revisar`: API retornou informações para conferência editorial.
- `sem_credenciais`: token OAuth não configurado.
- `sem_id_anuncio`: URL não identifica um anúncio MLB consultável.
- `inacessivel`: API negou acesso ou retornou erro.
- `bloqueado`: reservado para respostas HTML que exigem verificação de acesso.

## Teste offline do Scrapling

Com a dependência instalada, utilize a página de teste sintética incluída no repositório:

```powershell
py scripts/importar_afiliados.py --fixture tests/fixtures/anuncio_afiliado_exemplo.html
py -m unittest tests.test_importar_afiliados
```

A fixture é **sintética**. Ela não representa dados reais da árvore de Natal.

## Transformar dados em conteúdo para o blog

1. Validar o anúncio e os parâmetros do link de afiliado com o painel do programa.
2. Comparar título, modelo, imagens, características e acessórios com a ficha autorizada.
3. Verificar se os direitos de uso permitem exibir imagens ou textos do anunciante.
4. Redigir textos próprios que resolvam dúvidas reais dos compradores, não reproduzir descrições inteiras.
5. Identificar claramente publicidade, não divulgar preço ou estoque sem atualização confiável.
6. Publicar somente depois de revisão humana e das verificações das regras de aquisição por SEO.

## Estado desta implementação

O código e a entrada inicial estão no PR de revisão da Bordô. **Não foi realizada extração real da API neste ambiente**, porque não há token OAuth autorizado nem acesso de rede para executar o Scrapling. Não é possível afirmar que o anúncio de terceiros retornará todos os campos até autenticar e testar a API em um ambiente autorizado.
