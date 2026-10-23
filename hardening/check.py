from pathlib import Path
import importlib.util,json,subprocess,sys,hashlib,argparse
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[1];D=R/'hardening'
sys.path.insert(0,str(D));from check_cases import CASES
p=argparse.ArgumentParser();p.add_argument('stage');args=p.parse_args();O=D/args.stage;O.mkdir(exist_ok=False)
spec=importlib.util.spec_from_file_location('v',R/'original/tools/validate_packet.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
records=[]
def run(label,rows,want,arm,section=6):
 box=O/label/arm;box.mkdir(parents=True);source=box/'source-packet.md';card=box/'evaluator-card.md'
 source.write_text('\n'.join(f'S{i:03d} | {a} | {b}' for i,(a,b) in enumerate(rows,1))+'\n',encoding='utf-8')
 lines=[v.TITLE]
 for n,h in enumerate(v.HEADINGS,1):
  lines+=['',h];lines += [f'- “{b}” [source: source-packet.md:S{i:03d}; {a}]' for i,(a,b) in enumerate(rows,1)] if n==12 else ['- not in source']
 card.write_text('\n'.join(lines)+'\n',encoding='utf-8')
 cmd=[sys.executable,'-X','utf8',str(R/arm/'tools/validate_packet.py'),str(source),str(card)]
 r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8');sid=f'S{len(rows):03d}'
 warning=any('REVIEW' in l and f'Section {section}' in l and sid in l for l in r.stdout.splitlines())
 for name,text in [('command.json',json.dumps(cmd)),('stdout.txt',r.stdout),('stderr.txt',r.stderr),('exit-code.txt',str(r.returncode))]:(box/name).write_text(text,encoding='utf-8')
 records.append({'label':label,'arm':arm,'section':section,'sid':sid,'expected_warning':want,'warning':warning,'valid':r.returncode==0,'passed':r.returncode==0 and warning==want,'validator_sha256':hashlib.sha256((R/arm/'tools/validate_packet.py').read_bytes()).hexdigest()})
for label,rows,want in CASES:
 for arm in ('original','rebuild'):run(label,rows,want,arm)
for label,body,section in [('personal-money','My birthday dinner share is $20.',8),('personal-contact','For my retirement lunch, email me at alex@example.net.',10),('real-money','The contract fee is $20.',8),('real-contact','Proposals go to alex@example.net.',10)]:
 for arm in ('original','rebuild'):run(label,[('neutral line1',body)],label.startswith('real'),arm,section)
(O/'results.json').write_text(json.dumps({'cases':records,'count':len(records),'passed':{a:sum(c['passed'] for c in records if c['arm']==a) for a in ('original','rebuild')}},indent=2),encoding='utf-8');print(json.dumps({'count':len(records),'passed':{a:sum(c['passed'] for c in records if c['arm']==a) for a in ('original','rebuild')}}))
