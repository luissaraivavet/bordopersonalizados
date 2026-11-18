"""Gera os guias de lista do blog (blog/<slug>/index.html).

Uso:
    python scripts/gerar_listas_blog.py

Le scripts/dados_listas_blog.json (produtos de afiliado com nota, opinioes,
preco e link) e monta cada pagina com o visual de blog/assets/revista.css,
que usa os tokens da pagina principal. As fotos geradas ficam em
blog/assets/listas/; itens com o campo img usam a foto do anuncio. Edite os
dados ou os textos deste arquivo e rode de novo; nao edite o HTML gerado.
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
STYLE_VERSION = '20261118b'

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

LISTS = [
    {
        'slug': 'presentes-ate-50-reais', 'em': 'amigo secreto', 'cover': 'capa-ate-50.webp', 'section': 'Presentes', 'own': 'laco', 'limit': 50,
        'h1': '10 presentes até R$ 50 para o amigo secreto de 2026',
        'title': '10 presentes até R$ 50 para amigo secreto (2026) | Bordô',
        'card': 'Lista de presentes · até R$ 50',
        'description': 'Lista com 10 presentes até R$ 50 para amigo secreto e lembranças de Natal: copo térmico, fone, jogo, garrafa, pantufa e mais, com nota e preço.',
        'lead': 'Dez ideias que cabem no limite do amigo secreto, todas com nota 4,8 ou mais no Mercado Livre. Em menos de dois minutos você sai com o presente decidido.',
        'intro': 'O limite de R$ 50 é o mais comum nos sorteios de fim de ano, e é também onde mais se erra por pressa. Esta lista junta o que encontramos nessa faixa com muitas avaliações de compradores.',
        'items': ['A012+A013', 'A015', 'A018', 'A010', 'A017', 'A016', 'A026', 'A002', 'A014', 'B001'],
    },
    {
        'slug': 'presentes-para-homem', 'em': 'homem', 'cover': 'capa-homem.webp', 'section': 'Presentes', 'own': 'encomenda', 'limit': 150,
        'h1': '10 presentes para homem até R$ 150 no Natal de 2026',
        'title': '10 presentes para homem até R$ 150 (Natal 2026) | Bordô',
        'card': 'Lista de presentes · para ele',
        'description': 'Lista com 10 presentes para homem até R$ 150: perfume, fones sem fio, power bank, garrafas térmicas, carteira, kit churrasco e mais, com nota e preço.',
        'lead': 'Dez presentes para pai, marido, namorado ou amigo, de R$ 42,99 a R$ 149, todos com nota 4,8 ou mais no Mercado Livre.',
        'intro': 'Presente para homem costuma travar na mesma dúvida: o que ele ainda não tem? Esta lista foge do óbvio com itens de uso diário e muitas avaliações de compradores.',
        'items': ['A004', 'A001', 'A003', 'A006', 'A002', 'A005', 'B002', 'B003', 'B004', 'B005'],
    },
    {
        'slug': 'presentes-para-mulher', 'em': 'mulher', 'cover': 'capa-mulher.webp', 'section': 'Presentes', 'own': 'rainha', 'limit': 100,
        'h1': '10 presentes para mulher até R$ 100 no Natal de 2026',
        'title': '10 presentes para mulher até R$ 100 (Natal 2026) | Bordô',
        'card': 'Lista de presentes · para ela',
        'description': 'Lista com 10 presentes para mulher até R$ 100: perfumes Natura e O Boticário, copo térmico, difusor, necessaires, massageador e mais, com nota e preço.',
        'lead': 'Dez presentes para mãe, esposa, namorada ou amiga, de R$ 29 a R$ 94, todos com nota 4,8 ou mais no Mercado Livre.',
        'intro': 'Esta lista mistura cuidado pessoal, bem-estar e utilidade, sempre abaixo de R$ 100 e com muitas avaliações de compradores.',
        'items': ['A012', 'A008', 'A010', 'A007', 'A011', 'A009', 'B006', 'B007', 'B008', 'B009'],
    },
    {
        'slug': 'presentes-para-familia-e-criancas', 'em': 'família', 'cover': 'capa-familia.webp', 'section': 'Presentes', 'own': 'naninha', 'limit': 180,
        'h1': '10 presentes para a família e as crianças até R$ 180',
        'title': '10 presentes para a família e crianças até R$ 180 | Bordô',
        'card': 'Lista de presentes · família',
        'description': 'Lista com 10 presentes para a família e as crianças: War, Banco Imobiliário, Detetive, umidificadores, Galaxy Fit3, Hot Wheels e mais, com nota e preço.',
        'lead': 'Dez presentes para a casa inteira aproveitar, de R$ 48 a R$ 179, todos com nota 4,8 ou mais no Mercado Livre.',
        'intro': 'Presente para a família funciona quando todo mundo usa. Por isso a lista começa nos jogos de tabuleiro e passa por itens para a casa e brinquedos.',
        'items': ['A024', 'A025', 'A022', 'A023', 'A020', 'A021', 'A026', 'A019', 'B010', 'B011'],
    },
    {
        'slug': 'enfeites-de-natal-ate-70-reais', 'em': 'Natal', 'cover': 'capa-enfeites.webp', 'section': 'Decoração de Natal', 'own': 'naninha', 'limit': 70,
        'h1': '5 enfeites de Natal até R$ 70 para porta, parede e árvore',
        'title': '5 enfeites de Natal até R$ 70: porta, parede e árvore | Bordô',
        'card': 'Lista de decoração · até R$ 70',
        'description': 'Lista com 5 enfeites de Natal até R$ 70: cortina de LED, gancho e guirlanda para porta, laços para a árvore e vila natalina, com nota e preço.',
        'lead': 'Cinco enfeites para decorar a casa gastando pouco, de R$ 27,97 a R$ 69,90, com nota 4,5 ou mais no Mercado Livre.',
        'intro': 'Dá para mudar a cara da casa no Natal com poucas peças bem escolhidas: uma luz de fundo, a porta arrumada e um detalhe na árvore.',
        'items': ['P005', 'P003', 'P001', 'P004', 'P002'],
    },
]

esc = html.escape

SCRIPT = """<script>(function(){
var menu=document.getElementById('menu'),root=document.documentElement,data=JSON.parse(document.getElementById('listData').textContent),stage=document.getElementById('stage'),index=document.getElementById('index'),grid=document.getElementById('pieces');
var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches,current=Number(stage.dataset.current),timer=null,swap=null;
function q(id){return document.getElementById(id);}
function fill(i){var d=data[i],img=q('stageImg');img.src=d.img;img.alt=d.name;img.className=d.shot?'shot':'';q('stagePhoto').href=d.link;q('stageStep').textContent=(d.badge?d.badge+' \\u00b7 ':'')+'item '+d.pos+' de '+data.length;q('stageName').textContent=d.name;q('stageProof').textContent=d.proof;q('stagePara').textContent='Combina com '+d.para+'.';q('stagePrice').firstChild.textContent=d.price;q('stageDate').textContent='em '+d.date;q('stageLink').href=d.link;
[index,menu].forEach(function(g){g.querySelectorAll('button').forEach(function(b,k){b.setAttribute('aria-pressed',String(k===i));});});}
function show(i){current=i;clearTimeout(swap);if(reduce){fill(i);return;}new Image().src=data[i].img;stage.classList.add('is-changing');swap=setTimeout(function(){fill(i);void stage.offsetWidth;stage.classList.remove('is-changing');},520);}
function stop(){clearInterval(timer);timer=null;}
index.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;stop();show(Number(b.dataset.i));});var hover=null;menu.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;stop();show(Number(b.dataset.i));});menu.addEventListener('pointerover',function(e){var b=e.target.closest('button');if(!b||e.pointerType!=='mouse')return;stop();clearTimeout(hover);hover=setTimeout(function(){if(Number(b.dataset.i)!==current)show(Number(b.dataset.i));},120);});menu.addEventListener('focusin',function(e){var b=e.target.closest('button');if(!b)return;stop();if(Number(b.dataset.i)!==current)show(Number(b.dataset.i));});
stage.addEventListener('pointerenter',stop);stage.addEventListener('focusin',stop);
if(!reduce&&data.length>1){timer=setInterval(function(){if(document.hidden)return;show((current+1)%data.length);},5200);}
q('sort').addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;var group=this;
function apply(){group.querySelectorAll('button').forEach(function(x){x.setAttribute('aria-pressed',String(x===b));});var k=b.dataset.sort,cards=[].slice.call(grid.children);
cards.sort(function(a,c){return k==='price'?a.dataset.price-c.dataset.price:k==='sold'?(c.dataset.sold-a.dataset.sold||c.dataset.reviews-a.dataset.reviews):a.dataset.pos-c.dataset.pos;});cards.forEach(function(c){c.classList.add('is-in');grid.appendChild(c);});}
if(document.startViewTransition&&!reduce){document.startViewTransition(apply);}else{apply();}});
if('IntersectionObserver' in window){root.classList.add('js');var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('is-in');io.unobserve(e.target);}});},{rootMargin:'0px 0px -8% 0px'});[].forEach.call(grid.children,function(c){io.observe(c);});}
var n=new Date(),d=new Date(n.getFullYear(),11,25),k=Math.ceil((d-n)/864e5),c=q('natalCount');if(c&&k>0){c.textContent=(k===1?'Falta 1 dia':'Faltam '+k+' dias')+' para o Natal. Quanto antes pedir, mais folga no prazo.';c.hidden=false;}
})();</script>"""


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


def sold_number(value):
    return int(value.replace('mil', '000') or 0)


def short_date(text):
    return text.replace(' de novembro de 2026', '/11')


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
        result.append({'ids': ids, 'group': group, 'name': name, 'why': why, 'caution': ' '.join(cautions), 'price': min(item['preco'] for item in group),
                       'nota': first['nota'], 'opinioes': first['opinioes'], 'vendidos': first['vendidos'], 'para': PARA[ids[0]], 'consultado': first['consultado'], 'img': first.get('img')})
    # A ordem declarada na pagina: mais opinioes primeiro.
    return sorted(result, key=lambda entry: -entry['opinioes'])


def image_of(entry):
    return entry['img'] or f'../assets/listas/{entry["ids"][0]}.webp'


def proof_of(entry):
    text = f'Nota {note(entry["nota"])} em {number(entry["opinioes"])} avaliações'
    return text + (f' · {sold(entry["vendidos"])}' if entry['vendidos'] else '')


AFF = 'target="_blank" rel="sponsored nofollow noopener noreferrer"'
ARROW = '<img class="icon" src="/assets/icons/arrow-up-right.svg" alt="">'


def render_piece(position, entry, badge):
    shot = ' class="shot"' if entry['img'] else ''
    refer = ' referrerpolicy="no-referrer"' if entry['img'] else ''
    first = entry['group'][0]['link']
    tag = f'<span class="badge">{badge}</span>' if badge else ''
    alt = f'<a class="alt" href="{esc(entry["group"][1]["link"])}" {AFF}>Ver também em preto</a>' if len(entry['group']) > 1 else ''
    caution = f'<p><strong>Vale saber:</strong> {esc(entry["caution"])}</p>' if entry['caution'] else ''
    return (f'<article class="piece" id="item-{position}" style="view-transition-name:piece-{position}" data-pos="{position}" data-price="{entry["price"]}" data-reviews="{entry["opinioes"]}" data-sold="{sold_number(entry["vendidos"])}">'
            f'<a class="ph" href="{esc(first)}" {AFF} aria-label="{esc(entry["name"])}: ver no Mercado Livre"><img{shot} src="{esc(image_of(entry))}" width="640" height="800" loading="lazy" decoding="async"{refer} alt="{esc(entry["name"])}">{tag}</a>'
            f'<div class="meta"><span class="num" aria-hidden="true">{position:02d}</span><h3>{esc(entry["name"])}</h3><p class="proof">{proof_of(entry)}</p>'
            f'<p class="price">{money(entry["price"])}<small>em {short_date(entry["consultado"])}</small></p>'
            f'<a class="go" href="{esc(first)}" {AFF}>Ver o preço de hoje {ARROW}</a>{alt}'
            f'<details class="more"><summary>Por que entrou na lista</summary><p><strong>Combina com:</strong> {esc(entry["para"])}.</p><p>{esc(entry["why"])}</p>{caution}</details></div></article>')


def faq(spec, items):
    cheapest = min(items, key=lambda e: e['price'])
    most = max(items, key=lambda e: e['opinioes'])
    lowest = min(e['nota'] for e in items)
    return [
        ('Qual é o item mais barato da lista?', f'{cheapest["name"]}, por {money(cheapest["price"])} na consulta de {cheapest["consultado"]}.'),
        ('Qual é o item mais bem avaliado em volume?', f'{most["name"]}, com nota {note(most["nota"])} em {number(most["opinioes"])} opiniões no Mercado Livre.'),
        ('Como a lista foi montada?', f'Selecionamos produtos com nota {note(lowest)} ou mais no Mercado Livre e ordenamos pelo número de opiniões de compradores. Não testamos fisicamente os produtos: os dados vêm dos anúncios, consultados em {CHECKED}.'),
        ('Os preços ainda valem?', f'Os preços foram consultados em {CHECKED} e mudam com frequência. Preço, frete e prazo finais são os que aparecem no Mercado Livre na hora da compra.'),
        ('A Bordô vende esses produtos?', 'Não. A compra é feita no Mercado Livre e, em uma compra elegível, a Bordô pode receber comissão. A Bordô faz laços e bordados personalizados por encomenda, em Teixeiras, MG.'),
    ]


HEADER = (f'<a class="skip" href="#conteudo">Pular para o conteúdo</a><header class="mast"><div class="wrap"><a class="mast-logo" href="{BASE}/" aria-label="Bordô, página inicial">'
          '<img src="/assets/brand-logo-491.png" width="491" height="200" alt="Bordô — Bordados personalizados"></a>'
          f'<nav class="mast-nav" aria-label="Navegação principal"><a href="../">Casa &amp; Inspiração</a><a href="{BASE}/">Loja Bordô</a><a href="{BASE}/#personalizados">Personalizados</a><a href="../como-selecionamos/">Critérios</a></nav></div></header>')

FOOTER = (f'<footer class="foot"><div class="wrap"><div class="foot-main"><div><a class="foot-home" href="{BASE}/" aria-label="Bordô, página inicial"><img class="foot-logo" src="/assets/brand-logo-491.png" width="491" height="200" alt="Bordô — Bordados personalizados" loading="lazy"></a>'
          '<p>Um nome, uma lembrança, uma ideia. O próximo bordado pode começar com você.</p></div>'
          '<div><h3>Casa &amp; Inspiração</h3><a href="../">Todos os artigos</a><a href="../decoracao-de-natal-crista/">Natal com fé</a><a href="../arvore-de-natal-elegante-gastando-pouco/">Árvore de Natal elegante</a><a href="../como-selecionamos/">Como selecionamos</a><a href="../feed.xml">Acompanhar artigos (RSS)</a></div>'
          f'<div><h3>Bordô</h3><a href="{BASE}/">Loja de bordados personalizados</a><a href="{BASE}/#colinho">Naninhas Colinho do Céu</a><a href="{BASE}/#rainha">Laços Mãe &amp; Rainha</a><a href="{BASE}/presentes-personalizados/">Presentes personalizados</a><a href="https://www.instagram.com/bordobordadospersonalizados/" target="_blank" rel="noopener noreferrer">Instagram</a></div></div>'
          '<div class="foot-bottom">Bordô. Bordados personalizados, por encomenda, em Teixeiras, MG. Conteúdo com links comerciais identificados.</div></div></footer>')


def page(spec):
    slug, url = spec['slug'], f'{BASE}/blog/{spec["slug"]}/'
    items = entries(spec)
    assert all(e['price'] <= spec['limit'] for e in items), slug
    figure, _, rest = spec['h1'].partition(' ')
    assert int(figure) == len(items), slug
    cover = f'{BASE}/blog/assets/listas/{spec["cover"]}'
    questions = faq(spec, items)
    others = [other for other in LISTS if other['slug'] != slug]
    cheapest = min(range(len(items)), key=lambda i: items[i]['price'])
    most = max(range(len(items)), key=lambda i: items[i]['opinioes'])
    sold_rank = max(range(len(items)), key=lambda i: (sold_number(items[i]['vendidos']), items[i]['opinioes']))
    badges = {most: 'Escolha segura', cheapest: 'O mais barato'}
    badges.setdefault(sold_rank, 'Um dos mais vendidos')
    graph = [
        {'@type': 'Organization', '@id': f'{BASE}/#organization', 'name': 'Bordô - Bordados Personalizados', 'url': f'{BASE}/', 'logo': {'@type': 'ImageObject', 'url': f'{BASE}/assets/brand-logo.png'}, 'sameAs': ['https://www.instagram.com/bordobordadospersonalizados/']},
        {'@type': 'WebSite', '@id': f'{BASE}/#website', 'name': 'Bordô - Bordados Personalizados', 'url': f'{BASE}/', 'inLanguage': 'pt-BR', 'publisher': {'@id': f'{BASE}/#organization'}},
        {'@type': 'BreadcrumbList', '@id': f'{url}#breadcrumbs', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Bordô', 'item': f'{BASE}/'}, {'@type': 'ListItem', 'position': 2, 'name': 'Casa & Inspiração', 'item': f'{BASE}/blog/'}, {'@type': 'ListItem', 'position': 3, 'name': spec['h1'], 'item': url}]},
        {'@type': 'BlogPosting', '@id': f'{url}#article', 'headline': spec['h1'], 'name': spec['h1'], 'description': spec['description'], 'url': url, 'mainEntityOfPage': {'@type': 'WebPage', '@id': url}, 'inLanguage': 'pt-BR', 'datePublished': PUBLISHED, 'dateModified': PUBLISHED, 'isPartOf': {'@id': f'{BASE}/#website'}, 'author': {'@id': f'{BASE}/#organization'}, 'publisher': {'@id': f'{BASE}/#organization'}, 'breadcrumb': {'@id': f'{url}#breadcrumbs'}, 'image': [cover], 'articleSection': spec['section']},
        {'@type': 'ItemList', '@id': f'{url}#lista', 'name': spec['h1'], 'numberOfItems': len(items), 'itemListOrder': 'https://schema.org/ItemListOrderDescending', 'itemListElement': [{'@type': 'ListItem', 'position': index, 'name': entry['name'], 'url': f'{url}#item-{index}'} for index, entry in enumerate(items, 1)]},
        {'@type': 'FAQPage', '@id': f'{url}#faq', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in questions]},
    ]
    stage_data = [{'pos': index, 'name': entry['name'], 'img': image_of(entry), 'shot': bool(entry['img']), 'price': money(entry['price']), 'date': short_date(entry['consultado']), 'proof': proof_of(entry), 'para': entry['para'], 'link': entry['group'][0]['link'], 'badge': badges.get(index - 1, '')} for index, entry in enumerate(items, 1)]
    first = stage_data[most]
    first_shot = ' class="shot"' if first['shot'] else ''
    preload = '' if first['shot'] else f'<link rel="preload" as="image" href="{esc(first["img"])}" fetchpriority="high">'
    head = (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#631f35">'
            f'<meta name="robots" content="index,follow,max-image-preview:large"><title>{esc(spec["title"])}</title><meta name="description" content="{esc(spec["description"])}">'
            f'<link rel="canonical" href="{url}"><meta property="og:type" content="article"><meta property="og:locale" content="pt_BR"><meta property="og:title" content="{esc(spec["h1"])}">'
            f'<meta property="og:description" content="{esc(spec["description"])}"><meta property="og:url" content="{url}"><meta property="og:image" content="{cover}"><meta name="twitter:card" content="summary_large_image">'
            f'<link rel="icon" href="/assets/brand-logo-491.png" type="image/png"><link rel="alternate" type="application/rss+xml" title="Bordô | Casa &amp; Inspiração" href="../feed.xml">'
            f'<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/CormorantGaramond.woff2" crossorigin>{preload}'
            f'<link rel="stylesheet" href="/assets/tokens.css"><link rel="stylesheet" href="/assets/base.css"><link rel="stylesheet" href="/assets/acabamento.css?v=20261118"><link rel="stylesheet" href="../assets/revista.css?v={STYLE_VERSION}">'
            f'<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))}</script></head>')
    thumbs = ''.join(f'<button type="button" data-i="{index}" aria-pressed="{str(index == most).lower()}" aria-label="Destacar o item {d["pos"]}: {esc(d["name"])}" title="{esc(d["name"])}"><img{" class=\"shot\"" if d["shot"] else ""} src="{esc(d["img"])}" width="128" height="128" loading="lazy" decoding="async" referrerpolicy="no-referrer" alt="">{d["pos"]:02d}</button>' for index, d in enumerate(stage_data))
    word = spec['em']
    title_html = esc(rest).replace(esc(word), f'<em>{esc(word)}</em>', 1)
    menu = ''.join(f'<li><button type="button" data-i="{index}" aria-pressed="{str(index == most).lower()}"><span class="menu-num">{d["pos"]:02d}</span><span class="menu-name">{esc(d["name"])}</span><span class="menu-dots" aria-hidden="true"></span><span class="menu-price">{d["price"]}</span></button></li>' for index, d in enumerate(stage_data))
    pieces = ''.join(render_piece(index, entry, badges.get(index - 1)) for index, entry in enumerate(items, 1))
    share = 'https://wa.me/?text=' + quote(f'{spec["h1"]}: {url}')
    chevron = '<img class="icon" src="/assets/icons/chevron-down.svg" alt="">'
    faq_html = ''.join(f'<details><summary>{esc(q)}{chevron}</summary><p>{esc(a)}</p></details>' for q, a in questions)
    rows = ''.join(f'<a class="row" href="../{other["slug"]}/"><img src="../assets/listas/{other["cover"]}" width="320" height="208" loading="lazy" decoding="async" alt=""><div><strong>{esc(other["h1"])}</strong><span>{esc(other["lead"])}</span></div><img class="icon" src="/assets/icons/arrow-right.svg" alt=""></a>' for other in others)
    safe = items[most]
    body = (f'<body>{HEADER}<main id="conteudo"><section class="cover"><div class="wrap"><nav class="crumbs" aria-label="Você está aqui"><a href="{BASE}/">Bordô</a> / <a href="../">Casa &amp; Inspiração</a></nav>'
            f'<div class="cover-grid"><div><h1><span class="fig">{figure}</span> {title_html}</h1><p class="lead">{esc(spec["lead"])}</p><p class="count" id="natalCount" hidden></p>'
            f'<p class="ad-note">Publicidade: links de afiliado do Mercado Livre; a Bordô pode receber comissão. Preços e notas de {CHECKED}, sujeitos a alteração. <a href="../como-selecionamos/">Critérios</a>.</p></div>'
            f'<div class="stage" id="stage" data-current="{most}"><a class="stage-photo" id="stagePhoto" href="{esc(first["link"])}" {AFF}><img id="stageImg"{first_shot} src="{esc(first["img"])}" width="640" height="800" fetchpriority="high" decoding="async" referrerpolicy="no-referrer" alt="{esc(first["name"])}"></a>'
            f'<div class="stage-info"><p class="stage-step" id="stageStep">{first["badge"]} · item {first["pos"]} de {len(items)}</p><h2 id="stageName">{esc(first["name"])}</h2><p class="proof" id="stageProof">{first["proof"]}</p>'
            f'<p class="stage-para" id="stagePara">Combina com {esc(first["para"])}.</p><p class="price" id="stagePrice">{first["price"]}<small id="stageDate">em {first["date"]}</small></p>'
            f'<a class="button" id="stageLink" href="{esc(first["link"])}" {AFF}>Ver o preço de hoje {ARROW}</a><p class="safe">Você confere preço, frete e prazo antes de pagar.</p></div></div></div>'
            f'<div class="index" id="index" role="group" aria-label="Itens da lista">{thumbs}</div><ol class="menu" id="menu" aria-label="Os itens desta lista">{menu}</ol></div></section><div class="seam" aria-hidden="true"></div>'
            f'<section class="issue" aria-labelledby="lista"><div class="wrap"><div class="issue-head"><h2 id="lista">Os {len(items)} itens</h2><div class="seg" id="sort" role="group" aria-label="Ordenar a lista"><button type="button" data-sort="pos" aria-pressed="true">Mais avaliados</button><button type="button" data-sort="price" aria-pressed="false">Menor preço</button><button type="button" data-sort="sold" aria-pressed="false">Mais vendidos</button></div></div>'
            f'<div class="pieces" id="pieces">{pieces}</div></div></section>'
            f'<section class="band"><div class="wrap"><h2>Ainda em dúvida? Vá de {esc(safe["name"])}.</h2><p>Foi o item que mais gente avaliou nesta lista: {number(safe["opinioes"])} opiniões, nota {note(safe["nota"])}.</p>'
            f'<div class="band-actions"><a class="button" href="#item-{most + 1}">Ver a escolha segura</a><a class="button ghost" href="{esc(share)}" target="_blank" rel="noopener noreferrer">Guardar a lista no WhatsApp</a></div></div></section>'
            f'<div class="wrap split"><h2 id="faq">Perguntas frequentes</h2><div class="faq">{faq_html}</div></div>'
            f'<section class="others"><div class="wrap"><h2>Continue escolhendo</h2>{rows}</div></section></main>{FOOTER}'
            f'<script type="application/json" id="listData">{json.dumps(stage_data, ensure_ascii=False)}</script>{SCRIPT}</body></html>')
    return head + body


def main():
    for spec in LISTS:
        target = BLOG / spec['slug'] / 'index.html'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page(spec) + '\n', encoding='utf-8')
        print('gerado', target.relative_to(ROOT))


if __name__ == '__main__':
    main()
