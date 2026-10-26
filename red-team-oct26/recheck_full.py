from pathlib import Path
import hashlib,json,re,subprocess,sys
R=Path(__file__).resolve().parents[1];D=Path(__file__).resolve().parent;source=R/'hardening/fixtures/Z-full-length-noisy.md';e=json.loads((R/'final-submission/full-expectations.json').read_text());out={'method':'Read-only replay of existing full-length cards; no new full-length model calls or replacement scores','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'arms':{}}
for arm in ['original','rebuild']:
 base=R/('run-'+arm)/'final-submission-full';parts=sorted(base.glob('part-*/bid-compliance-card.md'),key=lambda p:int(p.parent.name.split('-')[1]));cmd=[sys.executable,'-B','-X','utf8',str(R/arm/'tools/validate_packet.py'),str(source),*[str(p) for p in parts]];r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8');pos={};section=0
 text=(base/'bid-compliance-card.md').read_text(encoding='utf-8')
 for line in text.splitlines():
  if m:=re.match(r'## (\d+)\.',line):section=int(m[1])
  if m:=re.search(r'\[source: source-packet.md:(S\d+);',line):pos.setdefault(m[1],[]).append(section)
 out['arms'][arm]={'command':cmd,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'card_sha256':hashlib.sha256((base/'bid-compliance-card.md').read_bytes()).hexdigest(),'missing_required':{s:[n for n in ns if n not in pos.get(s,[])] for s,ns in e['routing'].items() if not all(n in pos.get(s,[]) for n in ns)},'forbidden_found':{s:[n for n in ns if n in pos.get(s,[])] for s,ns in e['forbidden'].items() if any(n in pos.get(s,[]) for n in ns)},'noise_only12':{s:pos.get(s)==[12] for s in e['noise_only12']}}
(D/'full-recheck.json').open('x',encoding='utf-8').write(json.dumps(out,indent=2));print({a:{k:v for k,v in x.items() if k in ['exit_code','missing_required','noise_only12']} for a,x in out['arms'].items()})
