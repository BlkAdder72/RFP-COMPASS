from pathlib import Path
import json,subprocess,sys,hashlib
R=Path(__file__).resolve().parents[1];D=Path(__file__).resolve().parent;O=D/'prior-controls';O.mkdir(exist_ok=False)
definitions=R/'polarity-repair/control-definitions-release.json';out=[]
for c in json.loads(definitions.read_text(encoding='utf-8')):
 p=O/c['name'];p.mkdir();s=p/'source-packet.md';t=p/'card.md';s.write_text(c['source'],encoding='utf-8',newline='\n');t.write_text(c['card'],encoding='utf-8',newline='\n')
 cmd=[sys.executable,'-B','-X','utf8',str(R/'rebuild/tools/validate_packet.py'),str(s),str(t)];r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8')
 warning=any('REVIEW' in l and 'Section 6' in l and c['sid'] in l for l in r.stdout.splitlines())
 x={'case':c['name'],'command':cmd,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'expected_valid':c['valid'],'expected_warning':c['warning'],'observed_warning':warning,'passed':(r.returncode==0)==c['valid'] and (c['warning'] is None or warning==c['warning'])};(p/'result.json').open('x',encoding='utf-8').write(json.dumps(x,indent=2));out.append(x)
(D/'prior-control-replay.json').open('x',encoding='utf-8').write(json.dumps({'definitions_sha256':hashlib.sha256(definitions.read_bytes()).hexdigest(),'passed':all(x['passed'] for x in out),'total':len(out),'results':out},indent=2));print(len(out),sum(x['passed'] for x in out))
