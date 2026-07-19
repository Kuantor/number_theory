"""Render a Markdown file to a styled PDF using headless Microsoft Edge.

This is how the project's docs (e.g. ``docs/USER_GUIDE.md``) are turned into
``.pdf``. It uses Edge's ``--print-to-pdf`` as the renderer (Edge ships with
Windows 10/11, so there's no PDF-engine dependency) and python-markdown to
convert the Markdown — including fenced code blocks, tables, and blockquotes,
which developer docs rely on.

Usage:
    python docs/scripts/md2pdf.py <input.md> [output.pdf]

    # defaults output next to the input:
    python docs/scripts/md2pdf.py docs/USER_GUIDE.md

Requires:
    pip install markdown      # python-markdown
    Microsoft Edge            # standard install location, checked below
"""
import subprocess
import sys
import tempfile
from pathlib import Path

import markdown

EDGE_PATHS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]

CSS = """
@page { margin: 1.8cm 1.7cm; }
body { font-family: Calibri, 'Segoe UI', sans-serif; font-size: 10.5pt;
       color: #22303C; line-height: 1.4; }
h1 { color: #2E6BA0; font-size: 22pt; margin: 0 0 6pt; }
h2 { color: #2E6BA0; font-size: 15pt; margin: 18pt 0 6pt;
     border-bottom: 1px solid #E1E7EC; padding-bottom: 3pt; }
h3 { color: #22303C; font-size: 12.5pt; margin: 13pt 0 5pt; }
p  { margin: 0 0 7pt; }
ul, ol { margin: 0 0 8pt 1.4em; padding: 0; }
li { margin: 0 0 4pt; }
hr { border: none; border-bottom: 1.5pt solid #D9B13C; margin: 12pt 0; }
a  { color: #2E6BA0; text-decoration: none; }
table { border-collapse: collapse; margin: 4pt 0 12pt; width: 100%; }
th { background: #2E6BA0; color: #fff; text-align: left; }
th, td { border: 1px solid #B9C6D2; padding: 4pt 7pt; font-size: 9.5pt;
         vertical-align: top; }
code { font-family: Consolas, monospace; font-size: 9.5pt;
       background: #EEF1F4; padding: 1pt 3pt; border-radius: 3px; }
pre { background: #F4F6F8; border: 1px solid #D9E0E6; border-radius: 4px;
      padding: 9pt 11pt; margin: 6pt 0 12pt; overflow-x: auto;
      white-space: pre-wrap; word-break: break-word; }
pre code { background: none; padding: 0; font-size: 9.5pt; line-height: 1.35;
           color: #1B2733; }
blockquote { border-left: 3px solid #D9B13C; margin: 8pt 0; padding: 2pt 0 2pt 12pt;
             color: #5B6B7A; }
pre, blockquote, table, h2, h3, li { page-break-inside: avoid; }
* { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
"""


def find_edge():
    for p in EDGE_PATHS:
        if Path(p).exists():
            return p
    sys.exit("Microsoft Edge not found in the standard locations.")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = Path(sys.argv[1])
    out = (Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_suffix(".pdf")).resolve()
    body = markdown.markdown(
        src.read_text(encoding="utf-8"),
        extensions=["fenced_code", "tables", "sane_lists", "toc"],
    )
    page = ("<!doctype html><html><head><meta charset='utf-8'>"
            f"<style>{CSS}</style></head><body>{body}</body></html>")

    with tempfile.TemporaryDirectory() as tmp:
        html_path = Path(tmp) / "doc.html"
        html_path.write_text(page, encoding="utf-8")
        subprocess.run(
            [find_edge(), "--headless", "--disable-gpu",
             "--no-pdf-header-footer",
             f"--print-to-pdf={out}", html_path.as_uri()],
            check=True, timeout=120,
        )
    print(f"written: {out}")


if __name__ == "__main__":
    main()
