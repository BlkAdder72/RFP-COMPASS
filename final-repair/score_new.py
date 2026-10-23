from pathlib import Path
import hashlib,json,re,subprocess,sys
R=Path(__file__).resolve().parents[1];D=Path(__file__).resolve().parent;expected=json.loads((D/'expectations.json').read_text());results={}
for arm in ['original','rebuild']:
 results[arm]={}
 for name,exp in expected.items():
  source=D/'fixtures'/(name+'.md');assert hashlib.sha256(source.read_bytes()).hexdigest()==exp['source_sha256'];rows={s:(a,b) for s,a,b in (l.split(' | ',2) for l in source.read_text(encoding='utf-8').splitlines())}
  trial=R/('run-'+arm)/'final-repair-new'/name;card=trial/'bid-compliance-card.md';text=card.read_text(encoding='utf-8');section=0;p={};bad=[]
  for line in text.splitlines():
   if m:=re.match(r'## (\d+)\.',line):section=int(m[1])
   if m:=re.match(r'^- [“"](.+)[”"] \[source: source-packet.md:(S\d+); (.+)\]$',line):
    body,sid,a=m.groups();p.setdefault(sid,[]).append(section)
    if rows.get(sid)!=(a,body):bad.append({'sid':sid,'section':section})
  cmd=[sys.executable,'-B','-X','utf8',str(R/arm/'tools/validate_packet.py'),str(source),str(card)];r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8')
  for n,t in [('validation-command.json',json.dumps(cmd)),('validation-stdout.txt',r.stdout),('validation-stderr.txt',r.stderr),('validation-exit.txt',str(r.returncode))]:(trial/n).open('x',encoding='utf-8').write(t)
  checks={'strict_copy':not bad,'mechanical_validation':r.returncode==0,**{s+'_required':all(k in p.get(s,[]) for k in ns) for s,ns in exp['required'].items()},**{s+'_exclusive':p.get(s)==ns for s,ns in exp['exclusive'].items()}}
  if name=='W-personal-graduation':checks['no_false_date_warning']=not any('REVIEW' in l and 'Section 6' in l for l in r.stdout.splitlines())
  results[arm][name]={'checks':checks,'passed':all(checks.values()),'positions':p,'copy_mismatches':bad}
(D/'new-results.json').open('x',encoding='utf-8').write(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
