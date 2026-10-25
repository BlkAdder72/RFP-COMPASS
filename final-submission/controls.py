from pathlib import Path
import json,subprocess,sys
R=Path(__file__).resolve().parents[1];D=R/'final-submission';before='--before' in sys.argv;O=D/('before-controls' if before else 'controls');O.mkdir(exist_ok=False)
results=[]
for c in json.loads((D/'control-definitions.json').read_text(encoding='utf-8')):
 f=O/c['name'];f.mkdir();(f/'source-packet.md').write_text(c['source'],encoding='utf-8');(f/'card.md').write_text(c['card'],encoding='utf-8')
 for arm in ['original','rebuild']:
  cmd=[sys.executable,'-B','-X','utf8',str(R/arm/'tools/validate_packet.py'),str(f/'source-packet.md'),str(f/'card.md')];r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8');a=f/arm;a.mkdir()
  for name,t in [('stdout.txt',r.stdout),('stderr.txt',r.stderr),('command.json',json.dumps(cmd)),('exit-code.txt',str(r.returncode))]:(a/name).write_text(t,encoding='utf-8')
  warning=any('REVIEW' in l and 'Section 6' in l and c['sid'] in l for l in r.stdout.splitlines())
  results.append({'case':c['name'],'arm':arm,'expected_valid':c['valid'],'valid':r.returncode==0,'expected_warning':c['warning'],'warning':warning,'passed':(r.returncode==0)==c['valid'] and (c['warning'] is None or warning==c['warning'])})
(D/('before-control-results.json' if before else 'control-results.json')).open('x').write(json.dumps(results,indent=2));print(json.dumps([x for x in results if not x['passed']],indent=2))
