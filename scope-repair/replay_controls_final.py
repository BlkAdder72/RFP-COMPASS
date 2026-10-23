from pathlib import Path
import json,subprocess,sys
R=Path(__file__).resolve().parents[1];D=R/'scope-repair';O=D/'historical-control-replays-final';O.mkdir(exist_ok=False);out=[]
for c in json.loads((R/'final-repair/control-results.json').read_text())['cases']:
 arm=c['arm'];f=R/'final-repair/controls'/c['label'];oldcmd=json.loads((f/arm/'command.json').read_text());args=[]
 for n in oldcmd[5:]:args.append(str(R/n.replace('\\','/').split('Competition 15/',1)[1]))
 cmd=[sys.executable,'-B','-X','utf8',str(R/arm/'tools/validate_packet.py'),*args]
 r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8');p=O/c['label']/arm;p.mkdir(parents=True)
 for n,t in [('command.json',json.dumps(cmd)),('stdout.txt',r.stdout),('stderr.txt',r.stderr),('exit-code.txt',str(r.returncode))]:(p/n).write_text(t,encoding='utf-8')
 # Keep exact historical warning predicate as recorded: compare warning-bearing lines, not counts.
 old=(f/arm/'stdout.txt').read_text(encoding='utf-8');warnings=[l for l in r.stdout.splitlines() if 'REVIEW' in l];oldwarnings=[l for l in old.splitlines() if 'REVIEW' in l]
 out.append({'case':c['label'],'arm':arm,'expected_valid':c['expected_valid'],'exit_code':r.returncode,'same_warning_lines':warnings==oldwarnings,'passed':(r.returncode==0)==c['expected_valid'] and warnings==oldwarnings})
for c in json.loads((R/'final-repair/followup-control-results.json').read_text()):
 arm=c['arm'];label=c['label'];f=R/'final-repair/followup-controls'/label/arm
 oldcmd=json.loads((f/'command.json').read_text());args=[]
 for n in oldcmd[5:]:
  normalized=n.replace('\\','/');args.append(str(R/normalized.split('Competition 15/',1)[1]))
 cmd=[sys.executable,'-B','-X','utf8',str(R/arm/'tools/validate_packet.py'),*args];r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8');p=O/('followup-'+label)/arm;p.mkdir(parents=True)
 for n,t in [('command.json',json.dumps(cmd)),('stdout.txt',r.stdout),('stderr.txt',r.stderr),('exit-code.txt',str(r.returncode))]:(p/n).write_text(t,encoding='utf-8')
 out.append({'case':'followup-'+label,'arm':arm,'expected_valid':c['expected_valid'],'exit_code':r.returncode,'passed':(r.returncode==0)==c['expected_valid']})
(D/'historical-control-replays-final.json').open('x').write(json.dumps(out,indent=2));print(json.dumps([x for x in out if not x['passed']],indent=2))
