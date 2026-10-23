from pathlib import Path
import json
R=Path.cwd();D=R/'scope-repair';p=R/'rebuild/tools/validate_packet.py';assert p.read_bytes()==(D/'before/rebuild/tools/validate_packet.py').read_bytes(),'Refusing to overwrite another candidate';s=p.read_text(encoding='utf-8')
s=s.replace('OBLIGATION_CUE = re.compile(r"\\b(?:(?:have|has|had|need|needs)\\s+to|(?:is|are|be)\\s+(?:obliged|obligated)\\s+to)\\b", re.IGNORECASE)', '''OBLIGATION_CUE = re.compile(
    r"\\b(?:(?:have|has|had|need|needs)\\s+to|(?:am|is|are|was|were)\\s+to|will\\s+be\\s+expected\\s+to|"
    r"(?:is|are|be)\\s+(?:obliged|obligated)\\s+to|condition\\s+of\\s+(?:entry|participation))\\b", re.IGNORECASE)
# A private first-person duty is not itself a solicitation requirement. Require
# positive personal evidence in that same clause; mixed or unknown duties keep hints.
PRIVATE_SELF_DUTY = re.compile(r"^\\s*I\\s+(?:(?:do|did)\\s+not\\s+)?(?:have|had|need)\\s+to\\b", re.IGNORECASE)''')
s=s.replace('OFFER_DELIVERY_CUE = re.compile(r"\\b(?:deliver|send|lodge|provide|return|present)\\b[^.;!?]*\\boffers?\\b", re.IGNORECASE)', '''OFFER_DELIVERY_CUE = re.compile(
    r"\\b(?:deliver|send|lodge|provide|return|present)\\b[^.;!?]*\\boffers?\\b|"
    r"\\boffers?\\b[^.;!?]*\\b(?:reach|arrive|received|receipt)\\b", re.IGNORECASE)''')
s=s.replace('baptism(?:\\s+ceremony)?|baby\\s+shower|','(?:baptism|christening)(?:\\s+ceremony)?|(?:baby|bridal)\\s+shower|')
start=s.index('        procurement = PROCUREMENT_CUE.search(body)');end=s.index('        only12 =',start)
s=s[:start]+'''        personal = (PERSONAL_OWNER.search(body) and PERSONAL_ACTIVITY.search(body)) or PERSONAL_CONTRIBUTION.search(body)
        hard_procurement = PROCUREMENT_CUE.search(body) or OFFER_DELIVERY_CUE.search(body)
        clinical = CLINICAL_CUE.search(body)
        duty_clauses = [c for c in re.split(r"[;.!?](?:\\s+|$)", body) if OBLIGATION_CUE.search(c)]
        private_duty = bool(duty_clauses) and all(
            PRIVATE_SELF_DUTY.search(c) and PERSONAL_OWNER.search(c) and PERSONAL_ACTIVITY.search(c)
            and len(OBLIGATION_CUE.findall(c)) == 1 and not re.search(r"\b(and|but|while|also)\b", c, re.IGNORECASE)
            for c in duty_clauses)
        procurement = hard_procurement or (bool(duty_clauses) and not private_duty)
        requirement_heading = body.rstrip().endswith(":") or (len(body) <= 120 and body.isupper())
        private_heading = PERSONAL_HEADER.fullmatch(body)
        # Unknown event-list headings preserve context even when their modality
        # is unfamiliar. A private self-duty never creates or clears this scope.
        unknown_event_heading = requirement_heading and EVENT_HEADER.search(body) and not personal and not private_heading
        if ((procurement or clinical) and (EVENT_HEADER.search(body) or requirement_heading)) or unknown_event_heading:
            protected = True
        elif private_heading and not procurement and not clinical:
            protected = False
''' +s[end:]
assert s!=p.read_text(encoding='utf-8');p.write_text(s,encoding='utf-8',newline='\n')
plan=json.loads((D/'submission-plan.json').read_text(encoding='utf-8'));(R/'SUBMISSION_COMMENT.md').write_text('DRAFT — do not post; replace the public URL only after publication is authorized.\n\n'+' '.join(plan['sentences'])+'\n',encoding='utf-8',newline='\n')
print('Warning scope and three-sentence draft repaired; strict validator unchanged.')
