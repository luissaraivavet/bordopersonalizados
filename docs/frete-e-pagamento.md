# Bordô: frete por CEP e pagamento no site

Preparação em 08/10/2026. Origem confirmada pelo proprietário: 36580-000, Teixeiras/MG.

## Situação

O domínio continua no GitHub Pages. A sacola existente será preservada, assim como a chave `bordo_cart_v2`, preços, desconto Pix, embalagem e contatos. A API de cotação foi preparada em `integrations/shipping/worker.mjs`, com validação e testes. Ela ainda não está publicada nem conectada à conta Melhor Envio. Não há checkout financeiro implementado nesta alteração.

## Solução selecionada

Site estático existente + API de frete Melhor Envio + serviço de servidor + Mercado Pago Checkout Transparente. O servidor pode ser hospedado separadamente sem transferir o domínio ou alterar sua hospedagem. Cloudflare Workers possui plano gratuito com limites; verificar as condições da conta antes da publicação. Integração Melhor Envio sem mensalidade; etiquetas e transporte têm custo. Mercado Pago cobra processamento conforme modalidade e condições da conta.

## Ativar cotação

1. Criar/validar a conta Melhor Envio pelo proprietário; autorizar apenas os acessos necessários à cotação. Produção e sandbox usam contas/tokens distintos.
2. Medir e pesar as peças embaladas, incluindo proteção e embalagem. Confirmar perfil separado de embalagem para presente. Não usar medidas do laço como medidas do pacote. Para kits, medir o kit embalado. Validar o empacotamento retornado com pedidos de uma e várias peças.
3. Publicar o módulo de servidor com acesso HTTPS. Configurar variáveis abaixo e binding de limite de consultas. Não inserir tokens no HTML, GitHub ou painel público.
4. Confirmar onde cada transportadora disponível pode receber as encomendas de Teixeiras; filtrar os serviços que a operação não consiga postar.
5. Integrar campo CEP na sacola. Enviar somente identificadores, opções e quantidades; o servidor usa preços do catálogo e medidas cadastradas. Invalidar a cotação após alteração de CEP, peças, quantidades ou embalagem. Usar `textContent` ao apresentar nomes de serviços.
6. Conferir valores e prazos contra o painel Melhor Envio com carrinhos reais; depois ativar a interface. Em erro, informar indisponibilidade e permitir atendimento; nunca substituir erro por frete zero.

### Configuração do servidor

- `ORIGIN_POSTAL_CODE`: `36580000`.
- `MELHOR_ENVIO_ENVIRONMENT`: `sandbox` para homologação, `production` após conferência.
- `MELHOR_ENVIO_TOKEN`: segredo da conta/integração.
- `MELHOR_ENVIO_CONTACT`: e-mail técnico confirmado pelo proprietário.
- `SHIPMENT_PROFILES`: JSON por ID de produto com `width`, `height`, `length` em cm e `weight` em kg. IDs devem corresponder ao catálogo. Para presente, incluir `gift-packaging` representando o acréscimo de embalagem; validar empiricamente para evitar dupla contagem.
- `QUOTE_LIMITER`: binding de rate limiting do Worker. O código recusa ativação sem ele. CORS restringe navegadores, mas não substitui limite de chamadas ou autenticação. Avaliar proteção adicional contra abuso antes do lançamento.

Endpoint: `POST /shipping/quote`, body `{ "postalCode": "CEP do cliente", "items": [{ "id": "ID real", "variation": "opção real", "qty": 1 }], "gift": false }`. Resposta: serviços disponíveis com preço e prazo de transporte, ou mensagem de erro. Catálogo JSON é empacotado na implantação; mudanças de preço/publicação/opções exigem atualização do servidor para evitar divergência.

Não criar preço fictício ou cadastrar pesos aproximados sem autorização. Valores ilustrativos dos testes são fixtures técnicas e não dados da Bordô.

## Pagamento, próxima implementação

O painel Mercado Pago retornou erro de acesso no navegador integrado; nenhuma conta, credencial ou cobrança foi criada. Após acesso, confirmar habilitação, tarifas, aplicação e credenciais. Montar pedido durável com preço validado no servidor, disponibilidade e cotação de frete; só então renderizar pagamento. O futuro endpoint financeiro precisa revalidar a cotação e o carrinho: a resposta de frete no navegador não deve autorizar um valor de pagamento.

Para cobrar automaticamente, também faltam confirmação de disponibilidade/capacidade e prazos de preparação. Prazo de transporte começa na postagem e deve ser exibido separado do preparo. Retirada/entrega local só após definir as regras com o proprietário. Não comprar etiquetas automaticamente nesta etapa.

## Verificação

`node --test integrations/shipping/worker.test.mjs`

Além dos testes locais, homologar API real depois da conexão. A compra completa, pagamento, notificação, estoque e emissão de etiquetas não estão cobertos nem ativos neste módulo.

## Fontes oficiais

- https://docs.melhorenvio.com.br/reference/introducao-api-melhor-envio
- https://docs.melhorenvio.com.br/docs/cotacao-de-fretes
- https://docs.melhorenvio.com.br/reference/calculo-de-fretes-por-produtos
- https://developers.cloudflare.com/workers/platform/pricing/
- https://developers.cloudflare.com/workers/runtime-apis/bindings/rate-limit/
- https://www.mercadopago.com.br/developers/pt/docs/checkout-bricks/overview
