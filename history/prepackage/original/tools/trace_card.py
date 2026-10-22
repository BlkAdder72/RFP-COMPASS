#!/usr/bin/env python3
"""Trace every claim in an RFP Compass card back to the original document.

Usage: python -X utf8 tools/trace_card.py ORIGINAL SOURCE_PACKET CARD_PART_1 [CARD_PART_2 ...] [--full]

Runs both checks and joins them:
  1. card -> packet: every bullet is one entire packet statement with its ID and anchor
     (tools/validate_packet.py);
  2. packet -> original: every statement appears verbatim, in order, at its anchored page
     (tools/make_packet.py verify).
Then prints, for every bullet, the section, the statement ID and where its text sits in the
original. With --full the table lists every bullet; otherwise it lists only problems.
ORIGINAL may be a PDF (needs pdfplumber) or a .txt/.md file.
"""
from pathlib import Path
import contextlib
import io
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_packet  # noqa: E402
import validate_packet  # noqa: E402

BULLET = validate_packet.BULLET


def main() -> int:
    args = [arg for arg in sys.argv[1:] if arg != "--full"]
    full = "--full" in sys.argv[1:]
    if len(args) < 3:
        print(__doc__.strip().splitlines()[2], file=sys.stderr)
        return 2
    original, packet, parts = Path(args[0]), Path(args[1]), [Path(arg) for arg in args[2:]]

    card_errors, card_notes = validate_packet.validate(packet, parts)
    locations: dict = {}
    report = io.StringIO()
    with contextlib.redirect_stdout(report):
        packet_status = make_packet.verify(original, packet, False, locations)
    packet_lines = report.getvalue().splitlines()
    packet_problems = {line.split(":")[0].strip() for line in packet_lines if re.match(r"\s+S\d+:", line)}

    rows, section = [], None
    lines, _ = validate_packet.join_parts(parts)
    for line in lines:
        if line.startswith("## "):
            section = line[3:].split(".")[0]
            continue
        match = BULLET.match(line)
        if match:
            source_id = match.group(4)
            page = locations.get(source_id)
            if source_id in packet_problems or source_id not in locations:
                status = "NOT TRACED (see packet check)"
            else:
                status = f"found in original{f' on p. {page}' if page else ''}"
            rows.append((section, source_id, match.group(5), status))

    traced = sum(1 for row in rows if row[3].startswith("found"))
    print(f"CLAIMS: {len(rows)} bullets in the card")
    print(f"  card -> packet:   {'PASS' if not card_errors else 'FAIL (' + str(len(card_errors)) + ' problem(s))'}")
    print(f"  packet -> original: {'PASS' if packet_status == 0 else 'FAIL'}")
    print(f"  traced end to end: {traced} of {len(rows)} bullets")
    shown = rows if full else [row for row in rows if not row[3].startswith("found")]
    if shown:
        print("\nSection | Statement | Anchor | Where the quote sits in the original")
        for section_number, source_id, anchor, status in shown:
            print(f"  §{section_number} | {source_id} | {anchor} | {status}")
    for error in card_errors:
        print(f"CARD: {error}")
    for note in card_notes:
        print(f"NOTE: {note}")
    for line in packet_lines:
        if line.startswith(("FAIL", "REVIEW", "NOT TEXT", "NOTE")) or re.match(r"\s+S\d+:", line):
            print(f"PACKET: {line.strip()}")
    return 0 if not card_errors and packet_status == 0 and traced == len(rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
