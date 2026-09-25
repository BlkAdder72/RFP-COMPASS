#!/usr/bin/env python3
"""Build or verify an RFP Compass source-packet.md.

build:  python -X utf8 tools/make_packet.py build ORIGINAL [--prefix NAME] [--keep-furniture] > source-packet.md
verify: python -X utf8 tools/make_packet.py verify ORIGINAL source-packet.md [--keep-furniture]

build copies text; it never rewords, corrects or reorders it.
  - Lines the source wrapped mid-sentence (including across page breaks) are rejoined.
  - Each block is split into sentences, never inside abbreviations such as p.m., U.S. or No.
  - Tab-separated table cells become " | ". In a PDF, each row of a ruled table becomes one
    statement with its cells in column order, instead of text with the columns interleaved.
  - Page headers and footers repeated on at least half the pages of a PDF (running titles,
    "Page 3 of 41", revision stamps) are kept once, at their first appearance, and the
    dropped repeats are reported. --keep-furniture keeps every repeat.
  - Every statement is anchored to the page and line where it starts.
  The result is a draft: review it against the original before use.

verify walks the packet in order and checks that:
  - each statement appears verbatim at its own position in the original, allowing only
    whitespace and line-break-hyphen differences (a statement whose text exists only
    somewhere else in the document fails);
  - the cells of a table row sit next to each other in the original.
It then checks every "p. N" anchor against the page where the statement's text starts
(allowing a consistent offset, such as printed page numbers), and lists the original text
that no statement covers, grouped, so a reviewer can confirm each omission was intended.

ORIGINAL may be .txt/.md, or .pdf when pdfplumber is installed.
"""
from pathlib import Path
import argparse
import re
import sys
from collections import Counter

ABBREVIATION = re.compile(
    r"(?:^|\s)(?:(?:[A-Za-z]\.){2,}|No\.|Nos\.|Mr\.|Ms\.|Mrs\.|Dr\.|St\.|Inc\.|Co\.|Corp\.|Ltd\.|"
    r"LLC\.|vs\.|etc\.|Sec\.|Art\.|Fig\.|Vol\.|Jan\.|Feb\.|Mar\.|Apr\.|Aug\.|Sept\.|Sep\.|Oct\.|Nov\.|Dec\.|"
    r"[A-Z]\.|[IVXLC]+\.)$"
)
LIST_MARKER = re.compile(r"^\(?[0-9A-Za-z]{1,4}[.)]$")
LIST_START = re.compile(
    r"^(?:\(?\d{1,3}(?:\.\d{1,3})+\.?|\(?\d{1,3}[.)]|\(?[A-Za-z][.)]|\(?[ivxlcIVXLC]{1,5}[.)])\s"
)
BULLET_START = re.compile(r"^(?:[•▪◦●■\-\*–]|o|<U\+F0B7>)\s")
PAGE_LABEL = re.compile(r"^page\s+\d+(\s+of\s+\d+)?$", re.IGNORECASE)
BOUNDARY = re.compile(r"(?<=[.!?])[\"”’)]?\s+(?=[A-Z0-9\"“(])")
TERMINAL = (".", "!", "?", ":", ";")
NOTE = "\u2063"      # brackets a table row's column note inside a raw line (invisible separator)
BACKTRACK = 2000     # verify: minimum look-back (grows to about 1.5 pages for PDFs)
CELL_GAP = 40        # verify: maximum whitespace between cells of one table row


def pdf_page_lines(page) -> list[str]:
    """A PDF page's lines in reading order, with each ruled-table row as one tab-separated line.

    Plain text extraction interleaves table columns ("Vendor Selection June 19, 2026 July 10, 2026"
    spread over wrapped lines), which breaks the link between a row label and its dates.
    Rows found by pdfplumber's table finder keep their cells together instead.
    """
    tables = page.find_tables()
    boxes = [table.bbox for table in tables]
    items = []
    for line in page.extract_text_lines():
        middle = (line["top"] + line["bottom"]) / 2
        inside = any(top <= middle <= bottom and line["x0"] < right and line["x1"] > left
                     for left, top, right, bottom in boxes)
        if not inside:
            items.append((line["top"], line["text"]))
    for table in tables:
        for index, row in enumerate(table.extract()):
            cells = [re.sub(r"\s+", " ", cell or "").strip() for cell in row]
            filled = [position for position, cell in enumerate(cells) if cell]
            if not filled:
                continue
            first, last = filled[0], filled[-1]
            text = "\t".join(cells[first:last + 1])
            if first > 0 or last < len(cells) - 1:
                # Blank (often merged) cells at the edges: record which columns the text fills,
                # so "Building Supervisor | 1 | 2:30pm" is not read as starting in column 1.
                text = f"{NOTE}columns {first + 1}–{last + 1} of {len(cells)}{NOTE}{text}"
            top = table.rows[index].bbox[1] if index < len(table.rows) else table.bbox[1]
            items.append((top + 0.01, text))
    items.sort(key=lambda item: item[0])
    return [text for _, text in items]


def split_note(text: str) -> tuple[str | None, str]:
    """Separate a table row's column note (added by pdf_page_lines) from its text."""
    if text.startswith(NOTE):
        note, _, rest = text[len(NOTE):].partition(NOTE)
        return note, rest
    return None, text


def pdf_non_text(path: Path) -> list[str]:
    """Pages whose content includes images, which text extraction cannot copy."""
    import pdfplumber
    report = []
    with pdfplumber.open(path) as pdf:
        for number, page in enumerate(pdf.pages, 1):
            images = page.images
            area = page.width * page.height
            large = [image for image in images if image["width"] * image["height"] > 0.05 * area]
            small = len(images) - len(large)
            if not page.chars:
                report.append(f"p. {number}: no extractable text at all (scanned or image-only page?)")
            elif large:
                report.append(f"p. {number}: {len(large)} large image(s) (figure, map, logo or scan): "
                              "any text inside is not in the packet")
            if small:
                report.append(f"p. {number}: {small} small image(s) (often checkbox marks or symbols): "
                              "whether a box is checked is not in the packet")
    return report


def show_symbols(text: str) -> str:
    """Write private-use characters (symbol-font glyphs such as a Wingdings check mark, U+F0FC)
    as <U+XXXX>. They print as nothing or a box, so readers and models otherwise drop them;
    the code keeps them visible and copyable without guessing what they depict."""
    return re.sub("[\ue000-\uf8ff]", lambda match: f"<U+{ord(match.group(0)):04X}>", text)


def read_raw(path: Path) -> list[tuple[int | None, int, str]]:
    """Return (page, line, text) for every raw line, symbol-font characters written as <U+XXXX>."""
    return [(page, number, show_symbols(text)) for page, number, text in read_raw_text(path)]


def read_raw_text(path: Path) -> list[tuple[int | None, int, str]]:
    if path.suffix.lower() == ".pdf":
        try:
            import pdfplumber
        except ImportError:
            sys.exit("PDF input needs pdfplumber (pip install pdfplumber), or extract the text first.")
        lines = []
        with pdfplumber.open(path) as pdf:
            for page_number, page in enumerate(pdf.pages, 1):
                for line_number, line in enumerate(pdf_page_lines(page), 1):
                    lines.append((page_number, line_number, line))
        return lines
    try:
        text = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        text = path.read_bytes().decode("cp1252", errors="replace")
        print(f"warning: {path.name} is not UTF-8; read it as Windows-1252. Curly quotes and other characters "
              "may already have been lost when it was saved. Re-extract it as UTF-8 if you can.", file=sys.stderr)
    if "\f" in text:
        # Form feeds (as written by pdftotext) mark page breaks.
        return [(page, number, line)
                for page, chunk in enumerate(text.split("\f"), 1)
                for number, line in enumerate(chunk.splitlines(), 1)]
    return [(None, number, line) for number, line in enumerate(text.splitlines(), 1)]


def location(page: int | None, line: int) -> str:
    return f"p. {page} line {line}" if page is not None else f"line {line}"


def furniture(lines: list[tuple[int | None, int, str]]) -> set[str]:
    """Digit-normalised header/footer lines that repeat on at least half the pages."""
    pages: dict[int, list[str]] = {}
    for page, _, text in lines:
        if page is not None and text.strip():
            pages.setdefault(page, []).append(text.strip())
    if len(pages) < 4:
        return set()
    counts = Counter()
    for texts in pages.values():
        zone = texts[:3] + texts[-4:]
        counts.update({re.sub(r"\d+", "#", text).lower() for text in zone})
    threshold = max(3, len(pages) / 2)
    return {pattern for pattern, count in counts.items() if count >= threshold}


def ends_sentence(text: str) -> bool:
    text = text.rstrip()
    return text.endswith(TERMINAL) and not ABBREVIATION.search(text)


def starts_new_block(text: str) -> bool:
    stripped = text.strip()
    letters = [c for c in stripped if c.isalpha()]
    heading = len(stripped) <= 80 and letters and sum(c.isupper() for c in letters) / len(letters) > 0.8
    return bool(LIST_START.match(stripped) or BULLET_START.match(stripped)
                or PAGE_LABEL.match(stripped) or heading)


def set_aside_repeats(lines, keep_furniture: bool):
    """Drop repeated page headers/footers after their first appearance.

    Returns the kept lines as (page, line, text, is_furniture) and a count of dropped repeats.
    """
    repeated = set() if keep_furniture else furniture(lines)
    seen, kept, dropped = set(), [], Counter()
    for page, number, text in lines:
        pattern = re.sub(r"\d+", "#", text.strip()).lower()
        if text.strip() and pattern in repeated:
            if pattern in seen:
                dropped[re.sub(r"\d+", "#", text.strip())] += 1
                continue
            seen.add(pattern)
            kept.append((page, number, text, True))
        else:
            kept.append((page, number, text, False))
    return kept, dropped


def blocks(lines, keep_furniture: bool):
    """Join wrapped lines into blocks of continuous text.

    Returns (blocks, dropped repeats). Each block is (text, marks): marks lists
    (offset in text, location) for every raw line joined into it, so each sentence
    split from the block can be anchored where it actually starts.
    """
    kept, dropped = set_aside_repeats(lines, keep_furniture)
    widths = sorted(len(text.strip()) for _, _, text in lines if text.strip())
    full = widths[int(len(widths) * 0.9)] * 0.7 if widths else 0
    result, last_width = [], 0
    for page, number, raw_text, is_furniture in kept:
        note, text = split_note(raw_text)
        stripped = re.sub(r"\s+", " ", text).strip() if "\t" not in text else text.strip()
        if not stripped:
            continue
        where = location(page, number) + (f" ({note})" if note else "")
        if is_furniture or note:
            result.append([stripped, [(0, where)], True])
            last_width = 0
            continue
        if result and not result[-1][2] and "\t" not in text and "\t" not in result[-1][0]:
            previous = result[-1][0]
            unfinished = not ends_sentence(previous) or previous.endswith("-")
            continues = stripped[:1].islower() or last_width >= full or previous.endswith("-") \
                or ABBREVIATION.search(previous.rstrip())
            if unfinished and continues and not starts_new_block(stripped):
                joiner = "" if previous.endswith("-") and stripped[:1].islower() else " "
                result[-1][1].append((len(previous) + len(joiner), where))
                result[-1][0] = previous + joiner + stripped
                last_width = len(stripped)
                continue
        result.append([stripped, [(0, where)], False])
        last_width = len(stripped)
    return [(text, marks) for text, marks, _ in result], dropped


def split_sentences(text: str) -> list[str]:
    """Split at sentence ends, never inside abbreviations such as p.m., U.S., No. or II."""
    parts, start = [], 0
    for match in BOUNDARY.finditer(text):
        before = text[start:match.start()]
        if ABBREVIATION.search(before) or LIST_MARKER.match(before.strip()) or before.endswith(".."):
            continue
        closer = len(match.group(0)) - len(match.group(0).lstrip("\"”’)"))
        parts.append(text[start:match.start() + closer].strip())
        start = match.end()
    parts.append(text[start:].strip())
    return [part for part in parts if part]


def build(raw: Path, prefix: str, keep_furniture: bool) -> str:
    joined, dropped = blocks(read_raw(raw), keep_furniture)
    statements = []
    for text, marks in joined:
        if "\t" in text:
            statements.append((marks[0][1], " | ".join(cell.strip() for cell in text.split("\t"))))
            continue
        pointer = 0
        for sentence in split_sentences(text):
            start = text.find(sentence, pointer)
            pointer = start + len(sentence)
            where = [where for offset, where in marks if offset <= start][-1]
            statements.append((where, sentence))
    for text, count in dropped.items():
        print(f"collapsed {count} repeat(s) of page header/footer: {text}", file=sys.stderr)
    print(f"{len(statements)} statements", file=sys.stderr)
    symbols = [text for _, text in statements if re.search(r"<U\+[0-9A-F]{4}>", text)]
    if symbols:
        print(f"{len(symbols)} statement(s) contain symbol-font characters written as <U+XXXX> "
              "(often check marks or boxes); copy them exactly", file=sys.stderr)
    if raw.suffix.lower() == ".pdf":
        for line in pdf_non_text(raw):
            print(f"not copied: {line}", file=sys.stderr)
    return "".join(f"S{index:03d} | {prefix} {where} | {text}\n"
                   for index, (where, text) in enumerate(statements, 1))


def normalise(text: str) -> str:
    text = text.replace("\u00a0", " ").replace("\u200b", "").replace("\ufeff", "")
    text = re.sub(r"(\w)-\s+(\w)", r"\1-\2", text)
    return re.sub(r"\s+", " ", text).strip()


def verify(raw: Path, packet: Path, keep_furniture: bool) -> int:
    raw_lines = read_raw(raw)
    packet_lines = packet.read_text(encoding="utf-8-sig").splitlines()
    if not keep_furniture:
        # A packet that repeats a page header/footer was built keeping every repeat.
        patterns = furniture(raw_lines)
        found = Counter(re.sub(r"\d+", "#", line.split(" | ", 2)[-1].strip()).lower() for line in packet_lines)
        keep_furniture = any(found[pattern] > 1 for pattern in patterns)
    kept, dropped = set_aside_repeats(raw_lines, keep_furniture)
    kept = [(page, number, split_note(text)[1], flag) for page, number, text, flag in kept]
    source = normalise("\n".join(text for _, _, text, _ in kept))
    covered = bytearray(len(source))
    pages = len({page for page, _, _, _ in kept if page is not None})
    window = max(BACKTRACK, int(1.5 * len(source) / pages)) if pages else BACKTRACK
    cursor, problems, page_checks = 0, [], []
    # Where each page starts in the normalised source, to check "p. N" anchors.
    page_starts, before = [], []
    for page, _, text, _ in kept:
        if page is not None and (not page_starts or page_starts[-1][0] != page):
            page_starts.append((page, len(normalise("\n".join(before))) + (1 if before else 0)))
        before.append(text)

    def page_at(position: int) -> int | None:
        found = None
        for page, start in page_starts:
            if start <= position + 1:
                found = page
        return found

    def nearest(cell: str, start: int) -> int:
        """First copy of cell at or after start that no earlier statement has claimed."""
        position = source.find(cell, start)
        while position >= 0 and covered[position]:
            position = source.find(cell, position + 1)
        return position if position >= 0 else source.find(cell, start)

    for number, line in enumerate(packet_lines, 1):
        if not line.strip():
            continue
        parts = line.split(" | ", 2)
        if len(parts) != 3:
            problems.append(f"line {number}: not in `S001 | anchor | text` form")
            continue
        source_id, anchor, text = parts
        # Cells are separated by "|"; blank cells may be written "| |", so split on any pipe.
        cells = [normalise(show_symbols(cell)) for cell in re.split(r"\s*\|\s*", text)]
        cells = [cell for cell in cells if cell] or [""]
        first = nearest(cells[0], max(0, cursor - window))
        if first < 0:
            where = "exists only elsewhere in the document (wrong position)" if cells[0] in source \
                else "not found in the original"
            problems.append(f"{source_id}: {where}: {cells[0][:150]}")
            continue

        def row_at(start: int):
            """Spans of every cell if the row's cells sit together from start, else None."""
            spans, end = [(start, start + len(cells[0]))], start + len(cells[0])
            for cell in cells[1:]:
                if not cell:
                    continue
                position = source.find(cell, end)
                if position < 0 or source[end:position].strip() or position - end > CELL_GAP:
                    return None
                spans.append((position, position + len(cell)))
                end = position + len(cell)
            return spans

        spans, candidate, tries = row_at(first), first, 0
        while spans is None and tries < 500:
            candidate = source.find(cells[0], candidate + 1)
            if candidate < 0:
                break
            spans, tries = row_at(candidate), tries + 1
        ok = spans is not None
        if ok:
            end = spans[-1][1]
        else:
            problems.append(f"{source_id}: table cells not found side by side in the original: {text[:100]}")
        if ok:
            for a, b in spans:
                covered[a:b] = b"\x01" * (b - a)
            cursor = end
            cited_page = re.search(r"(?<!p)\bp\. (\d+)\b", anchor)
            if cited_page and page_starts:
                page_checks.append((source_id, int(cited_page.group(1)), page_at(spans[0][0])))
    uncovered, piece = Counter(), []
    for index, character in enumerate(source + " "):
        if index < len(source) and not covered[index]:
            piece.append(character)
        elif piece:
            text = "".join(piece).strip(" |")
            if re.search(r"\w", text):
                uncovered[re.sub(r"\d+", "#", text) if len(text) < 60 else text] += 1
            piece = []
    if problems:
        print("FAIL: packet text not found verbatim at its position in the original")
        for problem in problems:
            print(f"  {problem}")
    else:
        print("PASS: every packet statement appears verbatim, in order, in the original.")
    if page_checks:
        # Anchors may use printed page numbers that differ from the file's by a fixed amount.
        offset = Counter(cited - actual for _, cited, actual in page_checks if actual).most_common(1)[0][0]
        wrong = [(source_id, cited, actual) for source_id, cited, actual in page_checks
                 if actual and cited - actual != offset]
        if offset:
            print(f"NOTE: page anchors are consistently {offset:+d} from the file's page numbers "
                  "(for example printed page numbers); checked on that basis.")
        if wrong:
            print("REVIEW: page anchors that do not match where the text starts:")
            for source_id, cited, actual in wrong[:20]:
                print(f"  - {source_id}: anchor says p. {cited}, text starts on p. {actual + offset}")
        else:
            print(f"ANCHORS: all {len(page_checks)} page anchors match where their text starts.")
    if raw.suffix.lower() == ".pdf":
        non_text = pdf_non_text(raw)
        if non_text:
            print("NOT TEXT: content in images cannot be copied or verified; check these pages by eye:")
            for line in non_text:
                print(f"  - {line}")
    if dropped:
        print("SET ASIDE: page headers/footers repeated on most pages, kept once at first appearance:")
        for text, count in dropped.items():
            print(f"  - {text}   ({count} repeats)")
    if uncovered:
        print("REVIEW: original text not carried into any statement (confirm each omission is intended):")
        for text, count in uncovered.items():
            print(f"  - {text[:200]}" + (f"   (x{count})" if count > 1 else ""))
    else:
        print("COVERAGE: all original text is carried into the packet.")
    return 1 if problems else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    build_parser = commands.add_parser("build", help="write a draft packet to stdout")
    build_parser.add_argument("raw", type=Path)
    build_parser.add_argument("--prefix", help="anchor prefix (default: the original's file name)")
    build_parser.add_argument("--keep-furniture", action="store_true",
                              help="keep every repeat of page headers and footers")
    verify_parser = commands.add_parser("verify", help="check a packet against its original")
    verify_parser.add_argument("raw", type=Path)
    verify_parser.add_argument("packet", type=Path)
    verify_parser.add_argument("--keep-furniture", action="store_true",
                               help="the packet keeps every header/footer repeat")
    args = parser.parse_args()
    if args.command == "build":
        sys.stdout.reconfigure(encoding="utf-8", newline="\n")
        sys.stdout.write(build(args.raw, args.prefix or args.raw.name, args.keep_furniture))
        return 0
    return verify(args.raw, args.packet, args.keep_furniture)


if __name__ == "__main__":
    raise SystemExit(main())
