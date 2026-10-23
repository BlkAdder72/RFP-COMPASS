from pathlib import Path
R=Path(__file__).resolve().parents[1]
p=R/'rebuild/tools/validate_packet.py';s=p.read_text(encoding='utf-8')
s=s.replace('birthday|dentist|wedding', 'birthday|dentist|graduation\\s+(celebration|party|ceremony)|wedding')
s=s.replace('''        if body != body.rstrip():
            notes.append(f"{source}: {source_id} ends with spaces; they are ignored when comparing quotations")
        statements[source_id] = (anchor, body.rstrip())''','''        statements[source_id] = (anchor, body)''')
s=s.replace('''                straight += 1''','''                tainted.add(source_id)
                errors.append(f"{output}: {heading}: straight quotation delimiters on {source_id}; curly delimiters required")''')
s=s.replace('''                if visible(quote).rstrip() == visible(expected).rstrip():
                    invisible.add(source_id)
                elif len(quote) < len(expected) and quote in expected:''','''                if len(quote) < len(expected) and quote in expected:''')
# Remove obsolete normalization and tolerant-success diagnostics entirely.
start=s.index('INVISIBLE =');end=s.index('def difference(',start);s=s[:start]+s[end:]
s=s.replace('cited, straight, invisible, placed = set(), 0, set(), {}','cited, placed = set(), {}')
start=s.index('    if straight:\n');end=s.index('    return errors, notes',start);s=s[:start]+s[end:]
p.write_text(s,encoding='utf-8',newline='\n')
p=R/'rebuild/rules.md';s=p.read_text(encoding='utf-8');s=s.replace('8. Before writing', '8. Before writing',1)
s=s.replace('A statement already placed elsewhere still counts.','A statement already placed elsewhere still counts. Build each section by checking all source IDs, not by assigning each ID one primary destination. For response-content lists, carry the enclosing submission context through the list: required reports, information, narratives and statements belong in Section 5 as well as Section 4 when they must be provided with the response. Phrases such as "shall also provide information" create a required response item even when no named form or attachment is mentioned. Never omit an item from Section 5 because its evidence is already in Section 4; do not apply this rule to post-award deliverables or merely suggested material.')
p.write_text(s,encoding='utf-8',newline='\n')
p=R/'rebuild/reference/output-schema.md';s=p.read_text(encoding='utf-8');s=s.replace('Reports the winning contractor produces while performing the contract belong in Section 8, not here.','Required response information and narratives count even without a named document, form or attachment. In a required submittal-content list, "shall also provide information" is a mandatory response-content instruction; preserve its whole statement in this section and Section 4. Carry enclosing response context across list entries. Reports the winning contractor produces while performing the contract belong in Section 8, not here.')
p.write_text(s,encoding='utf-8',newline='\n')
print('Applied strict validation and general required-information routing rule')
