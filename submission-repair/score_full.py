from pathlib import Path
import json,re,subprocess,sys
R=Path(__file__).resolve().parents[1];D=R/'submission-repair';source=R/'hardening/fixtures/Z-full-length-noisy.md'
expected=json.loads((D/'full-expectations.json').read_text(encoding='utf-8'));results={}
final='--final' in sys.argv
arms=[a for a in sys.argv[1:] if a!='--final'] or ['original','rebuild']
for arm in arms:
 base=R/('run-'+arm)/'submission-repair-full';parts=sorted(base.glob('part-*/bid-compliance-card.md'),key=lambda p:int(p.parent.name.split('-')[1]));card=base/'bid-compliance-card.md'
 if not card.exists():
  results[arm]={'complete':False,'parts_retained':len(parts),'passed':False};continue
 cmd=[sys.executable,'-X','utf8',str(R/arm/'tools/validate_packet.py'),str(source),*[str(p) for p in parts]]
 r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8')
 strict=subprocess.run([sys.executable,'-B','-X','utf8',str(R/'rebuild/tools/validate_packet.py'),str(source),*[str(p) for p in parts]],capture_output=True,text=True,encoding='utf-8')
 (base/'common-strict-validation.json').open('x',encoding='utf-8').write(json.dumps({'exit_code':strict.returncode,'stdout':strict.stdout,'stderr':strict.stderr},indent=2))
 prefix='validation-final' if final else 'validation'
 for name,t in [(prefix+'-command.json',json.dumps(cmd,indent=2)),(prefix+'.txt',r.stdout),(prefix+'-stderr.txt',r.stderr),(prefix+'-exit.txt',str(r.returncode))]:(base/name).write_text(t,encoding='utf-8')
 text=card.read_text(encoding='utf-8');positions={};section=0;bad_quotes=[];bad_anchors=[]
 source_rows={l.split(' | ',2)[0]:l.split(' | ',2)[1:] for l in source.read_text(encoding='utf-8').splitlines() if l}
 for line in text.splitlines():
  if m:=re.match(r'## (\d+)\.',line):section=int(m[1])
  if m:=re.search(r'\[source: source-packet.md:(S\d+);',line):positions.setdefault(m[1],[]).append(section)
  if m:=re.match(r'^- [“"](.+)[”"] \[source: source-packet\.md:(S\d+); (.+)\]$',line):
   quote,sid,anchor=m.groups();expected_anchor,expected_quote=source_rows[sid]
   if quote!=expected_quote:bad_quotes.append({'sid':sid,'section':section})
   if anchor!=expected_anchor:bad_anchors.append({'sid':sid,'section':section,'actual':anchor,'expected':expected_anchor})
 forbidden={sid:all(n not in positions.get(sid,[]) for n in ns) for sid,ns in expected['forbidden'].items()}
 noise={sid:positions.get(sid)==[12] for sid in expected['noise_only12']}
 routing={sid:all(s in positions.get(sid,[]) for s in sections) for sid,sections in expected['routing'].items()}
 false_hints=[l for l in r.stdout.splitlines() if 'REVIEW' in l and any(sid in l for sid in expected['noise_only12'])]
 budgets=[sum(l.startswith('- “') or l.startswith('- "') for l in p.read_text(encoding='utf-8').splitlines()) for p in parts]
 checks={'exact_shape_quotes_coverage':strict.returncode==0,'exact_statement_text':not bad_quotes,'exact_anchors':not bad_anchors,'all_221_ids':len(positions)==221,'noise_only12':all(noise.values()),'genuine_routing':all(routing.values()),'forbidden_routing_clear':all(forbidden.values()),'no_personal_review_hints':not false_hints,'max150_bullets_per_reply':all(n<=150 for n in budgets),'complete':not (base/'incomplete.txt').exists()}
 results[arm]={'checks':checks,'passed':all(checks.values()),'quote_mismatches':bad_quotes,'anchor_mismatches':bad_anchors,'noise_only12':noise,'genuine_routing':routing,'personal_review_hints':false_hints,'parts':len(parts),'bullets_per_part':budgets,'cited_distinct_ids':len(positions),'positions':positions,'forbidden_checks':forbidden}
(D/('full-length-results-final.json' if final else 'full-length-results.json' if len(arms)==2 else 'full-length-results-'+arms[0]+'.json')).write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps({a:{k:v for k,v in c.items() if k!='positions'} for a,c in results.items()},indent=2))
