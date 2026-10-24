from pathlib import Path
R=Path(__file__).resolve().parents[1];p=R/'rebuild/tools/validate_packet.py';old=p.read_bytes();s=old.decode('utf-8');assert '\r' not in s
needle='PERSONAL_OWNER = re.compile('
i=s.index(needle)
s=s[:i]+r'''# Dependency constructions can carry participation requirements without a colon.
DEPENDENCY_CUE = re.compile(
    r"\b(?:participation|admission|entry|eligibility)\b[^.;!?]*\b"
    r"(?:depends?\s+on|contingent\s+on|conditional\s+on|conditioned\s+on|determined\s+by)\b", re.IGNORECASE)
# Only a literal body-supported reference can keep a private-looking nested
# heading inside the inherited requirement. Anchors and output placement do not.
SCOPE_REFERENCE = re.compile(r"\b(?:including|subsections?|sections?|labelled|labeled|titled|headed)\b", re.IGNORECASE)
''' +s[i:]
a=s.index('PERSONAL_HEADER = re.compile(');b=s.index('\n',a)
s=s[:a]+r'''PERSONAL_HEADER = re.compile(
    r"\s*(?:(?:my|our|your|his|her|their)\s+)?(?:(?:personal|private|family)\s+)+"
    r"(?:calendar|correspondence|notes|schedule|email|thread|events|activities)\s*[:.—-]?\s*", re.IGNORECASE)'''+s[b:]
a=s.index('def personal_hint_exclusions(');b=s.index('def difference(',a)
s=s[:a]+r'''def personal_hint_exclusions(statements, placed):
    """Bounded warning filter; exact quotation/citation checks are separate.

    Require affirmative personal support in every clause before exemption.
    Explicitly referenced nested private headings inherit requirement scope;
    unrelated private headings reset it. Unknown transitions keep review hints.
    This finite heuristic is not a complete semantic classifier.
    """
    def personal_support(text):
        return bool((PERSONAL_OWNER.search(text) and PERSONAL_ACTIVITY.search(text))
                    or PERSONAL_CONTRIBUTION.search(text))

    result = set()
    protected = False
    scope_references = []
    for sid, (anchor, body) in statements.items():
        personal = personal_support(body)
        hard_procurement = PROCUREMENT_CUE.search(body) or OFFER_DELIVERY_CUE.search(body) or DEPENDENCY_CUE.search(body)
        clinical = CLINICAL_CUE.search(body)
        # A conjunction after a comma starts another clause; a calendar-year
        # comma does not. Unknown extra clauses cannot borrow personal support.
        clauses = [c for c in re.split(r"[;.!?](?:\s+|$)|,\s*(?=(?:then|and|but|while|also|or)\b)", body, flags=re.IGNORECASE) if c.strip()]
        private_statement = bool(clauses) and all(personal_support(c) for c in clauses)
        duty_clauses = [c for c in clauses if OBLIGATION_CUE.search(c)]
        private_duty = bool(duty_clauses) and len(clauses) == len(duty_clauses) and all(
            PRIVATE_SELF_DUTY.search(c) and PERSONAL_OWNER.search(c) and PERSONAL_ACTIVITY.search(c)
            and len(OBLIGATION_CUE.findall(c)) == 1
            and not re.search(r"\b(and|but|while|also|then|or)\b", c, re.IGNORECASE)
            for c in duty_clauses)
        procurement = hard_procurement or (bool(duty_clauses) and not private_duty) or (personal and not private_statement)
        requirement_heading = body.rstrip().endswith(":") or (len(body) <= 120 and body.isupper())
        private_heading = PERSONAL_HEADER.fullmatch(body)
        heading_key = body.strip().rstrip(":.—- ").casefold()
        referenced_private = private_heading and any(
            re.search(r"(?<!\w)" + re.escape(heading_key) + r"(?!\w)", text.casefold())
            for text in scope_references)
        unknown_event_heading = requirement_heading and EVENT_HEADER.search(body) and not personal and not private_heading
        if ((procurement or clinical) and (EVENT_HEADER.search(body) or requirement_heading)) or unknown_event_heading:
            protected = True
            if (procurement or clinical) and SCOPE_REFERENCE.search(body):
                scope_references.append(body)
        elif private_heading and not procurement and not clinical and not referenced_private:
            protected = False
            scope_references.clear()
        only12 = sid in placed.get(12, set()) and not any(sid in placed.get(s, set()) for s in range(1, 12))
        if private_statement and only12 and not procurement and not clinical and not protected:
            result.add(sid)
    return result

'''+s[b:]
new=s.encode('utf-8');assert new[new.index(b'def difference('):]==old[old.index(b'def difference('):]
assert not any(c<32 and c not in (9,10,13) for c in new)
compile(s,str(p),'exec');p.write_bytes(new);print('Applied warning-only fix; strict implementation byte-identical')
