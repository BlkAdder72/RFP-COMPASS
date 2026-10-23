from pathlib import Path
import json,re,subprocess,sys
R=Path(__file__).resolve().parents[1];D=R/'hardening';source=D/'fixtures/Z-full-length-noisy.md'
expected=json.loads((D/'full-length-expectations.json').read_text(encoding='utf-8'));results={}
for arm in ('original','rebuild'):
 base=R/('run-'+arm)/'hardening-full';parts=sorted(base.glob('part-*/bid-compliance-card.md'),key=lambda p:int(p.parent.name.split('-')[1]));card=base/'bid-compliance-card.md'
 if not card.exists():
  results[arm]={'complete':False,'parts_retained':len(parts),'passed':False};continue
 cmd=[sys.executable,'-X','utf8',str(R/arm/'tools/validate_packet.py'),str(source),*[str(p) for p in parts]]
 r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8')
 for name,t in [('validation-command.json',json.dumps(cmd,indent=2)),('validation.txt',r.stdout),('validation-stderr.txt',r.stderr),('validation-exit.txt',str(r.returncode))]:(base/name).write_text(t,encoding='utf-8')
 text=card.read_text(encoding='utf-8');positions={};section=0
 for line in text.splitlines():
  if m:=re.match(r'## (\d+)\.',line):section=int(m[1])
  if m:=re.search(r'\[source: source-packet.md:(S\d+);',line):positions.setdefault(m[1],[]).append(section)
 noise={sid:positions.get(sid)==[12] for sid in expected['noise_only12']}
 routing={sid:all(s in positions.get(sid,[]) for s in sections) for sid,sections in expected['routing'].items()}
 false_hints=[l for l in r.stdout.splitlines() if 'REVIEW' in l and any(sid in l for sid in expected['noise_only12'])]
 budgets=[sum(l.startswith('- “') or l.startswith('- "') for l in p.read_text(encoding='utf-8').splitlines()) for p in parts]
 checks={'exact_shape_quotes_coverage':r.returncode==0,'all_221_ids':len(positions)==221,'noise_only12':all(noise.values()),'genuine_routing':all(routing.values()),'no_personal_review_hints':not false_hints,'max150_bullets_per_reply':all(n<=150 for n in budgets),'complete':not (base/'incomplete.txt').exists()}
 results[arm]={'checks':checks,'passed':all(checks.values()),'noise_only12':noise,'genuine_routing':routing,'personal_review_hints':false_hints,'parts':len(parts),'bullets_per_part':budgets,'cited_distinct_ids':len(positions),'positions':positions}
(D/'full-length-results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps({a:{k:v for k,v in c.items() if k!='positions'} for a,c in results.items()},indent=2))
