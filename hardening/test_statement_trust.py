from pathlib import Path
import hashlib,json,subprocess,sys
R=Path(__file__).resolve().parents[1];D=R/'hardening';O=D/'statement-trust';O.mkdir(exist_ok=False)
text=(R/'run-original/Q8-validator/contained.md').read_text(encoding='utf-8');line=next(l for l in text.splitlines() if 'source-packet.md:S004;' in l)
deadline=next(l for l in text.splitlines() if 'source-packet.md:S002;' in l)
cases=[('normal',text,False,True),('unrelated-quote',text.replace('November 20','November 21'),False,False),('unrelated-anchor',text.replace(deadline,deadline.replace('RFP-15 p. 2','RFP-15 wrong')),False,False),('personal-anchor',text.replace(line,line.replace('line 1','line 99')),True,False),('personal-quote',text.replace(line,line.replace('December 11','December 12')),True,False),('duplicate-personal',text.replace(line,line+'\n'+line),True,False),('malformed-personal',text.replace(line,line[:-1]),True,False),('missing-heading',text.replace('## 3. Eligibility and qualifications stated',''),False,False)]
records=[]
for label,card,warn,valid in cases:
 box=O/label;box.mkdir();p=box/'card.md';p.write_text(card,encoding='utf-8')
 for arm in ('original','rebuild'):
  dest=box/arm;dest.mkdir();cmd=[sys.executable,'-X','utf8',str(R/arm/'tools/validate_packet.py'),str(R/'fixtures/A-stapled-thread.md'),str(p)]
  r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8');observed=any('REVIEW' in l and 'Section 6' in l and 'S004' in l for l in r.stdout.splitlines())
  for n,t in [('command.json',json.dumps(cmd)),('stdout.txt',r.stdout),('stderr.txt',r.stderr),('exit-code.txt',str(r.returncode))]:(dest/n).write_text(t,encoding='utf-8')
  records.append({'label':label,'arm':arm,'expected_warning':warn,'observed_warning':observed,'expected_valid':valid,'exit_code':r.returncode,'passed':observed==warn and (r.returncode==0)==valid,'validator_sha256':hashlib.sha256((R/arm/'tools/validate_packet.py').read_bytes()).hexdigest()})
(O/'results.json').write_text(json.dumps(records,indent=2),encoding='utf-8');print(json.dumps({'passed':{a:sum(c['passed'] for c in records if c['arm']==a) for a in ('original','rebuild')},'cases_per_arm':len(cases)}))
