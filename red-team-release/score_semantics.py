from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parents[1];D=Path(__file__).resolve().parent;plan=json.loads((D/'full-semantic-review-plan.json').read_text());source=R/'hardening/fixtures/Z-full-length-noisy.md';assert hashlib.sha256(source.read_bytes()).hexdigest()==plan['source_sha256'];rows={l.split(' | ',2)[0]:l for l in source.read_text(encoding='utf-8').splitlines()}
out={'method':plan['method'],'source_sha256':plan['source_sha256'],'matrix':plan,'arms':{}}
for arm in ['original','rebuild']:
 path=R/('run-'+arm)/'final-repair-v2-full/bid-compliance-card.md';text=path.read_text(encoding='utf-8');p={};lines={};section=0
 for n,line in enumerate(text.splitlines(),1):
  if m:=re.match(r'## (\d+)\.',line):section=int(m[1])
  if m:=re.search(r'source-packet.md:(S\d+);',line):p.setdefault(m[1],[]).append(section);lines.setdefault(m[1],[]).append({'line':n,'section':section})
 missing={s:[n for n in ns if n not in p.get(s,[])] for s,ns in plan['required'].items()};extra={s:[n for n in ns if n in p.get(s,[])] for s,ns in plan['forbidden'].items()}
 out['arms'][arm]={'path':str(path.relative_to(R)).replace('\\','/'),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'positions':{s:p.get(s,[]) for s in plan['required']},'missing_required':{s:ns for s,ns in missing.items() if ns},'forbidden_present':{s:ns for s,ns in extra.items() if ns},'witnesses':{s:{'source':rows[s],'card_lines':lines.get(s,[])} for s in plan['required']}}
out['new_regressions']={s:[n for n in ns if n in out['arms']['rebuild']['missing_required'].get(s,[])] for s,ns in plan['required'].items() if any(n not in out['arms']['original']['missing_required'].get(s,[]) and n in out['arms']['rebuild']['missing_required'].get(s,[]) for n in ns)}
(D/'full-semantic-results.json').open('x',encoding='utf-8').write(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps({a:{k:v for k,v in d.items() if k in ['missing_required','forbidden_present']} for a,d in out['arms'].items()},indent=2));print('Regressions:',out['new_regressions'])
