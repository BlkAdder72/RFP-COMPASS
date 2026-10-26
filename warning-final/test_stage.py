from pathlib import Path
import json,subprocess,sys,hashlib
R=Path(__file__).resolve().parents[1];D=Path(__file__).resolve().parent;stage=sys.argv[1];number=int(sys.argv[2]);O=D/'stages'/stage;O.mkdir(parents=True,exist_ok=False)
defs=json.loads((D/'control-definitions.json').read_text());result=[]
validators=[('original',R/'original/tools/validate_packet.py'),('before',D/'before/rebuild/tools/validate_packet.py'),('rebuild',R/'rebuild/tools/validate_packet.py')]
for c in defs:
 folder=O/c['name'];folder.mkdir();(folder/'source-packet.md').write_text(c['source'],encoding='utf-8',newline='\n');(folder/'card.md').write_text(c['card'],encoding='utf-8',newline='\n')
 for arm,v in validators:
  cmd=[sys.executable,'-B','-X','utf8',str(v),str(folder/'source-packet.md'),str(folder/'card.md')];p=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8');f=folder/arm;f.mkdir()
  for n,t in [('command.json',json.dumps(cmd)),('stdout.txt',p.stdout),('stderr.txt',p.stderr),('exit-code.txt',str(p.returncode))]:(f/n).open('x',encoding='utf-8',newline='\n').write(t)
  warning=any('REVIEW' in l and 'Section 6' in l and c['sid'] in l for l in p.stdout.splitlines())
  result.append({'case':c['name'],'issue':c['issue'],'arm':arm,'valid':p.returncode==0,'warning':warning,'passed':(p.returncode==0)==c['valid'] and (c['warning'] is None or warning==c['warning'])})
assert (R/'rebuild/tools/validate_packet.py').read_bytes().split(b'def difference',1)[1]==(D/'before/rebuild/tools/validate_packet.py').read_bytes().split(b'def difference',1)[1]
gate={'prior','guard',*[f'F{i}' for i in range(1,number+1)]};failed=[x for x in result if x['arm']=='rebuild' and x['issue'] in gate and not x['passed']]
out={'stage':stage,'validator_sha256':hashlib.sha256((R/'rebuild/tools/validate_packet.py').read_bytes()).hexdigest(),'required_issues':sorted(gate),'passed_required':not failed,'failures_in_required_gate':failed,'all_remaining_failures':[x for x in result if x['arm']=='rebuild' and not x['passed']],'results':result}
(O/'results.json').open('x',encoding='utf-8').write(json.dumps(out,indent=2));(O/'validator.py').write_bytes((R/'rebuild/tools/validate_packet.py').read_bytes());print(json.dumps({k:v for k,v in out.items() if k!='results'},indent=2));raise SystemExit(bool(failed))
