# Bordô: medição, contatos e relacionamento sem mensalidade

## Decisão

Começar com GA4 Standard para medir o funil, UTMs padronizadas para identificar campanhas, entrada voluntária de adultos na lista Bordô e acompanhamento manual dos interessados. Usar Brevo Free para e-mail quando houver volume e conta ativada. Clarity é opcional após a base estar estável. Meta Pixel prepara publicidade futura, mas exibir anúncios requer orçamento e consentimento específico de publicidade.

Monitoramento não identifica automaticamente o nome ou WhatsApp do visitante. Contato só existe após a pessoa fornecê-lo por formulário ou mensagem. Clique em WhatsApp não comprova conversa, cadastro ou compra.

## Preparação realizada

Módulo `integrations/marketing/measurement.mjs`, sem dependências, com eventos permitidos e ativação somente após consentimento explícito e ID GA4 válido. Nenhuma tag foi inserida na página publicada. Não foi criada conta ou campanha. O módulo não instala Meta Pixel ou Clarity nesta etapa. A interface de consentimento, a política de privacidade e os hooks do frontend ainda precisam ser implementados antes de ativar a coleta.

## Funil e eventos

| Ação | Evento | Interpretação |
|---|---|---|
| Coleção aparece na tela | view_collection | Interesse na coleção, disparar uma vez por visualização relevante |
| Abre detalhes reais da peça | view_item | Interesse específico |
| Item é adicionado com sucesso | add_to_cart | Intenção de compra |
| Abre a sacola | view_cart | Revisão do pedido |
| Clica para conversar | whatsapp_click | Tentativa de contato, não lead confirmado |
| Clica em inscrição | lead_signup_click | Interesse na lista, não inscrição concluída |

Compra deve vir da confirmação do servidor/provedor na implementação financeira futura. Cadastro concluído deve vir do formulário salvo e confirmado. Não marcar cliques como receita. Não usar recuperação automática de sacola anônima. Formulário de orçamento e aviso de novidades têm finalidades diferentes.

## Integração GA4

Criar propriedade e fluxo web da Bordô; informar ID público `G-...`. Desativar Medição Otimizada automática no fluxo nesta implementação, evitando coleta de consultas/fragmentos e formulários. Conferir configurações de publicidade/Google Signals, retenção e acesso. Implementar opções equivalentes Aceitar estatísticas/Rejeitar, preferências independentes de publicidade e link permanente para revogar.

Importar `createMeasurement`, passar o ID confirmado e chamar `consent(true)` apenas após escolha explícita do visitante ou preferência válida. Ao revogar, chamar `consent(false)` e eliminar os cookies de análise conforme orientações do provedor; não recriar cookies após recusa. O módulo interrompe novos eventos, mas não apaga histórico remoto. Testar comportamento na rede e cookies antes do lançamento.

Hooks em `assets/site.js` devem ocorrer após operações bem-sucedidas, respeitando sacola vazia e limites. Nunca enviar texto da mensagem, nomes, e-mails, telefones, CEP, endereço, dados de crianças ou dados digitados. Configurar DebugView/Tempo real e testar sem contaminar dados reais. Medir sessões e canais no GA4, não somar eventos repetidos como pessoas únicas. Recusas e bloqueadores fazem a medição ser parcial.

## Links de divulgação

- Bio: `https://bordopersonalizados.com.br/?utm_source=instagram&utm_medium=organic_social&utm_campaign=bordo_lancamento&utm_content=bio`
- Story floral: `https://bordopersonalizados.com.br/?utm_source=instagram&utm_medium=organic_social&utm_campaign=bordo_lancamento&utm_content=story_jardim#jardim`
- Reel animais: `https://bordopersonalizados.com.br/?utm_source=instagram&utm_medium=organic_social&utm_campaign=bordo_lancamento&utm_content=reel_sinfonia#sinfonia`
- Compartilhamento: `https://bordopersonalizados.com.br/?utm_source=whatsapp&utm_medium=referral&utm_campaign=bordo_lancamento&utm_content=presente`

Não incluir nome/telefone do cliente em UTMs. O módulo usa lista permitida desses valores; novas campanhas exigem ampliar a lista. Os campos UTM são enviados como parâmetros próprios; configurar dimensões personalizadas de evento para leitura, pois isso não substitui automaticamente a atribuição nativa de sessões do GA4.

## Captação proposta

Chamada no site: **Receba novidades da Bordô.** Texto: "Conheça novas peças e ideias para presentear. Escolha como quer receber: WhatsApp ou e-mail. Você pode sair quando quiser."

Alternativa inicial WhatsApp: botão com mensagem "Olá, Bordô! Quero receber novidades e ideias para presentear pelo WhatsApp. Como faço para participar?" O clique apenas abre mensagem para revisão; pessoa precisa enviá-la. Confirmar a inscrição e explicar frequência e saída antes de adicionar à lista. Sem disparos nesta etapa. Não usar grupos que exponham números. Não oferecer desconto sem definir margem.

Formulário de e-mail posterior: e-mail, interesse opcional (laços/presentes/personalizados), opção de marketing desmarcada, link de privacidade e confirmação de inscrição. Preferir formulário hospedado Brevo com confirmação dupla e CAPTCHA quando disponível. Não usar chave Brevo no navegador, não salvar contatos em repositório público/localStorage. Para formulário próprio, implementar servidor privado, proteção contra abuso, registro de autorização e descadastro. Ativar SPF/DKIM antes de campanhas. Revisar limites do plano e identidade do remetente.

## Relacionamento gratuito

1. Boas-vindas: explicar o que a pessoa receberá e oferecer coleção conforme interesse.
2. Conteúdo: mostrar acabamento e ajudar a escolher um presente.
3. Novidade real: divulgar peças/coleções disponíveis, com link específico.
4. Dúvida de compra: oferecer ajuda para quem iniciou conversa, sem insistência.

Começar manualmente. Uma mensagem semanal é hipótese de frequência a validar, não compromisso da marca. Sem automação prometida no plano grátis. Descadastro simples por resposta "SAIR" no WhatsApp e link no e-mail. Manter interesse e consentimento dos contatos adultos. Retomar apenas quem autorizou contato pertinente.

## Painel semanal

Sessões por canal, coleções visitadas, itens adicionados, cliques WhatsApp, conversas efetivas, inscrições confirmadas e pedidos pagos. Taxa clique WhatsApp/sessões é indicador de contato, não conversão de vendas. Acompanhar pedidos manualmente enquanto não houver checkout. Para atribuir pedidos, perguntar a origem ou usar referência da campanha de forma minimizada; não copiar dados do cliente para ferramentas de análise.

Diagnóstico: visita sem adição = revisar peça/oferta; sacola sem contato = revisar frete e confiança; contato sem compra = registrar dúvida/objeção. Não ampliar ferramentas até haver uso dos dados.

## Pendências para ativar

Conta GA4 e ID do fluxo, verificação do domínio Search Console se desejada, política de privacidade com controlador/contato e finalidades reais, interface de consentimento testada, CTA aprovado/integrado, conta e formulário de e-mail, opcional Meta Pixel após consentimento de publicidade. A ativação e publicação não ocorreram neste pacote.

## Fontes

- https://support.google.com/analytics/answer/11828307
- https://developers.google.com/tag-platform/security/guides/consent
- https://clarity.microsoft.com/pricing
- https://help.brevo.com/hc/en-us/articles/208580669-FAQs-What-are-the-limits-of-the-Free-plan
- https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia_orientativo_cookies_e_protecao_de_dados_pessoais
