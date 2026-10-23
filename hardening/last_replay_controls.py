"""Re-execute all 51 prior controls without changing their source/card evidence."""
from pathlib import Path
import json,subprocess,sys
R=Path(__file__).resolve().parents[1];D=R/'hardening';O=D/'final-prior-controls-v2';O.mkdir(exist_ok=False)
cases=json.loads((R/'revision/default-tests-v2-results.json').read_text(encoding='utf-8'))['cases'];out=[]
for c in cases:
 box=O/c['label']/c['arm'];box.mkdir(parents=True)
 cmd=[sys.executable,'-X','utf8',str(R/c['arm']/'tools/validate_packet.py'),str(R/c['source']),str(R/c['card'])]
 r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8')
 for name,t in [('command.json',json.dumps(cmd)),('stdout.txt',r.stdout),('stderr.txt',r.stderr),('exit-code.txt',str(r.returncode))]:(box/name).write_text(t,encoding='utf-8')
 warning=any('REVIEW' in l and f"Section {c['section']}" in l and c['sid'] in l for l in r.stdout.splitlines())
 # Declared behavior change: explicit personal meal contributions now clear their money hint.
 expected=False if c['label'] in ('generic-lunch-money','changed-quote') and c['arm']=='rebuild' else c['expect_warning']
 out.append({'label':c['label'],'arm':c['arm'],'old_expectation':c['expect_warning'],'new_expectation':expected,'observed':warning,'passed':warning==expected and (r.returncode==0)==c['expect_valid']})
(D/'final-prior-controls-v2.json').write_text(json.dumps({'count':len(out),'passed':sum(c['passed'] for c in out),'declared_change':'Please bring $30 for lunch: personal contribution only12; requirements and scope veto remain. Old expected warning preserved in revision/default-cases.json.','cases':out},indent=2),encoding='utf-8')
print(json.dumps({'count':len(out),'passed':sum(c['passed'] for c in out),'failures':[c for c in out if not c['passed']]}))
