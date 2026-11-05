# SEO do blog Bordô | Casa & Inspiração

Plano técnico e editorial da versão de revisão, atualizado em 4 de novembro de 2026.

## De onde vêm as recomendações

- [OpenSEO](https://github.com/every-app/open-seo): auditoria por famílias de página, agrupamento de palavras-chave por intenção, comparação das páginas concorrentes e prioridade de mudanças fundamentadas por dados.
- [SEO Skill](https://github.com/iannuttall/seo): Google Search Console como fonte de cliques, impressões e posições reais; auditoria de indexação e links internos; distinção entre ausência de observações, ausência de tráfego e falhas de rastreamento.
- Diretrizes práticas do Google Search Central: [conteúdo útil](https://developers.google.com/search/docs/fundamentals/creating-helpful-content), [dados estruturados](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data) e [links qualificados para publicidade](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links).

O repositório Bordô continua sendo um site estático. Não é preciso incorporar o código de nenhuma das duas ferramentas ao frontend.

## Situação atual

- Site principal acessível publicamente, blog desenvolvido em branch de revisão `codex/blog-natal-editorial-20261104`.
- **Não existe baseline de Search Console verificada nesta implementação.** Nenhum volume de palavras-chave, posição, CTR, conversão ou receita foi inventado.
- A prévia remota não equivale ao ambiente publicado. Nenhuma indicação de indexação foi verificada no Google.
- A URL do link comercial foi informada pelo proprietário e deve ser validada no programa de afiliados antes do lançamento.
- O Mercado Livre publica orientações potencialmente divergentes sobre SEO orgânico em sites de afiliados. Confirmar o enquadramento da estratégia diretamente com o programa.

## Intenção de busca por página

| URL | Pergunta principal do leitor | Próximo passo útil |
| --- | --- | --- |
| /blog/ | Como começar a decorar a casa para o Natal? | Escolher um guia ou montar checklist |
| /blog/arvore-de-natal-elegante-gastando-pouco/ | Como decorar gastando pouco e sem compras desnecessárias? | Reaproveitar itens e comparar árvore |
| /blog/arvore-de-natal-180-ou-210/ | Qual altura de árvore comprar? | Medir teto/diâmetro e consultar o produto |
| /blog/quantos-metros-de-pisca-pisca/ | Como estimar a metragem da iluminação? | Calcular com base no formato da árvore |
| /blog/decoracao-de-natal-crista/ | Como destacar o presépio na decoração? | Planejar localização, cor e segurança |
| /blog/como-selecionamos/ | Posso confiar nas recomendações? | Entender critérios e anúncios comerciais |

Esses são **agrupamentos de intenção editorial**, não dados de volume medidos. Revisar títulos e prioridades após coletar consultas reais, sem reescrever páginas que já estejam bem posicionadas.

## Implantação e validação

1. Antes de publicar: testar HTML e sitemap, metadados, schema JSON-LD, links internos e URL do afiliado. Conferir visual e responsividade em navegadores reais.
2. Confirmar autorização do canal de divulgação com o Mercado Livre.
3. Integrar a branch em `main` somente após aprovação. Esperar a conclusão do deploy do GitHub Pages e testar respostas HTTP 200 das seis páginas; não confundir push/merge com deploy concluído.
4. No [Google Search Console](https://search.google.com/search-console), confirmar a propriedade `https://bordopersonalizados.com.br/`, enviar `https://bordopersonalizados.com.br/sitemap.xml` e inspecionar as páginas principais.
5. **Documentar antes de mudar:** data de publicação, status de indexação, consultas e páginas, cliques, impressões, CTR e posição média.
6. Revisar desempenho após existir uma janela suficiente de dados, sem supor que ausências no GSC significam posição zero. Priorizar páginas com impressões relevantes e CTR abaixo do esperado **para o tipo de consulta**, sempre verificando o título exibido pelo Google.

## Medição operacional

| Indicador | Fonte | Unidade | Observação |
| --- | --- | --- | --- |
| Impressões por consulta/página | Google Search Console | impressões | Data e filtro de país/dispositivo importam |
| Cliques orgânicos por página | Google Search Console | cliques | Diferente de sessões do Analytics |
| CTR orgânica | Google Search Console | cliques / impressões | Não somar percentuais entre páginas |
| Posição média | Google Search Console | posição média | Não é o ranking de uma consulta individual |
| Indexação de uma URL | Inspeção de URL | status | Verificar ao vivo, não deduzir do sitemap |
| Cliques nos links de afiliado | Painel do programa e/ou medição própria | cliques | Não são automaticamente vendas |
| Vendas e comissão elegíveis | Painel do programa | pedidos / R$ | Regras de validação de vendas se aplicam |
| Tempo de carregamento | Lighthouse / dados CrUX quando disponíveis | LCP, INP, CLS | Validar desktop e celular |

## Ferramentas, opcionais

### SEO Skill

O projeto [iannuttall/seo](https://github.com/iannuttall/seo) publica o pacote `seo` e uma conexão OAuth com Search Console:

```bash
npm i -g seo
seo start
seo report --site https://bordopersonalizados.com.br/
seo page https://bordopersonalizados.com.br/blog/
seo internal-links
```

Os comandos exigem ambiente Node.js e, para dados privados do Google, autenticação autorizada pelo proprietário. Conferir opções na documentação da versão instalada. Não inserir tokens ou senhas no repositório. Esses comandos **não foram executados nesta entrega**.

### OpenSEO

O [OpenSEO](https://github.com/every-app/open-seo) pode auxiliar a pesquisar demanda e concorrência e analisar questões de rastreamento, porém é uma plataforma separada. Algumas análises requerem conta, integração e créditos. Não há integração ativa atestada nesta revisão.

## Revisão editorial recorrente

- Uma consulta de busca por página: dê a resposta primeiro e detalhe o raciocínio depois.
- Manter critérios, limites de indicação, fontes e links comerciais visíveis.
- Usar texto-âncora descritivo para links internos. Cada página deve ligar a pelo menos uma irmã e à página do blog.
- Não usar datas de atualização fictícias nem produtos/preços inventados; revisar no anúncio original.
- Evitar páginas programáticas quase idênticas, excesso de palavras-chave e marcações de schema que não correspondam a conteúdo visível.
- Criar próximos artigos somente após observar consultas reais, dúvidas de clientes ou lacunas editoriais verificáveis.
