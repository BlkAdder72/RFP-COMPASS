"""Retrospective source-bound review; not a prospectively frozen model test."""
from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parents[1];D=Path(__file__).resolve().parent
source=R/'citation-repair/fixtures/Z-full-length-noisy.md'
expected={'S076':[4,5]}
out={'method':'Retrospective semantic audit of unchanged latest full-length cards. Expectations selected after reading source and results, not a new holdout or part of the old frozen score.','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'required_sections':expected,'rationale':'S076 says the firm shall also provide information on federal/state desk or field reviews. In Section 5 Submittal Content, Format, and Instructions this is required response information, falling under the section-5 provide-with-response trigger as well as section 4.','source_rows':[l for l in source.read_text(encoding='utf-8').splitlines() if l.startswith('S076 | ')],'arms':{}}
for arm in ['original','rebuild']:
 path=R/('run-'+arm)/'citation-repair-v2-full/bid-compliance-card.md';text=path.read_text(encoding='utf-8');section=0;positions={};witness=[]
 for n,line in enumerate(text.splitlines(),1):
  if m:=re.match(r'## (\d+)\.',line):section=int(m[1])
  if m:=re.search(r'source-packet.md:(S\d+);',line):
   sid=m[1]
   if sid in expected:positions.setdefault(sid,[]).append(section);witness.append({'line':n,'section':section,'text':line})
 out['arms'][arm]={'path':str(path.relative_to(R)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'positions':positions,'missing_required':{s:[n for n in ns if n not in positions.get(s,[])] for s,ns in expected.items()},'witness':witness}
(D/'semantic-review.json').open('x',encoding='utf-8').write(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps(out,ensure_ascii=False,indent=2))
