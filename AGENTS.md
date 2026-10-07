# Repository Guidelines

## Estrutura do Projeto

`index.html` contém estrutura e CSS; `assets/site.js` controla catálogo, sacola e orçamento. O conteúdo público fica em `content/site.json` e `assets/content.js`. Mantenha os dois equivalentes. Imagens, fontes e ícones estão em `assets/`, com suas licenças.

`admin/` contém o painel, e `admin_server.py`, seu servidor privado. `tests/` verifica conteúdo e proteção do painel. `build.py` valida o site; `CNAME` configura o domínio. Preserve o frontend estático, sem frameworks.

## Desenvolvimento e Verificação

Requer Python 3.10 ou superior, sem dependências externas:

- `python build.py`: valida HTML, assets e conteúdo; falhas retornam código diferente de zero.
- `python build.py --serve --port=8080`: inicia prévia local.
- `python admin_server.py`: abre o painel privado.
- `python -m unittest discover -s tests -v`: executa os testes.
- `node --check assets/site.js` e `node --check admin/admin.js`: verificam sintaxe, quando Node estiver disponível.
- `git diff --check`: verifica espaços nas alterações.

## Estilo e Nomenclatura

Use dois espaços no HTML e quatro no Python. Acompanhe o JavaScript existente, com `const`, funções em `camelCase` e arquivos/classes em `kebab-case`. Não há formatador ou linter obrigatório. Identificadores do conteúdo devem ser únicos, com letras minúsculas, números e hifens.

## Testes

Use `unittest`, arquivos `test_*.py` e casos `test_*`. Não há meta de cobertura. Testes de escrita usam diretório temporário; nunca publique durante verificações.

Teste também computador e celular: menu, imagens, formulário, teclado, foco, sacola vazia, quantidades, remoção e persistência. Confira desconto Pix, embalagem e mensagem do WhatsApp sem enviar pedidos. No painel, teste edição, rascunho, prévia e exportação.

## Commits e Pull Requests

O histórico usa descrições em português, incluindo `docs:`, sem exigir exclusivamente Conventional Commits. Prefira branches `codex/<descricao>` e commits focados.

Explique problema, solução e validação no PR. Vincule issues quando aplicável e inclua capturas de computador/celular nas mudanças visuais. Integrar ao `main` pode publicar via GitHub Pages; confirme autorização para essa etapa.

## Marca e Segurança

A Bordô é de Teixeiras, MG, com atendimento online por encomenda. Não enfatize exclusividade do linho. Preserve o logo e o português brasileiro. Por solicitação do proprietário, não exiba avisos de imagens ilustrativas no site. Não invente preços, depoimentos ou propriedades.

Preserve `bordo_cart_v2` e valide dados armazenados. Nunca versione credenciais ou `.bordo-admin/`. Mantenha o servidor restrito a loopback, autenticação e proteção CSRF. Confirme alterações de contatos e condições comerciais.
