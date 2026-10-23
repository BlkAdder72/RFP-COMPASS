"""Additional adversarial header guards, frozen before their repair."""
from pathlib import Path
import hashlib,importlib.util,json,subprocess,sys
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[1];D=R/'hardening';O=D/sys.argv[1];O.mkdir(exist_ok=False)
spec=importlib.util.spec_from_file_location('v',R/'original/tools/validate_packet.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
cases=[('required-charges','Required charges:','Please bring $20 for lunch.',8,True),('mandatory-meals','Mandatory bidder meals:','Please bring $20 for lunch.',8,True),('uppercase-meal','MANDATORY BIDDER LUNCH','Please bring $20 for lunch.',8,True),('requirements','Bidder requirements:','Our retirement lunch is February 3, 2027, at noon.',6,True),('clinical-header','Patient appointments:','My physical therapy appointment is March 4, 2027, at 9:00 AM.',6,True),('private-reset','Personal calendar:','Please bring $20 for lunch.',8,False)]
records=[]
for label,header,body,section,want in cases:
 for arm in ('original','rebuild'):
  box=O/label/arm;box.mkdir(parents=True);rows=[('RFP p3 line1',header),('RFP p4 line1',body)]
  source=box/'source-packet.md';source.write_text('\n'.join(f'S{i:03d} | {a} | {b}' for i,(a,b) in enumerate(rows,1))+'\n',encoding='utf-8')
  lines=[v.TITLE]
  for n,h in enumerate(v.HEADINGS,1):
   lines+=['',h];lines += [f'- “{b}” [source: source-packet.md:S{i:03d}; {a}]' for i,(a,b) in enumerate(rows,1)] if n==12 else ['- not in source']
  card=box/'evaluator-card.md';card.write_text('\n'.join(lines)+'\n',encoding='utf-8')
  cmd=[sys.executable,'-X','utf8',str(R/arm/'tools/validate_packet.py'),str(source),str(card)];r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8')
  for name,t in [('command.json',json.dumps(cmd)),('stdout.txt',r.stdout),('stderr.txt',r.stderr),('exit-code.txt',str(r.returncode))]:(box/name).write_text(t,encoding='utf-8')
  warning=any('REVIEW' in l and f'Section {section}' in l and 'S002' in l for l in r.stdout.splitlines())
  records.append({'label':label,'arm':arm,'expected':want,'observed':warning,'passed':r.returncode==0 and warning==want,'validator_sha256':hashlib.sha256((R/arm/'tools/validate_packet.py').read_bytes()).hexdigest()})
(O/'results.json').write_text(json.dumps(records,indent=2),encoding='utf-8');print(json.dumps({'passed':{a:sum(c['passed'] for c in records if c['arm']==a) for a in ('original','rebuild')},'cases_per_arm':len(cases)}))
