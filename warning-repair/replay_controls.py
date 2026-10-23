from pathlib import Path
import json,subprocess,sys
R=Path(__file__).resolve().parents[1];D=R/'warning-repair';O=D/'historical-control-replays';O.mkdir(exist_ok=False);out=[]
for c in json.loads((R/'final-repair/control-results.json').read_text())['cases']:
 arm=c['arm'];f=R/'final-repair/controls'/c['label'];cmd=[sys.executable,'-B','-X','utf8',str(R/arm/'tools/validate_packet.py'),str(f/'source-packet.md'),str(f/'card.md')]
 r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8');p=O/c['label']/arm;p.mkdir(parents=True)
 for n,t in [('command.json',json.dumps(cmd)),('stdout.txt',r.stdout),('stderr.txt',r.stderr),('exit-code.txt',str(r.returncode))]:(p/n).write_text(t,encoding='utf-8')
 # Keep exact historical warning predicate as recorded: compare warning-bearing lines, not counts.
 old=(f/arm/'stdout.txt').read_text(encoding='utf-8');warnings=[l for l in r.stdout.splitlines() if 'REVIEW' in l];oldwarnings=[l for l in old.splitlines() if 'REVIEW' in l]
 out.append({'case':c['label'],'arm':arm,'expected_valid':c['expected_valid'],'exit_code':r.returncode,'same_warning_lines':warnings==oldwarnings,'passed':(r.returncode==0)==c['expected_valid'] and warnings==oldwarnings})
(D/'historical-control-replays.json').open('x').write(json.dumps(out,indent=2));print(json.dumps([x for x in out if not x['passed']],indent=2))
