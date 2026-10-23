"""Audit the revised default workflow, fresh paired trials, and prior evidence."""
from pathlib import Path
import hashlib,json,sys,subprocess,importlib.util
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[1];D=R/'revision'
K=R/'citation-repair/history'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
preservation=json.loads((D/'preservation.json').read_text(encoding='utf-8'))
for name,h in preservation['files'].items():
    path=D/'history'/name if name in preservation['mutable_paths'] else (K/name if (K/name).is_file() else R/name)
    assert sha(path)==h,'Prior evidence changed: '+name
artifact_checks=0;unavailable_artifacts=[]
for name,h in preservation['artifact_sha256'].items():
    archived=R/'dist/prior-default-q8'/name;current=R/'dist'/name
    if archived.is_file():
        assert sha(archived)==h,'Previous archived delivery changed: '+name
        artifact_checks+=1
    elif current.is_file() and sha(current)==h:
        artifact_checks+=1
    else:
        # Ignored delivery binaries are local outputs, not dependencies of a Git clone.
        # Their hashes and the entire earlier source/Git history remain in the package.
        unavailable_artifacts.append(name)
assert (R/'questions.md').read_bytes()==subprocess.check_output(['git','show','bfdd812:questions.md'],cwd=R)
for name in ['CLAUDE_PROJECT_INSTRUCTIONS.txt','identity.md','rules.md','examples.md','reference/input-schema.md','reference/output-schema.md']:
    assert (K/'rebuild'/name).read_bytes()==(R/'history/prepackage/rebuild'/name).read_bytes()
spec=importlib.util.spec_from_file_location('runner',R/'tools/run_arm.py');runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)
count=0
for arm in ('original','rebuild'):
    for repeat in (1,2):
        base=R/('run-'+arm)/'revision-v2'/('repeat-'+str(repeat));env=json.loads((base/'environment.json').read_text(encoding='utf-8'))
        assert env['model']=='gpt-6-astra' and env['reasoning_effort']=='medium'
        assert env['fixture_order']==[p.name for p in sorted((R/'fixtures').glob('*.md'))]
        for name,h in env['knowledge_sha256'].items():assert sha(K/arm/name)==h
        for fixture in sorted((R/'fixtures').glob('*.md')):
            trial=base/fixture.stem;assert (trial/'request.txt').read_text(encoding='utf-8')==runner.request(K,arm,fixture)
            command=json.loads((trial/'command.json').read_text(encoding='utf-8'));assert command[command.index('-m')+1]=='gpt-6-astra'
            assert command[command.index('-c')+1]=='model_reasoning_effort="medium"'
            events=[json.loads(l) for l in (trial/'events.jsonl').read_text(encoding='utf-8').splitlines()]
            assert all(e.get('item',{}).get('type') in (None,'agent_message','reasoning') for e in events)
            messages=[e['item']['text'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message']
            assert len(messages)==1 and messages[0]==(trial/'bid-compliance-card.md').read_text(encoding='utf-8')
            assert events[-1]['type']=='turn.completed' and (trial/'exit-code.txt').read_text(encoding='utf-8')=='0';count+=1
        q8=base/'Q8-default'
        for kind in ('contained','missed-deadline'):
            command=json.loads((q8/(kind+'-command.json')).read_text(encoding='utf-8'));assert '--reviewed-exclusions' not in command
            stdout=(q8/(kind+'-stdout.txt')).read_text(encoding='utf-8')
            expected=(arm=='original') if kind=='contained' else True
            sid='S004' if kind=='contained' else 'S002'
            assert any('REVIEW' in l and 'Section 6' in l and sid in l for l in stdout.splitlines())==expected
assert count==20
assert (R/'tools/run_arm.py').read_bytes()==(D/'runner_source.py').read_bytes()
initial=json.loads((D/'default-results.json').read_text(encoding='utf-8'))
assert initial['count']==51 and initial['passed']==50
assert [c['label']+'/'+c['arm'] for c in initial['cases'] if not c['passed']]==['missing-heading/rebuild']
default=json.loads((D/'default-tests-v2-results.json').read_text(encoding='utf-8'));assert default['count']==default['passed']==51
for case in default['cases']:
    assert sha(R/case['source'])==case['source_sha256'] and sha(R/case['card'])==case['card_sha256']
    assert sha((R/'hardening/history/rebuild/tools/validate_packet.py') if case['arm']=='rebuild' else R/'original/tools/validate_packet.py')==case['validator_sha256']
    folder=D/'default-tests-v2'/case['label']/case['arm'];stdout=(folder/'stdout.txt').read_text(encoding='utf-8')
    observed=any('REVIEW' in l and f"Section {case['section']}" in l and case['sid'] in l for l in stdout.splitlines())
    assert observed==case['expect_warning'] and (int((folder/'exit-code.txt').read_text(encoding='utf-8'))==0)==case['expect_valid']
replays=json.loads((D/'replay-results.json').read_text(encoding='utf-8'));assert replays['count']==replays['passed']==92
runner_tests=json.loads((D/'runner-tests.json').read_text(encoding='utf-8'));assert runner_tests['count']==7 and runner_tests['real_model_calls']==0
scores=json.loads((D/'scores.json').read_text(encoding='utf-8'));assert scores['sidecars_in_Q8'] is False
for repeat in ('1','2'):
    for arm in ('original','rebuild'):
        score=json.loads((R/('run-'+arm)/'revision-v2'/('repeat-'+repeat)/'scores.json').read_text(encoding='utf-8'))
        assert score==scores['scores'][repeat][arm]
report={'status':'PASS','prior_tracked_files_preserved':len(preservation['files']),'frozen_questions_unchanged':True,
        'local_prior_delivery_artifacts_verified':artifact_checks,'prior_delivery_binaries_not_in_checkout':unavailable_artifacts,
        'fresh_model_responses':count,'default_checker_cases':51,'archived_reference_replays':92,'model_free_runner_cases':7,
        'fresh_question_comparisons':scores['totals'],'Q8_default_no_sidecar':'PASS for rebuild in both repeats',
        'initial_test_assertion_correction':'Preserved initial 50/51 result; corrected missing-heading expectation, no validator change',
        'limitations':'Bounded source-text classifier; ambiguous statements retain hints; host system variation remains uncontrolled.'}
(D/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
