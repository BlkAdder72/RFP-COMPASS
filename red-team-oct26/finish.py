from pathlib import Path
import json,hashlib,subprocess,importlib.util,sys
R=Path(__file__).resolve().parents[1];D=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
spec=importlib.util.spec_from_file_location('runner',R/'tools/run_arm.py');runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)
for arm in ['original','rebuild']:
 for f in sorted((D/'fixtures').glob('*.md')):
  t=D/('run-'+arm)/f.stem
  assert (t/'request.txt').read_text(encoding='utf-8')==runner.request(R,arm,f)
  cmd=read(t/'command.json');assert cmd[1:7]==['exec','--ignore-user-config','--ephemeral','--skip-git-repo-check','--sandbox','read-only']
  assert cmd[-6:]==['-m','gpt-6-astra','-c','model_reasoning_effort="medium"','--json','-']
  assert read(t/'audit.json')=={'exit_code':0,'agent_messages':1,'tool_events':[],'turn_completed':True}
controls=read(D/'control-results.json');summary={a:sum(c['passed'] for c in controls if c['arm']==a) for a in ['original','pre-repair','rebuild']}
prior={c['case']:c for c in controls if c['arm']=='pre-repair'}
comparison={k:0 for k in ['improved','tied','regressed']}
for c in controls:
 if c['arm']=='rebuild':comparison['tied' if c['passed']==prior[c['case']]['passed'] else 'improved' if c['passed'] else 'regressed']+=1
source=D/'fixtures/B-personal-boundaries.md';card=D/'run-rebuild/B-personal-boundaries/bid-compliance-card.md';replay={}
for name,v in [('original',R/'original/tools/validate_packet.py'),('pre-repair',D/'reference/pre-repair-validator.py'),('rebuild',R/'rebuild/tools/validate_packet.py')]:
 cmd=[sys.executable,'-B','-X','utf8',str(v),str(source),str(card)];p=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8');replay[name]={'command':cmd,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
(D/'same-card-warning-replay.json').open('x',encoding='utf-8').write(json.dumps({'source_sha256':sha(source),'card_sha256':sha(card),'arms':replay},indent=2))
freeze='b0553c95';baseline='ac42a324'
for n in ['PROTOCOL.md','control-definitions.json','expectations.json',*[str(p.relative_to(D)).replace('\\','/') for p in (D/'fixtures').glob('*.md')]]:assert subprocess.check_output(['git','show',freeze+':red-team-oct26/'+n],cwd=R)==(D/n).read_bytes()
assert subprocess.run(['git','merge-base','--is-ancestor',freeze,baseline],cwd=R).returncode==0
assert subprocess.check_output(['git','ls-tree','-r','--name-only',baseline,'red-team-oct26/run-rebuild'],cwd=R)==b''
transport=[{'path':str(p.relative_to(R)).replace('\\','/'),'lines':[l for l in p.read_text(encoding='utf-8').splitlines() if 'retrying sampling request' in l]} for a in ['original','rebuild'] for p in (D/('run-'+a)).glob('*/stderr.txt') if 'retrying sampling request' in p.read_text(encoding='utf-8')]
m=read(D/'model-results.json');out={'controls_passed_of_18':summary,'controls_vs_pre_repair':comparison,'new_model_combined_pass_of_3':{a:sum(x['passed_all_checks'] for x in m[a].values()) for a in m},'model_failed_checks':{a:{n:[k for k,v in x['semantic_checks'].items() if not v] for n,x in cases.items()} for a,cases in m.items()},'model_audit':{'canonical_requests':6,'complete_tool_free_turns':6,'agent_initiated_retries':0,'automatic_client_transport_retries':transport,'freeze_commit':freeze,'original_baseline_commit':baseline},'unpublished':True}
(D/'SUMMARY.json').open('x',encoding='utf-8').write(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
