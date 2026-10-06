"""
Bordô Bordados - Script de Otimização e Servidor Local
Executa verificação dos arquivos e pode iniciar um servidor local para testes.
Uso:
    python build.py           -> Valida arquivos e exibe resumo
    python build.py --serve   -> Inicia servidor local em http://localhost:8080
"""

import sys
import os
import http.server
import socketserver
from html.parser import HTMLParser

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def check_html():
    index_path = os.path.join(ROOT_DIR, 'index.html')
    if not os.path.exists(index_path):
        print("[ERRO] index.html nao encontrado!")
        return False

    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    class Validator(HTMLParser):
        def __init__(self):
            super().__init__()
            self.tags = []
            self.void_tags = {'meta', 'link', 'img', 'br', 'hr', 'input', 'source'}
        def handle_starttag(self, tag, attrs):
            if tag not in self.void_tags:
                self.tags.append(tag)
        def handle_endtag(self, tag):
            if tag not in self.void_tags:
                if self.tags and self.tags[-1] == tag:
                    self.tags.pop()

    v = Validator()
    v.feed(content)
    if v.tags:
        print(f"[AVISO] Tags nao fechadas em index.html: {v.tags}")
        return False

    print("[OK] index.html validado com sucesso! Sem erros de sintaxe.")
    return True

def check_assets():
    assets_dir = os.path.join(ROOT_DIR, 'assets')
    required = ['logo.svg', 'logo.png', 'hero.webp', 'bows.webp', 'art.webp']
    all_ok = True
    print("\nVerificando arquivos em assets/:")
    for req in required:
        p = os.path.join(assets_dir, req)
        if os.path.exists(p):
            sz_kb = round(os.path.getsize(p) / 1024, 1)
            print(f"  [OK] {req:<12} ({sz_kb} KB)")
        else:
            print(f"  [FALHA] {req:<12} AUSENTE!")
            all_ok = False
    return all_ok


def serve(port=8080):
    os.chdir(ROOT_DIR)
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"\n🚀 Servidor local rodando em: http://localhost:{port}")
        print("Pressione Ctrl+C para encerrar.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor finalizado.")

if __name__ == '__main__':
    print("=== OTIMIZAÇÃO BORDÔ BORDADOS ===")
    h_ok = check_html()
    a_ok = check_assets()

    if '--serve' in sys.argv:
        if h_ok and a_ok:
            port = 8080
            for arg in sys.argv:
                if arg.startswith('--port='):
                    port = int(arg.split('=')[1])
            serve(port)
    else:
        print("\nPara iniciar o preview local, execute: python build.py --serve")
