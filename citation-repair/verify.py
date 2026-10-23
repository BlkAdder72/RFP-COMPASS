"""Audit citation repair provenance, unedited model continuations and unchanged validation."""
from pathlib import Path
import hashlib,importlib.util,json,subprocess,sys
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[1];D=R/'citation-repair'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((D/'preservation.json').read_text(encoding='utf-8'))
for n,h in m['files'].items():assert sha(D/'history'/n if n in m['mutable_paths'] else R/n)==h,'Prior evidence changed: '+n
artifact_count=0;absent=[]
for n,h in m['artifacts'].items():
 archived=R/'dist/prior-citation-repair'/n;current=R/'dist'/n
 if archived.exists():assert sha(archived)==h;artifact_count+=1
 elif current.is_file() and sha(current)==h:artifact_count+=1
 else:absent.append(n)
assert (R/'questions.md').read_bytes()==subprocess.check_output(['git','show','bfdd812:questions.md'],cwd=R)
assert (D/'fixtures/Z-full-length-noisy.md').read_bytes()==(R/'hardening/fixtures/Z-full-length-noisy.md').read_bytes()
for arm in ('original','rebuild'):assert sha(R/arm/'tools/validate_packet.py')==m['files'][arm+'/tools/validate_packet.py'],'Validator changed'
changed=['CLAUDE_PROJECT_INSTRUCTIONS.txt','rules.md','reference/output-schema.md']
for name in changed:
 assert (R/'rebuild'/name).read_bytes()!=(D/'history/rebuild'/name).read_bytes()
 assert 'S072' not in (R/'rebuild'/name).read_text(encoding='utf-8')
for name in ['identity.md','examples.md','reference/input-schema.md']:assert (R/'rebuild'/name).read_bytes()==(D/'history/rebuild'/name).read_bytes()
spec=importlib.util.spec_from_file_location('runner',R/'tools/run_arm.py');runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)
turns=0
def audit(part,request):
 global turns
 assert (part/'request.txt').read_text(encoding='utf-8')==request
 events=[json.loads(l) for l in (part/'events.jsonl').read_text(encoding='utf-8').splitlines()]
 assert all(e.get('item',{}).get('type') in (None,'agent_message','reasoning') for e in events)
 texts=[e['item']['text'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message']
 assert len(texts)==1 and texts[0]==(part/'bid-compliance-card.md').read_text(encoding='utf-8')
 assert events[-1]['type']=='turn.completed' and (part/'exit-code.txt').read_text(encoding='utf-8')=='0'
 cmd=json.loads((part/'command.json').read_text(encoding='utf-8'));assert cmd[cmd.index('-m')+1]=='gpt-6-astra' and cmd[cmd.index('-c')+1]=='model_reasoning_effort="medium"'
 turns+=1;return events,texts[0]
full_parts={}
for arm in ('original','rebuild'):
 for suffix in ('core','full'):
  base=R/('run-'+arm)/('citation-repair-'+suffix);env=json.loads((base/'environment.json').read_text(encoding='utf-8'))
  assert env['model']=='gpt-6-astra' and env['reasoning_effort']=='medium'
  for n,h in env['knowledge_sha256'].items():assert sha(R/arm/n)==h
  if suffix=='core':
   assert env['fixture_order']==[p.name for p in sorted((R/'fixtures').glob('*.md'))]
   for fixture in sorted((R/'fixtures').glob('*.md')):audit(base/fixture.stem,runner.request(R,arm,fixture))
   for kind,sid,want in [('contained','S004',arm=='original'),('missed-deadline','S002',True)]:
    q=base/'Q8-final';cmd=json.loads((q/(kind+'-command.json')).read_text(encoding='utf-8'));assert '--reviewed-exclusions' not in cmd
    out=(q/(kind+'-stdout.txt')).read_text(encoding='utf-8');assert any('REVIEW' in l and 'Section 6' in l and sid in l for l in out.splitlines())==want
  else:
   assert env['fixture_sha256']==sha(D/'fixtures/Z-full-length-noisy.md');session=None;messages=[]
   parts=sorted(base.glob('part-*'),key=lambda p:int(p.name.split('-')[1]));full_parts[arm]=len(parts)
   for i,part in enumerate(parts,1):
    events,text=audit(part,runner.request(R,arm,D/'fixtures/Z-full-length-noisy.md') if i==1 else 'continue');messages.append(text)
    ids=[e['thread_id'] for e in events if e.get('type')=='thread.started'];assert len(ids)==1
    if i==1:session=ids[0]
    else:
     assert ids[0]==session and session in json.loads((part/'command.json').read_text(encoding='utf-8'))
     assert messages[-2].rstrip().endswith('<!-- RFP COMPASS: continued in next reply -->')
   assert (base/'bid-compliance-card.md').read_text(encoding='utf-8')=='\n'.join(messages)
controls=json.loads((D/'validation-results.json').read_text(encoding='utf-8'));assert controls['count']==controls['passed']==22
for c in controls['cases']:assert c['validator_sha256']==sha(R/c['arm']/'tools/validate_packet.py')
core=json.loads((D/'scores-final.json').read_text(encoding='utf-8'));full=json.loads((D/'full-length-results.json').read_text(encoding='utf-8'))
rebuilt=full['rebuild'];fixed=rebuilt['checks']['exact_anchors'] and rebuilt['checks']['exact_shape_quotes_coverage']
s072_routing=all(s in rebuilt['positions'].get('S072',[]) for s in (4,5))
prior=json.loads((R/'hardening/full-length-results-final.json').read_text(encoding='utf-8'))
assert len(prior['rebuild']['anchor_mismatches'])==2 and not prior['rebuild']['checks']['exact_anchors']
copies=R/'rebuild/run-results/citation-repair-full'
for p in (R/'run-rebuild/citation-repair-full').rglob('*'):
 if p.is_file():assert p.read_bytes()==(copies/p.relative_to(R/'run-rebuild/citation-repair-full')).read_bytes()
assert (copies/'source-packet.md').read_bytes()==(D/'fixtures/Z-full-length-noisy.md').read_bytes()
summary=('Fresh rebuild full-length run passes every frozen check; S072 exact-anchor failure not reproduced; historical failures preserved' if rebuilt['passed'] else 'MIXED/FAIL: new full-length rebuild still has failed checks; all results retained')
report={'status':'PASS: evidence integrity','prior_tracked_files_preserved':len(m['files']),'local_prior_artifacts_verified':artifact_count,'optional_prior_artifacts_absent':absent,'questions_unchanged':True,'both_validators_byte_identical':True,'changed_model_knowledge':changed,'fresh_core_sessions':10,'fresh_full_sessions':2,'fresh_model_turns':turns,'full_reply_counts':full_parts,'exact_anchor_rejection_controls':22,'core_question_comparisons':core['totals'],'full_length_checks':{a:r['checks'] for a,r in full.items()},'S072_copying_fix_observed':fixed,'S072_routes_to_4_and_5':s072_routing,'performance_summary':summary,'publication':'NOT PERFORMED','limits':'One fresh pair on known input; prompt repair is not a deterministic copying guarantee; no raw corrections, retries or statistical claim.'}
(D/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
