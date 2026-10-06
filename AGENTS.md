# AGENTS.md — Diretrizes para Agentes de IA & Engenheiros

Este arquivo estabelece os padrões técnicos, regras de negócio e diretrizes de design para assistentes de inteligência artificial (Claude, ChatGPT, Cursor, Copilot, Windsurf, Lovable, v0, Gemini) que forem editar ou estender o projeto **Bordô | Bordados Personalizados**.

---

## 1. Contexto do Negócio & Marca

- **Nome da Marca:** Bordô | Bordados Personalizados
- **Nicho:** Ateliê de bordados artesanais de alto padrão, laços infantis em linho puro, enxovais personalizados e presentes corporativos.
- **Público-alvo:** Mães exigentes classe A/B que priorizam conforto infantil (peças que não pinicam, não arrancam fios e não apertam a cabeça do bebê), famílias presenteando batizados/nascimento e empresas buscando elegância em uniformes e brindes nobres.
- **WhatsApp Oficial:** `+55 (31) 99795-4792` (`5531997954792`)
- **Instagram:** `@bordobordadospersonalizados` (URL: `https://www.instagram.com/bordobordadospersonalizados/`)
- **Domínio de Produção:** `https://bordopersonalizados.com.br` (GitHub Pages com CNAME ativo).

---

## 2. Princípios de Engenharia & Arquitetura

1. **Vanilla Web Stack:**
   - O projeto utiliza **HTML5 semântico**, **CSS3 moderno** e **JavaScript puro (Vanilla)** reunidos no arquivo `index.html`.
   - **NÃO introduza frameworks pesados** (React, Vue, Angular, Next.js ou compiladores complexos como Webpack/Vite) a menos que explicitamente solicitado pelo usuário. O carregamento instantâneo no GitHub Pages sem etapas de compilação é um requisito fundamental.
2. **Zero Quebras de Funcionalidades:**
   - **Sacola de Compras (Cart Drawer):** Nunca remova ou quebre o fluxo da sacola lateral, o cálculo de 5% de desconto via Pix, o acréscimo de embalagem kraft (+R$ 15), a persistência em `localStorage` (`bordo_cart_v2`) e a geração de links do WhatsApp (`https://wa.me/5531997954792?text=...`).
   - **Simulador Interativo:** Preserve os chips seletores e o botão de envio com mensagem formatada para o WhatsApp.
3. **Validação Obrigatória:**
   - Antes de concluir qualquer alteração em `index.html`, SEMPRE execute o comando:
     ```bash
     python build.py
     ```
   - O validador garante que nenhuma tag HTML ficou aberta por engano e que todos os assets obrigatórios continuam no diretório `assets/`.

---

## 3. Diretrizes de Design & UX (Padrão Luxo Editorial)

1. **Identidade Visual:**
   - **Cores Oficiais:**
     - Primária: `#5B1C2F` (Bordô Imperial)
     - Contraste: `#3A0F1D` (Bordô Profundo)
     - Acento: `#C5A059` e `#D4AF37` (Dourado Champagne)
     - Fundo Neutro: `#F9F6F0` (Linho Areia Nobre)
     - Fundo Puro: `#FFFFFF` (Branco Seda)
     - Tipografia: `#2C2A29` (Grafite Suave)
   - **Fontes Google Fonts integradas:**
     - `Playfair Display` para títulos principais e números de destaque.
     - `Plus Jakarta Sans` para corpo, navegação, botões e formulários.
     - `Cinzel` para monogramas, tags editoriais e subtítulos refinados.
2. **Responsividade & Mobile-First:**
   - Mais de 85% do tráfego deste negócio vem do Instagram em smartphones.
   - Todo layout DEVE ser 100% responsivo, com navegação hamburger fluida no mobile, áreas de toque generosas (mínimo 44x44px) e gaveta de sacola adaptada a telas verticais.
3. **Assets e Mídia:**
   - Todas as imagens de produtos devem utilizar as fotos reais em `assets/` convertidas em WebP com `loading="lazy"` para máxima velocidade de carregamento.
   - Sempre utilize tags de imagem com dimensões proporcionais e acabamento sutil de borda/sombra (`border-radius`, `box-shadow` suaves).

---

## 4. Mapeamento de Coleções & Assets Reais

| Identificador do Produto | Arquivo do Asset | Descrição Exata do Produto |
| :--- | :--- | :--- |
| **Corujinha do Sax** | `assets/bow-coruja.webp` | Laço em linho areia nobre com bordado autoral da corujinha tocando saxofone e notas musicais. |
| **Leãozinho do Sax** | `assets/bow-leao.webp` | Laço em linho verde sálvia com bordado autoral do leãozinho tocando saxofone. |
| **Gatinho do Sax** | `assets/bow-gato.webp` | Laço em linho crú aveludado com bordado autoral do gatinho tocando saxofone em bordô. |
| **Pôster Editorial** | `assets/sinfonia-poster.webp` | Imagem da coleção Sinfonia das Matas. |
| **Vídeo Reel** | `assets/sinfonia-reel.mp4` | Vídeo vertical demonstrando os detalhes dos laços e acabamento. |
| **Laço Animado** | `assets/laco-animado.gif` | Animação em loop do laço artesanal. |
| **Unboxing de Luxo** | `assets/unboxing.webp` | Caixa kraft Bordô com café, laços e cartão de agradecimento. |
| **Toalha Monograma** | `assets/gifts.webp` | Toalha de lavabo nobre bordada em algodão egípcio. |
| **Bordado Corporativo** | `assets/corporate.webp` | Camisas polo e peças profissionais bordadas. |
| **Bastidor Decorativo** | `assets/art.webp` | Bastidor em madeira com arte bordada. |
| **Textura de Linho** | `assets/craft.webp` | Foto macro dos pontos e fios acetinados de alta definição. |

---

## 5. Convenção para Checkout via WhatsApp

Ao gerar mensagens para o WhatsApp a partir de novas ações de compra, mantenha a estrutura limpa e profissional:

```javascript
const mensagem = `Olá, ateliê Bordô! ✨\n` +
  `Gostaria de fazer o pedido dos seguintes itens:\n\n` +
  itens.map(i => `• ${i.qty}x ${i.nome} (${i.variacao}) - R$ ${i.subtotal}`).join('\n') +
  `\n\nSubtotal: R$ ${subtotal}\n` +
  (temDescontoPix ? `Desconto Pix (5%): R$ ${valorPix}\n` : '') +
  (temEmbalagemPresente ? `Embalagem Kraft para Presente: Sim (+R$ 15)\n` : '') +
  `*Total do Pedido: R$ ${totalFinal}*\n\n` +
  `Por favor, me informe o prazo de entrega e os dados para pagamento.`;

const url = `https://wa.me/5531997954792?text=${encodeURIComponent(mensagem)}`;
window.open(url, '_blank');
```

---

## 6. Comandos de Manutenção & Deploy

- **Testar sintaxe e assets:**
  ```bash
  python build.py
  ```
- **Iniciar servidor de desenvolvimento:**
  ```bash
  python build.py --serve
  ```
- **Deploy:**
  - O repositório está conectado ao GitHub Pages na branch `main`.
  - Fazer commit e `git push origin main` publica automaticamente no domínio `bordopersonalizados.com.br`.
