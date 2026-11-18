"""Gera os guias de lista do blog (blog/<slug>/index.html).

Uso:
    python scripts/gerar_listas_blog.py

Le scripts/dados_listas_blog.json (produtos de afiliado com nota, opinioes,
preco e link, consultados na data indicada no arquivo) e reaproveita o estilo,
o cabecalho e o rodape de blog/decoracao-de-natal-crista/index.html. As fotos
ficam em blog/assets/listas/. Rode de novo depois de atualizar os dados; os
textos de cada item ficam neste arquivo.
"""
import html
import json
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
BLOG = ROOT / 'blog'
BASE = 'https://bordopersonalizados.com.br'
DATA = json.loads((ROOT / 'scripts/dados_listas_blog.json').read_text(encoding='utf-8'))
PRODUCTS = {item['id']: item for item in DATA['produtos']}
CHECKED = '17 e 18 de novembro de 2026'
PUBLISHED = '2026-11-18'
PUBLISHED_TEXT = '18 de novembro de 2026'

# Nome curto, por que entrou e o que vale saber. Tudo sai do titulo e dos numeros do anuncio.
COPY = {
    'A001': ('Fone sem fio QCY T13 ENC', 'Bluetooth 5.1, quatro microfones e bateria anunciada de 40 horas com o estojo.', 'É intra-auricular: quem não se adapta a ponteiras de silicone pode preferir outro formato.'),
    'A002': ('Kit churrasco de 9 peças em inox com estojo', 'Reúne os utensílios da churrasqueira em um estojo, pronto para presentear.', ''),
    'A003': ('Power bank Basike de 20.000 mAh', 'Carga rápida de 22,5 W, cabos embutidos e visor que mostra a bateria restante.', 'Confira peso e medidas no anúncio: 20.000 mAh costuma ocupar mais espaço na bolsa.'),
    'A004': ('Perfume Nautica Voyage 100 ml', 'É o item com mais opiniões de todas as nossas listas.', 'Perfume é gosto pessoal: se puder, descubra antes o que a pessoa costuma usar.'),
    'A005': ('Kit para barba com 5 itens', 'Shampoo, pomada, balm, óleo e pente no mesmo kit.', ''),
    'A006': ('Garrafa térmica de 1 litro em inox', 'O anúncio informa 18 horas para bebida gelada e 12 horas para quente.', 'Com 1 litro, é grande para bolsas pequenas.'),
    'A007': ('Kit presente Cuide-se Bem Deleite, O Boticário', 'Três itens da mesma linha, já em formato de presente.', 'Confira no anúncio quais são os três itens do kit.'),
    'A008': ('Floratta Flores Secretas 75 ml, O Boticário', 'Fragrância feminina com mais de 10 mil opiniões.', 'Perfume é gosto pessoal: se puder, descubra antes o que a pessoa costuma usar.'),
    'A009': ('Kit skincare de rosa mosqueta', 'Kit de limpeza de pele montado para presente.', ''),
    'A010': ('Kit com 3 necessaires impermeáveis', 'Três tamanhos para organizar mala, bolsa e banheiro.', 'O link abre na cor preta; outras cores podem ter outro preço.'),
    'A011': ('Massageador de pescoço e ombros com aquecimento', 'Recarregável por USB-C, sem fio, com aquecimento.', 'Leia no anúncio as orientações e contraindicações de uso.'),
    'A012': ('Copo térmico de 1,2 litro em inox, rosa', 'Vem com alça, tampa, canudo de inox e escova de limpeza.', 'Com 1,2 litro, não cabe em todo porta-copos de carro: confira as medidas.'),
    'A013': ('Copo térmico de 1,2 litro em inox, preto', 'Mesmo modelo do copo rosa, em preto fosco.', 'Com 1,2 litro, não cabe em todo porta-copos de carro: confira as medidas.'),
    'A014': ('Kit vinho com saca-rolhas, abridor, tampa e dosador', 'Quatro acessórios em um estojo de presente.', ''),
    'A015': ('Fone Bluetooth 5.4 Kaidi KD780', 'Fone sem fio na faixa de R$ 40, com mais de 10 mil opiniões.', 'É de marca menos conhecida: leia as avaliações recentes sobre bateria e microfone.'),
    'A016': ('Garrafa térmica de 800 ml com alça', 'Inox, pensada para academia e trabalho.', 'Confira no anúncio por quanto tempo ela mantém a temperatura.'),
    'A017': ('Pantufa com sola de borracha antiderrapante', 'Presente de conforto que serve para qualquer idade.', 'Tem numeração: confirme o tamanho antes de comprar.'),
    'A018': ('Kit de necessaires sem gênero', 'O item mais barato de todas as listas.', ''),
    'A019': ('Banco Imobiliário, Estrela', 'O clássico de tabuleiro para reunir a família depois da ceia.', 'As partidas são longas: combina mais com quem gosta de jogar sem pressa.'),
    'A020': ('Detetive com aplicativo, Estrela', 'Jogo de dedução em que um aplicativo conduz a partida.', 'Precisa de um celular com o aplicativo durante o jogo.'),
    'A021': ('Imagem & Ação 2, Grow', 'Jogo de mímica e desenho para grupos.', 'Rende mais com bastante gente: confira no anúncio o número de participantes.'),
    'A022': ('Umidificador ultrassônico de 2,3 litros, bivolt', 'Reservatório de 2,3 litros e funcionamento em qualquer voltagem.', 'Como todo umidificador, pede limpeza frequente do reservatório.'),
    'A023': ('Umidificador WAP com luminária e difusor de aromas', 'Três funções no mesmo aparelho: umidifica, ilumina e perfuma.', 'Escolha a voltagem certa no anúncio: 127 V ou 220 V.'),
    'A024': ('Samsung Galaxy Fit3, tela de 1,6 polegada', 'Pulseira inteligente com mais de 43 mil opiniões.', 'Confira a compatibilidade com o celular de quem vai ganhar.'),
    'A025': ('Kit com 5 carrinhos Hot Wheels', 'Cinco carrinhos da Mattel em uma embalagem.', 'Os modelos são sortidos: não dá para escolher os carrinhos.'),
    'A026': ('Cachorro robô que dança, com som e luz', 'Brinquedo musical para os pequenos.', 'Confira no anúncio a idade indicada e as pilhas necessárias.'),
    'P001': ('Cortina de LED 3 x 3 m com 300 luzes', 'Oito funções, controle remoto, regulagem de intensidade e ligação por USB.', 'A luz é branco frio, mais azulada que o branco quente.'),
    'P002': ('Vila natalina de madeira com 7 peças', 'Igreja de 11 cm, chalé, moinho, duas casas e duas árvores.', 'Não tem luz: as peças têm furo para LED, que não vem incluso.'),
    'P003': ('Gancho dourado de 38 cm para guirlanda', 'Encaixa no topo da porta e segura a guirlanda sem furar.', 'A guirlanda não vem inclusa.'),
    'P004': ('Guirlanda de Natal de 30 cm com laço vermelho', 'Vem com laço vermelho, frutinhas e plaquinha "Merry Christmas".', 'Com 30 cm, fica pequena em portas largas. Outras cores têm outro preço.'),
    'B001': ('Jogo Lince, Grow', 'Jogo de agilidade visual com partidas rápidas: ganha quem acha a figura primeiro.', 'Confira no anúncio a idade indicada.'),
    'B002': ('Fone sem fio Soundcore P20i, da Anker', 'Bluetooth 5.3, 30 horas de reprodução anunciadas e ajuste de som pelo aplicativo.', 'É intra-auricular: quem não se adapta a ponteiras de silicone pode preferir outro formato.'),
    'B003': ('Carteira masculina de couro com fecho', 'Presente clássico na faixa de R$ 43, com quase 5 mil opiniões.', 'O link abre na cor preta: confira as divisórias no anúncio.'),
    'B004': ('Garrafa térmica Stanley Quick Flip 710 ml', 'Marca desejada, tampa que abre com um toque e quase 20 mil opiniões.', 'Custa cerca do dobro da garrafa de 1 litro desta mesma lista.'),
    'B005': ('Kit Paulaner com 2 cervejas e 1 copo', 'Duas cervejas alemãs, Weissbier e Dunkel, com o copo da marca.', 'Presente só para maiores de 18 anos.'),
    'B006': ('Kaiak Feminino 100 ml, Natura', 'Um dos perfumes mais conhecidos da Natura, com mais de 6 mil opiniões.', 'Perfume é gosto pessoal: se puder, descubra antes o que a pessoa costuma usar.'),
    'B007': ('Liz Flora 100 ml, O Boticário', 'Colônia de O Boticário com mais de 50 mil unidades vendidas.', 'Perfume é gosto pessoal: se puder, descubra antes o que a pessoa costuma usar.'),
    'B008': ('Girassol eterno com colar', 'Uma flor que não murcha e um colar no mesmo presente.', 'Confira no anúncio o material do colar e o tamanho da flor.'),
    'B009': ('Difusor e umidificador Luatek 400 ml com LED', 'Umidifica, perfuma o ambiente e tem luz de LED, com acabamento em tom de madeira clara.', 'Com 400 ml, é um modelo pequeno, de mesa.'),
    'B010': ('War, Grow', 'O clássico de estratégia para quem gosta de partidas disputadas.', 'As partidas são longas: reserve a tarde.'),
    'B011': ('Jogo da Vida com aplicativo, Estrela', 'O clássico da Estrela em versão que usa aplicativo.', 'Precisa de um celular com o aplicativo durante o jogo.'),
    'P005': ('Kit com 12 laços de Natal com glitter', 'Doze laços de 7,5 cm em pano para a árvore.', 'O preço muda conforme a cor: o link abre no dourado.'),
}

# Para quem o presente combina: ajuda a pessoa a se reconhecer na escolha.
PARA = {
    'A001': 'quem ouve música ou podcast no caminho do trabalho', 'A002': 'o churrasqueiro da família', 'A003': 'quem vive com o celular em 5%',
    'A004': 'quem gosta de perfume para o dia a dia', 'A005': 'quem cuida da barba todo dia', 'A006': 'quem treina, viaja ou trabalha na rua',
    'A007': 'quem gosta de um ritual de cuidado depois do banho', 'A008': 'quem já usa O Boticário', 'A009': 'quem está começando a cuidar da pele',
    'A010': 'quem viaja ou leva meia casa na bolsa', 'A011': 'quem passa o dia no computador', 'A012': 'quem não larga a água ou o café gelado',
    'A013': 'quem não larga a água ou o café gelado', 'A014': 'quem gosta de abrir um vinho no fim de semana', 'A015': 'quem perdeu o fone e precisa de outro sem gastar muito',
    'A016': 'quem leva água para a academia', 'A017': 'quem ama ficar em casa', 'A018': 'qualquer pessoa do sorteio, quando você não a conhece bem',
    'A019': 'famílias que gostam de jogar por horas', 'A020': 'quem gosta de mistério e dedução', 'A021': 'turmas grandes e festas',
    'A022': 'casas em cidade de clima seco', 'A023': 'quem quer umidificar e perfumar o quarto', 'A024': 'quem quer começar a acompanhar passos e sono',
    'A025': 'crianças que colecionam carrinhos', 'A026': 'os pequenos que adoram música',
    'B001': 'famílias com crianças e turmas animadas', 'B002': 'quem quer um fone de marca conhecida sem passar de R$ 130', 'B003': 'o pai ou o avô de gosto clássico',
    'B004': 'quem repara em marca', 'B005': 'quem aprecia cerveja especial', 'B006': 'quem gosta de Natura', 'B007': 'quem gosta de perfume floral',
    'B008': 'a namorada ou a esposa, com um gesto romântico', 'B009': 'quem gosta de casa cheirosa', 'B010': 'adolescentes e adultos estrategistas', 'B011': 'famílias com crianças maiores',
    'P001': 'quem quer um fundo de luz para a ceia e as fotos', 'P002': 'quem monta um cantinho de Natal no rack ou na mesa', 'P003': 'quem não quer furar a porta',
    'P004': 'portas de apartamento e entradas pequenas', 'P005': 'quem quer renovar a árvore sem trocar tudo',
}

OWN = {
    'laco': ('/assets/jardim-margarida.webp', 'Laço bordado com margarida e borboleta, da Bordô', 'Um laço bordado, feito por encomenda', 'Os laços bordados da Bordô custam a partir de R$ 49,90 e são feitos por encomenda em Teixeiras, MG. Você escolhe o desenho e combina os detalhes pelo WhatsApp.', [('Ver os laços do Jardim de Encantos', f'{BASE}/#jardim'), ('Ver os laços Mãe & Rainha', f'{BASE}/#rainha')]),
    'rainha': ('/assets/mae-rainha-lacos.webp', 'Três laços Mãe & Rainha bordados, da Bordô', 'Laços Mãe & Rainha, bordados por encomenda', 'Uma homenagem a Nossa Senhora Aparecida em laço bordado, a partir de R$ 49,90, feita por encomenda pela Bordô em Teixeiras, MG.', [('Ver os laços Mãe & Rainha', f'{BASE}/#rainha'), ('Encomendar um bordado com nome', f'{BASE}/#personalizados')]),
    'naninha': ('/assets/colinho-do-ceu.webp', 'Naninhas bordadas da coleção Colinho do Céu, da Bordô', 'Naninhas bordadas Colinho do Céu', 'Naninhas bordadas de santos e de Nossa Senhora, a R$ 59,90, feitas por encomenda pela Bordô em Teixeiras, MG.', [('Ver as naninhas Colinho do Céu', f'{BASE}/#colinho'), ('Ver os laços bordados', f'{BASE}/#jardim')]),
    'encomenda': ('/assets/embalagem-unboxing.webp', 'Peça bordada da Bordô embalada para presente', 'Um bordado com o nome dele, sob encomenda', 'Um nome, uma data ou a marca da empresa bordados em uma peça. A Bordô faz por encomenda em Teixeiras, MG, e o orçamento começa no WhatsApp.', [('Descrever minha encomenda', f'{BASE}/#personalizados'), ('Ver presentes personalizados', f'{BASE}/presentes-personalizados/')]),
}

LISTS = [
    {
        'slug': 'presentes-ate-50-reais', 'cover': 'capa-ate-50.webp', 'section': 'Presentes', 'own': 'laco', 'limit': 50,
        'h1': '10 presentes até R$ 50 para o amigo secreto de 2026',
        'title': '10 presentes até R$ 50 para amigo secreto (2026) | Bordô',
        'card': 'Lista de presentes · até R$ 50',
        'description': 'Lista com 10 presentes até R$ 50 para amigo secreto e lembranças de Natal: copo térmico, fone, jogo, garrafa, pantufa e mais, com nota e preço.',
        'lead': 'Dez ideias que cabem no limite do amigo secreto, todas com nota 4,8 ou mais no Mercado Livre. Em menos de dois minutos você sai com o presente decidido.',
        'intro': 'O limite de R$ 50 é o mais comum nos sorteios de fim de ano, e é também onde mais se erra por pressa. Esta lista junta o que encontramos nessa faixa com muitas avaliações de compradores.',
        'items': ['A012+A013', 'A015', 'A018', 'A010', 'A017', 'A016', 'A026', 'A002', 'A014', 'B001'],
    },
    {
        'slug': 'presentes-para-homem', 'cover': 'capa-homem.webp', 'section': 'Presentes', 'own': 'encomenda', 'limit': 150,
        'h1': '10 presentes para homem até R$ 150 no Natal de 2026',
        'title': '10 presentes para homem até R$ 150 (Natal 2026) | Bordô',
        'card': 'Lista de presentes · para ele',
        'description': 'Lista com 10 presentes para homem até R$ 150: perfume, fones sem fio, power bank, garrafas térmicas, carteira, kit churrasco e mais, com nota e preço.',
        'lead': 'Dez presentes para pai, marido, namorado ou amigo, de R$ 42,99 a R$ 149, todos com nota 4,8 ou mais no Mercado Livre.',
        'intro': 'Presente para homem costuma travar na mesma dúvida: o que ele ainda não tem? Esta lista foge do óbvio com itens de uso diário e muitas avaliações de compradores.',
        'items': ['A004', 'A001', 'A003', 'A006', 'A002', 'A005', 'B002', 'B003', 'B004', 'B005'],
    },
    {
        'slug': 'presentes-para-mulher', 'cover': 'capa-mulher.webp', 'section': 'Presentes', 'own': 'rainha', 'limit': 100,
        'h1': '10 presentes para mulher até R$ 100 no Natal de 2026',
        'title': '10 presentes para mulher até R$ 100 (Natal 2026) | Bordô',
        'card': 'Lista de presentes · para ela',
        'description': 'Lista com 10 presentes para mulher até R$ 100: perfumes Natura e O Boticário, copo térmico, difusor, necessaires, massageador e mais, com nota e preço.',
        'lead': 'Dez presentes para mãe, esposa, namorada ou amiga, de R$ 29 a R$ 94, todos com nota 4,8 ou mais no Mercado Livre.',
        'intro': 'Esta lista mistura cuidado pessoal, bem-estar e utilidade, sempre abaixo de R$ 100 e com muitas avaliações de compradores.',
        'items': ['A012', 'A008', 'A010', 'A007', 'A011', 'A009', 'B006', 'B007', 'B008', 'B009'],
    },
    {
        'slug': 'presentes-para-familia-e-criancas', 'cover': 'capa-familia.webp', 'section': 'Presentes', 'own': 'naninha', 'limit': 180,
        'h1': '10 presentes para a família e as crianças até R$ 180',
        'title': '10 presentes para a família e crianças até R$ 180 | Bordô',
        'card': 'Lista de presentes · família',
        'description': 'Lista com 10 presentes para a família e as crianças: War, Banco Imobiliário, Detetive, umidificadores, Galaxy Fit3, Hot Wheels e mais, com nota e preço.',
        'lead': 'Dez presentes para a casa inteira aproveitar, de R$ 48 a R$ 179, todos com nota 4,8 ou mais no Mercado Livre.',
        'intro': 'Presente para a família funciona quando todo mundo usa. Por isso a lista começa nos jogos de tabuleiro e passa por itens para a casa e brinquedos.',
        'items': ['A024', 'A025', 'A022', 'A023', 'A020', 'A021', 'A026', 'A019', 'B010', 'B011'],
    },
    {
        'slug': 'enfeites-de-natal-ate-70-reais', 'cover': 'capa-enfeites.webp', 'section': 'Decoração de Natal', 'own': 'naninha', 'limit': 70,
        'h1': '5 enfeites de Natal até R$ 70 para porta, parede e árvore',
        'title': '5 enfeites de Natal até R$ 70: porta, parede e árvore | Bordô',
        'card': 'Lista de decoração · até R$ 70',
        'description': 'Lista com 5 enfeites de Natal até R$ 70: cortina de LED, gancho e guirlanda para porta, laços para a árvore e vila natalina, com nota e preço.',
        'lead': 'Cinco enfeites para decorar a casa gastando pouco, de R$ 27,97 a R$ 69,90, com nota 4,5 ou mais no Mercado Livre.',
        'intro': 'Dá para mudar a cara da casa no Natal com poucas peças bem escolhidas: uma luz de fundo, a porta arrumada e um detalhe na árvore.',
        'items': ['P005', 'P003', 'P001', 'P004', 'P002'],
    },
]

EXTRA_CSS = """
.rank-table{width:100%;border-collapse:collapse;margin:0 0 30px;font-size:14px;line-height:1.5}
.rank-table th,.rank-table td{padding:11px 10px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
.rank-table th{font-size:12px;color:var(--muted);font-weight:700}
.rank-table td:nth-child(3),.rank-table td:nth-child(4){white-space:nowrap}
.rank-table a{font-weight:700;text-underline-offset:3px}
.rank-wrap{overflow-x:auto}
.highlights{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin:0 0 30px}
.highlights a{display:block;padding:16px 18px;border:1px solid var(--line);border-radius:3px;background:#fff;text-decoration:none;color:var(--ink);font-size:14px;line-height:1.5}
.highlights strong{display:block;color:var(--wine);font-size:13px}
.rank-item{display:grid;grid-template-columns:220px minmax(0,1fr);gap:26px;padding:30px 0;border-top:1px solid var(--line);scroll-margin-top:24px}
.rank-item img{border-radius:3px;aspect-ratio:4/5;object-fit:cover;background:var(--cream)}
.rank-item h3{font-size:25px;margin:0 0 10px}
.rank-num{font-family:Lora,Georgia,serif;color:var(--gold);font-size:19px;margin-right:6px}
.article-content .rank-facts{display:flex;flex-wrap:wrap;gap:6px 18px;margin:0 0 12px;padding:0;list-style:none;font-size:13px;color:var(--muted);line-height:1.5}
.rank-facts strong{color:var(--ink)}
.rank-item p{margin:0 0 12px;font-size:15px;line-height:1.75}
.rank-item .btn{margin-top:4px}
.rank-item .btn+.btn{margin-left:8px}
.own-pick{display:grid;grid-template-columns:220px minmax(0,1fr);gap:26px;margin:34px 0;padding:24px;background:var(--cream);border:1px solid var(--line);border-radius:3px}
.own-pick img{border-radius:3px;aspect-ratio:4/5;object-fit:cover}
.own-pick h3{font-size:25px;margin:0 0 10px}
.own-pick p{margin:0 0 14px;font-size:15px;line-height:1.75}
.own-pick a{display:block;font-weight:700;margin-top:6px;text-underline-offset:3px}
.rank-badge{display:inline-block;margin:0 0 8px;padding:4px 10px;border-radius:3px;background:var(--wine);color:#fff;font-size:12px;font-weight:700;line-height:1.4}
.rank-proof{margin:0 0 10px!important;font-size:14px!important;font-weight:700;color:#3f503d}
.rank-safe{margin:10px 0 0!important;font-size:12px!important;color:var(--muted)}
.rank-item img.shot{object-fit:contain;background:#fff;border:1px solid var(--line);padding:10px}
.decide{margin:0 0 30px;padding:24px 26px;background:var(--cream);border-left:3px solid var(--gold)}
.decide h2{margin:0 0 12px!important;font-size:28px!important}
.decide p{margin:0 0 6px;font-size:15px;line-height:1.75}
.decide .share-row{margin-top:16px}
.decide-count{font-weight:700;color:var(--wine)}
.decide.closing{margin:40px 0 10px}
.faq-list details{border-top:1px solid var(--line);padding:4px 0}
.faq-list details:last-child{border-bottom:1px solid var(--line)}
.faq-list summary{cursor:pointer;padding:14px 0;font-family:Lora,Georgia,serif;font-size:20px;color:var(--wine);line-height:1.35}
.faq-list details p{margin:0 0 16px;font-size:15px}
.share-row{display:flex;flex-wrap:wrap;gap:10px;margin:28px 0 0}
.btn.ghost{background:#fff;color:var(--wine)}
@media(max-width:600px){.rank-table th:nth-child(4),.rank-table td:nth-child(4){display:none}.rank-item,.own-pick{grid-template-columns:1fr;gap:16px}.rank-item img,.own-pick img{max-width:260px}.highlights{grid-template-columns:1fr}.rank-item .btn{width:100%}.rank-item .btn+.btn{margin:8px 0 0}}
"""

esc = html.escape

# Contagem real ate 25 de dezembro; some depois do Natal.
COUNTDOWN = ("<script>(function(){var n=new Date(),d=new Date(n.getFullYear(),11,25),k=Math.ceil((d-n)/864e5),e=document.getElementById('natalCount');"
             "if(e&&k>0){e.textContent=(k===1?'Falta 1 dia':'Faltam '+k+' dias')+' para o Natal. O prazo de entrega depende do seu CEP: quanto antes você pedir, mais folga.';e.hidden=false;}})();</script>")


def money(value):
    text = f'{value:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    return 'R$ ' + (text[:-3] if text.endswith(',00') else text)


def number(value):
    return f'{value:,}'.replace(',', '.')


def note(value):
    return str(value).replace('.', ',')


def sold(value):
    if not value:
        return ''
    amount = value.replace('mil', ' mil') if 'mil' in value else number(int(value))
    return f'mais de {amount} vendidos'


def entries(spec):
    """Um item da lista pode juntar dois anuncios do mesmo produto em cores diferentes."""
    result = []
    for key in spec['items']:
        ids = key.split('+')
        group = [PRODUCTS[i] for i in ids]
        first = group[0]
        name, why, caution = COPY[ids[0]]
        if len(group) > 1:
            name = 'Copo térmico de 1,2 litro em inox, rosa ou preto'
        cautions = [caution] if caution else []
        if any(item['full'] is False for item in group):
            cautions.append('Não é envio Full: confira o prazo para o seu CEP antes de fechar.')
        if first['opinioes'] < 600:
            cautions.append(f'Tem menos opiniões ({number(first["opinioes"])}) que outros itens: leia as avaliações recentes.')
        result.append({'ids': ids, 'group': group, 'name': name, 'why': why, 'caution': ' '.join(cautions), 'price': min(item['preco'] for item in group), 'nota': first['nota'], 'opinioes': first['opinioes'], 'vendidos': first['vendidos'], 'para': PARA[ids[0]], 'consultado': first['consultado'], 'img': first.get('img')})
    # A ordem declarada na pagina: mais opinioes primeiro.
    return sorted(result, key=lambda entry: -entry['opinioes'])


def link(url, label, cls='btn'):
    return f'<a class="{cls}" href="{esc(url)}" target="_blank" rel="sponsored nofollow noopener noreferrer">{label}</a>'


def render_item(position, entry, spec, badge):
    anchor = f'item-{position}'
    if entry['img']:
        image = f'<img class="shot" src="{esc(entry["img"])}" width="640" height="800" loading="lazy" decoding="async" referrerpolicy="no-referrer" alt="{esc(entry["name"])}">'
    else:
        image = f'<img src="../assets/listas/{entry["ids"][0]}.webp" width="640" height="800" loading="lazy" decoding="async" alt="{esc(entry["name"])}">'
    facts = [f'<li><strong>{money(entry["price"])}</strong> em {entry["consultado"]}</li>', f'<li>Nota <strong>{note(entry["nota"])}</strong> de 5</li>']
    proof = f'{number(entry["opinioes"])} pessoas já avaliaram'
    if entry['vendidos']:
        proof += f' · {sold(entry["vendidos"])}'
    if len(entry['group']) > 1:
        buttons = link(entry['group'][0]['link'], 'Ver o rosa no Mercado Livre') + link(entry['group'][1]['link'], 'Ver o preto no Mercado Livre', 'btn ghost')
    else:
        buttons = link(entry['group'][0]['link'], 'Ver o preço de hoje no Mercado Livre')
    caution = f'<p><strong>Vale saber:</strong> {esc(entry["caution"])}</p>' if entry['caution'] else ''
    tag = f'<span class="rank-badge">{badge}</span>' if badge else ''
    spare = spec['limit'] - entry['price']
    room = f'<li>Sobram <strong>{money(spare)}</strong> do limite</li>' if spare >= 5 else ''
    return (f'<section class="rank-item" id="{anchor}">{image}'
            f'<div>{tag}<h3><span class="rank-num">{position}.</span>{esc(entry["name"])}</h3><p class="rank-proof">{proof}</p><ul class="rank-facts">{"".join(facts)}{room}</ul>'
            f'<p><strong>Combina com:</strong> {esc(entry["para"])}.</p><p><strong>Por que está na lista:</strong> {esc(entry["why"])}</p>{caution}{buttons}'
            f'<p class="rank-safe">Você confere preço, frete e prazo antes de pagar.</p></div></section>')


def render_own(key):
    image, alt, title, text, links = OWN[key]
    anchors = ''.join(f'<a href="{esc(url)}">{esc(label)} →</a>' for label, url in links)
    return f'<aside class="own-pick" aria-label="Da Bordô"><img src="{image}" width="640" height="800" loading="lazy" decoding="async" alt="{esc(alt)}"><div><h3>{esc(title)}</h3><p>{esc(text)}</p>{anchors}</div></aside>'


def faq(spec, items):
    cheapest = min(items, key=lambda e: e['price'])
    most = max(items, key=lambda e: e['opinioes'])
    lowest = min(e['nota'] for e in items)
    return [
        ('Qual é o item mais barato da lista?', f'{cheapest["name"]}, por {money(cheapest["price"])} na consulta de {CHECKED}.'),
        ('Qual é o item mais bem avaliado em volume?', f'{most["name"]}, com nota {note(most["nota"])} em {number(most["opinioes"])} opiniões no Mercado Livre.'),
        ('Como a lista foi montada?', f'Selecionamos produtos com nota {note(lowest)} ou mais no Mercado Livre e ordenamos pelo número de opiniões de compradores. Não testamos fisicamente os produtos: os dados vêm dos anúncios, consultados em {CHECKED}.'),
        ('Os preços ainda valem?', f'Os preços foram consultados em {CHECKED} e mudam com frequência. Preço, frete e prazo finais são os que aparecem no Mercado Livre na hora da compra.'),
        ('A Bordô vende esses produtos?', 'Não. A compra é feita no Mercado Livre e, em uma compra elegível, a Bordô pode receber comissão. A Bordô faz laços e bordados personalizados por encomenda, em Teixeiras, MG.'),
    ]


def page(spec, template):
    slug, url = spec['slug'], f'{BASE}/blog/{spec["slug"]}/'
    items = entries(spec)
    assert all(e['price'] <= spec['limit'] for e in items), slug
    assert int(spec['h1'].split()[0]) == len(items), slug
    cover = f'{BASE}/blog/assets/listas/{spec["cover"]}'
    style = template[template.index('<style>'):template.index('</style>')] + EXTRA_CSS + '</style>'
    header = template[template.index('<body>') + 6:template.index('<main')]
    footer = template[template.index('<footer'):]
    questions = faq(spec, items)
    others = [other for other in LISTS if other['slug'] != slug]
    graph = [
        {'@type': 'Organization', '@id': f'{BASE}/#organization', 'name': 'Bordô - Bordados Personalizados', 'url': f'{BASE}/', 'logo': {'@type': 'ImageObject', 'url': f'{BASE}/assets/brand-logo.png'}, 'sameAs': ['https://www.instagram.com/bordobordadospersonalizados/']},
        {'@type': 'WebSite', '@id': f'{BASE}/#website', 'name': 'Bordô - Bordados Personalizados', 'url': f'{BASE}/', 'inLanguage': 'pt-BR', 'publisher': {'@id': f'{BASE}/#organization'}},
        {'@type': 'BreadcrumbList', '@id': f'{url}#breadcrumbs', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Bordô', 'item': f'{BASE}/'}, {'@type': 'ListItem', 'position': 2, 'name': 'Casa & Inspiração', 'item': f'{BASE}/blog/'}, {'@type': 'ListItem', 'position': 3, 'name': spec['h1'], 'item': url}]},
        {'@type': 'BlogPosting', '@id': f'{url}#article', 'headline': spec['h1'], 'name': spec['h1'], 'description': spec['description'], 'url': url, 'mainEntityOfPage': {'@type': 'WebPage', '@id': url}, 'inLanguage': 'pt-BR', 'datePublished': PUBLISHED, 'dateModified': PUBLISHED, 'isPartOf': {'@id': f'{BASE}/#website'}, 'author': {'@id': f'{BASE}/#organization'}, 'publisher': {'@id': f'{BASE}/#organization'}, 'breadcrumb': {'@id': f'{url}#breadcrumbs'}, 'image': [cover], 'articleSection': spec['section']},
        {'@type': 'ItemList', '@id': f'{url}#lista', 'name': spec['h1'], 'numberOfItems': len(items), 'itemListOrder': 'https://schema.org/ItemListOrderDescending', 'itemListElement': [{'@type': 'ListItem', 'position': index, 'name': entry['name'], 'url': f'{url}#item-{index}'} for index, entry in enumerate(items, 1)]},
        {'@type': 'FAQPage', '@id': f'{url}#faq', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in questions]},
    ]
    head = (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#631f35">'
            f'<meta name="robots" content="index,follow,max-image-preview:large"><title>{esc(spec["title"])}</title><meta name="description" content="{esc(spec["description"])}">'
            f'<link rel="canonical" href="{url}"><meta property="og:type" content="article"><meta property="og:locale" content="pt_BR"><meta property="og:title" content="{esc(spec["h1"])}">'
            f'<meta property="og:description" content="{esc(spec["description"])}"><meta property="og:url" content="{url}"><meta property="og:image" content="{cover}"><meta name="twitter:card" content="summary_large_image">'
            f'<link rel="icon" href="{BASE}/assets/brand-logo.png" type="image/png"><link rel="alternate" type="application/rss+xml" title="Bordô | Casa &amp; Inspiração" href="../feed.xml">'
            f'{style}<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))}</script></head>')
    rows = ''.join(f'<tr><td>{index}</td><td><a href="#item-{index}">{esc(entry["name"])}</a></td><td>{money(entry["price"])}</td><td>{note(entry["nota"])} ({number(entry["opinioes"])})</td></tr>' for index, entry in enumerate(items, 1))
    cheapest = min(range(len(items)), key=lambda i: items[i]['price'])
    most = max(range(len(items)), key=lambda i: items[i]['opinioes'])
    highlights_unused = (f'<div class="highlights"><a href="#item-{most + 1}"><strong>Mais avaliado</strong>{esc(items[most]["name"])}, com {number(items[most]["opinioes"])} opiniões</a>'
                  f'<a href="#item-{cheapest + 1}"><strong>Mais barato</strong>{esc(items[cheapest]["name"])}, por {money(items[cheapest]["price"])}</a></div>')
    sold_rank = max(range(len(items)), key=lambda i: (int(items[i]['vendidos'].replace('mil', '000') or 0), items[i]['opinioes']))
    badges = {most: 'Escolha segura: o mais avaliado', cheapest: 'O mais barato da lista'}
    badges.setdefault(sold_rank, 'Um dos mais vendidos')
    item = lambda index, entry: render_item(index, entry, spec, badges.get(index - 1))
    body_items = ''.join(item(index, entry) for index, entry in enumerate(items, 1))
    safe = items[most]
    decide = (f'<div class="decide"><p class="decide-count" id="natalCount" hidden></p><h2>Sem tempo? Vá direto nestes dois</h2>'
              f'<p><strong>Na dúvida, escolha: {esc(safe["name"])}.</strong> É o item que mais gente já avaliou nesta lista: {number(safe["opinioes"])} opiniões, nota {note(safe["nota"])}. '
              f'Com o orçamento apertado, vá de {esc(items[cheapest]["name"])}, por {money(items[cheapest]["price"])}.</p>'
              f'<div class="share-row"><a class="btn" href="#item-{most + 1}">Ver a escolha segura</a><a class="btn ghost" href="#item-{cheapest + 1}">Ver o mais barato</a></div></div>')
    countdown = COUNTDOWN
    share = 'https://wa.me/?text=' + quote(f'{spec["h1"]}: {url}')
    faq_html = ''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in questions)
    more = ''.join(f'<a href="../{other["slug"]}/">{esc(other["h1"])} →</a>' for other in others)
    cards = ''.join(f'<article class="card"><a href="../{other["slug"]}/"><img class="card-image" src="../assets/listas/{other["cover"]}" width="1500" height="780" loading="lazy" decoding="async" alt=""><div class="card-content"><h3>{esc(other["h1"])}</h3><p>{esc(other["lead"])}</p><span class="more">Ver a lista →</span></div></a></article>' for other in others[:2])
    main = (f'<main id="conteudo"><section class="article-hero"><div class="container"><nav class="breadcrumbs" aria-label="Você está aqui"><a href="{BASE}/">Bordô</a> / <a href="../">Casa &amp; Inspiração</a> / <span aria-current="page">{esc(spec["h1"])}</span></nav>'
            f'<h1>{esc(spec["h1"])}</h1><p class="lead">{esc(spec["lead"])}</p><div class="meta"><span>Atualizado em {PUBLISHED_TEXT}</span><span>{len(items)} itens</span><span>Por Bordô | Casa &amp; Inspiração</span></div>'
            f'<img class="cover" fetchpriority="high" decoding="async" src="../assets/listas/{spec["cover"]}" width="1500" height="780" alt="Quatro itens desta lista"></div></section>'
            f'<div class="container article-layout"><article class="article-content"><section class="answer-first" aria-label="Resposta resumida"><h2>A lista em um minuto</h2><p>{esc(spec["intro"])}</p></section>'
            f'<div class="editorial-note"><strong>Publicidade e método.</strong> Os links levam ao Mercado Livre e, em uma compra elegível, a Bordô poderá receber comissão. Não testamos fisicamente os produtos: preço, nota e número de opiniões vêm dos anúncios, consultados em {CHECKED}, e podem mudar. <a href="../como-selecionamos/">Saiba como selecionamos.</a></div>'
            f'{decide}<div class="rank-wrap"><table class="rank-table"><caption class="sr-only">Resumo da lista</caption><thead><tr><th scope="col">Nº</th><th scope="col">Produto</th><th scope="col">Preço</th><th scope="col">Nota (opiniões)</th></tr></thead><tbody>{rows}</tbody></table></div>'
            f'<h2 id="lista">Os {len(items)} itens, um a um</h2>{body_items}'
            f'<div class="decide closing"><h2>Ainda em dúvida?</h2><p>Volte ao item {most + 1}: {esc(safe["name"])}. Foi o que mais gente avaliou nesta lista. Ou guarde a lista para decidir depois.</p><div class="share-row"><a class="btn" href="#item-{most + 1}">Voltar à escolha segura</a><a class="btn ghost" href="{esc(share)}" target="_blank" rel="noopener noreferrer">Guardar a lista no WhatsApp</a></div></div>'
            f'<h2 id="faq">Perguntas frequentes</h2><div class="faq-list">{faq_html}</div>'
            f'<div class="share-row"><a class="btn" href="{esc(share)}" target="_blank" rel="noopener noreferrer">Enviar esta lista pelo WhatsApp</a><a class="btn ghost" href="#lista">Voltar ao início da lista</a></div></article>'
            f'<aside class="sidebar"><div class="side-sticky"><div class="side-card"><h3>Outras listas</h3>{more}</div><div class="side-card"><h3>Da Bordô para presentear</h3><p>Laços e naninhas bordados por encomenda, em Teixeiras, MG.</p><a href="{BASE}/#colinho">Naninhas Colinho do Céu →</a><a href="{BASE}/#rainha">Laços Mãe &amp; Rainha →</a><a href="{BASE}/#personalizados">Encomendar um bordado →</a></div></div></aside></div></main>'
            f'<section class="related"><div class="container"><div class="section-head"><h2>Continue escolhendo</h2></div><div class="cards">{cards}</div></div></section>')
    return head + '<body>' + header + main + countdown + footer


def main():
    template = (BLOG / 'decoracao-de-natal-crista/index.html').read_text(encoding='utf-8')
    if '.sr-only' not in template:
        global EXTRA_CSS
        EXTRA_CSS += '.sr-only{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}\n'
    for spec in LISTS:
        target = BLOG / spec['slug'] / 'index.html'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page(spec, template) + '\n', encoding='utf-8')
        print('gerado', target.relative_to(ROOT))


if __name__ == '__main__':
    main()
