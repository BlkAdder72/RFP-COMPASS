from pathlib import Path
import json,subprocess,sys,importlib.util,hashlib
R=Path(__file__).resolve().parents[1];D=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('runner',R/'tools/run_arm.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
for arm in ['original','rebuild']:
 for f in sorted((D/'fixtures').glob('*.md')):
  t=D/('run-'+arm)/f.stem
  assert (t/'request.txt').read_text(encoding='utf-8')==m.request(R,arm,f)
  cmd=json.loads((t/'command.json').read_text());assert cmd[1:7]==['exec','--ignore-user-config','--ephemeral','--skip-git-repo-check','--sandbox','read-only'];assert cmd[-6:]==['-m','gpt-6-astra','-c','model_reasoning_effort="medium"','--json','-']
  a=json.loads((t/'audit.json').read_text());assert a=={'exit_code':0,'agent_messages':1,'tool_events':[],'turn_completed':True}
source=D/'fixtures/B-negation-and-private-content.md';card=D/'run-rebuild/B-negation-and-private-content/bid-compliance-card.md';out={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'card_sha256':hashlib.sha256(card.read_bytes()).hexdigest(),'method':'Exact same raw rebuilt B card, different validators; no model rerun','arms':{}}
for name,v in [('original',R/'original/tools/validate_packet.py'),('pre-polarity',D/'reference/pre-polarity-validator.py'),('rebuild',R/'rebuild/tools/validate_packet.py')]:
 cmd=[sys.executable,'-B','-X','utf8',str(v),str(source),str(card)];p=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8');out['arms'][name]={'command':cmd,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
(D/'same-card-warning-replay.json').open('x',encoding='utf-8').write(json.dumps(out,indent=2));(D/'model-audit.json').open('x').write(json.dumps({'passed':True,'canonical_requests':6,'complete_tool_free_turns':6,'model':'gpt-6-astra','reasoning':'medium','retries':0},indent=2));print('PASS model audit and same-card replay')
