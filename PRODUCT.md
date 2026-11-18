# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Dois públicos com o mesmo peso (confirmado pelo proprietário em 2026-11-17):

- Quem quer um laço infantil bordado pronto para escolher: mães e familiares de meninas, que escolhem um desenho do catálogo e fecham o pedido pelo WhatsApp.
- Quem quer um presente ou bordado personalizado sob encomenda: batizado, maternidade, lembranças, empresas e marcas. Essa pessoa chega com uma ideia (um nome, uma data, um desenho) e precisa de um caminho para conversar.

As visitas chegam por vários canais, sem um dominante: Instagram, WhatsApp, Google e indicação (confirmado pelo proprietário em 2026-11-18).

## Product Purpose

A Bordô faz laços infantis e bordados personalizados por encomenda, em Teixeiras, MG, com atendimento online. O site apresenta as coleções, permite montar uma sacola ou descrever uma ideia e leva a conversa para o WhatsApp, onde disponibilidade, materiais, prazo, frete e pagamento são combinados. Sucesso é a visitante chegar ao WhatsApp com o pedido ou a ideia já descritos.

## Positioning

Cada peça parte de um desenho com significado: uma flor, um bichinho músico, um nome. A marca tem um rosto, Priscila, e a conversa faz parte de cada pedido. O nome vem de "bordou", que no jeito mineiro de falar vira "bordô", e bordô também é a cor da marca.

## Operating Context

- Não há backend nem cobrança no site. A sacola (`bordo_cart_v2`, no navegador) e o formulário de personalizados terminam em um link `wa.me` com a mensagem pronta.
- O conteúdo é editado pela Priscila em um painel local (`admin/`, `admin_server.py`) e publicado no GitHub Pages em `bordopersonalizados.com.br`.
- Instagram: `@bordobordadospersonalizados`.

## Capabilities and Constraints

- Site estático, sem frameworks: `index.html` com CSS embutido, `assets/tokens.css`, `assets/base.css` e `assets/site.js`. Preservar. O sistema visual em vigor está em `design.md`.
- Catálogo publicado (2026-11-18): Mãe & Rainha (3 laços a R$ 49,90), Colinho do Céu (12 naninhas a R$ 59,90), Jardim de Encantos (5 laços) e Sinfonia das Matas (34 laços) a R$ 49,90 cada; 2 kits de 3 laços a R$ 119,90; Bastidor Afetivo Floral (R$ 145). A Toalha Lavabo Monograma está oculta no painel até existir uma foto real da peça.
- Desconto de 5% no Pix sobre as peças; embalagem kraft para presente opcional por R$ 15 por pedido. Mudanças em contatos e condições comerciais exigem confirmação do proprietário.
- `assets/site.js` localiza elementos por seletores estruturais; reorganizar o HTML exige ajustar o script junto.
- Imagens são arquivos locais em `assets/`. Uma peça só fica à venda com foto real dela.
- Não exibir avisos de "imagem ilustrativa" (pedido do proprietário).

## Brand Commitments

- Nome Bordô e logo atual (`assets/brand-logo.png`): fixos.
- Bordô continua sendo a cor principal da marca (confirmado em 2026-11-17).
- Cores de apoio e fontes não são compromisso de marca; as atuais estão em `design.md`.
- Português do Brasil em todo texto voltado ao público.
- Não enfatizar exclusividade do linho; os laços usam diferentes tecidos.
- O resultado não deve parecer loja grande e fria, nem infantil demais, nem ficar carregado ou lento no celular (confirmado em 2026-11-17).

## Evidence on Hand

- Fotos de produto: `assets/jardim-*.webp|jpg`, `assets/sinfonia-*.webp`, `assets/bow-*.webp`, `assets/naninha-*.webp`, `assets/mae-rainha-lacos.webp`, `assets/colinho-do-ceu.webp`.
- Vídeo da coleção Sinfonia das Matas: `assets/sinfonia-reel.mp4`, com pôster `assets/sinfonia-poster.webp`.
- Retratos da idealizadora: `assets/priscila-presentes.png`, `assets/priscila-sinfonia.png`, `assets/priscila-bordo.jpg`, `assets/priscila-retrato.jpg`.
- História da marca em `content/site.json` (`settings.story`).
- Não há depoimentos nem artigos publicados. Não inventar depoimentos, preços, prazos ou propriedades das peças.

## Product Principles

1. A conversa é o fechamento: toda escolha no site prepara a mensagem que segue para o WhatsApp.
2. Laço pronto e bordado sob encomenda têm o mesmo peso; nenhum dos dois caminhos fica escondido.
3. O desenho bordado é o que se vende: as peças aparecem antes de qualquer discurso.
4. Marca de ateliê com rosto e lugar: Priscila, Teixeiras, MG.
5. Só o que é verdade: detalhes da peça são confirmados no atendimento, nunca prometidos pela página.

## Accessibility & Inclusion

Navegação completa por teclado, foco visível, contraste de texto de pelo menos 4,5:1, alvos de toque de 44 px ou mais e respeito a `prefers-reduced-motion`, como já verificado na versão atual.
