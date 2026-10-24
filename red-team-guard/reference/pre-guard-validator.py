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
import argparse
import hashlib
import json

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
# Body-supported, conservative personal evidence. Never classify from a filename,
# source ID, date, or the card's own placement alone. Explicit requirements win.
PROCUREMENT_CUE = re.compile(
    r"\b(responses?|applicants?|applications?|proposals?|bidders?|respondents?|solicitations?|rfp|ifb|rfq|bids?|contracts?|"
    r"procurement|addend(?:um|a)|tenders?|vendors?|submissions?|submit|submitted|required|requires|requirements?|mandatory|shall|must|"
    r"deadlines?|due|closing|closes?|eligibility|registration|awards?|fees?|pricing)\b", re.IGNORECASE)
# Obligation phrases protect warning context even without a procurement noun.
# Delivery of offers is a response cue; "offer" alone is too broad.
OBLIGATION_CUE = re.compile(
    r"\b(?:(?:have|has|had|need|needs)\s+to|(?:am|is|are|was|were)\s+to|will\s+be\s+expected\s+to|"
    r"(?:is|are|be)\s+(?:obliged|obligated)\s+to|condition\s+of\s+(?:entry|participation))\b", re.IGNORECASE)
# A private first-person duty is not itself a solicitation requirement. Require
# positive personal evidence in that same clause; mixed or unknown duties keep hints.
PRIVATE_SELF_DUTY = re.compile(r"^\s*I\s+(?:(?:do|did)\s+not\s+)?(?:have|had|need)\s+to\b", re.IGNORECASE)
OFFER_DELIVERY_CUE = re.compile(
    r"\b(?:deliver|send|lodge|provide|return|present)\b[^.;!?]*\boffers?\b|"
    r"\boffers?\b[^.;!?]*\b(?:reach|arrive|received|receipt)\b", re.IGNORECASE)
PERSONAL_OWNER = re.compile(r"\b(my|our|your|his|her|their)\b", re.IGNORECASE)
PERSONAL_ACTIVITY = re.compile(
    r"\b(potluck|birthday|dentist|(?:baptism|christening)(?:\s+ceremony)?|(?:baby|bridal)\s+shower|graduation\s+(celebration|party|ceremony)|wedding\s+anniversary|family\s+(picnic|party|reunion|dinner)|"
    r"(piano|school|dance)\s+recital|(retirement|farewell)\s+(lunch|dinner|party)|"
    r"(physical\s+therapy|physiotherapy|doctor|medical)\s+appointment)\b", re.IGNORECASE)
EVENT_HEADER = re.compile(r"\b(events?|meetings?|conferences?|attendance|activities|schedules?|calendars?|appointments?|meals?|lunch|dinner|visits?)\b", re.IGNORECASE)
CLINICAL_CUE = re.compile(r"\b(patients?|clinical|beneficiaries|services?|providers?|healthcare)\b", re.IGNORECASE)
PERSONAL_HEADER = re.compile(r"\s*(personal|private|family)\s+(calendar|correspondence|notes|schedule|email|thread|events|activities)\s*[:.—-]?\s*", re.IGNORECASE)
PERSONAL_CONTRIBUTION = re.compile(r"\b(?:please\s+)?bring\s+\$\s*\d+(?:\.\d+)?\s+for\s+(?:lunch|dinner)\b", re.IGNORECASE)


def personal_hint_exclusions(statements, placed):
    """Bounded personal-calendar filter, with a veto for requirement-bearing text.

    This is not a complete semantic classifier. Unknown meetings and mixed
    requirements keep their hints. Requirement context follows source order,
    independent of line, paragraph, page or document anchors. Only an explicit
    personal heading in the source body resets it; unknown transitions do not.
    """
    result = set()
    protected = False
    for sid, (anchor, body) in statements.items():
        personal = (PERSONAL_OWNER.search(body) and PERSONAL_ACTIVITY.search(body)) or PERSONAL_CONTRIBUTION.search(body)
        hard_procurement = PROCUREMENT_CUE.search(body) or OFFER_DELIVERY_CUE.search(body)
        clinical = CLINICAL_CUE.search(body)
        clauses = [c for c in re.split(r"[;.!?](?:\s+|$)", body) if c.strip()]
        duty_clauses = [c for c in clauses if OBLIGATION_CUE.search(c)]
        private_duty = bool(duty_clauses) and len(clauses) == len(duty_clauses) and all(
            PRIVATE_SELF_DUTY.search(c) and PERSONAL_OWNER.search(c) and PERSONAL_ACTIVITY.search(c)
            and len(OBLIGATION_CUE.findall(c)) == 1
            and not re.search(r"\b(and|but|while|also)\b", c, re.IGNORECASE)
            for c in duty_clauses)
        procurement = hard_procurement or (bool(duty_clauses) and not private_duty)
        requirement_heading = body.rstrip().endswith(":") or (len(body) <= 120 and body.isupper())
        private_heading = PERSONAL_HEADER.fullmatch(body)
        # Unknown event-list headings preserve scope without a fixed modality list.
        # A private duty cannot create or clear genuine inherited requirements.
        unknown_event_heading = requirement_heading and EVENT_HEADER.search(body) and not personal and not private_heading
        if ((procurement or clinical) and (EVENT_HEADER.search(body) or requirement_heading)) or unknown_event_heading:
            protected = True
        elif private_heading and not procurement and not clinical:
            protected = False
        only12 = sid in placed.get(12, set()) and not any(sid in placed.get(s, set()) for s in range(1, 12))
        if personal and only12 and not procurement and not clinical and not protected:
            result.add(sid)
    return result
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


def reviewed_exclusions(source, statements, placed, review_path):
    """Validate an explicitly selected external adjudication; never trust anchors."""
    if review_path is None:
        return set(), []
    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key {key}")
            result[key] = value
        return result
    def require(condition, message):
        if not condition:
            raise ValueError(message)
    try:
        review = json.loads(Path(review_path).read_text(encoding="utf-8-sig"), object_pairs_hook=unique_object)
        require(isinstance(review, dict), "review must be an object")
        require(set(review) == {"schema_version", "packet_sha256", "reviewer", "decisions"}, "unexpected review fields")
        require(type(review["schema_version"]) is int and review["schema_version"] == 1, "unsupported schema version")
        require(review["packet_sha256"] == hashlib.sha256(source.read_bytes()).hexdigest(), "packet SHA-256 mismatch")
        require(isinstance(review["reviewer"], str) and review["reviewer"].strip(), "reviewer must be named")
        require(isinstance(review["decisions"], list), "decisions must be a list")
        approved = set()
        procurement = re.compile(r"\b(proposals?|bidders?|respondents?|solicitations?|rfp|ifb|rfq|bids?|contracts?|procurement|addend(?:um|a)|tenders?)\b|\bpricing\s+sheet\b", re.IGNORECASE)
        for decision in review["decisions"]:
            require(isinstance(decision, dict) and set(decision) == {"source_id", "statement_sha256", "reason"}, "unexpected decision fields")
            sid = decision["source_id"]
            require(isinstance(sid, str) and sid in statements, "unknown source ID")
            require(sid not in approved, f"duplicate decision ID {sid}")
            require(isinstance(decision["reason"], str) and decision["reason"].strip(), f"{sid}: reason required")
            body = statements[sid][1]
            require(decision["statement_sha256"] == hashlib.sha256(body.encode("utf-8")).hexdigest(), f"{sid}: statement SHA-256 mismatch")
            require(not procurement.search(body), f"{sid}: procurement wording cannot be excluded by this conservative review mechanism")
            require(sid in placed.get(12, set()) and not any(sid in placed.get(section, set()) for section in range(1, 12)),
                    f"{sid}: selected exclusion must appear only in Section 12")
            approved.add(sid)
        return approved, []
    except (OSError, ValueError, TypeError, KeyError) as error:
        return set(), [f"{review_path}: invalid reviewed exclusions: {error}; no exclusions applied"]


def validate(source: Path, outputs: list[Path], review_path: Path | None = None) -> tuple[list[str], list[str]]:
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
        statements[source_id] = (anchor, body)
        order.append(source_id)
    if order != [f"S{i:03d}" for i in range(1, len(order) + 1)]:
        errors.append(f"{source}: source IDs must be sequential from S001")
    markup = [source_id for source_id, (_, body) in statements.items()
              if "<!--" in body or re.search("</?[A-Za-z][^>]*>|[\u202a-\u202e\u2066-\u2069]", body)]
    if markup:
        notes.append(f"{source}: {', '.join(markup[:8])} contain HTML tags, comments or text-direction "
                     "controls. A rendered Markdown view may hide or rearrange them, so read the raw card "
                     "file to see those quotes in full")

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

    cited, placed = set(), {}
    # Trust personal placement per exact citation. An unrelated bad citation must
    # still fail the card, without turning valid personal rows into false hints.
    filter_shape_safe = not errors
    trusted, tainted, citation_counts = set(), set(), {}
    for index, heading in enumerate(HEADINGS):
        start = lines.index(heading) + 1
        end = lines.index(HEADINGS[index + 1]) if index + 1 < len(HEADINGS) else len(lines)
        content = [line for line in lines[start:end] if line.strip()]
        if not content:
            filter_shape_safe = False
            errors.append(f"{output}: {heading} is empty (needs bullets or `{MISSING}`)")
            continue
        if MISSING in content and len(content) != 1:
            filter_shape_safe = False
            errors.append(f"{output}: {heading} mixes `{MISSING}` with other lines")
        ids = []
        for line in content:
            if line == MISSING:
                continue
            match = BULLET.match(line)
            if not match:
                filter_shape_safe = False
                errors.append(f"{output}: {heading}: line is not a valid bullet: {line[:120]}")
                continue
            opening, quote, closing, source_id, cited_anchor = match.groups()
            citation_counts[source_id] = citation_counts.get(source_id, 0) + 1
            if (opening, closing) == ('"', '"'):
                tainted.add(source_id)
                errors.append(f"{output}: {heading}: straight quotation delimiters on {source_id}; curly delimiters required")
            elif (opening, closing) != ("“", "”"):
                tainted.add(source_id)
                errors.append(f"{output}: {heading}: mismatched quotation marks on {source_id}")
            ids.append(source_id)
            cited.add(source_id)
            if source_id not in statements:
                tainted.add(source_id)
                errors.append(f"{output}: {heading}: citation {source_id} does not exist in the packet")
            elif cited_anchor != statements[source_id][0]:
                tainted.add(source_id)
                errors.append(f"{output}: {heading}: anchor for {source_id} does not match the packet")
            elif quote != statements[source_id][1]:
                tainted.add(source_id)
                expected = statements[source_id][1]
                if len(quote) < len(expected) and quote in expected:
                    errors.append(f"{output}: {heading}: quotation is only part of {source_id}; "
                                  "the entire statement is required")
                else:
                    errors.append(f"{output}: {heading}: quotation does not match {source_id} "
                                  f"{difference(expected, quote)}")
            else:
                trusted.add(source_id)
        if len(set(ids)) != len(ids):
            errors.append(f"{output}: {heading}: a source ID appears twice")
        if ids != sorted(ids, key=lambda value: int(value[1:])):
            errors.append(f"{output}: {heading}: bullets are not in source-ID order")
        placed[index + 1] = set(ids)

    approved, review_errors = reviewed_exclusions(source, statements, placed, review_path)
    errors += review_errors
    if approved and not errors:
        notes.append(f"APPLIED EXCLUSIONS {review_path}: {', '.join(sorted(approved))}; explicit review decisions, not automatic relevance proof")
    elif errors:
        approved = set()
    personal = personal_hint_exclusions(statements, placed) if filter_shape_safe and not review_errors else set()
    personal = {sid for sid in personal if sid in trusted and sid not in tainted and citation_counts.get(sid) == 1}
    if personal:
        notes.append(f"PERSONAL HINT FILTER: {', '.join(sorted(personal))}; personal activity in source text, no procurement cue, quoted only in Section 12; bounded heuristic, not semantic proof")
    for number, pattern in LIKELY.items():
        matching = [source_id for source_id, (_, body) in statements.items()
                    if pattern.search(body) and source_id not in approved and source_id not in personal]
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
    return errors, notes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path, help="source packet followed by card parts")
    parser.add_argument("--reviewed-exclusions", type=Path, help="explicit operator-selected review record; never inferred from source labels")
    args = parser.parse_args()
    if len(args.paths) >= 2:
        pairs = ((args.paths[0], args.paths[1:]),)
    elif not args.paths and args.reviewed_exclusions is None:
        pairs = tuple((source, [card]) for source, card in PAIRS)
    else:
        parser.error("provide source packet and card parts; review records cannot be applied to the default sample sweep")
    errors, notes = [], []
    for source, outputs in pairs:
        missing = [path for path in [source, *outputs] if not path.is_file()]
        if missing:
            errors.append(f"missing file: {missing[0]}")
            continue
        pair_errors, pair_notes = validate(source, outputs, args.reviewed_exclusions)
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
