"""Read-only current-repair evidence audit; never regenerates runs or scores."""
from pathlib import Path
import hashlib,importlib.util,json,re,subprocess,sys
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[1];D=R/'final-repair'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((D/'preservation.json').read_text(encoding='utf-8'))
extra=json.loads((D/'additional-mutable-paths.json').read_text())['paths']
for n,h in m['files'].items():assert sha(D/'history'/n if n in m['mutable_paths']+extra else R/n)==h,'Prior evidence changed: '+n
for n,h in json.loads((D/'attempt-1/manifest.json').read_text()).items():assert sha(R/n)==h,'Failed first-attempt evidence changed: '+n
assert (R/'questions.md').read_bytes()==subprocess.check_output(['git','show','bfdd812:questions.md'],cwd=R)
assert sha(R/'original/tools/validate_packet.py')==m['files']['original/tools/validate_packet.py']
assert sha(R/'rebuild/tools/validate_packet.py')!=m['files']['rebuild/tools/validate_packet.py']
spec=importlib.util.spec_from_file_location('runner',R/'tools/run_arm.py');core=importlib.util.module_from_spec(spec);spec.loader.exec_module(core)
turns=0
def audit(part,prompt):
 global turns
 assert (part/'request.txt').read_text(encoding='utf-8')==prompt
 events=[json.loads(l) for l in (part/'events.jsonl').read_text(encoding='utf-8').splitlines()]
 assert all(e.get('item',{}).get('type') in (None,'agent_message','reasoning') for e in events)
 msgs=[e['item']['text'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message']
 assert len(msgs)==1 and msgs[0]==(part/'bid-compliance-card.md').read_text(encoding='utf-8')
 assert events[-1]['type']=='turn.completed' and (part/'exit-code.txt').read_text()=='0'
 cmd=json.loads((part/'command.json').read_text());assert cmd[cmd.index('-m')+1]=='gpt-6-astra' and cmd[cmd.index('-c')+1]=='model_reasoning_effort="medium"'
 turns+=1
 return events
for prefix,knowledge in [('final-repair',D/'attempt-1-knowledge'),('final-repair-v2',R)]:
 for arm in ['original','rebuild']:
  for kind,folder in [('core',R/'fixtures'),('new',D/'fixtures'),('full',R/'hardening/fixtures')]:
   base=R/('run-'+arm)/(prefix+'-'+kind);env=json.loads((base/'environment.json').read_text());assert env['model']=='gpt-6-astra' and env['reasoning_effort']=='medium'
   for name,h in env['knowledge_sha256'].items():assert sha(knowledge/arm/name)==h
   if kind!='full':
    fixtures=sorted(folder.glob('*.md'));assert env['fixture_order']==[p.name for p in fixtures]
    for fixture in fixtures:audit(base/fixture.stem,core.request(knowledge,arm,fixture))
   else:
    source=folder/'Z-full-length-noisy.md';assert sha(source)==env['fixture_sha256']==json.loads((D/'full-expectations.json').read_text())['packet_sha256']
    parts=sorted(base.glob('part-*'),key=lambda p:int(p.name.split('-')[1]));session=None
    for i,part in enumerate(parts):
     events=audit(part,core.request(knowledge,arm,source) if i==0 else 'continue');threads=[e['thread_id'] for e in events if e.get('type')=='thread.started']
     if i==0:assert len(threads)==1;session=threads[0]
     assert all(t==session for t in threads)
     if i:assert session in json.loads((part/'command.json').read_text())
    assert (base/'bid-compliance-card.md').read_text(encoding='utf-8')=='\n'.join((p/'bid-compliance-card.md').read_text(encoding='utf-8') for p in parts)
controls=json.loads((D/'control-results.json').read_text());assert not controls['rebuild_failures']
provenance=json.loads((D/'control-provenance.json').read_text())
assert sha(R/'rebuild/tools/validate_packet.py')==provenance['validator_sha256']
assert sha(D/'control-results.json')==provenance['result_file_sha256']
assert all(c['exit_code']==0 for c in json.loads((D/'identical-strict-fidelity.json').read_text()))
assert all(c['exit_code']==0 for c in json.loads((D/'identical-strict-fidelity-v2.json').read_text()))
assert all(c['passed'] for c in json.loads((D/'followup-control-results.json').read_text()))
artifact_verified=[];artifact_absent=[]
for name,h in m['artifacts'].items():
 path=R/'dist'/name
 if path.exists():assert sha(path)==h;artifact_verified.append(name)
 else:artifact_absent.append(name) # Local old delivery binaries are not source-tree dependencies.
copied=R/'rebuild/run-results/final-repair-v2-full'
for p in (R/'run-rebuild/final-repair-v2-full').rglob('*'):
 if p.is_file():assert (copied/p.relative_to(R/'run-rebuild/final-repair-v2-full')).read_bytes()==p.read_bytes()
assert (copied/'source-packet.md').read_bytes()==(R/'hardening/fixtures/Z-full-length-noisy.md').read_bytes()
E=D/'attempt-2'
scores=json.loads((E/'scores-final.json').read_text());full=json.loads((E/'full-length-results.json').read_text());new=json.loads((E/'new-results.json').read_text())
# Recheck the current validator on actual full reply parts without rewriting raw evidence.
current={}
def placements(text):
 result={};section=0
 for line in text.splitlines():
  if match:=re.match(r'## (\d+)\.',line):section=int(match[1])
  if match:=re.search(r'\[source: source-packet.md:(S\d+);',line):result.setdefault(match[1],[]).append(section)
 return result
for arm in ['original','rebuild']:
 parts=sorted((R/('run-'+arm)/'final-repair-v2-full').glob('part-*/bid-compliance-card.md'),key=lambda p:int(p.parent.name.split('-')[1]))
 r=subprocess.run([sys.executable,'-B','-X','utf8',str(R/arm/'tools/validate_packet.py'),str(R/'hardening/fixtures/Z-full-length-noisy.md'),*[str(p) for p in parts]],capture_output=True,text=True,encoding='utf-8')
 assert (r.returncode==0)==full[arm]['checks']['exact_shape_quotes_coverage'];current[arm]={'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
 text=(R/('run-'+arm)/'final-repair-v2-full/bid-compliance-card.md').read_text(encoding='utf-8');pos=placements(text);assert pos==full[arm]['positions']
 exp=json.loads((D/'full-expectations.json').read_text())
 for sid,ns in exp['routing'].items():assert all(n in pos.get(sid,[]) for n in ns)==full[arm]['genuine_routing'][sid]
 for sid in exp['noise_only12']:assert (pos.get(sid)==[12])==full[arm]['noise_only12'][sid]
 assert full[arm]['passed']==all(full[arm]['checks'].values())
 for name,expect in json.loads((D/'expectations.json').read_text()).items():
  source=D/'fixtures'/(name+'.md');assert sha(source)==expect['source_sha256']
  pos=placements((R/('run-'+arm)/'final-repair-v2-new'/name/'bid-compliance-card.md').read_text(encoding='utf-8'));assert pos==new[arm][name]['positions']
  for sid,ns in expect['required'].items():assert all(n in pos.get(sid,[]) for n in ns)==new[arm][name]['checks'][sid+'_required']
  for sid,ns in expect['exclusive'].items():assert (pos.get(sid)==ns)==new[arm][name]['checks'][sid+'_exclusive']
  assert new[arm][name]['passed']==all(new[arm][name]['checks'].values())
old_parts=sorted((R/'run-rebuild/final-repair-full').glob('part-*/bid-compliance-card.md'),key=lambda p:int(p.parent.name.split('-')[1]))
old=subprocess.run([sys.executable,'-B','-X','utf8',str(R/'rebuild/tools/validate_packet.py'),str(R/'hardening/fixtures/Z-full-length-noisy.md'),*[str(p) for p in old_parts]],capture_output=True,text=True,encoding='utf-8')
assert old.returncode==1 and 'S100' in old.stdout
print(json.dumps({'preserved_S100_failure_still_rejected':True,'status':'PASS: evidence integrity; consult performance separately','preserved_tracked_files':len(m['files']),'frozen_questions_unchanged':True,'prior_local_artifacts_verified':artifact_verified,'prior_local_artifacts_absent_in_source_clone':artifact_absent,'fresh_raw_model_turns':turns,'core_comparisons':scores['totals'],'full_performance':{a:x['checks'] for a,x in full.items()},'new_performance':{a:{k:v['passed'] for k,v in x.items()} for a,x in new.items()},'control_cases':controls['count'],'rebuild_control_failures':controls['rebuild_failures'],'full_validation':current,'published':False},indent=2))
