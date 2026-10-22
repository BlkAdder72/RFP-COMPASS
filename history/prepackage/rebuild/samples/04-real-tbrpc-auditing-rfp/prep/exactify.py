# Replace each packet cell with the PDF's exact characters (apostrophes/quotes/dashes), whitespace collapsed.
import re, pdfplumber
from pathlib import Path
SAMPLE = Path(__file__).resolve().parent.parent
PACKET = SAMPLE / "source-packet.md"
with pdfplumber.open(SAMPLE / "original-source.pdf") as pdf:
    raw = "\n".join(p.extract_text() or "" for p in pdf.pages)
raw = re.sub(r"[\u2022\uf0b7]", " ", raw)
def pat(cell):
    out = []
    for ch in cell:
        if ch == "'": out.append("['’]")
        elif ch == '"': out.append('["“”]')
        elif ch == "-": out.append(r"-\s*")
        elif ch == " ": out.append(r"\s+")
        else: out.append(re.escape(ch))
    return "".join(out)
lines, changed, missing = [], 0, []
for line in open(PACKET, encoding="utf-8"):
    sid, anc, txt = line.rstrip("\n").split(" | ", 2)
    cells = []
    for c in txt.split(" | "):
        m = re.search(pat(c), raw)
        if not m: missing.append((sid, c)); cells.append(c); continue
        exact = re.sub(r"-\s+", "-", re.sub(r"\s+", " ", m.group(0)))
        # keep line-break hyphen joins; but restore any real "x - y" spacing from source
        exact = exact if re.sub(r"\s","",exact) == re.sub(r"\s","",m.group(0)) else c
        changed += exact != c; cells.append(exact)
    lines.append(f"{sid} | {anc} | {' | '.join(cells)}\n")
open(PACKET, "w", encoding="utf-8", newline="\n").writelines(lines)
print("cells updated to exact PDF characters:", changed, "| unmatched:", missing)
