"""Gera as miniaturas usadas no índice da capa (assets/thumbs/*.webp).

Uso:
    python scripts/gerar_miniaturas.py

Requer o ffmpeg no PATH. Lê as fotos dos produtos em content/site.json e grava
uma cópia de 240 px de largura para cada uma; as fotos originais não são
alteradas. Rode de novo depois de publicar fotos novas pelo painel. Sem a
miniatura, o site usa a foto original no lugar.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THUMBS = ROOT / "assets" / "thumbs"


def main():
    if not shutil.which("ffmpeg"):
        print("ffmpeg não encontrado no PATH; nenhuma miniatura foi gerada.")
        return 1
    content = json.loads((ROOT / "content" / "site.json").read_text(encoding="utf-8"))
    images = sorted({product["image"] for product in content["products"]})
    THUMBS.mkdir(parents=True, exist_ok=True)
    made = 0
    for image in images:
        source = ROOT / image
        target = THUMBS / f"{source.stem}.webp"
        if target.exists() and target.stat().st_mtime >= source.stat().st_mtime:
            continue
        result = subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-i", str(source), "-frames:v", "1",
             "-vf", "scale=240:-2:flags=lanczos", "-c:v", "libwebp", "-quality", "72", str(target)],
            check=False,
        )
        if result.returncode:
            print(f"Falha ao gerar a miniatura de {image}.")
            return 1
        made += 1
    print(f"{made} miniatura(s) gerada(s); {len(images)} foto(s) conferida(s).")
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
