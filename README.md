# Bordô | Bordados Personalizados

Site estático da Bordô, de Teixeiras, MG, com atendimento online por encomenda. Coleções, presentes, orçamento personalizado e sacola que continua pelo WhatsApp. Os laços utilizam diferentes tecidos.

## Executar

Requer Python 3.10 ou mais recente. Não há dependências Python externas nem instalação npm.

- `python build.py`: valida HTML, imagens e consistência do conteúdo.
- `python build.py --serve --port=8080`: prévia estática em localhost.
- `python admin_server.py` ou duplo clique em `Abrir_Painel.cmd`: abre o painel privado.
- `python -m unittest discover -s tests -v`: testa validação, autenticação, rascunhos, exportação e proteção de publicação.
- `node --check assets/site.js` e `node --check admin/admin.js`: verificam sintaxe JavaScript, quando Node estiver disponível.

## Gestão do Conteúdo

O painel permite criar, editar, ordenar, ocultar e excluir produtos, coleções, depoimentos, artigos e links. Fotos PNG, JPEG ou WebP de até 10 MB ficam na biblioteca. Preço vazio indica consulta pelo WhatsApp.

Edite um item, conclua a edição e salve o rascunho. A prévia e o ZIP também salvam antes de abrir. Configurações permitem alterar contatos, história, desconto Pix e embalagem. Use apenas depoimentos autorizados e mantenha a sinalização de imagens ilustrativas.

Rascunhos ficam em `.bordo-admin/draft.json`, com uma cópia anterior em `backup.json`. Essa pasta é ignorada pelo Git. Fechar o processo encerra o painel; os rascunhos permanecem. Reabra pelo atalho para obter uma nova sessão.

O servidor aceita conexões somente em `127.0.0.1`, exige sessão local e protege alterações com verificação de origem e token CSRF. Não exponha o processo na rede nem em hospedagem. As páginas do painel não contêm credenciais; o site público não executa o servidor.

## Publicação

Na branch de revisão, o botão Publicar fica desabilitado. Depois que a versão inicial for integrada ao `main`, execute o painel neste checkout atualizado. Git precisa estar instalado e autenticado no repositório `luissaraivavet/bordopersonalizados`.

Publicar exige confirmação, branch `main`, remoto correto e ausência de mudanças alheias. O painel atualiza apenas o conteúdo e as fotos selecionadas, cria commit e envia ao GitHub. GitHub Pages processa o envio posteriormente; sucesso do push não confirma a conclusão do deploy.

Para usar um pacote sem Git, exporte o ZIP e entregue os arquivos à hospedagem. O ZIP contém somente o site e assets, sem painel, sessão ou rascunhos internos.

## Arquivos

- `index.html`: apresentação responsiva, estilos e estrutura.
- `assets/site.js`: catálogo, sacola, orçamento e conteúdo editorial.
- `content/site.json` e `assets/content.js`: conteúdo público equivalente.
- `admin/` e `admin_server.py`: interface e servidor privado.
- `tests/`: testes automatizados sem alteração do catálogo real.
- `CNAME`: domínio configurado no GitHub Pages.

O logo original e as fontes Lora/Manrope foram preservados. As imagens sinalizadas são ilustrativas. Preços e condições iniciais foram preservados do catálogo existente: desconto Pix de 5% sobre peças e embalagem opcional de R$ 15 por pedido. Frete, prazo, materiais e disponibilidade são confirmados no atendimento.
