"""Portable, offline final-package audit. Historical evidence is read, never regenerated."""
from pathlib import Path
import hashlib,json,subprocess,sys,re
R=Path(__file__).resolve().parents[1];P=R/'packaging';H=R/'history/prepackage'
sys.dont_write_bytecode=True
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
manifest=json.loads((P/'preservation.json').read_text(encoding='utf-8'))
for name,h in manifest['files'].items():assert sha(H/name)==h,'Historical snapshot changed: '+name
mutable={'README.md','results.md','tools/verify_submission.py','.gitignore'}
for name,h in manifest['files'].items():
    if name not in mutable and not name.startswith('rebuild/'):
        assert sha(R/name)==h,'Prior evidence changed: '+name
required=['original','feedback.md','rebuild','results.md','questions.md','run-original','run-rebuild']
assert all((R/name).exists() for name in required)
knowledge=['CLAUDE_PROJECT_INSTRUCTIONS.txt','identity.md','rules.md','examples.md','reference/input-schema.md','reference/output-schema.md']
assert all((R/'rebuild'/name).read_bytes()==(H/'rebuild'/name).read_bytes() for name in knowledge)
assert (R/'rebuild/tools/validate_packet.py').read_bytes()==(H/'repair/candidate/tools/validate_packet.py').read_bytes()
for name in ['identity.md','rules.md','examples.md','reference','README.md']:assert (R/'rebuild'/name).exists()
judged='92847d2a17250fa18914d932826db63d99dcb75c'
assert git('rev-parse','judged-original-comp13').decode().strip()==judged
entries={}
for row in git('ls-tree','-r','-z',judged).split(b'\0'):
    if row:
        meta,name=row.split(b'\t',1);entries[name.decode()]=meta.decode().split()[2]
actual={str(p.relative_to(R/'original')).replace('\\','/') for p in (R/'original').rglob('*') if p.is_file()}
assert actual==set(entries)
for name,obj in entries.items():
    data=(R/'original'/name).read_bytes()
    assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==obj,'Original differs from judged Git object: '+name
raw=(R/'original-integrity.json').read_bytes()
original_manifest=json.loads(raw.decode('utf-16' if raw.startswith((b'\xff\xfe',b'\xfe\xff')) else 'utf-8-sig'))
assert sha(R/'feedback.md')==original_manifest['feedback_sha256']
questions=(R/'questions.md').read_text(encoding='utf-8');assert len(set(re.findall(r'\| (Q\d+) \|',questions)))==8
stages=['be4d956','bfdd812','045e74e','c97a79c','f10babd','85c7e5a','b1f808c','a4d23ff','f7ee602','e86e16f','5c30121','1cc70ee','ef6c5a8']
for first,second in zip(stages,stages[1:]):
    assert subprocess.run(['git','merge-base','--is-ancestor',first,second],cwd=R).returncode==0
assert git('show','bfdd812:questions.md')==(R/'questions.md').read_bytes()
for commit in ('be4d956','bfdd812','045e74e'):
    assert subprocess.run(['git','cat-file','-e',commit+':rebuild'],cwd=R,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode!=0
count=0
for arm in ('original','rebuild'):
    for supplemental in (False,True):
        base=R/'supplemental' if supplemental else R
        for fixture in sorted((base/'fixtures').glob('*.md')):
            for repeat in ((1,2) if supplemental else (None,)):
                trial=base/('run-'+arm)/fixture.stem
                if repeat:trial=trial/('repeat-'+str(repeat))
                envpath=trial/'environment.json' if supplemental else base/('run-'+arm)/'environment.json'
                env=json.loads(envpath.read_text(encoding='utf-8'))
                assert env['model']=='gpt-6-astra' and env['reasoning_effort']=='medium'
                req=(trial/'request.txt').read_text(encoding='utf-8')
                for name,h in env['knowledge_sha256'].items():
                    assert sha(H/arm/name)==h
                    assert '<file name="'+name+'">\n'+(H/arm/name).read_text(encoding='utf-8')+'\n</file>' in req
                assert '<attachment name="source-packet.md">\n'+fixture.read_text(encoding='utf-8')+'\n</attachment>' in req
                assert req.endswith('Use the attached source-packet.md as the only active input. Apply the RFP Compass contract and return bid-compliance-card.md.\n')
                events=[json.loads(line) for line in (trial/'events.jsonl').read_text(encoding='utf-8').splitlines()]
                msgs=[e['item']['text'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message']
                assert len(msgs)==1 and msgs[0]==(trial/'bid-compliance-card.md').read_text(encoding='utf-8')
                assert events[-1]['type']=='turn.completed'
                assert (trial/'exit-code.txt').read_text(encoding='utf-8')=='0'
                assert all(e.get('item',{}).get('type') in (None,'agent_message','reasoning') for e in events)
                count+=1
assert count==42
repair=json.loads((R/'repair/results.json').read_text(encoding='utf-8'));assert len(repair['cases'])==75
versions={'original':H/'original/tools/validate_packet.py','historical-rebuild':H/'rebuild/tools/validate_packet.py','repaired':H/'repair/candidate/tools/validate_packet.py'}
for case in repair['cases']:
    folder=R/'repair/run'/case['label']/case['version']
    assert sha(versions[case['version']])==case['validator_sha256']
    assert sha(R/case['source'])==case['source_sha256'] and sha(R/case['card'])==case['card_sha256']
    if case['review']:assert sha(R/case['review'])==case['review_sha256']
    text=(folder/'stdout.txt').read_text(encoding='utf-8');code=int((folder/'exit-code.txt').read_text(encoding='utf-8'))
    assert code==case['exit_code'] and (code==0)==case['expectation'].get('valid',True)
    hints=[l for l in text.splitlines() if 'REVIEW' in l and 'Section 6' in l]
    for sid,want in case['expectation'].get('hints',{}).items():assert any(sid in l for l in hints)==want
    if 'applied' in case['expectation']:assert ('APPLIED EXCLUSIONS' in text)==case['expectation']['applied']
# Execute final root validator on archived cards and critical repair cases.
checks=[];logs=P/'final-checks';logs.mkdir(exist_ok=True)
def run(label,source,card,warnings=None,review=None):
    args=[sys.executable,'-X','utf8','rebuild/tools/validate_packet.py',str(source.relative_to(R)),str(card.relative_to(R))]
    if review:args+=['--reviewed-exclusions',str(review.relative_to(R))]
    result=subprocess.run(args,cwd=R,capture_output=True,text=True,encoding='utf-8')
    assert result.returncode==0,(label,result.stdout,result.stderr)
    for sid,want in (warnings or {}).items():
        assert any('REVIEW' in line and 'Section 6' in line and sid in line for line in result.stdout.splitlines())==want
    (logs/(label+'.stdout.txt')).write_text(result.stdout,encoding='utf-8')
    (logs/(label+'.stderr.txt')).write_text(result.stderr,encoding='utf-8')
    checks.append({'label':label,'arguments':args[1:],'exit_code':result.returncode,'warning_expectations':warnings or {}})
for arm in ('original','rebuild'):
    for extra in (False,True):
        base=R/'supplemental' if extra else R
        for fixture in sorted((base/'fixtures').glob('*.md')):
            for repeat in ((1,2) if extra else (None,)):
                trial=base/('run-'+arm)/fixture.stem
                if repeat:trial=trial/('repeat-'+str(repeat))
                run(('stress-' if extra else 'first-')+arm+'-'+fixture.stem+('-'+str(repeat) if repeat else ''),fixture,trial/'bid-compliance-card.md')
for sample in sorted((R/'rebuild/samples').iterdir()):run('sample-'+sample.name,sample/'source-packet.md',sample/'bid-compliance-card.md')
A=R/'fixtures/A-stapled-thread.md';F=R/'supplemental/fixtures/F-neutral-personal.md';K=R/'supplemental/fixtures/K-unrelated-label.md'
run('N1-regression',K,R/'supplemental/tool-original/N1-mislabeled-real-deadline/evaluator-card.md',{'S002':True})
run('feedback-contained-reviewed',A,R/'run-original/Q8-validator/contained.md',{'S004':False},R/'repair/review-records/personal-A.json')
run('feedback-real-deadline-reviewed',A,R/'run-original/Q8-validator/missed-deadline.md',{'S002':True,'S004':False},R/'repair/review-records/personal-A.json')
run('neutral-personal-reviewed',F,R/'supplemental/tool-original/N2-neutral-personal/evaluator-card.md',{'S002':False},R/'repair/review-records/personal-F.json')
for fixture in sorted((R/'fixtures').glob('[ABC]-*.md')):
    copied=R/'rebuild/run-results/rebuild-noisy-input'/fixture.stem
    for item in (R/'run-rebuild'/fixture.stem).iterdir():assert (copied/item.name).read_bytes()==item.read_bytes()
    assert (copied/'source-packet.md').read_bytes()==fixture.read_bytes()
result={'local_compliance':'PASS','preserved_prepackage_files':len(manifest['files']),'judged_original_files':len(entries),
        'raw_model_responses_verified':count,'historical_repair_checks_audited':75,'final_root_validator_checks':len(checks),
        'git_sequence':'PASS; questions and baseline precede first rebuild; all later stages retained',
        'review_record_dependency':'Explicit adjudication required to suppress personal hints; no claim of automatic classification',
        'external_gates':{'publication':'NOT PERFORMED, as requested','public_submission_link':'PENDING publication','premium_or_vip_eligibility':'NOT VERIFIED'},'checks':checks}
(P/'final-compliance.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
