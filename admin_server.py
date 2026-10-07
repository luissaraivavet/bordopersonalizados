"""Private, loopback-only content editor for the Bordo static website."""
import argparse
import hashlib
import http.cookies
import io
import json
import math
import os
from pathlib import Path
import re
import secrets
import subprocess
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, unquote, urlsplit
import webbrowser
import zipfile

ROOT = Path(__file__).resolve().parent
STATE = ROOT / '.bordo-admin'
CONTENT = ROOT / 'content/site.json'
LOCK = threading.RLock()
RESERVED = {'conteudo', 'colecoes', 'historia', 'faq', 'personalizados'}


def text(value, label, maximum=4000, required=True):
    if not isinstance(value, str) or len(value) > maximum or (required and not value.strip()):
        raise ValueError(f'{label}: preencha um texto valido (ate {maximum} caracteres).')


def number(value, label, maximum):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= maximum:
        raise ValueError(f'{label}: valor fora do intervalo permitido.')


def image_path(value):
    text(value, 'Imagem', 300)
    if not re.fullmatch(r'assets/[A-Za-z0-9_./-]+\.(webp|png|jpe?g)', value, re.I):
        raise ValueError('Selecione uma imagem local PNG, JPEG ou WebP.')
    path = (ROOT / value).resolve()
    if not path.is_relative_to(ROOT / 'assets') or not path.is_file():
        raise ValueError('A imagem selecionada nao foi encontrada.')


def url(value):
    text(value, 'Link', 2000)
    parsed = urlsplit(value)
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError('Links devem comecar com https:// e nao incluir credenciais.')


def validate(data):
    if not isinstance(data, dict) or data.get('schemaVersion') != 1:
        raise ValueError('Formato de conteudo invalido.')
    settings = data.get('settings', {})
    for field in ('headline', 'intro', 'location', 'story'):
        text(settings.get(field), field, 12000 if field == 'story' else 250)
    if not re.fullmatch(r'55\d{10,11}', str(settings.get('whatsapp', ''))):
        raise ValueError('WhatsApp: informe 55, DDD e numero, somente digitos.')
    url(settings.get('instagram'))
    number(settings.get('pixDiscount'), 'Desconto Pix', 100)
    number(settings.get('giftPrice'), 'Embalagem', 10000)
    for field in ('storyImage', 'storyImageSecondary'):
        if settings.get(field):
            image_path(settings[field])
    all_ids = set(RESERVED)
    for group in ('collections', 'products', 'testimonials', 'articles', 'links'):
        items = data.get(group)
        if not isinstance(items, list) or len(items) > 300:
            raise ValueError(f'{group}: lista invalida ou acima de 300 itens.')
        for item in items:
            if not isinstance(item, dict):
                raise ValueError('Item invalido.')
            ident = item.get('id', '')
            if not isinstance(ident, str) or not re.fullmatch(r'[a-z][a-z0-9-]{0,69}', ident) or ident in all_ids:
                raise ValueError('Identificador duplicado ou invalido: use letras minusculas, numeros e hifens.')
            all_ids.add(ident)
            if not isinstance(item.get('published'), bool):
                raise ValueError('Selecione a visibilidade do item.')
            for field in {'collections': ('name', 'description'), 'products': ('title', 'description'), 'testimonials': ('name', 'text'), 'articles': ('title', 'excerpt', 'body'), 'links': ('title',)}[group]:
                text(item.get(field), field, 20000 if field == 'body' else 4000)
            if group in ('collections', 'products', 'articles'):
                image_path(item.get('image'))
            if group in ('collections', 'products') and not isinstance(item.get('illustrative'), bool):
                raise ValueError('Informe se a imagem e ilustrativa.')
            if group == 'collections' and not isinstance(item.get('featured'), bool):
                raise ValueError('Informe se a colecao aparece em destaque.')
            if group == 'products':
                if item.get('price') is not None:
                    number(item.get('price'), 'Preco', 1000000)
                options = item.get('options')
                if not isinstance(options, list) or not 1 <= len(options) <= 30:
                    raise ValueError('Informe de 1 a 30 opcoes da peca, uma por linha.')
                for option in options:
                    text(option, 'Opcao', 200)
                if len(set(options)) != len(options):
                    raise ValueError('As opcoes nao podem se repetir.')
            if group == 'links':
                url(item.get('url'))
    collection_ids = {item['id'] for item in data['collections']}
    product_ids = {item['id'] for item in data['products'] if not item.get('bundle')}
    for product in data['products']:
        if product.get('collection') not in collection_ids:
            raise ValueError('Todo produto precisa pertencer a uma colecao existente.')
        if 'bundle' in product:
            bundle = product['bundle']
            if not isinstance(bundle, list) or len(bundle) != 3 or not all(isinstance(ident, str) and ident in product_ids for ident in bundle) or len(set(bundle)) != 3:
                raise ValueError('Um kit precisa conter tres produtos distintos existentes.')
    if not any(c['published'] and c['featured'] for c in data['collections']):
        raise ValueError('Mantenha pelo menos uma colecao ativa em destaque.')
    return data


def encoded(data):
    return (json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8')


def script(data):
    return b'window.BORDO_CONTENT = ' + encoded(public_content(data)).rstrip() + b';\n'


def public_content(data):
    result = {**data}
    for group in ('collections', 'products', 'testimonials', 'articles', 'links'):
        result[group] = [item for item in data[group] if item['published']]
    visible_collections = {item['id'] for item in result['collections']}
    result['products'] = [item for item in result['products'] if item['collection'] in visible_collections]
    visible_products = {item['id'] for item in result['products']}
    result['products'] = [item for item in result['products'] if all(ident in visible_products for ident in item.get('bundle', []))]
    return result


def atomic(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_bytes(payload)
    os.replace(temporary, path)


def draft():
    path = STATE / 'draft.json'
    return json.loads((path if path.exists() else CONTENT).read_text(encoding='utf-8'))


def revision(data):
    return hashlib.sha256(encoded(data)).hexdigest()


def git(*args):
    result = subprocess.run(['git', *args], cwd=ROOT, capture_output=True, text=True, timeout=60, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
    if result.returncode:
        raise ValueError('Git nao concluiu a operacao. Verifique a conexao e a autenticacao do repositorio.')
    return result.stdout.strip()


def status():
    try:
        branch = git('branch', '--show-current')
        remote = git('remote', 'get-url', 'origin')
        ready = branch == 'main' and remote in ('https://github.com/luissaraivavet/bordopersonalizados.git', 'git@github.com:luissaraivavet/bordopersonalizados.git')
        return {'branch': branch, 'canPublish': ready}
    except (ValueError, OSError):
        return {'branch': '', 'canPublish': False}


def publish(data):
    if not status()['canPublish']:
        raise ValueError('A publicacao inicial precisa ser integrada ao main. Rascunho, previa e exportacao continuam disponiveis.')
    # Never stage unrelated work or rewrite remote history.
    allowed = {'content/site.json', 'assets/content.js'}
    files = git('status', '--porcelain', '-uall').splitlines()
    if any(line[3:] not in allowed and not line[3:].startswith('assets/uploads/') for line in files):
        raise ValueError('Existem outras alteracoes no repositorio. Resolva-as antes de publicar pelo painel.')
    git('fetch', 'origin', 'main')
    if git('rev-parse', 'HEAD') != git('rev-parse', 'origin/main'):
        raise ValueError('O repositorio local e o remoto diferem. Sincronize antes de publicar.')
    apply_content(data)
    paths = ['content/site.json', 'assets/content.js']
    visible = public_content(data)
    paths += sorted({item['image'] for group in ('products', 'collections', 'articles') for item in visible[group] if item['image'].startswith('assets/uploads/')})
    paths += [visible['settings'][field] for field in ('storyImage', 'storyImageSecondary') if visible['settings'].get(field, '').startswith('assets/uploads/')]
    git('add', '--', *paths)
    if git('diff', '--cached', '--name-only'):
        git('commit', '-m', 'content: atualizar catalogo pelo painel Bordo')
    git('push', 'origin', 'main')


def apply_content(data):
    validate(data)
    atomic(CONTENT, encoded(public_content(data)))
    atomic(ROOT / 'assets/content.js', script(data))


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_):
        pass  # Launch URLs contain a short-lived credential; never log them.

    def reply(self, code, payload, kind='application/json; charset=utf-8', extra=None):
        if isinstance(payload, (dict, list)):
            payload = encoded(payload)
        if isinstance(payload, str):
            payload = payload.encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', kind)
        self.send_header('Content-Length', str(len(payload)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'DENY')
        self.send_header('Referrer-Policy', 'no-referrer')
        for key, value in (extra or {}).items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(payload)

    def authorized(self):
        if self.headers.get('Host') != self.server.host:
            return False
        cookie = http.cookies.SimpleCookie()
        try:
            cookie.load(self.headers.get('Cookie', ''))
            return 'bordo_session' in cookie and secrets.compare_digest(cookie['bordo_session'].value, self.server.session)
        except http.cookies.CookieError:
            return False

    def do_GET(self):
        parsed = urlsplit(self.path)
        if self.headers.get('Host') != self.server.host:
            return self.reply(403, {'error': 'Host nao autorizado.'})
        if parsed.path == '/entrar':
            key = parse_qs(parsed.query).get('key', [''])[0]
            with LOCK:
                if not self.server.launch_key or not secrets.compare_digest(key, self.server.launch_key):
                    return self.reply(401, {'error': 'Abra o painel pelo atalho neste computador.'})
                self.server.launch_key = None
            return self.reply(303, b'', extra={'Location': '/admin/', 'Set-Cookie': f'bordo_session={self.server.session}; HttpOnly; SameSite=Strict; Path=/'})
        if not self.authorized():
            return self.reply(401, {'error': 'Abra o painel pelo atalho neste computador.'})
        try:
            if parsed.path == '/api/content':
                with LOCK:
                    data = draft()
                    return self.reply(200, {'content': data, 'revision': revision(data), 'csrf': self.server.csrf, **status()})
            if parsed.path == '/api/media':
                files = [p.relative_to(ROOT).as_posix() for p in (ROOT / 'assets').rglob('*') if p.suffix.lower() in ('.png', '.jpg', '.jpeg', '.webp') and p.is_file()]
                return self.reply(200, sorted(files))
            if parsed.path == '/api/export':
                with LOCK:
                    data = public_content(validate(draft()))
                    used_uploads = {item['image'] for group in ('collections', 'products', 'articles') for item in data[group]}
                    used_uploads.update(data['settings'].get(field, '') for field in ('storyImage', 'storyImageSecondary'))
                    buffer = io.BytesIO()
                    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as archive:
                        archive.write(ROOT / 'index.html', 'index.html')
                        archive.writestr('assets/content.js', script(data))
                        archive.writestr('content/site.json', encoded(data))
                        for path in (ROOT / 'assets').rglob('*'):
                            if path.is_file() and path.name != 'content.js':
                                if path.is_relative_to(ROOT / 'assets/uploads') and path.relative_to(ROOT).as_posix() not in used_uploads:
                                    continue
                                archive.write(path, path.relative_to(ROOT).as_posix())
                    return self.reply(200, buffer.getvalue(), 'application/zip', {'Content-Disposition': 'attachment; filename="Bordo_Site.zip"'})
            if parsed.path == '/preview/assets/content.js':
                return self.reply(200, script(draft()), 'text/javascript; charset=utf-8')
            relative = unquote(parsed.path).lstrip('/')
            if relative.startswith('preview/'):
                relative = relative[len('preview/'):] or 'index.html'
            if relative in ('admin', 'admin/'):
                relative = 'admin/index.html'
            if relative == '':
                return self.reply(303, b'', extra={'Location': '/admin/'})
            path = (ROOT / relative).resolve()
            allowed = (relative == 'index.html' or
                       (relative.startswith('assets/') and path.is_relative_to(ROOT / 'assets')) or
                       (relative.startswith('admin/') and path.is_relative_to(ROOT / 'admin')))
            if not allowed or not path.is_relative_to(ROOT) or not path.is_file():
                return self.reply(404, {'error': 'Arquivo nao encontrado.'})
            import mimetypes
            kind = mimetypes.guess_type(path.name)[0] or 'application/octet-stream'
            return self.reply(200, path.read_bytes(), kind + ('; charset=utf-8' if kind.startswith('text/') else ''))
        except (ValueError, OSError) as error:
            return self.reply(400, {'error': str(error)})

    def do_POST(self):
        if not self.authorized() or self.headers.get('Origin') != 'http://' + self.server.host or not secrets.compare_digest(self.headers.get('X-CSRF-Token', ''), self.server.csrf):
            return self.reply(403, {'error': 'Sessao invalida. Abra o painel novamente pelo atalho.'})
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= 10 * 1024 * 1024:
                return self.reply(413, {'error': 'Arquivo ou conteudo deve ter ate 10 MB.'})
            raw = self.rfile.read(length)
            with LOCK:
                if self.path == '/api/upload':
                    if raw.startswith(b'\x89PNG\r\n\x1a\n'):
                        extension = 'png'
                    elif raw.startswith(b'\xff\xd8\xff'):
                        extension = 'jpg'
                    elif raw[:4] == b'RIFF' and raw[8:12] == b'WEBP':
                        extension = 'webp'
                    else:
                        raise ValueError('Envie uma foto PNG, JPEG ou WebP.')
                    relative = f'assets/uploads/{secrets.token_hex(12)}.{extension}'
                    atomic(ROOT / relative, raw)
                    return self.reply(200, {'path': relative})
                body = json.loads(raw)
                current = draft()
                if body.get('revision') != revision(current):
                    return self.reply(409, {'error': 'O rascunho mudou em outra janela. Recarregue antes de salvar.'})
                data = validate(body.get('content'))
                if self.path == '/api/save':
                    if (STATE / 'draft.json').exists():
                        atomic(STATE / 'backup.json', encoded(current))
                    atomic(STATE / 'draft.json', encoded(data))
                elif self.path == '/api/publish':
                    publish(data)
                    atomic(STATE / 'draft.json', encoded(data))
                else:
                    return self.reply(404, {'error': 'Operacao desconhecida.'})
                return self.reply(200, {'revision': revision(data)})
        except (ValueError, KeyError, TypeError, OSError, subprocess.TimeoutExpired) as error:
            return self.reply(400, {'error': str(error)})


def make_server(port=0):
    server = ThreadingHTTPServer(('127.0.0.1', port), Handler)
    server.host = f'127.0.0.1:{server.server_port}'
    server.session = secrets.token_urlsafe(32)
    server.csrf = secrets.token_urlsafe(32)
    server.launch_key = secrets.token_urlsafe(32)
    return server


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-browser', action='store_true')
    parser.add_argument('--port', type=int, default=0)
    args = parser.parse_args()
    validate(draft())
    with make_server(args.port) as server:
        launch_url = f'http://{server.host}/entrar?key={server.launch_key}'
        print('Painel Bordo privado iniciado. Feche esta janela para encerrar.', flush=True)
        if args.no_browser:
            print(launch_url, flush=True)
        else:
            webbrowser.open(launch_url)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
