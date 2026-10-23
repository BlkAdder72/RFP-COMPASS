"""Offline integrity and raw-event audit of the final hardening stage."""
from pathlib import Path
import hashlib,importlib.util,json,subprocess,sys
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[1];D=R/'hardening'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((D/'preservation.json').read_text(encoding='utf-8'))
for n,h in manifest['files'].items():
 p=D/'history'/n if n in manifest['mutable_paths'] else R/n
 assert sha(p)==h,'Prior evidence changed: '+n
artifact_count=0;absent_artifacts=[]
for n,h in manifest['artifacts'].items():
 archived=R/'dist/prior-scope-hardening'/n;current=R/'dist'/n
 if archived.is_file():
  assert sha(archived)==h,'Prior delivery changed: '+n
  artifact_count+=1
 elif current.is_file() and sha(current)==h:artifact_count+=1
 else:absent_artifacts.append(n)
assert subprocess.check_output(['git','show','bfdd812:questions.md'],cwd=R)==(R/'questions.md').read_bytes()
for name in ['hardening/check_cases.py','hardening/protocol.md','hardening/full-length-expectations.json','hardening/fixtures/Z-full-length-noisy.md','hardening/calendar.txt']:
 assert subprocess.check_output(['git','show','531f3f5:'+name],cwd=R)==(R/name).read_bytes(),'Frozen challenge changed: '+name
assert subprocess.check_output(['git','show','0686922:hardening/guard_probes.py'],cwd=R)==(D/'guard_probes.py').read_bytes()
assert (R/'tools/run_arm.py').read_bytes()==(R/'revision/runner_source.py').read_bytes()
assert (R/'rebuild/tools/validate_packet.py').read_bytes()==(D/'candidates/final.py').read_bytes()
spec=importlib.util.spec_from_file_location('runner',R/'tools/run_arm.py');runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)
turns=0
def audit(part,expected):
 global turns
 assert (part/'request.txt').read_text(encoding='utf-8')==expected
 events=[json.loads(l) for l in (part/'events.jsonl').read_text(encoding='utf-8').splitlines()]
 assert all(e.get('item',{}).get('type') in (None,'agent_message','reasoning') for e in events)
 msgs=[e['item']['text'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message']
 assert len(msgs)==1 and msgs[0]==(part/'bid-compliance-card.md').read_text(encoding='utf-8')
 assert events[-1]['type']=='turn.completed' and (part/'exit-code.txt').read_text(encoding='utf-8')=='0'
 cmd=json.loads((part/'command.json').read_text(encoding='utf-8'));assert cmd[cmd.index('-m')+1]=='gpt-6-astra' and cmd[cmd.index('-c')+1]=='model_reasoning_effort="medium"'
 turns+=1
 return events,msgs[0]
for arm in ('original','rebuild'):
 base=R/('run-'+arm)/'hardening';env=json.loads((base/'environment.json').read_text(encoding='utf-8'))
 assert env['fixture_order']==[p.name for p in sorted((R/'fixtures').glob('*.md'))]
 for n,h in env['knowledge_sha256'].items():assert sha(R/arm/n)==h
 for fixture in sorted((R/'fixtures').glob('*.md')):audit(base/fixture.stem,runner.request(R,arm,fixture))
 for kind,sid,want in [('contained','S004',arm=='original'),('missed-deadline','S002',True)]:
  box=base/'Q8-final';cmd=json.loads((box/(kind+'-command.json')).read_text(encoding='utf-8'));assert '--reviewed-exclusions' not in cmd
  stdout=(box/(kind+'-stdout.txt')).read_text(encoding='utf-8')
  assert any('REVIEW' in l and 'Section 6' in l and sid in l for l in stdout.splitlines())==want
 full=R/('run-'+arm)/'hardening-full';env=json.loads((full/'environment.json').read_text(encoding='utf-8'))
 assert env['fixture_sha256']==sha(D/'fixtures/Z-full-length-noisy.md')
 for n,h in env['knowledge_sha256'].items():assert sha(R/arm/n)==h
 session=None;messages=[]
 for i,part in enumerate(sorted(full.glob('part-*'),key=lambda p:int(p.name.split('-')[1])),1):
  events,msg=audit(part,runner.request(R,arm,D/'fixtures/Z-full-length-noisy.md') if i==1 else 'continue');messages.append(msg)
  ids=[e['thread_id'] for e in events if e.get('type')=='thread.started']
  assert len(ids)==1
  if i==1:session=ids[0]
  else:
   assert ids[0]==session and session in json.loads((part/'command.json').read_text(encoding='utf-8'))
   assert messages[-2].rstrip().endswith('<!-- RFP COMPASS: continued in next reply -->')
 assert (full/'bid-compliance-card.md').read_text(encoding='utf-8')=='\n'.join(messages)
checks={}
for stage,code in [('before',D/'history/rebuild/tools/validate_packet.py'),('after',D/'candidates/initial.py'),('after-v2',D/'candidates/second.py'),('after-v3',R/'rebuild/tools/validate_packet.py')]:
 data=json.loads((D/stage/'results.json').read_text(encoding='utf-8'));assert data['count']==52
 for c in data['cases']:
  assert c['validator_sha256']==sha(code if c['arm']=='rebuild' else R/'original/tools/validate_packet.py')
  box=D/stage/c['label']/c['arm'];stdout=(box/'stdout.txt').read_text(encoding='utf-8')
  observed=any('REVIEW' in l and f"Section {c['section']}" in l and c['sid'] in l for l in stdout.splitlines())
  assert observed==c['warning']
 checks[stage]=data['passed']
assert checks['after-v2']['rebuild']==26 and checks['after']['rebuild']==25
guards={}
for stage,code in [('guards-before',D/'candidates/second.py'),('guards-after',R/'rebuild/tools/validate_packet.py')]:
 data=json.loads((D/stage/'results.json').read_text(encoding='utf-8'));guards[stage]={a:sum(c['passed'] for c in data if c['arm']==a) for a in ('original','rebuild')}
 for c in data:assert c['validator_sha256']==sha(code if c['arm']=='rebuild' else R/'original/tools/validate_packet.py')
assert guards['guards-before']['rebuild']==1 and guards['guards-after']['rebuild']==6
prior=json.loads((D/'final-prior-controls.json').read_text(encoding='utf-8'));assert prior['count']==prior['passed']==51
replays=json.loads((D/'final-replay-results.json').read_text(encoding='utf-8'));assert replays['count']==replays['passed']==92
base=(R/'original/samples/04-real-tbrpc-auditing-rfp/source-packet.md').read_bytes();fixture=(D/'fixtures/Z-full-length-noisy.md').read_bytes();assert fixture.startswith(base)
rows=fixture.decode('utf-8').splitlines();assert sum(l.startswith('S') for l in rows)==221
noise=[l.split(' | ',2)[2] for l in rows if l.startswith(tuple(f'S{i}' for i in range(215,222)))]
assert '\n'.join(noise)+'\n'==(D/'calendar.txt').read_text(encoding='utf-8')
scores=json.loads((D/'scores-final.json').read_text(encoding='utf-8'));assert scores['totals']=={'improved':5,'tied':3,'regressed':0}
full=json.loads((D/'full-length-results.json').read_text(encoding='utf-8'))
assert full['rebuild']['checks']['exact_shape_quotes_coverage'] and full['rebuild']['checks']['noise_only12']
copies=R/'rebuild/run-results/full-length-noisy'
for p in (R/'run-rebuild/hardening-full').rglob('*'):
 if p.is_file():assert p.read_bytes()==(copies/p.relative_to(R/'run-rebuild/hardening-full')).read_bytes()
assert (copies/'source-packet.md').read_bytes()==fixture and (copies/'calendar.txt').read_bytes()==(D/'calendar.txt').read_bytes()
report={'status':'PASS','prior_tracked_files_preserved':len(manifest['files']),'local_prior_artifacts_verified':artifact_count,'optional_prior_artifacts_absent':absent_artifacts,'questions_unchanged':True,'fresh_core_sessions':10,'fresh_full_sessions':2,'fresh_model_turns':turns,'deterministic_controls':checks,'broader_header_guards':guards,'prior_controls':51,'archived_card_replays':92,'core_question_comparisons':scores['totals'],'full_length_checks':{a:r['checks'] for a,r in full.items()},'publication':'NOT PERFORMED','limits':'Bounded English hint classifier; synthetic known fixtures; one fresh pair per fixture; no statistical or fresh Claude claim.'}
(D/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
