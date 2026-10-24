from pathlib import Path
import json,subprocess,sys
R=Path(__file__).resolve().parents[1];D=Path(__file__).resolve().parent;O=D/'controls';O.mkdir(exist_ok=False);out=[]
for c in json.loads((D/'control-definitions.json').read_text(encoding='utf-8')):
 f=O/c['name'];f.mkdir();(f/'source-packet.md').write_text(c['source'],encoding='utf-8',newline='\n');(f/'card.md').write_text(c['card'],encoding='utf-8',newline='\n')
 for arm,validator in [('original',R/'original/tools/validate_packet.py'),('pre-scope',D/'reference/pre-scope-validator.py'),('rebuild',R/'rebuild/tools/validate_packet.py')]:
  cmd=[sys.executable,'-B','-X','utf8',str(validator),str(f/'source-packet.md'),str(f/'card.md')];r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8');p=f/arm;p.mkdir()
  for n,t in [('command.json',json.dumps(cmd)),('stdout.txt',r.stdout),('stderr.txt',r.stderr),('exit-code.txt',str(r.returncode))]:(p/n).open('x',encoding='utf-8').write(t)
  warning=any('REVIEW' in l and 'Section 6' in l and c['sid'] in l for l in r.stdout.splitlines())
  out.append({'case':c['name'],'arm':arm,'expected_valid':c['valid'],'exit_code':r.returncode,'expected_warning':c['warning'],'observed_warning':warning,'passed':(r.returncode==0)==c['valid'] and (c['warning'] is None or warning==c['warning'])})
(D/'control-results.json').open('x').write(json.dumps(out,indent=2));print(json.dumps([x for x in out if x['arm']=='rebuild' and not x['passed']],indent=2))
