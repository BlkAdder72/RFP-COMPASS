from pathlib import Path
R=Path(__file__).resolve().parents[1];p=R/'rebuild/tools/validate_packet.py';old=p.read_bytes();s=old.decode('utf-8');assert '\r' not in s
s=s.replace(r'\b(?:participation|admission|entry|eligibility)\b[^.;!?]*\b', r'\b(?:participation|admission|entry|eligibility)\b[^.;!?]*?\b')
start=s.index('PERSONAL_HEADER = re.compile(');end=s.index('PERSONAL_CONTRIBUTION =',start)
s=s[:start]+r'''PERSONAL_HEADER = re.compile(
    r"\s*(?P<label>(?:(?:my|our|your|his|her|their)\s+)?(?:(?:personal|private|family)\s+)+"
    r"(?:calendar|correspondence|notes|schedule|email|thread|events|activities))"
    r"(?:\s*(?:[—–-]|:)\s*(?:unrelated\s+)?(?:personal|private|family)\s+"
    r"(?:correspondence|notes|calendar|schedule|email|thread))?\s*[:.—-]?\s*", re.IGNORECASE)
# An official participation payment cannot borrow a personal activity cue.
PAYMENT_CUE = re.compile(r"\b(?:official\s+(?:participation\s+|entry\s+)?|participation\s+|entry\s+)(?:deposits?|payments?|charges?|dues)\b", re.IGNORECASE)
EXCLUSION_CUE = re.compile(r"\b(?:unrelated|exclud(?:ed|ing|es?)|outside|not\s+(?:included|part\s+of))\b", re.IGNORECASE)
''' + s[end:]
start=s.index('def personal_hint_exclusions(');end=s.index('def difference(',start)
s=s[:start]+r'''def personal_hint_exclusions(statements, placed):
    """Finite warning filter, separate from unchanged exact-copy validation.

    Unknown event statements keep scope without a modality/colon requirement.
    Negated dependencies do not create or clear genuine inherited scope.
    The latest body-supported reference to a private heading controls its
    inclusion; exclusions are local to that heading, not global resets.
    """
    def personal_support(text):
        return bool((PERSONAL_OWNER.search(text) and PERSONAL_ACTIVITY.search(text))
                    or PERSONAL_CONTRIBUTION.search(text))

    def negative_dependency(text):
        # "not only depends" is affirmative; "does not depend" is not.
        text = re.sub(r"\bnot\s+only\b", "only", text, flags=re.IGNORECASE)
        return bool(re.search(r"\b(?:not|never|no\s+longer)\b", text, re.IGNORECASE))

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
            if re.search(r"(?<!\w)" + re.escape(key) + r"(?!\w)", reference):
                # A negated exclusion remains conservative rather than resetting.
                reference = re.sub(r"\bnot\s+(?:excluded|unrelated|outside)\b", "included", reference)
                return not EXCLUSION_CUE.search(reference)
        return False

    result = set()
    protected = False
    scope_references = []
    for sid, (anchor, body) in statements.items():
        personal = personal_support(body)
        dependencies = list(DEPENDENCY_CUE.finditer(body))
        positive_dependency = any(not negative_dependency(m.group()) for m in dependencies)
        only_negative_dependency = bool(dependencies) and not positive_dependency
        hard_procurement = PROCUREMENT_CUE.search(body) or OFFER_DELIVERY_CUE.search(body) or PAYMENT_CUE.search(body) or positive_dependency
        clinical = CLINICAL_CUE.search(body)
        # Coordinating conjunctions delimit clauses even without a comma.
        clauses = [c.strip() for c in re.split(
            r"[;.!?](?:\s+|$)|(?:,\s*)?\b(?:and|but|while|also|then|or)\b\s+",
            body, flags=re.IGNORECASE) if c.strip()]
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
        unknown_event_scope = EVENT_HEADER.search(body) and not personal and not private_heading and not only_negative_dependency
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

'''+s[end:]
new=s.encode();assert new[new.index(b'def difference('):]==old[old.index(b'def difference('):];assert not any(c<32 and c not in (9,10,13) for c in new);compile(s,str(p),'exec');p.write_bytes(new);print('Applied polarity/clause warning repair; strict block unchanged')
