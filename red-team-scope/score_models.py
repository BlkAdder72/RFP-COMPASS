from pathlib import Path
import hashlib,json,re,subprocess,sys
R=Path(__file__).resolve().parents[1];D=Path(__file__).resolve().parent;expected=json.loads((D/'expectations.json').read_text());out={}
for arm in ['original','rebuild']:
 out[arm]={};base=D/('run-'+arm);env=json.loads((base/'environment.json').read_text());assert env['model']=='gpt-6-astra' and env['reasoning_effort']=='medium';assert env['fixture_order']==[n+'.md' for n in expected]
 for n,h in env['knowledge_sha256'].items():assert hashlib.sha256((R/arm/n).read_bytes()).hexdigest()==h
 for name,exp in expected.items():
  source=D/'fixtures'/(name+'.md');assert hashlib.sha256(source.read_bytes()).hexdigest()==exp['source_sha256'];rows={s:(a,b) for s,a,b in (l.split(' | ',2) for l in source.read_text(encoding='utf-8').splitlines())}
  trial=base/name;text=(trial/'bid-compliance-card.md').read_text(encoding='utf-8');p={};bad=[];section=0
  for line in text.splitlines():
   if m:=re.match(r'## (\d+)\.',line):section=int(m[1])
   if m:=re.match(r'^- [“"](.+)[”"] \[source: source-packet.md:(S\d+); (.+)\]$',line):
    body,sid,anchor=m.groups();p.setdefault(sid,[]).append(section)
    if rows.get(sid)!=(anchor,body):bad.append({'sid':sid,'section':section,'actual_anchor':anchor,'expected':rows.get(sid),'actual_body':body})
  validations={}
  for label,validator in [('native',arm),('common-strict','rebuild')]:
   cmd=[sys.executable,'-B','-X','utf8',str(R/validator/'tools/validate_packet.py'),str(source),str(trial/'bid-compliance-card.md')];r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8');validations[label]={'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'command':cmd}
  (trial/'validation-results.json').open('x',encoding='utf-8').write(json.dumps(validations,indent=2))
  events=[json.loads(l) for l in (trial/'events.jsonl').read_text(encoding='utf-8').splitlines()];msgs=[e['item']['text'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message'];assert msgs==[text] and events[-1]['type']=='turn.completed';assert all(e.get('item',{}).get('type') in [None,'agent_message','reasoning'] for e in events)
  request=(trial/'request.txt').read_text(encoding='utf-8')
  for n in env['knowledge_sha256']:assert '<file name="'+n+'">\n'+(R/arm/n).read_text(encoding='utf-8')+'\n</file>' in request
  assert '<attachment name="source-packet.md">\n'+source.read_text(encoding='utf-8')+'\n</attachment>' in request
  checks={**{s+'_required':all(n in p.get(s,[]) for n in ns) for s,ns in exp['required'].items()},**{s+'_forbidden_clear':all(n not in p.get(s,[]) for n in ns) for s,ns in exp['forbidden'].items()},**{s+'_exclusive':p.get(s)==ns for s,ns in exp['exclusive'].items()}}
  personal_hints=[l for l in validations['native']['stdout'].splitlines() if 'REVIEW' in l and any(s in l for s in exp['exclusive'])]
  out[arm][name]={'strict_fidelity_pass':not bad and validations['common-strict']['exit_code']==0,'mismatches':bad,'semantic_checks':checks,'semantic_pass':all(checks.values()),'positions':p,'personal_review_hints':personal_hints,'no_personal_false_hints':not personal_hints,'native_exit':validations['native']['exit_code'],'passed_all_checks':not bad and validations['common-strict']['exit_code']==0 and all(checks.values()) and not personal_hints}
(D/'model-results.json').open('x',encoding='utf-8').write(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps({a:{n:{k:x[k] for k in ['strict_fidelity_pass','semantic_pass','no_personal_false_hints','passed_all_checks','mismatches']} for n,x in d.items()} for a,d in out.items()},ensure_ascii=False,indent=2))
