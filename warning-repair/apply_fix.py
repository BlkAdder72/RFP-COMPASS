from pathlib import Path
R=Path.cwd();p=R/'rebuild/tools/validate_packet.py';s=p.read_text(encoding='utf-8')
s=s.replace('PERSONAL_OWNER = re.compile(','''# Obligation phrases protect warning context even without a procurement noun.
# Delivery of offers is a response cue; "offer" alone is too broad.
OBLIGATION_CUE = re.compile(r"\\b(?:(?:have|has|had|need|needs)\\s+to|(?:is|are|be)\\s+(?:obliged|obligated)\\s+to)\\b", re.IGNORECASE)
OFFER_DELIVERY_CUE = re.compile(r"\\b(?:deliver|send|lodge|provide|return|present)\\b[^.;!?]*\\boffers?\\b", re.IGNORECASE)
PERSONAL_OWNER = re.compile(''')
s=s.replace('r"\\b(potluck|birthday|dentist|graduation', 'r"\\b(potluck|birthday|dentist|baptism(?:\\s+ceremony)?|baby\\s+shower|graduation')
s=s.replace('procurement = PROCUREMENT_CUE.search(body)','procurement = PROCUREMENT_CUE.search(body) or OBLIGATION_CUE.search(body) or OFFER_DELIVERY_CUE.search(body)')
assert s!=p.read_text(encoding='utf-8');p.write_text(s,encoding='utf-8',newline='\n')
print('Warning filter updated; structural checks unchanged.')
