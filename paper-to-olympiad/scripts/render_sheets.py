#!/usr/bin/env python3
"""Render every page of a PDF into contact sheets for a quick visual check.

Usage:
  python3 render_sheets.py booklet.pdf out_dir [--dpi 45] [--cols 8] [--rows 2]

Requires PyMuPDF (pip install pymupdf) and Pillow (pip install pillow).
Look for half-empty pages, split boxes, headings at page bottoms, overlapping labels.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import fitz  # PyMuPDF
from PIL import Image


def render(pdf: Path, out_dir: Path, dpi: int, cols: int, rows: int) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf)
    pages = []
    for index in range(doc.page_count):
        pix = doc[index].get_pixmap(dpi=dpi)
        pages.append(Image.frombytes("RGB", (pix.width, pix.height), pix.samples))
    per_sheet = cols * rows
    sheets = []
    for start in range(0, len(pages), per_sheet):
        group = pages[start:start + per_sheet]
        width, height = group[0].size
        sheet = Image.new("RGB", (cols * width, rows * height), "white")
        for offset, page in enumerate(group):
            sheet.paste(page, ((offset % cols) * width, (offset // cols) * height))
        path = out_dir / f"{pdf.stem}_sheet{start // per_sheet + 1:02d}.png"
        sheet.save(path)
        sheets.append(path)
    return sheets


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("out_dir", type=Path)
    parser.add_argument("--dpi", type=int, default=45)
    parser.add_argument("--cols", type=int, default=8)
    parser.add_argument("--rows", type=int, default=2)
    args = parser.parse_args()
    for path in render(args.pdf, args.out_dir, args.dpi, args.cols, args.rows):
        print(path)


if __name__ == "__main__":
    main()
