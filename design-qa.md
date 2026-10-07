# Design QA

final result: passed

## Referência e Evidências

Direção escolhida: galeria editorial, proposta 02. Comparação conjunta em `work/design-comparison-final.jpg`, com referência e implementação normalizadas para 1440 x 1100, sem moldura de navegador. Captura da implementação: `work/site-1440.jpg`. O relatório acompanha o pacote local em `outputs/`; caminhos de evidência são relativos ao workspace de produção.

## Iterações

Na primeira comparação, a proporção do logo e a quebra do título deslocavam a galeria (P2). O enquadramento da faixa personalizada mostrava a peça inteira em vez do detalhe (P2). Ajustados dimensões do logo, título, espaçamento, recorte CSS e enquadramento da faixa. A comparação posterior confirma título em uma linha, galeria ampla e detalhe do bordado na faixa. Não restam diferenças P0, P1 ou P2 identificadas.

## Superfícies Obrigatórias

- Tipografia: Lora e Manrope originais da marca, carregadas localmente. Pesos, hierarquia, legibilidade e quebras conferidos. A fonte real substitui a aproximação tipográfica da imagem conceitual.
- Espaçamento: masthead central, duas coleções sem cartões decorativos, grids e faixas abertas. Pequenas diferenças de altura são aceitáveis para acomodar navegação funcional e rótulos.
- Cores: bordô, branco, sálvia e detalhes dourados; sem gradientes decorativos. Estados de foco visíveis e contraste dos comandos conferidos.
- Imagens: logo original e assets raster; galeria Jardim gerada como imagem ilustrativa. Diferenças de fundo e escala da composição são esperadas pela reutilização dos modelos aprovados. Sem substituição por desenhos SVG.
- Conteúdo: Teixeiras, MG, tecidos variados, sem depoimentos inventados nem alegações médicas. Textos e condições comerciais conferidos.

## Verificação Funcional

Sem transbordamento horizontal em 320, 390, 768, 1440 e 1920 px. Menu móvel, ampliação, formulário, sacola, quantidades, remoção, recarga, Pix e embalagem testados. Nenhum pedido enviado. Preço alterado pelo painel refletiu na prévia e foi restaurado ao original.

Painel com edição, biblioteca, rascunho e exportação; dez testes automatizados passaram. Validador do projeto e sintaxe JavaScript passaram. Publicação real permanece pendente de autorização; teste de publicação usa bloqueio da branch e não envia commits ao main.

## Checklist

- [x] Referência e implementação abertas em comparação conjunta.
- [x] Cinco superfícies de fidelidade verificadas.
- [x] Correções recapturadas e comparadas.
- [x] Computador e celular conferidos.
- [x] Fluxos e proteção local verificados.
