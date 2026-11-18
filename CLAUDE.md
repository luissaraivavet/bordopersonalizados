# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

As regras de estilo, marca, segurança, commits e PRs estão em AGENTS.md e valem aqui:

@AGENTS.md

Este arquivo acrescenta apenas o que AGENTS.md e README.md não cobrem: comandos pontuais e a arquitetura que exige ler vários arquivos para entender.

## Comandos

Python 3.10+ sem dependências; não há etapa de build, npm ou linter.

```bash
python build.py                                   # valida index.html, assets obrigatórios e conteúdo
python build.py --serve --port=8080               # prévia estática em 127.0.0.1
python admin_server.py --no-browser               # painel; imprime a URL de entrada de uso único
python -m unittest discover -s tests -v           # todos os testes
python -m unittest discover -s tests -k test_kit_members_and_visibility -v   # um único teste
node --check assets/site.js && node --check admin/admin.js
```

Para um único teste use `discover -k`. A forma `python -m unittest tests.test_admin.Classe.teste` falha com `ModuleNotFoundError` porque `tests/` não é um pacote.

Regenerar `assets/content.js` depois de editar `content/site.json` à mão (valida e grava os dois arquivos):

```bash
python -c "import json, admin_server as a; a.apply_content(json.loads(a.CONTENT.read_text(encoding='utf-8')))"
```

## Fluxo do conteúdo

```
.bordo-admin/draft.json  ->  validate()  ->  public_content()  ->  content/site.json
   (privado, completo)                         (filtra ocultos)     assets/content.js  ->  assets/site.js  ->  index.html
```

- `admin_server.validate` é o único esquema do conteúdo (`schemaVersion: 1`). `build.py`, os testes, os scripts e o painel importam essa mesma função.
- `content/site.json` guarda somente itens publicados. Itens ocultos existem apenas no rascunho local (`.bordo-admin/draft.json`, fora do Git). Não trate `site.json` como fonte completa do catálogo.
- `assets/content.js` é o mesmo JSON com o prefixo `window.BORDO_CONTENT = ` e `;` no final. `build.py` falha se os dois divergirem.
- `public_content` remove em cascata: item oculto, produto de coleção oculta, kit com algum membro oculto.
- Acrescentar um campo de conteúdo exige mexer em três lugares: `validate` (`admin_server.py`), `schemas` (`admin/admin.js`) e a renderização (`assets/site.js`).

Regras de `validate` que costumam surpreender:

- Identificadores são únicos entre todos os grupos e não podem repetir as âncoras reservadas de `index.html` (`conteudo`, `colecoes`, `historia`, `faq`, `personalizados`).
- Imagens precisam ser caminhos locais em `assets/` e existir no disco; URLs externas são rejeitadas. Links exigem `https`.
- `price: null` significa "sob consulta": o produto perde o botão de sacola e vira link para o formulário.
- Um kit (`bundle`) tem exatamente três produtos distintos que não são kits.
- Deve existir pelo menos uma coleção publicada e em destaque.

## Página principal

`index.html` traz o CSS da página inline e importa `assets/tokens.css` (cores, fontes e escalas) e `assets/base.css` (regras-base); `design.md` descreve o sistema visual compartilhado com as páginas de SEO. O HTML traz apenas os contêineres; `assets/site.js` preenche o catálogo, os textos de `settings`, os links de WhatsApp/Instagram e o rodapé.

- `site.js` localiza elementos por seletor estrutural (`.footer-main>div:last-child a`, `.intro>.button`, `.story-copy`, `#catalogSections`, `.collection-grid`). Reorganizar o HTML quebra a renderização sem erro de build; confira no navegador.
- O `id` de cada coleção vira âncora e classe CSS da seção (`.section.jardim`). A coleção `sinfonia` recebe o vídeo de `#filmTemplate`.
- "Mãe & Rainha" e "Colinho do Céu" não estão no JSON: são seções fixas em `index.html` com links fixos no menu em `renderProducts` (`site.js`).
- Os scripts são carregados com `?v=...` em `index.html`. O painel não altera esse valor; ao mudar `site.js` ou a estrutura do conteúdo, atualize o parâmetro para invalidar o cache.
- A sacola (`bordo_cart_v2`) é reconciliada com o catálogo em `loadCart`: preço, título e imagem vêm sempre do produto atual, nunca do `localStorage`. O desconto Pix é calculado em centavos e incide só sobre as peças, não sobre a embalagem. O pedido termina em um link `wa.me`; não há backend.

## Painel privado

`admin_server.py` é um `ThreadingHTTPServer` em `127.0.0.1`, com a interface em `admin/`.

- Entrada por `/entrar?key=` de uso único, que troca a chave por um cookie de sessão. Toda requisição confere o cabeçalho `Host`; todo POST confere `Origin` e `X-CSRF-Token`.
- Salvar e publicar enviam a `revision` (SHA-256 do rascunho); se o rascunho mudou em outra janela, a resposta é 409.
- Arquivos estáticos seguem uma lista de permissão: `index.html`, `assets/` e `admin/`.
- `/preview/` no painel serve o `index.html` da raiz com o `content.js` gerado do rascunho.
- `publish()` faz commit e `git push origin main` direto, o que publica no GitHub Pages. Só roda na branch `main`, com o remoto `luissaraivavet/bordopersonalizados`, sem outras alterações na árvore e com `HEAD` igual a `origin/main`. Os testes bloqueiam isso com `patch` em `status`; mantenha esse bloqueio em qualquer teste novo.

## Páginas fora do fluxo do painel

- `lacos-infantis-bordados/`, `bordados-personalizados/` e `presentes-personalizados/` são páginas de descoberta para SEO, autocontidas, com CSS próprio e listadas em `sitemap.xml`. Repetem à mão o número do WhatsApp e os textos da marca: uma mudança de contato em `settings` ou de estilo compartilhado precisa ser replicada nelas e no JSON-LD de `index.html`.
- `blog/` é o blog "Casa & Inspiração", indexável e listado em `sitemap.xml`, com guias de Natal e links de afiliado do Mercado Livre marcados com `rel="sponsored nofollow"` e aviso de comissão. Os guias de Natal são HTMLs estáticos escritos à mão, com CSS próprio. As listas de presentes e enfeites (`blog/presentes-*/`, `blog/enfeites-*/`) são geradas por `python scripts/gerar_listas_blog.py` a partir de `scripts/dados_listas_blog.json`; edite o script ou os dados e gere de novo, não o HTML. As fotos em `blog/assets/listas/` foram geradas no Google Flow; os itens acrescentados depois usam a foto do anúncio (campo `img`). Por decisão do proprietário, as listas não exibem aviso sobre a origem das imagens. Links novos de afiliado saem do gerador do Mercado Livre (`/afiliados/linkbuilder`), com a etiqueta `bordopersonalizados`. O diretório `preview/` do repositório guarda só redirecionamentos para `/blog/` e é outra coisa que o `/preview/` do painel, que mostra o rascunho do site.
- `build.py` valida somente o `index.html` da raiz, uma lista fixa de assets (`required` em `check_assets`) e a equivalência do conteúdo. Ao renomear ou remover um asset dessa lista, atualize-a. As páginas de SEO e o blog não são verificados.

## Testes e scripts

- `ValidationTests.test_original_catalog` fixa fatos do catálogo real: 39 laços a R$ 49,90 em `jardim` e `sinfonia`, 2 kits a R$ 119,90, `Teixeiras, MG` e nenhuma opção com "faix". Uma mudança legítima de catálogo ou preço exige atualizar esse teste junto.
- `PrivateServerTests` copia `assets/`, `admin/`, `content/` e `index.html` para um diretório temporário e redireciona `ROOT`, `STATE` e `CONTENT` com `patch`. Depende de `assets/priscila-bordo.jpg` e `assets/brand-logo.png`.
- `scripts/` contém migrações pontuais já aplicadas (preços de outubro de 2026, história da marca). Elas gravam `site.json`, `content.js` e o rascunho local; `update_bow_catalog.py` ainda exige Pillow e fotos em `~/Downloads`. Não fazem parte da validação.

<!-- imported-from: codex:project:instructions -->
<!-- O conteúdo de AGENTS.md entra pela linha @AGENTS.md no topo; o marcador acima evita que /import o anexe de novo. -->
