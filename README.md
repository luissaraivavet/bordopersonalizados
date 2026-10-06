# Bordô | Bordados Personalizados

> **Landing Page & Boutique Digital de Alto Padrão**  
> Peças autorais em linho puro, laços infantis com acabamento antialérgico, enxovais personalizados e presentes corporativos refinados.

🌐 **Site Oficial:** [https://bordopersonalizados.com.br](https://bordopersonalizados.com.br)  
📱 **WhatsApp Oficial:** [+55 (31) 99795-4792](https://wa.me/5531997954792)  
📸 **Instagram:** [@bordobordadospersonalizados](https://www.instagram.com/bordobordadospersonalizados/)  
📍 **Deploy:** GitHub Pages (`luissaraivavet/bordopersonalizados`)

---

## 📖 Visão Geral do Projeto

Este projeto é a presença digital oficial da marca **Bordô | Bordados Personalizados**. Foi concebido sob uma direção de arte editorial de luxo, inspirada em publicações de moda europeias e ateliês de alta costura, com foco em conversão e experiência de compra premium para mães, famílias e clientes corporativos.

### Principais Dores Solucionadas pelo Produto
- **Avesso Envelopado e Macio:** Elimina nós ásperos e linhas soltas que irritam a pele sensível da cabeça do bebê.
- **Presilhas 100% Forradas:** Sem metal exposto, impedindo puxões ou quebra de fios finos de cabelo.
- **Linho Nobre Puro:** Tecido termorregulador, respirável e hipoalergênico.
- **Fios de Brilho Acetinado:** Fios de bordado de alta tenacidade que não desbotam com lavagens.

---

## 💎 Coleções & Produtos em Destaque

### 1. Coleção Autoral: *Sinfonia das Matas*
Peças de assinatura autoral bordadas à mão e máquina sobre linho puro, retratando bichinhos músicos tocando instrumentos de sopro (Saxofone):
- **Corujinha do Sax:** Bordada em linho areia nobre com notas musicais douradas.
- **Leãozinho do Sax:** Bordado em linho verde sálvia com juba em textura especial.
- **Gatinho do Sax:** Bordado em linho crú aveludado com detalhes em tom bordô.
- *Opções de Fixação:* Presilha Bico de Pato 100% forrada com fita de gorgurão ou Faixa de Seda Anatômica ultraelástica.

### 2. Boutique Bordô (Pronta-Entrega & Presentes)
- **Toalha de Lavabo Nobre com Monograma:** Algodão egípcio e barra em linho bordado.
- **Bastidores de Madeira Decorativos:** Bordados decorativos de maternidade e quarto infantil.

### 3. Personalizados Sob Medida
- Simulador interativo em tempo real para enxovais infantis, lembrancinhas de batizado e bordados corporativos.

---

## 🛠️ Arquitetura Técnica

O projeto foi construído propositalmente com **Vanilla Web Technologies** (HTML5, CSS3, JavaScript ES6+) sem frameworks pesados (Node/React/Vue/Tailwind), trazendo vantagens estratégicas:
- **Zero build step complexo:** Funciona diretamente no navegador e no GitHub Pages.
- **Performance extrema:** Carregamento em menos de 1 segundo (First Contentful Paint < 0.6s).
- **Sem quebras de dependências ou vulnerabilidades de terceiros.**
- **SEO e Acessibilidade:** Marcação semântica com Open Graph, Twitter Cards, Schema.org e contrastes validados.

### Recursos Interativos Implementados
1. **Sacola de Compras Interativa (Shopping Cart Drawer):**
   - Gaveta lateral animada com controle de itens e quantidades.
   - Cálculo dinâmico de subtotal e desconto de 5% via Pix.
   - Opção de Embalagem Especial de Presente Kraft (+R$ 15,00).
   - Persistência em `localStorage` (o cliente não perde o carrinho ao recarregar).
   - **Checkout Estruturado no WhatsApp:** Gera uma mensagem perfeitamente formatada com lista de itens, acabamentos, total com desconto e dados de entrega.
2. **Simulador de Personalizados:**
   - Seletores de categoria, estilo de bordado, tecido e acabamento que geram briefing pronto para o WhatsApp do ateliê.
3. **Mídia Imersiva:**
   - Vídeo Reel vertical da produção artesanal (`assets/sinfonia-reel.mp4`).
   - Animação artesanal de laço em movimento (`assets/laco-animado.gif`).
   - Fotos reais de alta definição comprimidas em formato moderno WebP.
4. **FAQ Acordeão:**
   - Dúvidas sobre prazos, cuidados de lavagem, segurança e formas de pagamento.

---

## 📁 Estrutura de Diretórios

```text
bordo-bordados/
├── assets/
│   ├── logo.svg               # Logotipo vetorial oficial Bordô
│   ├── logo.png               # Logotipo em alta resolução
│   ├── unboxing.webp          # Foto hero: embalagem kraft de luxo com laços
│   ├── sinfonia-poster.webp   # Pôster editorial da coleção Sinfonia das Matas
│   ├── bow-coruja.webp        # Foto de produto: Laço Corujinha do Sax
│   ├── bow-leao.webp          # Foto de produto: Laço Leãozinho do Sax
│   ├── bow-gato.webp          # Foto de produto: Laço Gatinho do Sax
│   ├── gifts.webp             # Foto de toalhas nobres monogramadas
│   ├── corporate.webp         # Foto de camisas com bordado corporativo
│   ├── craft.webp             # Macro de fios e pontos de bordado
│   ├── hero.webp              # Imagem clássica de laço em linho
│   ├── art.webp               # Bastidor decorativo bordado
│   ├── sinfonia-reel.mp4      # Vídeo de demonstração da coleção
│   ├── laco-animado.gif       # Animação fluida de laço em cetim
│   └── original.css           # Estilos base e tokens CSS
├── build.py                   # Validador de tags HTML e servidor local
├── CNAME                      # Apontamento de domínio para bordopersonalizados.com.br
├── index.html                 # Página única com layout responsivo, CSS e scripts
├── AGENTS.md                  # Instruções e diretrizes técnicas para Agentes de IA
└── README.md                  # Documentação geral do projeto
```

---

## 🚀 Como Executar Localmente

### Pré-requisitos
- Python 3.8+ (ou qualquer servidor HTTP estático, como Live Server do VSCode).

### 1. Validar integridade dos arquivos
```bash
python build.py
```
*Verifica o fechamento de todas as tags em `index.html` e a presença dos assets necessários.*

### 2. Iniciar servidor local
```bash
python build.py --serve
# ou definir uma porta específica:
python build.py --serve --port=3000
```
Acesse no navegador: [http://localhost:8080](http://localhost:8080)

---

## 🎨 Paleta de Cores & Tipografia

| Nome da Cor | Hexadecimal | Uso Principal |
| :--- | :--- | :--- |
| **Bordô Imperial** | `#5B1C2F` | Cor primária, botões principais, destaques |
| **Bordô Escuro** | `#3A0F1D` | Rodapé, contrastes profundos |
| **Dourado Champagne** | `#C5A059` / `#D4AF37` | Selos, acentos, estrelas e bordas sutis |
| **Linho Areia** | `#F9F6F0` | Fundo principal da página |
| **Branco Puro** | `#FFFFFF` | Cards e superfícies destacadas |
| **Cinza Grafite** | `#2C2A29` | Textos de leitura e tipografia base |

- **Títulos & Headlines:** `Playfair Display` (Serif de alto contraste editorial)
- **Corpo & Interface:** `Plus Jakarta Sans` (Sans-serif moderno e ultra legível)
- **Monogramas & Detalhes:** `Cinzel` (Serif clássico romano)

---

## 🤝 Instruções para Outras IAs

Se você estiver utilizando assistentes de inteligência artificial (ChatGPT, Claude, Cursor, Lovable, Copilot, v0) para continuar o desenvolvimento deste projeto, consulte o arquivo [`AGENTS.md`](./AGENTS.md) presente na raiz. Ele contém regras rígidas de preservação arquitetural, padrões de design e convenções de código estabelecidas para a marca.
