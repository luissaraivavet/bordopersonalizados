"""Apply the owner's October 2026 prices and product copy, idempotently."""
import copy
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import admin_server as app

COPY = {
    'margarida': ('Laço bordado Encanto de Margarida', 'Margarida branca e borboleta lilás: um laço floral para dar delicadeza ao penteado infantil. O desenho da coleção Jardim de Encantos combina com passeios, fotos e presentes cheios de carinho. Escolha este encanto e confirme o acabamento na encomenda.'),
    'girassol': ('Laço bordado Encanto de Girassol', 'Um girassol amarelo e uma borboleta para iluminar o penteado com um detalhe alegre. Este laço infantil bordado da coleção Jardim de Encantos acompanha combinações leves e ocasiões especiais. Leve um pouco de jardim para o dia a dia ou presenteie com esse desenho.'),
    'rosa': ('Laço bordado Encanto de Rosa', 'Flor rosa e borboleta se encontram neste laço infantil bordado da Jardim de Encantos. Uma escolha delicada para completar o penteado, combinar com produções florais e transformar um presente em uma lembrança especial. Converse com a Bordô sobre o acabamento da sua peça.'),
    'hibisco': ('Laço bordado Encanto de Hibisco', 'Hibisco cor-de-rosa e borboleta dão destaque a este laço floral bordado da Jardim de Encantos. O desenho traz personalidade ao penteado infantil e combina com celebrações, passeios e presentes. Escolha o seu hibisco e confirme os detalhes da peça pelo WhatsApp.'),
    'lavanda': ('Laço bordado Encanto de Lavanda', 'O ramo de lavanda em lilás e a borboleta floral criam uma composição suave para o penteado. Este laço infantil bordado da Jardim de Encantos é uma opção para quem gosta de flores e detalhes delicados. Complete sua coleção ou presenteie alguém com este encanto.'),
    'coruja': ('Laço bordado Corujinha do Sax', 'Uma corujinha tocando saxofone para levar música e personalidade ao penteado infantil. Este laço bordado da coleção Sinfonia das Matas é uma escolha divertida para passeios, festas e presentes. Selecione a opção da peça e monte seu pedido com a Bordô.'),
    'leao': ('Laço bordado Leãozinho do Sax', 'O pequeno leão e seu saxofone transformam este laço infantil bordado em um detalhe cheio de imaginação. Parte da Sinfonia das Matas, o desenho combina com produções divertidas e presentes para quem ama bichinhos. Escolha sua opção e leve esse músico para a sua coleção.'),
    'gato': ('Laço bordado Gatinho do Sax', 'Um gatinho músico para dar charme ao penteado e um toque lúdico à combinação. Este laço infantil bordado da Sinfonia das Matas reúne bichinhos e música em um desenho marcante. Selecione a opção da peça e presenteie ou complete o trio da coleção.')
}

# File, then reading order: upper left, upper right, lower left, lower right.
CHARACTERS = {
    '9888': [('guaxinim', 'Guto', 'Guaxinim', 'descobrir novas melodias'), ('esquilo', 'Nico', 'Esquilo', 'guardar uma nota alegre para cada aventura'), ('lhama', 'Lili', 'Lhama', 'passear com seu cachecol e uma canção'), ('coala', 'Kiko', 'Coala', 'transformar uma pausa em um pequeno concerto')],
    '9889': [('shiba', 'Bento', 'Shiba', 'acompanhar cada passeio com música'), ('feneco', 'Fifi', 'Feneco', 'escutar o mundo com suas grandes orelhas'), ('cervo', 'Theo', 'Cervo', 'encontrar melodias pelos caminhos da mata'), ('lobo', 'Luca', 'Lobo', 'reunir os amigos para tocar')],
    '9891': [('vaquinha', 'Mimosa', 'Vaquinha', 'levar uma canção para a fazendinha'), ('cavalo', 'Tito', 'Cavalinho', 'trocar o galope por um ritmo alegre'), ('boi', 'Bóris', 'Boizinho', 'fazer uma grande entrada com seu pequeno sax'), ('ovelha', 'Lola', 'Ovelhinha', 'espalhar notas doces entre os amigos')],
    '9892': [('jacare', 'Joca', 'Jacaré', 'animar a banda à beira do rio'), ('panda', 'Pipo', 'Panda', 'tocar uma melodia entre uma brincadeira e outra'), ('sapo', 'Zeca', 'Sapinho', 'dar um novo ritmo ao jardim'), ('hipopotamo', 'Hugo', 'Hipopótamo', 'transformar o rio em palco')],
    '9893': [('gato', 'Milo', 'Gatinho', 'ensaiar sua próxima canção de boina'), ('capivara', 'Capi', 'Capivara', 'tocar sem pressa e aproveitar cada nota')],
    '9894': [('coelho', 'Bunny', 'Coelhinho', 'saltar de uma nota para outra'), ('leao', 'Leon', 'Leãozinho', 'comandar a banda com seu chapéu'), ('urso', 'Balu', 'Ursinho', 'abraçar os amigos com uma canção'), ('coruja', 'Olívia', 'Corujinha', 'abrir o concerto quando a mata fica quietinha')],
    '9895': [('porquinho', 'Paco', 'Porquinho', 'dar um toque divertido a cada ensaio'), ('tubarao', 'Maré', 'Tubarão', 'levar o jazz para debaixo d’água'), ('patinho', 'Dudu', 'Patinho', 'marcar o compasso com seus passinhos'), ('lontra', 'Luna', 'Lontrinha', 'brincar com as notas perto do rio')],
    '9896': [('axolote', 'Ari', 'Axolote', 'inventar uma canção cheia de curiosidade'), ('ganso', 'Gigi', 'Ganso', 'chegar elegante para o ensaio'), ('preguica', 'Pérola', 'Preguiça', 'aproveitar a música no seu próprio ritmo'), ('girafa', 'Gabi', 'Girafinha', 'alcançar as notas lá no alto')],
    '9897': [('pinguim', 'Pingo', 'Pinguim', 'aquecer o dia com uma canção'), ('cachorro', 'Biscoito', 'Cachorrinho', 'seguir os amigos em toda aventura musical'), ('raposa', 'Flora', 'Raposinha', 'inventar melodias pelo caminho'), ('dinossauro', 'Dino', 'Dinossauro', 'mostrar que até um pequeno rugido pode virar música')],
}
FLOWERS = {'margarida': ('Daisy', 'Margarida', 'abre o jardim para receber as borboletas'), 'girassol': ('Sol', 'Girassol', 'segue a luz e colore cada passeio'), 'rosa': ('Rosie', 'Rosa', 'guarda um carinho em cada pétala'), 'hibisco': ('Bella', 'Hibisco', 'convida as borboletas para uma dança de cores'), 'lavanda': ('Violeta', 'Lavanda', 'conta histórias entre flores lilás')}


def prepare_photos():
    from PIL import Image
    for filename, characters in CHARACTERS.items():
        with Image.open(Path.home() / 'Downloads' / (filename + '.png')) as photo:
            w, h = photo.size
            for index, (ident, *_rest) in enumerate(characters):
                if len(characters) == 2:
                    bounds = [(0, 0, .57, .74), (.52, .30, 1, 1)]
                else:
                    bounds = [(0, 0, .53, .49), (.50, .075, 1, .59), (0, .40, .53, .96), (.50, .485, 1, 1)]
                left, top, right, bottom = bounds[index]
                box = (int(left*w), int(top*h), int(right*w), int(bottom*h))
                photo.crop(box).convert('RGB').save(app.ROOT / f'assets/sinfonia-{ident}.webp', quality=88)


def update(data):
    result = copy.deepcopy(data)
    items = {p['id']: p for p in result['products']}
    for ident in ('hibisco', 'lavanda'):
        if ident not in items:
            items[ident] = {'id': ident, 'image': f'assets/jardim-{ident}.jpg', 'options': ['Acabamento a confirmar no atendimento'], 'collection': 'jardim', 'published': True, 'illustrative': True}
    for ident, (title, description) in COPY.items():
        items[ident].update(title=title, description=description, price=49.90)
        if items[ident]['options'] == ['Sob consulta']:
            items[ident]['options'] = ['Acabamento a confirmar no atendimento']
    for ident, (name, flower, story) in FLOWERS.items():
        items[ident]['title'] = f'Laço bordado {name} — {flower} e Borboleta'
        items[ident]['description'] = f'No Jardim de Encantos, {name} {story}. A flor e a borboleta bordadas fazem deste laço infantil um detalhe delicado para passeios, fotos e momentos especiais. Escolha seu encanto para completar o penteado ou presentear com carinho. Acabamento a combinar na encomenda.'
    animal_ids = []
    for characters in CHARACTERS.values():
        for ident, name, animal, story in characters:
            animal_ids.append(ident)
            item = items.setdefault(ident, {'id': ident, 'options': ['Acabamento a confirmar no atendimento'], 'published': True, 'illustrative': True})
            item.update(title=f'Laço bordado {name} — {animal} do Sax', description=f'Na banda Sinfonia das Matas, {name} adora {story}. O bordado de {animal.lower()} com saxofone e a clave em forma de coração trazem um toque lúdico ao penteado. Um laço infantil bordado para acompanhar passeios, festas e presentes cheios de personalidade. Escolha {name} para fazer parte da sua coleção.', price=49.90, collection='sinfonia', image=f'assets/sinfonia-{ident}.webp')
    items['kit-jardim'] = {
        'id': 'kit-jardim', 'title': 'Kit 3 laços bordados Jardim de Encantos', 'price': 119.90,
        'image': 'assets/jardim-cover.webp', 'collection': 'kits', 'published': True, 'illustrative': True,
        'bundle': ['margarida', 'girassol', 'rosa'], 'options': ['Margarida + Girassol + Rosa — acabamento a confirmar'],
        'description': 'Três laços florais para variar o penteado: Encanto de Margarida, Encanto de Girassol e Encanto de Rosa. O kit Jardim de Encantos reúne flores e borboletas para presentear ou começar uma coleção. Por R$ 119,90, você economiza R$ 29,80 em relação às três unidades avulsas. Acabamento a combinar no atendimento.'
    }
    items['trio'].update(title='Kit 3 laços bordados Sinfonia das Matas', price=119.90, collection='kits', bundle=['coruja', 'leao', 'gato'], description='Corujinha, Leãozinho e Gatinho do Sax juntos em um kit com três laços infantis bordados. Uma coleção de bichinhos músicos para alternar os penteados ou surpreender com um presente. Escolha a opção das peças e leve o trio por R$ 119,90: economia de R$ 29,80 sobre a compra avulsa.')
    items['kit-jardim']['description'] = 'Daisy, Sol e Rosie: três laços bordados com flores e borboletas para levar um jardim ao penteado. O kit Jardim de Encantos reúne Margarida, Girassol e Rosa para variar as combinações ou presentear com carinho. Economia de R$ 29,80 sobre três unidades avulsas. Acabamento a combinar no atendimento.'
    items['trio']['description'] = 'Olívia, Leon e Milo formam uma pequena banda: Corujinha, Leãozinho e Gatinho do Sax em três laços infantis bordados. Um kit Sinfonia das Matas para variar os penteados e criar novas histórias a cada passeio. Economia de R$ 29,80 sobre três unidades avulsas. Escolha o acabamento das peças na encomenda.'
    order = list(FLOWERS) + animal_ids + ['kit-jardim', 'trio']
    result['products'] = [items.pop(ident) for ident in order] + list(items.values())
    if not any(c['id'] == 'kits' for c in result['collections']):
        result['collections'].insert(2, {'id': 'kits', 'name': 'Kits de 3 laços', 'description': 'Três desenhos para variar os penteados e presentear. Escolha seu kit por R$ 119,90 e economize R$ 29,80 em relação a três laços avulsos de R$ 49,90.', 'image': 'assets/caixa-artesanal.webp', 'published': True, 'featured': False, 'illustrative': True})
    return app.validate(result)


if __name__ == '__main__':
    prepare_photos()
    public = json.loads(app.CONTENT.read_text(encoding='utf-8'))
    local = app.draft()
    new_public, new_local = update(public), update(local)
    app.atomic(app.STATE / 'backup.json', app.encoded(local))
    app.apply_content(new_public)
    app.atomic(app.STATE / 'draft.json', app.encoded(new_local))
    report = app.ROOT.parents[1] / 'outputs/Catalogo_Bordo.md'
    lines = ['# Catálogo Bordô', '', 'Laços avulsos: R$ 49,90. Kits de três: R$ 119,90.', '']
    for collection in ('jardim', 'sinfonia', 'kits'):
        group = next(c for c in new_public['collections'] if c['id'] == collection)
        lines.extend(['## ' + group['name'], ''])
        for product in new_public['products']:
            if product['collection'] == collection:
                lines.extend(['### ' + product['title'], '', product['description'], ''])
    report.write_text('\n'.join(lines), encoding='utf-8')
    print('Atualizados: 39 lacos avulsos a R$ 49,90 e 2 kits a R$ 119,90. Rascunho sincronizado.')
