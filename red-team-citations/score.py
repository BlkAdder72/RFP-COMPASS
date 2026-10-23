from pathlib import Path
import hashlib,json,re,subprocess,sys
R=Path(__file__).resolve().parents[1];D=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,t):p.open('x',encoding='utf-8',newline='\n').write(t)
source=D/'fixtures/U-unseen-citations.md';exp=json.loads((D/'expectations.json').read_text(encoding='utf-8'));assert sha(source)==exp['source_sha256']
rows={s:(a,b) for s,a,b in (l.split(' | ',2) for l in source.read_text(encoding='utf-8').splitlines())};results={}
for arm in ['original','rebuild']:
 base=D/('run-'+arm);trial=base/'U-unseen-citations';text=(trial/'bid-compliance-card.md').read_text(encoding='utf-8');positions={};bad=[];section=0
 for line in text.splitlines():
  if m:=re.match(r'## (\d+)\.',line):section=int(m[1])
  if m:=re.match(r'^- [“"](.+)[”"] \[source: source-packet.md:(S\d+); (.+)\]$',line):
   body,sid,anchor=m.groups();positions.setdefault(sid,[]).append(section)
   if rows.get(sid)!=(anchor,body):bad.append({'sid':sid,'section':section,'actual_anchor':anchor,'actual_body':body})
 cmd=[sys.executable,'-B','-X','utf8',str(R/arm/'tools/validate_packet.py'),str(source),str(trial/'bid-compliance-card.md')];run=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8')
 new(trial/'validation-stdout.txt',run.stdout);new(trial/'validation-stderr.txt',run.stderr);new(trial/'validation-command.json',json.dumps(cmd));new(trial/'validation-exit.txt',str(run.returncode))
 audit=json.loads((trial/'audit.json').read_text());assert audit['exit_code']==0 and audit['agent_messages']==1 and not audit['tool_events'] and audit['turn_completed']
 env=json.loads((base/'environment.json').read_text());assert all(sha(R/arm/n)==h for n,h in env['knowledge_sha256'].items())
 routing={s:all(n in positions.get(s,[]) for n in sections) for s,sections in exp['routing'].items()};exclusive={s:positions.get(s)==sections for s,sections in exp['exclusive'].items()}
 results[arm]={'exact_anchors_and_statements':not bad,'mismatches':bad,'positions':positions,'required_routing':routing,'exclusive_routing':exclusive,'mechanical_validator_pass':run.returncode==0,'passed_all_frozen_checks':not bad and all(routing.values()) and all(exclusive.values()) and run.returncode==0}
new(D/'model-results.json',json.dumps(results,ensure_ascii=False,indent=2));print(json.dumps(results,ensure_ascii=False,indent=2))
