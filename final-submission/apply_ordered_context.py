from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'final-submission'
p=R/'rebuild/rules.md';old=(D/'before/rebuild/rules.md').read_text(encoding='utf-8');assert p.read_text(encoding='utf-8')==old
needle='   - A private-looking heading describes';assert needle in old
ordered='''   - Establish relevance in source order before applying topical triggers. Keep an internal decision for each statement: AI-addressed evidence, unrelated private evidence, or solicitation evidence, with the source text that supports the decision. A private block covers its genuinely personal records, not every later line. Conversely, a later procurement requirement does not retroactively make earlier personal records procurement evidence unless it explicitly incorporates them.
   - In an explicitly private block, a negative dependency or optional private attendance is not affirmative evidence connecting an activity to the solicitation. Merely mentioning participation, entry, attendance or a date does not resume procurement routing. Keep those personal statements and their personal dates only in Section 12 unless independent affirmative source evidence actually links them to a solicitation requirement. Read contractions and negation for meaning; do not treat denial of an attendance condition as establishment of that condition. An optional meeting in genuine procurement context still follows ordinary routing with its optional wording preserved.
'''
new=old.replace(needle,ordered+needle,1)
needle='   - Before routing an ID, internally form its complete exact bullet from its packet row.';assert needle in new
new=new.replace(needle,'''   - Separate placement planning from literal emission. Plan placements by source ID only; do not regenerate citation strings while reasoning about sections, events or document page spans. Before routing an ID, internally form its complete exact bullet from its packet row.''',1)
needle='    - the complete citation suffix, character for character against that same ID\'s original packet row, including all anchor qualifiers; check every repeated occurrence and every continuation, not only the page or section number;';assert needle in new
new=new.replace(needle,needle+'''
    - immediately before each emitted occurrence, retrieve that ID's original text and anchor fields and compare the actual output suffix to that literal row again; checking one occurrence does not certify another occurrence in a later section or continuation. Document geography and a nearby page range cannot replace the literal row value;''',1)
needle='    - that every statement was tested against every trigger;';assert needle in new
new=new.replace(needle,needle+'''
    - both directions of the relevance boundary: every operationally placed personal record has an affirmative source link to the solicitation, not merely a negated/optional relation or a later unrelated duty; every Section-12-only record lacks a genuine source-stated procurement duty that was hidden by a private heading;''',1)
p.write_text(new,encoding='utf-8',newline='\n')
p=R/'rebuild/reference/output-schema.md';old=(D/'before/rebuild/reference/output-schema.md').read_text(encoding='utf-8');assert p.read_text(encoding='utf-8')==old
needle='**Context boundaries:**';assert needle in old
ordered='''**Relevance before triggers:** Work in source order and distinguish AI-addressed evidence, private evidence and solicitation evidence before testing dates or other topics. Inside an explicitly private block, a negated participation/attendance dependency or optional private activity does not establish a link to the solicitation; general words such as participation, attendance and entry are not by themselves affirmative procurement evidence. Those personal statements and dates remain only in Section 12 unless an independent affirmative source statement actually incorporates them into a solicitation requirement. A later genuine requirement cannot retroactively contaminate earlier private records without an explicit source link. A genuinely optional procurement meeting still routes normally with its optional wording preserved. Recheck both kinds of mistake: private dates leaked operationally, and genuine duties quarantined only because a private heading appeared earlier.

'''
new=old.replace(needle,ordered+needle,1)
needle='- The COMPLETE anchor is opaque data copied from that same ID\'s packet line,';assert needle in new
new=new.replace(needle,'- Plan section placements by ID, then retrieve that ID’s literal row fields anew for each emitted occurrence. Never reconstruct a citation from the topic, another output occurrence or a section-wide page span. The COMPLETE anchor is opaque data copied from that same ID\'s packet line,',1)
p.write_text(new,encoding='utf-8',newline='\n')
print('Applied ordered, two-direction relevance classification to two knowledge files; validator unchanged')
