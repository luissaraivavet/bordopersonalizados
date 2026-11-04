# Importador de anúncios afiliados | Bordô

Integração opcional com [Scrapling](https://github.com/D4Vinci/Scrapling), separada do site público. **Não é um plugin de checkout, nem publica produtos automaticamente.**

O importador lê URLs previamente escolhidas pelo proprietário, consulta `robots.txt` e tenta extrair os campos públicos de cada anúncio para análise editorial e curadoria.

## O que é coletado

- Identificadores MLB de catálogo e anúncio, URL afiliada **sem alterar parâmetros**, título e categoria, marca, modelo, SKU/GTIN/MPN, cor e tamanho, quando existentes.
- Preço apresentado no código estruturado ou HTML, moeda, eventual preço anterior, disponibilidade e condição.
- Vendedor indicado, avaliação agregada, quantidade de avaliações e texto de parcelas visível.
- Fotografias do **produto** vinculadas ao catálogo/anúncio, descrição pública, tabela de características e variantes disponíveis no HTML.
- Data e fonte de captura, advertências e estado de revisão.
- Opcionalmente, uma cópia do HTML recebido (`--guardar-html`), limitada a 6 MB e guardada **somente no computador**, não no GitHub.

**Não se garante a coleta integral de todas as informações**: preços por usuário, frete, entrega, CEP, estoque atualizado, variações carregadas sob demanda, perguntas, todas as avaliações ou conteúdo acessível apenas por autenticação podem ficar indisponíveis.

Imagens/textos de terceiros não devem ser automaticamente republicados no blog. A Bordô transforma as informações verificadas em guias editoriais originais e sempre identifica links comerciais.

## Instalação no Windows

No terminal, na pasta do repositório da Bordô:

```powershell
py -m pip install -r scripts/requirements-scrapling.txt
py scripts/importar_afiliados.py --guardar-html
```

No Linux/macOS:

```bash
python3 -m pip install -r scripts/requirements-scrapling.txt
python3 scripts/importar_afiliados.py --guardar-html
```

Por padrão, o arquivo de entrada é `content/afiliados-links.json`, com o link da árvore já fornecido pelo proprietário. Para adicionar outros anúncios, acrescente entradas:

```json
{
  "links": [
    {
      "slug": "arvore-de-natal-210-600-galhos",
      "url_afiliado": "https://www.mercadolivre.com.br/p/MLB54646018?...seus-parametros-de-afiliado..."
    },
    {
      "slug": "outro-produto",
      "url_afiliado": "https://produto.mercadolivre.com.br/MLB-1234567890-anuncio-_JM"
    }
  ]
}
```

**O exemplo acima tem endereço ilustrativo para a segunda entrada.** Cole somente links gerados e validados pela sua conta de afiliado. Não substitua o link pelo endereço canônico na vitrine: os parâmetros de atribuição podem estar na URL completa.

O comando grava `.bordo-scraping/resultados.json` e `.bordo-scraping/html/`, ambos ignorados pelo Git. Os campos `revisado` e `publicar_no_site` começam sempre como `false`. O importador **não** altera `content/site.json` nem o carrinho.

Para ler uma única página de teste previamente salva, sem realizar chamadas à internet:

```powershell
py scripts/importar_afiliados.py --links content/afiliados-links.json --fixture tests/fixtures/anuncio_afiliado_exemplo.html
```

A fixture é sintética, não é um dado verdadeiro do Mercado Livre.

## Estados do resultado

| Estado | Significado | Ação |
| --- | --- | --- |
| `revisar` | Há título e alguns campos recuperados | Conferir tudo no anúncio oficial |
| `inacessivel` | Falha HTTP, erro de acesso, conteúdo sem título | Não publicar; buscar fonte autorizada |
| `bloqueado` | `robots.txt` não autoriza ou a página exige verificação | Não contornar CAPTCHA/bloqueio |

O importador respeita `robots.txt`, recusa domínios não permitidos, mantém pausa mínima de dois segundos, faz apenas uma tentativa por anúncio e não usa rotação de proxies nem mecanismos de evasão. Se o Mercado Livre negar acesso, encerre a tentativa e obtenha dados por integrações autorizadas, exportação do vendedor ou cadastramento manual.

## Checklist editorial após a coleta

1. Confirmar que URL e identificador MLB correspondem exatamente ao produto escolhido.
2. Conferir foto, nome, descrição, materiais, dimensões, acessórios incluídos e variantes.
3. Conferir preço, frete e prazo no anúncio real, sem apresentar o dado histórico como oferta atual.
4. Confirmar direitos de uso de fotos e descrições antes de publicar.
5. Gerar a **descrição original da Bordô** como orientação de compra, não copiar textos integrais do anúncio.
6. Verificar a atribuição de comissões e as regras do programa.
7. Só então aprovar a publicação manual no site.

## Limitações desta entrega

O script está implementado e documentado no repositório. **Não houve extração real bem-sucedida do anúncio neste ambiente**: o runtime disponível não possui Scrapling instalado nem acesso de rede ao Mercado Livre, que também pode bloquear consultas automatizadas. Os testes de parsing precisam ser executados após a instalação local da dependência; os testes unitários comuns verificam o restante sem baixar conteúdo externo.

O código suporta múltiplos links, mas apenas **um** link real foi fornecido nesta conversa. Nenhum cadastro de produto adicional foi inventado.
