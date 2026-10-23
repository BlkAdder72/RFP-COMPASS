from pathlib import Path
R=Path(__file__).resolve().parents[1]
p=R/'rebuild/rules.md';s=p.read_text(encoding='utf-8');needle='Equal statement text or a shared section number does not make two IDs\' anchors interchangeable.'
assert needle in s;s=s.replace(needle,needle+' A section spanning several pages does not expand the anchor of a statement on one page: never replace a row\'s `p.` citation with an adjacent row\'s `pp.` range, even when they share the same heading or discuss the same event. Before emitting a repeated statement, retrieve its anchor by source ID from the input row, not by section heading or the previous output bullet.')
p.write_text(s,encoding='utf-8',newline='\n')
p=R/'rebuild/examples.md';s=p.read_text(encoding='utf-8');s=s.replace('Two identical statement texts have different anchors.','Four identical statement texts have different anchors.',1);s=s.replace('These example statements are never evidence for a new input.','Single-page and page-range anchors are likewise distinct even under a shared section heading; local paragraph context cannot broaden a statement’s citation. These example statements are never evidence for a new input.',1)
source='S002 | Harbor notice p. 2 §3 bullet | Applicants must include a signed disclosure form.'
s=s.replace(source,source+'\nS003 | Harbor notice p. 4 §6 | Applicants must include a signed disclosure form.\nS004 | Harbor notice pp. 4–5 §6 | Applicants must include a signed disclosure form.',1)
bullet='- “Applicants must include a signed disclosure form.” [source: source-packet.md:S002; Harbor notice p. 2 §3 bullet]'
assert s.count(bullet)==2;s=s.replace(bullet,bullet+'\n- “Applicants must include a signed disclosure form.” [source: source-packet.md:S003; Harbor notice p. 4 §6]\n- “Applicants must include a signed disclosure form.” [source: source-packet.md:S004; Harbor notice pp. 4–5 §6]')
p.write_text(s,encoding='utf-8',newline='\n');print('Applied general page/range citation safeguard and synthetic example')
