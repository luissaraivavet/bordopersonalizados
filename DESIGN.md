---
name: Bordô
description: "Guia de campo de laços e bordados: capa de tecido bordô, pranchas de papel e fio dourado."
colors:
  wine: "#631f35"
  wine-deep: "#4a1427"
  gold: "#d8b25a"
  gold-bright: "#e6c373"
  gold-ink: "#3a0f1d"
  tab-jardim: "#4f6b3f"
  tab-sinfonia: "#8f5a1c"
  tab-kits: "#2f5f6b"
  tab-presentes: "#5f4f8a"
  paper: "#e7ebe3"
  paper-deep: "#dbe1d5"
  label: "#fbfaf6"
  white: "#fff"
  ink: "#2b1119"
  ink-soft: "#5a3b45"
  ink-wash: "#2b111914"
  scrim: "#2b1119a6"
  cloth-text: "#f7eee6"
  cloth-soft: "#e6ccd2"
  cloth-line: "#f7eee647"
  cloth-edge: "#f7eee699"
  cloth-wash: "#f7eee61f"
  line: "#b9c2b1"
  field: "#6f7a68"
  shadow: "#1a040b"
typography:
  display:
    fontFamily: "Besley, Georgia, 'Times New Roman', serif"
    fontSize: "2.25rem"
    fontWeight: 600
    lineHeight: 0.98
    letterSpacing: "-0.025em"
  headline:
    fontFamily: "Besley, Georgia, 'Times New Roman', serif"
    fontSize: "1.9rem"
    fontWeight: 600
    lineHeight: 1.05
    letterSpacing: "-0.02em"
  title:
    fontFamily: "Besley, Georgia, 'Times New Roman', serif"
    fontSize: "1.5rem"
    fontWeight: 600
    lineHeight: 1.15
    letterSpacing: "-0.01em"
  specimen:
    fontFamily: "Besley, Georgia, 'Times New Roman', serif"
    fontSize: "1.5rem"
    fontWeight: 600
    lineHeight: 1.1
    letterSpacing: "-0.01em"
  body:
    fontFamily: "'Hanken Grotesk', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.6
    fontFeature: "tnum"
  label:
    fontFamily: "'Hanken Grotesk', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: "0.9375rem"
    fontWeight: 650
    lineHeight: 1.2
    fontFeature: "tnum"
rounded:
  xs: "2px"
  sm: "3px"
  tab: "5px"
  full: "50%"
spacing:
  gutter-sm: "20px"
  gutter-md: "32px"
  gutter-lg: "56px"
  section: "clamp(56px, 8vw, 104px)"
components:
  button-primary:
    backgroundColor: "{colors.wine}"
    textColor: "{colors.white}"
    typography: "{typography.label}"
    rounded: "{rounded.sm}"
    padding: "12px 22px"
    height: "48px"
  button-primary-hover:
    backgroundColor: "{colors.wine-deep}"
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.wine}"
    typography: "{typography.label}"
    rounded: "{rounded.sm}"
    padding: "12px 22px"
    height: "48px"
  button-secondary-hover:
    backgroundColor: "{colors.label}"
  button-on-cloth:
    backgroundColor: "{colors.label}"
    textColor: "{colors.wine}"
    typography: "{typography.label}"
    rounded: "{rounded.sm}"
    padding: "12px 22px"
    height: "48px"
  button-on-cloth-hover:
    backgroundColor: "{colors.white}"
  button-gold:
    backgroundColor: "{colors.gold}"
    textColor: "{colors.gold-ink}"
    typography: "{typography.label}"
    rounded: "{rounded.sm}"
    padding: "12px 22px"
    height: "48px"
  button-gold-hover:
    backgroundColor: "{colors.gold-bright}"
  icon-button:
    rounded: "{rounded.sm}"
    size: "48px"
  icon-button-hover:
    backgroundColor: "{colors.ink-wash}"
  chip:
    backgroundColor: "transparent"
    textColor: "{colors.cloth-text}"
    rounded: "{rounded.sm}"
    padding: "10px 16px"
    height: "44px"
  chip-selected:
    backgroundColor: "{colors.label}"
    textColor: "{colors.wine}"
    typography: "{typography.label}"
  input:
    backgroundColor: "{colors.label}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    padding: "12px"
    height: "48px"
  ficha:
    backgroundColor: "{colors.label}"
    textColor: "{colors.ink}"
  product-figure:
    backgroundColor: "{colors.label}"
    padding: "5px"
  rail-tab:
    backgroundColor: "{colors.wine}"
    textColor: "{colors.white}"
    rounded: "{rounded.tab}"
    padding: "14px 0"
    width: "44px"
  rail-tab-jardim:
    backgroundColor: "{colors.tab-jardim}"
  rail-tab-sinfonia:
    backgroundColor: "{colors.tab-sinfonia}"
  rail-tab-kits:
    backgroundColor: "{colors.tab-kits}"
  rail-tab-presentes:
    backgroundColor: "{colors.tab-presentes}"
---

# Design System: Bordô

## Overview

**Creative North Star: "O Guia de Campo"**

Um guia de campo de naturalista do Jardim e das Matas: cada laço é um espécime com nome próprio, linha de espécie e rótulo, e a página se folheia por abas de índice coloridas. Dois materiais e um metal: tecido bordô na capa, papel de prancha verde-acinzentado no catálogo e dourado de estampagem.

A peça chega primeiro; o texto é legenda. Não pode parecer loja grande e fria, nem infantil, nem pesar no celular: o sistema é plano, com duas famílias de fonte locais e um único movimento autoral. A direção foi assumida pelo construtor depois que o proprietário não respondeu à segunda rodada de decisão, em 2026-11-17, e aguarda a confirmação dele.

**Key Characteristics:**
- Capa de tecido bordô com filete dourado; catálogo em pranchas de papel.
- Cada peça é um espécime: nome em itálico, espécie e tipo.
- Dourado cheio só nas ações de pedido sobre o bordô.
- Uma tinta de aba por coleção; plano por padrão.

## Colors

Estratégia comprometida: o bordô ocupa superfícies inteiras, o papel recebe o catálogo e o dourado risca os dois.

### Primary
- **Bordô de Capa** (#631f35): cabeçalho, abertura, encomenda e rodapé; sobre papel, títulos, nomes de espécime e botão de pedido.
- **Bordô Profundo** (#4a1427): hover do botão bordô, menu no celular e aviso.

### Secondary
- **Dourado de Estampagem** (#d8b25a): filete, linhas-guia, alfinetes, sublinhado de links e contador da sacola. Em botão, texto **Tinta do Dourado** (#3a0f1d) e hover **Dourado Claro** (#e6c373).

### Tertiary
- **Tintas de Aba**: Verde-folha (#4f6b3f) no Jardim, Ocre (#8f5a1c) na Sinfonia, Petróleo (#2f5f6b) nos kits, Lilás (#5f4f8a) nos presentes; marcam faixa da prancha, contagem e abas de índice.

### Neutral
- **Papel de Prancha** (#e7ebe3) e **Papel Fundo** (#dbe1d5): fundos do catálogo.
- **Papel de Rótulo** (#fbfaf6): rótulos, molduras, campos, diálogos e etiqueta do logo; branco puro (#fff) só em texto sobre bordô e tintas de aba.
- **Tinta** (#2b1119) e **Tinta Suave** (#5a3b45) sobre papel; **Creme** (#f7eee6) e **Rosa de Tecido** (#e6ccd2) sobre o bordô.
- **Fio de Papel** (#b9c2b1) nas bordas de 1px, **Fio de Campo** (#6f7a68) nos campos, **Sombra de Vinho** (#1a040b) nas sombras.

### Named Rules
**A Regra do Dourado de Pedido.** Botão dourado cheio existe só para pôr na sacola e seguir ao WhatsApp, e só sobre o bordô. Sobre papel, a ação de pedido é bordô.

**A Regra da Tinta de Aba.** Cada coleção tem uma tinta e só ela: prancha, contagem e aba; nunca botões nem títulos.

**A Regra do Logo Intocado.** O logo é fixo, de uma cor, vinho. Sobre o bordô vem numa etiqueta de papel e nunca é recolorido.

## Typography

**Display Font:** Besley (com Georgia, serif)
**Body Font:** Hanken Grotesk (com system-ui, sans-serif)

**Character:** Serifa de prancha gravada com grotesca neutra, ambas variáveis e locais em woff2. O itálico de Besley é a voz do guia: nomes, linhas de apoio, contagens e legendas. Lora e Manrope permanecem apenas para outras páginas.

### Hierarchy
- **Display** (600, 2.25rem, 0.98, -0.025em): título da capa; 3.5rem a partir de 768px e 3.75rem a partir de 1400px (3.5rem entre 1100px e 1399px).
- **Headline** (600, 1.9rem, 1.05, -0.02em): título de seção; 2.5rem a partir de 900px e 3rem a partir de 1300px.
- **Title** (600, 1.5rem, 1.15, -0.01em): títulos de rótulos e blocos.
- **Specimen** (itálico 600, 1.5rem, 1.1, -0.01em): nome próprio da peça; na capa, itálico 500 em 1.9rem, 2.5rem a partir de 900px e 3rem a partir de 1300px, dourado.
- **Body** (400, 1.0625rem, 1.6): texto corrido até 66ch; algarismos tabulares em toda a página.
- **Label** (650, 0.9375rem, 1.2): botões e controles, sem caixa alta.

**A Regra dos Degraus.** Títulos mudam de tamanho em degraus por largura (tokens `--fs-*` no `:root`), nunca por `vw`.

### Named Rules
**A Regra da Linha de Apoio.** Nenhum sobretítulo acima de títulos: a linha secundária vem abaixo, em Besley itálico 500 (1.1875rem, entrelinha 1.35). No rótulo de espécime o nome vem primeiro; espécie, tipo e coleção vêm abaixo dele.

## Layout

Coluna centralizada de min(100% − 2 × margem, 1320px); margem de 20px, 32px a partir de 768px e 56px a partir de 1200px. Seções alternam tecido e papel, com clamp(56px, 8vw, 104px) de respiro vertical. Parte do celular e muda em 768px (três colunas), 900px (seções em duas colunas), 1100px (capa lado a lado) e 1200px (quatro colunas e abas na margem direita).

## Elevation & Depth

Plano. A profundidade vem dos materiais: papel de rótulo sobre papel de prancha, papel sobre tecido. Os diálogos não têm sombra: separam-se por um véu de tinta a 65%.

### Shadow Vocabulary
- **Montagem do espécime** (`box-shadow: 0 22px 40px -24px #1a040b`): foto em destaque da capa.
- **Menu suspenso** (`box-shadow: 0 18px 34px -18px #1a040b`): lista de coleções e menu no celular.
- **Aviso flutuante** (`box-shadow: 0 14px 28px -14px #1a040b`): confirmação de peça adicionada.

### Named Rules
**A Regra do Papel sobre Tecido.** Peças e rótulos levam borda de 1px, nunca sombra; sombra é só para a montagem do espécime e para o que flutua acima da página.

## Shapes

Cantos quase retos: 2px em etiquetas e miniaturas, 3px em botões, botões de ícone, campos, fichas e aviso, 5px no canto livre das abas de índice. O fio é a forma dominante: filete de dois fios dourados de 1px recuados 8px e 12px (16px e 22px a partir de 768px); rótulo com borda de 1px e segundo fio 6px para dentro; linha-guia dourada de 1.5px com alfinete de 8px; faixa de 10px na tinta da coleção abrindo cada prancha. Fotos de peça em 4:5, montadas em papel.

## Components

### Buttons
- **Shape:** cantos de 3px, altura mínima de 48px (12px 22px), borda de 1.5px.
- **Primary:** bordô com texto branco, a ação de pedido sobre papel; hover em bordô profundo. Secundário em contorno bordô.
- **Sobre tecido:** papel de rótulo com texto bordô e, para o pedido, dourado com hover dourado claro.
- **Hover / Focus:** transição de 0.2s só de cor; foco de 3px afastado 3px, bordô sobre papel e dourado sobre tecido.
- **Link de texto:** peso 600, sublinhado dourado de 2px.

### Chips
- **Style:** fichas de escolha sobre o tecido, com contorno de 1px em creme a 60%, cantos de 3px e 44px de altura; a selecionada vira papel de rótulo com texto bordô.

### Cards / Containers
- **Cartão de espécime:** figura em papel de rótulo com 5px de margem e borda de 1px; abaixo, linha-guia dourada de 20px com alfinete de 8px até o rótulo de papel (fio duplo) com nome em itálico bordô, espécie e tipo; depois preço em 700 e botão bordô de largura total. A opção genérica "Acabamento a confirmar no atendimento" não aparece como legenda nem na mensagem.
- **Rótulo de papel:** fio duplo sobre papel de rótulo, para coleções sob consulta, índice de espécies e prévia da mensagem.

### Inputs / Fields
- **Style:** papel de rótulo, borda de 1px em fio de campo, cantos de 3px, altura mínima de 48px; sem estilo de erro definido.

### Navigation
- **Cabeçalho:** tecido bordô com o logo na etiqueta de papel; itens em 600 com sublinhado dourado no hover.
- **Abas de índice:** na tinta de cada coleção, texto branco 650 (0.875rem). Até 1199px formam uma faixa de 44px fixa no topo do catálogo; a partir de 1200px ficam verticais na margem direita, com 44px de largura. A da seção atual ganha um fio de papel de 4px. A última aba é a **Sacola**, em bordô com contador dourado de cantos de 3px: no fim da faixa a partir de 768px e no pé do trilho, com fio dourado de 1px, a partir de 1200px.

### Etiqueta de espécime
Na capa, rótulos se ligam à foto por linhas-guia douradas. Na troca de espécime tudo sai em 0.14s e se refaz no lugar (linha 0.6s, texto 0.45s, foto 0.5s), na curva cubic-bezier(.16, 1, .3, 1). É o único movimento autoral; as abas da margem só deslizam para dentro depois da capa (0.5s) e tudo se desliga sob prefers-reduced-motion.

## Do's and Don'ts

### Do:
- **Faça** a peça chegar antes do discurso: foto montada em papel, nome em itálico, espécie e preço.
- **Faça** cada coleção nova receber uma única tinta de aba, com contraste de 4.5:1 para o texto branco.
- **Faça** alvos de toque de 44px ou mais e foco visível de 3px.

### Don't:
- **Não** faça parecer loja grande e fria: prancha de espécimes com nome, não vitrine de cartões com sombra.
- **Não** faça infantil: paleta de bordô, papel e dourado, cantos entre 2px e 5px.
- **Não** pese no celular: duas famílias de fonte locais, superfícies planas, um único movimento autoral.
- **Não** ponha sobretítulo acima de títulos.
- **Não** use dourado como texto sobre papel.
