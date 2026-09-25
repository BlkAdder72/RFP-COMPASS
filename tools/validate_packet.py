#!/usr/bin/env python3
"""Validate an RFP Compass card against its source packet.

Checks: exact title and twelve headings in order; nothing but bullets or `- not in source`
anywhere in the card (no prose, subheadings or notes); every bullet quotes one ENTIRE source
statement verbatim with its exact ID and anchor; IDs ascending and unrepeated within each
section; every source statement cited at least once.

It cannot prove that a statement is in the right section or that a `- not in source`
marker is true. As a hint for the human reader it prints REVIEW notes (never failures) when
a statement that looks like a date, an evaluation term, a money amount or a contact
detail is missing from Section 6, 7, 8 or 10, or when one of those sections says `- not in source` although such
statements exist.

A long card may arrive in several replies. Pass the parts in order: every part except the
last must end with the continuation marker line, and the last must not. Parts pasted
together into one file, markers included, are also accepted.

Usage: python -X utf8 tools/validate_packet.py [SOURCE_PACKET CARD_PART_1 [CARD_PART_2 ...]]
With no arguments it checks every packaged sample.
"""
from pathlib import Path
import re
import sys
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = ("01-real-public-notice", "02-sparse", "03-conflicting", "04-real-tbrpc-auditing-rfp")
PAIRS = tuple((ROOT / "samples" / name / "source-packet.md", ROOT / "samples" / name / "bid-compliance-card.md")
              for name in SAMPLES)
TITLE = "# RFP COMPASS — BID COMPLIANCE CARD"
HEADINGS = (
    "## 1. Opportunity identity", "## 2. Scope, term, and program context stated", "## 3. Eligibility and qualifications stated",
    "## 4. Application stages and submission mechanics stated", "## 5. Mandatory attachments and forms stated",
    "## 6. Dates and events stated", "## 7. Evaluation stated", "## 8. Commercial, performance, and post-award terms stated",
    "## 9. Tables, schedules, and templates", "## 10. Definitions, authority, and administrative terms",
    "## 11. Addenda, conflicts, and open items", "## 12. Unmapped source evidence",
)
MISSING = "- not in source"
CONTINUED = "<!-- RFP COMPASS: continued in next reply -->"
SOURCE = re.compile(r"^(S\d+) \| ([^|]+?) \| (\S.*)$")
BULLET = re.compile(r"^- (“|\")(.+)(”|\") \[source: source-packet\.md:(S\d+); (.+)\]$")
# Review hints (never failures): wording that usually means a statement belongs in a section.
MONTHS = r"(January|February|March|April|May|June|July|August|September|October|November|December)"
LIKELY = {
    6: re.compile(MONTHS + r"\s+\d{1,2}\b|\b\d{1,2}/\d{1,2}/\d{2,4}\b|\b\d{1,2}\s?:\s?\d{2}\s*(a\.?m\.?|p\.?m\.?)(\W|$)",
                  re.IGNORECASE),
    7: re.compile(r"\b(evaluat\w*|scor(e|ed|es|ing)|criteria|weighted)\b|\b\d+\s*points?\b", re.IGNORECASE),
    8: re.compile(r"\$\s?\d"),
    10: re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+|\(\d{3}\)\s?\d{3}-\d{4}|\b\d{3}-\d{3}-\d{4}\b"),
}
LIKELY_NAMES = {6: "dates or times", 7: "evaluation terms", 8: "money amounts", 10: "contact details"}
INVISIBLE = {"\u00a0": " ", "\u202f": " ", "\u2007": " ", "\u200b": "", "\u200c": "", "\u200d": "",
             "\u2060": "", "\ufeff": "", "\u00ad": ""}


def visible(text: str) -> str:
    """Text with invisible spacing characters made ordinary, for comparison only."""
    return "".join(INVISIBLE.get(character, character) for character in text)


def difference(expected: str, actual: str) -> str:
    """Where two strings first differ, shown with a little context."""
    index = next((i for i, (a, b) in enumerate(zip(expected, actual)) if a != b), min(len(expected), len(actual)))
    def show(text: str) -> str:
        piece = text[max(0, index - 20):index + 20]
        return "".join(f"<U+{ord(c):04X}>" if unicodedata.category(c) in ("Zs", "Cf", "Co") and c != " " else c for c in piece)
    return f"at character {index + 1}: packet …{show(expected)}… card …{show(actual)}…"


def join_parts(outputs: list[Path]) -> tuple[list[str], list[str]]:
    """Concatenate card parts, checking continuation markers."""
    errors, lines = [], []
    for number, output in enumerate(outputs, 1):
        part = output.read_text(encoding="utf-8-sig").splitlines()
        while part and not part[-1].strip():
            part.pop()
        last = number == len(outputs)
        ends_continued = bool(part) and part[-1].strip() == CONTINUED
        if ends_continued and last:
            errors.append(f"{output}: the card is incomplete: this part ends with the continuation marker, "
                          "so reply `continue` and pass the next part too")
        if not ends_continued and not last:
            errors.append(f"{output}: part {number} of {len(outputs)} does not end with the continuation marker")
        if ends_continued:
            part.pop()
        if len(outputs) > 1 and any(line.strip() == CONTINUED for line in part):
            errors.append(f"{output}: the continuation marker may appear only as the last line of a part")
        # A single file may hold all parts pasted together, markers included.
        lines += [line for line in part if line.strip() != CONTINUED]
    return lines, errors


def validate(source: Path, outputs: list[Path]) -> tuple[list[str], list[str]]:
    errors, notes = [], []
    output = outputs[0] if len(outputs) == 1 else Path(f"{outputs[0]} (+{len(outputs) - 1} part(s))")
    statements, order = {}, []
    for number, line in enumerate(source.read_text(encoding="utf-8-sig").splitlines(), 1):
        if not line.strip():
            continue
        match = SOURCE.match(line)
        if not match:
            errors.append(f"{source}:{number}: invalid source statement (need `S001 | anchor | text`)")
            continue
        source_id, anchor, body = match.groups()
        if source_id in statements:
            errors.append(f"{source}:{number}: duplicate source ID {source_id}")
        if body != body.rstrip():
            notes.append(f"{source}: {source_id} ends with spaces; they are ignored when comparing quotations")
        statements[source_id] = (anchor, body.rstrip())
        order.append(source_id)
    if order != [f"S{i:03d}" for i in range(1, len(order) + 1)]:
        errors.append(f"{source}: source IDs must be sequential from S001")

    lines, part_errors = join_parts(outputs)
    errors += part_errors
    while lines and not lines[0].strip():
        lines.pop(0)
    if lines and lines[0].strip() == "INPUT NOT READY":
        return [f"{output}: no card produced (response is INPUT NOT READY)"], notes
    if not lines or lines[0] != TITLE:
        errors.append(f"{output}: first line must be exactly `{TITLE}` (no fence, preamble or blank title)")
        return errors, notes
    if any(lines.count(heading) != 1 for heading in HEADINGS) or \
            [lines.index(h) for h in HEADINGS] != sorted(lines.index(h) for h in HEADINGS):
        absent = [heading[3:] for heading in HEADINGS if heading not in lines]
        detail = f" (missing: {'; '.join(absent)})" if absent else ""
        errors.append(f"{output}: the twelve headings are missing, duplicated, renamed or out of order{detail}")
        return errors, notes
    stray = [line for line in lines[1:lines.index(HEADINGS[0])] if line.strip()]
    if stray:
        errors.append(f"{output}: text between the title and section 1 is not allowed: {stray[0]}")

    cited, straight, invisible, placed = set(), 0, set(), {}
    for index, heading in enumerate(HEADINGS):
        start = lines.index(heading) + 1
        end = lines.index(HEADINGS[index + 1]) if index + 1 < len(HEADINGS) else len(lines)
        content = [line for line in lines[start:end] if line.strip()]
        if not content:
            errors.append(f"{output}: {heading} is empty (needs bullets or `{MISSING}`)")
            continue
        if MISSING in content and len(content) != 1:
            errors.append(f"{output}: {heading} mixes `{MISSING}` with other lines")
        ids = []
        for line in content:
            if line == MISSING:
                continue
            match = BULLET.match(line)
            if not match:
                errors.append(f"{output}: {heading}: line is not a valid bullet: {line[:120]}")
                continue
            opening, quote, closing, source_id, cited_anchor = match.groups()
            if (opening, closing) == ('"', '"'):
                straight += 1
            elif (opening, closing) != ("“", "”"):
                errors.append(f"{output}: {heading}: mismatched quotation marks on {source_id}")
            ids.append(source_id)
            cited.add(source_id)
            if source_id not in statements:
                errors.append(f"{output}: {heading}: citation {source_id} does not exist in the packet")
            elif cited_anchor != statements[source_id][0]:
                errors.append(f"{output}: {heading}: anchor for {source_id} does not match the packet")
            elif quote != statements[source_id][1]:
                expected = statements[source_id][1]
                if visible(quote) == visible(expected):
                    invisible.add(source_id)
                elif len(quote) < len(expected) and quote in expected:
                    errors.append(f"{output}: {heading}: quotation is only part of {source_id}; "
                                  "the entire statement is required")
                else:
                    errors.append(f"{output}: {heading}: quotation does not match {source_id} "
                                  f"{difference(expected, quote)}")
        if len(set(ids)) != len(ids):
            errors.append(f"{output}: {heading}: a source ID appears twice")
        if ids != sorted(ids, key=lambda value: int(value[1:])):
            errors.append(f"{output}: {heading}: bullets are not in source-ID order")
        placed[index + 1] = set(ids)

    for number, pattern in LIKELY.items():
        matching = [source_id for source_id, (_, body) in statements.items() if pattern.search(body)]
        unplaced = [source_id for source_id in matching if source_id not in placed.get(number, set())]
        if matching and not placed.get(number):
            notes.append(f"REVIEW {output}: Section {number} says `not in source`, but {', '.join(matching[:8])} "
                         f"look like {LIKELY_NAMES[number]}. Check the section trigger; a false `not in source` is the "
                         "one error that matters most")
        elif unplaced:
            notes.append(f"REVIEW {output}: {', '.join(unplaced[:8])} look like {LIKELY_NAMES[number]} "
                         f"but are not in Section {number}; confirm that is intended")

    uncited = sorted(set(statements) - cited, key=lambda value: int(value[1:]))
    if uncited:
        errors.append(f"{output}: source statements never cited: {', '.join(uncited)}")
    if straight:
        notes.append(f"{output}: {straight} bullet(s) use straight quotes; the contract form is “curly” quotes")
    if invisible:
        notes.append(f"{output}: invisible spacing characters (such as a non-breaking space) differ from the packet in "
                     f"{', '.join(sorted(invisible, key=lambda value: int(value[1:])))}; the visible text matches")
    return errors, notes


def main() -> int:
    if len(sys.argv) >= 3:
        pairs = ((Path(sys.argv[1]), [Path(part) for part in sys.argv[2:]]),)
    elif len(sys.argv) == 1:
        pairs = tuple((source, [card]) for source, card in PAIRS)
    else:
        print("Usage: validate_packet.py [SOURCE_PACKET CARD_PART_1 [CARD_PART_2 ...]]", file=sys.stderr)
        return 2
    errors, notes = [], []
    for source, outputs in pairs:
        missing = [path for path in [source, *outputs] if not path.is_file()]
        if missing:
            errors.append(f"missing file: {missing[0]}")
            continue
        pair_errors, pair_notes = validate(source, outputs)
        errors += pair_errors
        notes += pair_notes
    for note in notes:
        print(f"NOTE: {note}")
    if errors:
        print("FAIL\n" + "\n".join(errors))
        return 1
    print(f"PASS ({len(pairs)} card{'s' if len(pairs) != 1 else ''}): fixed shape, no extra text, "
          "entire-statement quotations, exact citations, ID order, full source coverage.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
