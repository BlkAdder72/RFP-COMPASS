"""Verify exact-anchor rejection without changing either validator."""
from pathlib import Path
import importlib.util,json,subprocess,sys,hashlib
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[1];D=R/'citation-repair';O=D/'validation-controls';O.mkdir(exist_ok=False)
spec=importlib.util.spec_from_file_location('v',R/'original/tools/validate_packet.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
source=O/'source-packet.md';rows=[('S001','Memo p. 4 §2','The Council requests proposals for audit services.'),('S002','Memo p. 4 §2 item (a)','Applicants must include a peer review report.')]
source.write_text('\n'.join(' | '.join(row) for row in rows)+'\n',encoding='utf-8')
lines=[v.TITLE]
for n,h in enumerate(v.HEADINGS,1):
 lines+=['',h]
 selected=[rows[0]] if n==1 else [rows[1]] if n in (4,5) else []
 lines += [f'- “{b}” [source: source-packet.md:{sid}; {a}]' for sid,a,b in selected] if selected else ['- not in source']
exact='\n'.join(lines)+'\n';anchor=rows[1][1]
cases=[('exact-layout-qualifier',exact,True),('drop-qualifier',exact.replace(anchor,'Memo p. 4 §2'),False),('swap-neighbor-anchor',exact.replace(anchor,rows[0][1]),False),('changed-punctuation',exact.replace(anchor,'Memo p. 4 §2 item a'),False),('changed-unicode',exact.replace(anchor,'Memo p. 4 section 2 item (a)'),False),('changed-case',exact.replace(anchor,anchor.upper()),False),('changed-spacing',exact.replace(anchor,'Memo p.  4 §2 item (a)'),False),('short-quote',exact.replace(rows[1][2],'Applicants must include a report.'),False),('missing-coverage',exact.replace(next(l for l in exact.splitlines() if 'source-packet.md:S001;' in l),'- not in source'),False)]
results=[]
def run(label,arm,src,parts,want):
 box=O/label/arm;box.mkdir(parents=True);cmd=[sys.executable,'-B','-X','utf8',str(R/arm/'tools/validate_packet.py'),str(src),*[str(p) for p in parts]]
 r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8')
 for n,t in [('command.json',json.dumps(cmd,indent=2)),('stdout.txt',r.stdout),('stderr.txt',r.stderr),('exit-code.txt',str(r.returncode))]:(box/n).write_text(t,encoding='utf-8')
 results.append({'label':label,'arm':arm,'expected_valid':want,'exit_code':r.returncode,'passed':(r.returncode==0)==want,'validator_sha256':hashlib.sha256((R/arm/'tools/validate_packet.py').read_bytes()).hexdigest()})
for label,card,want in cases:
 p=O/(label+'.md');p.write_text(card,encoding='utf-8')
 for arm in ('original','rebuild'):run(label,arm,source,[p],want)
for arm in ('original','rebuild'):
 run('preserved-S072-failure',arm,R/'hardening/fixtures/Z-full-length-noisy.md',sorted((R/'run-rebuild/hardening-full').glob('part-*/bid-compliance-card.md')),False)
 run('exact-original-full-control',arm,R/'hardening/fixtures/Z-full-length-noisy.md',sorted((R/'run-original/hardening-full').glob('part-*/bid-compliance-card.md')),True)
report={'cases':results,'count':len(results),'passed':sum(c['passed'] for c in results),'real_model_calls':0,'validator_changed':False}
(D/'validation-results.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in report.items() if k!='cases'}));assert all(c['passed'] for c in results)
