"""Apply the owner's founder story and remove nonexistent headband options."""
import copy
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import admin_server as app

STORY = '''A Bordô tem um rosto e um nome: Priscila, idealizadora deste projeto em Teixeiras, Minas Gerais. Por trás dos laços e dos bordados, está uma proposta simples: dar forma ao carinho que acompanha um presente.

Uma flor pode lembrar um passeio. Um bichinho pode se tornar o personagem favorito de uma criança. Um nome bordado pode fazer uma peça pertencer a alguém de um jeito especial. É nesse encontro entre desenho e significado que a Bordô encontra sua identidade.

O Jardim de Encantos leva flores e borboletas aos laços. A Sinfonia das Matas transforma bichinhos músicos em pequenos personagens. Cada coleção é um convite para escolher um detalhe que converse com a sua história, seja para usar, presentear ou guardar.

Até o nosso nome carrega um pedacinho de quem somos. “Bordou” é a ideia que ganhou forma no tecido. No nosso jeito mineiro de falar, vira “bordô”. E bordô também é a cor da nossa marca: um encontro entre o bordado, o mineirês e a identidade que escolhemos.

Somos de Teixeiras, MG, e atendemos online, por encomenda. A conversa faz parte de cada pedido: nela combinamos o desenho, os materiais, o acabamento e os detalhes da entrega. Assim, uma ideia sua encontra um caminho para virar peça.

Priscila é a idealizadora. Você traz o nome, a ocasião, a pessoa que quer surpreender. E a próxima história que a Bordô vai bordar pode começar nessa conversa.'''


def update(data):
    result = copy.deepcopy(data)
    result['settings'].update(story=STORY, storyImage='assets/priscila-bordo.jpg', storyImageSecondary='assets/priscila-retrato.jpg')
    for product in result['products']:
        product['options'] = [option for option in product['options'] if 'faix' not in option.lower()]
        if not product['options']:
            product['options'] = ['Acabamento a confirmar no atendimento']
    return app.validate(result)


if __name__ == '__main__':
    local = app.draft()
    public = json.loads(app.CONTENT.read_text(encoding='utf-8'))
    app.atomic(app.STATE / 'backup.json', app.encoded(local))
    app.apply_content(update(public))
    app.atomic(app.STATE / 'draft.json', app.encoded(update(local)))
    print('Historia atualizada. Opcoes de faixinhas removidas do site e do rascunho.')
