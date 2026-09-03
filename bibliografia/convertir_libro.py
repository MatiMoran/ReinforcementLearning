#!/usr/bin/env python3
"""Convierte un EPUB en un arbol de markdown chunked (un .md por capitulo/seccion).

Uso:
    python bibliografia/convertir_libro.py <libro.epub> [--out-dir libro]

Dependencias (provistas por shell.nix):
    ebooklib, markdownify, beautifulsoup4
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from bs4 import BeautifulSoup
from ebooklib import ITEM_DOCUMENT, ITEM_IMAGE, epub
from markdownify import markdownify as html_to_md


def slugify(text: str, fallback: str) -> str:
    text = re.sub(r"<[^>]+>", "", text or "")
    text = re.sub(r"[^a-zA-Z0-9]+", "_", text).strip("_")
    return (text or fallback).lower()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("epub", help="Ruta al archivo .epub")
    parser.add_argument("--out-dir", default="libro", help="Carpeta de salida (default: libro)")
    parser.add_argument("--write-images", action="store_true", default=True,
                        help="Extraer y guardar las imagenes del EPUB en <out-dir>/images")
    parser.add_argument("--no-write-images", dest="write_images", action="store_false")
    args = parser.parse_args()

    epub_path = Path(args.epub)
    out_dir = Path(args.out_dir)
    images_dir = out_dir / "images"
    out_dir.mkdir(parents=True, exist_ok=True)

    book = epub.read_epub(str(epub_path.resolve()))

    images = []
    if args.write_images:
        images_dir.mkdir(parents=True, exist_ok=True)
        for item in book.get_items_of_type(ITEM_IMAGE):
            name = Path(item.file_name).name
            (images_dir / name).write_bytes(item.get_content())
            images.append(name)
        print(f"Imagenes extraidas: {len(images)} -> {images_dir}")

    docs = [it for it in book.get_items_of_type(ITEM_DOCUMENT)]
    # El spine de ebooklib no siempre preserva el orden de lectura; usar el orden fisico
    # de los items document es lo mas estable para libros como este.
    written = 0
    for idx, item in enumerate(docs, start=1):
        soup = BeautifulSoup(item.get_content(), "html.parser")
        for tag in soup(["script", "style"]):
            tag.decompose()

        title_el = soup.find(["h1", "h2", "title"])
        title = title_el.get_text(" ", strip=True) if title_el else ""
        body = soup.body or soup

        # Rewrite image srcs to point to the local images/ directory
        if args.write_images:
            for img in soup.find_all("img"):
                orig = Path(img.get("src", ""))
                name = Path(orig.name or (images_dir / orig).name).name
                img["src"] = f"images/{name}"

        md = html_to_md(str(body), heading_style="ATX", bullets="*")

        # Limpieza basica: remover lineas vacias repetidas y espacio de sobra
        md = re.sub(r"\n{3,}", "\n\n", md).strip() + "\n"

        name = slugify(title, f"seccion_{idx:03d}")
        out_file = out_dir / f"{idx:03d}_{name}.md"
        out_file.write_text(md, encoding="utf-8")
        written += 1
        print(f"  [{written:03d}] {out_file.name}")

    print(f"\nListo: {written} archivos markdown en {out_dir}")


if __name__ == "__main__":
    main()
