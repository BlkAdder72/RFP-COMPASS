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
# A reservation to modify an RFP is an administrative right. Its incidental
# "including ... selection criteria" object supplies no scoring method by itself.
# Remove only that complete object in an analysis copy, never the source/card.
MODIFY_RESERVATION = re.compile(r"\breserves?\s+the\s+right\b[^.;!?]{0,100}\b(?:modify|amend|revise|change)\b[^.;!?]{0,60}\b(?:rfp|solicitation|request\s+for\s+proposals)\b", re.IGNORECASE)
INCIDENTAL_CRITERIA = re.compile(r"\(\s*including(?:\s+but\s+not\s+limited\s+to)?\s+(?:the\s+)?(?:selection|evaluation)\s+criteria\s*\)|,\s*including(?:\s+but\s+not\s+limited\s+to)?\s+(?:the\s+)?(?:selection|evaluation)\s+criteria(?=\s*[.;!?]?\s*$)", re.IGNORECASE)
EVALUATION_ACTION = re.compile(r"\b(?:review(?:ed|s)?|rank(?:ed|s|ing)?|short.?list\w*|scor\w*|evaluat\w*|weight\w*|points?)\b|\d", re.IGNORECASE)

def likely_match(number, pattern, body):
    if number == 7 and MODIFY_RESERVATION.search(body):
        remainder=INCIDENTAL_CRITERIA.sub('', body)
        if remainder != body and not pattern.search(remainder) and not EVALUATION_ACTION.search(remainder):
            return False
    return bool(pattern.search(body))
# Body-supported, conservative personal evidence. Never classify from a filename,
# source ID, date, or the card's own placement alone. Explicit requirements win.
PROCUREMENT_CUE = re.compile(
    r"\b(responses?|applicants?|applications?|proposals?|bidders?|respondents?|solicitations?|rfp|ifb|rfq|bids?|contracts?|"
    r"procurement|addend(?:um|a)|tenders?|vendors?|submissions?|submit|submitted|required|requires|requirements?|mandatory|compulsory|shall|must|"
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
# Dependency constructions can carry participation requirements without a colon.
DEPENDENCY_CUE = re.compile(
    r"\b(?:participation|admission|entry|eligibility)\b[^.;!?]*?\b"
    r"(?:depends?\s+on|hinges?\s+on|dependent\s+on|contingent\s+on|conditional\s+on|conditioned\s+on|determined\s+by)\b", re.IGNORECASE)
# Only a literal body-supported reference can keep a private-looking nested
# heading inside the inherited requirement. Anchors and output placement do not.
SCOPE_REFERENCE = re.compile(r"\b(?:including|subsections?|sections?|labelled|labeled|titled|headed)\b", re.IGNORECASE)
PERSONAL_OWNER = re.compile(r"\b(my|our|your|his|her|their)\b", re.IGNORECASE)
PERSONAL_ACTIVITY = re.compile(
    r"\b(potluck|birthday(?:\s+(?:dinner|party|celebration))?|dentist|(?:baptism|christening)(?:\s+ceremony)?|(?:baby|bridal)\s+shower|graduation\s+(celebration|party|ceremony)|wedding\s+anniversary|family\s+(picnic|party|reunion|dinner)|"
    r"(piano|school|dance)\s+recital|(retirement|farewell)\s+(lunch|dinner|party)|"
    r"(physical\s+therapy|physiotherapy|doctor|medical)\s+appointment)\b", re.IGNORECASE)
EVENT_HEADER = re.compile(r"\b(events?|meetings?|conferences?|attendance|activities|schedules?|calendars?|appointments?|meals?|lunch|dinner|visits?)\b", re.IGNORECASE)
CLINICAL_CUE = re.compile(r"\b(patients?|clinical|beneficiaries|services?|providers?|healthcare)\b", re.IGNORECASE)
# Parentheses are accepted only around an explicitly private annotation.
PRIVATE_ANNOTATION = r"(?:unrelated\s+)?(?:personal|private|family)\s+(?:correspondence|notes|calendar|schedule|email|thread)"
OUTSIDE_PRIVATE_ANNOTATION = r"(?:outside|unrelated\s+to|not\s+part\s+of)\s+(?:the\s+)?(?:procurement|solicitation)"
PRIVATE_ANNOTATION = r"(?:" + PRIVATE_ANNOTATION + "|" + OUTSIDE_PRIVATE_ANNOTATION + ")"
PERSONAL_HEADER = re.compile(
    r"\s*(?P<label>(?:(?:my|our|your|his|her|their)\s+)?(?:(?:personal|private|family)\s+)+"
    r"(?:calendar|correspondence|notes|schedule|email|thread|events|activities))"
    r"(?:\s*(?:[—–-]|:)\s*" + PRIVATE_ANNOTATION + r"|\s*\(\s*" + PRIVATE_ANNOTATION + r"\s*\))?\s*[:.—-]?\s*", re.IGNORECASE)
# An official participation payment cannot borrow a personal activity cue.
PAYMENT_CUE = re.compile(r"\b(?:official\s+(?:participation\s+|entry\s+)?|participation\s+|entry\s+)(?:deposits?|payments?|charges?|dues)\b", re.IGNORECASE)
EXCLUSION_CUE = re.compile(r"\b(?:unrelated|exclud(?:ed|ing|es?)|outside|not\s+(?:included|part\s+of))\b", re.IGNORECASE)
PERSONAL_CONTRIBUTION = re.compile(r"\b(?:please\s+)?bring\s+\$\s*\d+(?:\.\d+)?\s+for\s+(?:lunch|dinner)\b", re.IGNORECASE)
# A complete bounded private cost-share phrase, never an arbitrary action.
SMALL_NUMBER = r"(?:one|two|three|four|five|six|seven|eight|nine)"
UNDER_HUNDRED = r"(?:zero|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|" + SMALL_NUMBER + r"|(?:twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety)(?:[ -]" + SMALL_NUMBER + r")?)"
UNDER_THOUSAND = r"(?:" + SMALL_NUMBER + r"\s+hundred(?:\s+(?:and\s+)?" + UNDER_HUNDRED + r")?|" + UNDER_HUNDRED + r")"
WORD_NUMBER = r"(?:" + UNDER_THOUSAND + r"\s+thousand(?:\s+(?:and\s+)?" + UNDER_THOUSAND + r")?|" + UNDER_THOUSAND + r")"
PERSONAL_SHARE = re.compile(r"(?:my|our|your|his|her|their)\s+share\s+(?:is|was)\s+(?:\$\s*\d+(?:\.\d{1,2})?|" + WORD_NUMBER + r"\s+dollars?)", re.IGNORECASE)
# Explicit optionality prevents a new unknown-event scope. It never clears an
# inherited duty, and independent procurement/clinical cues still take priority.
OPTIONAL_EVENT = re.compile(
    r"\b(?:attendance|events?|activities)\b[^.;!?]*\b(?:is|are)\s+optional\b|"
    r"\bno\s+attendance\s+condition\b", re.IGNORECASE)



def personal_hint_exclusions(statements, placed):
    """Finite warning filter, separate from unchanged exact-copy validation.

    Unknown event statements keep scope; explicit optionality cannot create it.
    Negated dependencies do not create or clear genuine inherited scope.
    The latest body-supported reference to a private heading controls its
    inclusion; exclusions are local to that heading, not global resets.
    """
    def personal_support(text):
        return bool((PERSONAL_OWNER.search(text) and PERSONAL_ACTIVITY.search(text))
                    or PERSONAL_CONTRIBUTION.search(text))

    def negative_dependency(text):
        # Analyze an expanded copy only; source and citation bytes never change.
        text = re.sub(r"\b(\w+)n['’]t\b", r"\1 not", text, flags=re.IGNORECASE)
        text = re.sub(r"\bnot\s+only\b", "only", text, flags=re.IGNORECASE)
        # Negation must modify the dependency predicate, not a subject qualifier
        # such as "Participation, not payment, depends on ...".
        return bool(re.search(
            r"\b(?:not|never|no\s+longer)\s+(?:\w+\s+){0,2}"
            r"(?:depends?|hinges?|dependent|contingent|conditional|conditioned|determined)\s+(?:on|by)\s*$",
            text, re.IGNORECASE))

    def private_activity_fragment(text):
        # Coordinated noun phrases may share ownership in this statement.
        # Require an entire activity/calendar fragment, never arbitrary actions.
        text = text.strip()
        activity = PERSONAL_ACTIVITY.match(text)
        if not activity:
            return False
        rest = text[activity.end():]
        calendar = r"\b(?:" + MONTHS + r"|is|are|on|at|am|pm)\b|[\d\s,.:/—–-]"
        return not re.sub(calendar, "", rest, flags=re.IGNORECASE)

    def referenced_heading(label, references):
        key = " ".join(label.split()).casefold()
        for reference in reversed(references):
            reference = " ".join(reference.split()).casefold()
            reference = re.sub(r"\bnot\s+(?:excluded|unrelated|outside)\b", "included", reference)
            match = re.search(r"(?<!\w)" + re.escape(key) + r"(?!\w)", reference)
            if match:
                prefix, suffix = reference[:match.start()], reference[match.end():]
                scope_object = r"(?:(?:these|the|this|those|all|our|your|their|required|mandatory)\s+)*(?:events?|activities|requirements?|scope|attendance|participation|procurement|solicitation)\b"
                # Link exclusion to this heading's predicate/object. Descriptive
                # "outside office hours" or "unrelated research" is not scope.
                excluded_before = re.search(
                    r"\b(?:exclud(?:e|es|ed|ing)|not\s+includ(?:e|ing))\s+(?:(?:the|a|this)\s+)?(?:(?:subsection|section|block)\s+)?(?:(?:titled|labelled|labeled|headed)\s+)?[\"“‘']*\s*$", prefix)
                if excluded_before:
                    if re.match(r"\s+from\b", suffix):
                        excluded_before = re.match(r"\s+from\s+" + scope_object, suffix)
                    else:
                        # A program/schedule subject is not the requirement
                        # scope. Bind the entire exclusion relation locally.
                        subject = prefix[:excluded_before.start()].strip(" ,:")
                        scoped_subject = re.fullmatch(
                            scope_object + r"\s*(?:(?:do|does|did)\s*)?", subject)
                        scoped_attendance = re.search(
                            r"\b(?:attend|attending|attendance\s+at)\s+" + scope_object + r"\s*$", subject)
                        excluded_before = scoped_subject or scoped_attendance
                excluded_after = re.match(
                    r"^[\s\"“”'‘’)]*(?:,\s*(?:which|that)\s+)?(?:(?:is|are|was|were|remains?)\s+)?(?:"
                    r"unrelated(?:[.:]?\s*$|\s+to\s+" + scope_object + r")|"
                    r"excluded(?:[.:]?\s*$|\s+from\s+" + scope_object + r")|"
                    r"not\s+(?:included\s+in|part\s+of)\s+" + scope_object + r"|outside\s+(?:the\s+)?(?:scope|requirements)\b)", suffix)
                return not (excluded_before or excluded_after)
        return False

    result = set()
    protected = False
    scope_references = []
    for sid, (anchor, body) in statements.items():
        personal = personal_support(body)
        dependencies = list(DEPENDENCY_CUE.finditer(body))
        positive_dependency = any(not negative_dependency(m.group()) for m in dependencies)
        only_negative_dependency = bool(dependencies) and not positive_dependency
        private_heading = PERSONAL_HEADER.fullmatch(body)
        # Only a complete private heading can neutralize the procurement noun
        # in its own negative annotation. Other cues and inherited scope stay.
        outside_private_heading = bool(private_heading and re.search(OUTSIDE_PRIVATE_ANNOTATION, body, re.IGNORECASE))
        hard_procurement = ((not outside_private_heading and PROCUREMENT_CUE.search(body))
                            or OFFER_DELIVERY_CUE.search(body) or PAYMENT_CUE.search(body) or positive_dependency)
        clinical = CLINICAL_CUE.search(body)
        # A "with ... to <action>" adjunct cannot borrow a preceding private
        # activity. Pure private calendar adjuncts remain intact and are checked
        # against the same independent procurement/clinical vetoes.
        # Collapse only a complete recognized private share in an analysis
        # copy. Its internal number conjunction is not a separate obligation.
        clause_body = PERSONAL_SHARE.sub(lambda m: m.group().split()[0] + " share is $0", body)
        clauses = [c.strip() for c in re.split(
            r"[;.!?](?:\s+|$)|(?:,\s*)?\b(?:and|but|while|also|then|or)\b\s+|"
            r"(?:,\s*)?\bwith\s+(?=[^.;!?]*\bto\s+\w+)",
            clause_body, flags=re.IGNORECASE) if c.strip()]
        private_statement = personal and bool(clauses) and all(
            personal_support(c) or PERSONAL_SHARE.fullmatch(c) or private_activity_fragment(c)
            for c in clauses)
        duty_clauses = [c for c in clauses if OBLIGATION_CUE.search(c)]
        private_duty = private_statement and bool(duty_clauses) and all(
            PRIVATE_SELF_DUTY.search(c) and PERSONAL_OWNER.search(c) and PERSONAL_ACTIVITY.search(c)
            and len(OBLIGATION_CUE.findall(c)) == 1 for c in duty_clauses)
        procurement = hard_procurement or (bool(duty_clauses) and not private_duty) or (personal and not private_statement)
        requirement_heading = body.rstrip().endswith(":") or (len(body) <= 120 and body.isupper())
        private_heading = PERSONAL_HEADER.fullmatch(body)
        referenced_private = private_heading and referenced_heading(private_heading.group('label'), scope_references)
        # Unknown nonprivate events retain hints without guessing a modal verb.
        unknown_event_scope = EVENT_HEADER.search(body) and not personal and not private_heading and not only_negative_dependency and not OPTIONAL_EVENT.search(body)
        if ((procurement or clinical) and (EVENT_HEADER.search(body) or requirement_heading)) or unknown_event_scope:
            protected = True
        elif private_heading and not procurement and not clinical and not referenced_private:
            protected = False
            scope_references.clear()
        if protected and not private_heading:
            for clause in clauses:
                if SCOPE_REFERENCE.search(clause) or EXCLUSION_CUE.search(clause):
                    scope_references.append(clause)
        only12 = sid in placed.get(12, set()) and not any(sid in placed.get(s, set()) for s in range(1, 12))
        if private_statement and only12 and not procurement and not clinical and not protected:
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
                    if likely_match(number, pattern, body) and source_id not in approved and source_id not in personal]
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
