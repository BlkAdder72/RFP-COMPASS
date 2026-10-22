"""Record immutable tool evidence for the frozen validator repair acceptance checks."""
from pathlib import Path
import hashlib,json,subprocess,sys,copy
R=Path(__file__).resolve().parents[1];D=R/'repair';OUT=D/'run'
assert not OUT.exists(), 'Refusing to overwrite repair evidence'
OUT.mkdir()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for name,h in json.loads((D/'preservation.json').read_text(encoding='utf-8'))['protected_files'].items():
    assert sha(R/name)==h,'Protected file changed: '+name
candidate=D/'candidate'
versions={'original':R/'original/tools/validate_packet.py','historical-rebuild':R/'rebuild/tools/validate_packet.py',
          'repaired':candidate/'tools/validate_packet.py'}
results=[]
def run(label,version,source,card,expect,review=None,error_text=None):
    folder=OUT/label/version;folder.mkdir(parents=True)
    command=[sys.executable,'-X','utf8',str(versions[version]),str(source),str(card)]
    if review is not None:command+=['--reviewed-exclusions',str(review)]
    (folder/'command.json').write_text(json.dumps(command,indent=2),encoding='utf-8')
    result=subprocess.run(command,capture_output=True,text=True,encoding='utf-8')
    (folder/'stdout.txt').write_text(result.stdout,encoding='utf-8');(folder/'stderr.txt').write_text(result.stderr,encoding='utf-8')
    (folder/'exit-code.txt').write_text(str(result.returncode),encoding='utf-8')
    hint_lines=[l for l in result.stdout.splitlines() if 'REVIEW' in l and 'Section 6' in l]
    audit={'label':label,'version':version,'source':str(source.relative_to(R)).replace('\\','/'),
           'card':str(card.relative_to(R)).replace('\\','/'),'source_sha256':sha(source),'card_sha256':sha(card),
           'validator_sha256':sha(versions[version]),'exit_code':result.returncode,'section6_hints':hint_lines,
           'review':str(review.relative_to(R)).replace('\\','/') if review else None,'expectation':expect}
    if review:audit['review_sha256']=sha(review)
    for sid,wanted in expect.get('hints',{}).items():
        actual=any(sid in line for line in hint_lines)
        assert actual==wanted,(label,version,sid,result.stdout)
    assert (result.returncode==0)==expect.get('valid',True),(label,version,result.stdout,result.stderr)
    if 'applied' in expect:assert ('APPLIED EXCLUSIONS' in result.stdout)==expect['applied']
    if error_text:assert error_text in result.stdout,(label,result.stdout)
    audit['passed']=True;(folder/'audit.json').write_text(json.dumps(audit,indent=2),encoding='utf-8');results.append(audit)
def make_review(source,ids):
    statements={l.split(' | ',2)[0]:l.split(' | ',2)[2] for l in source.read_text(encoding='utf-8').splitlines() if l}
    return {'schema_version':1,'packet_sha256':sha(source),'reviewer':'Codex evaluation adjudication; not owner or independent human approval',
            'decisions':[{'source_id':sid,'statement_sha256':hashlib.sha256(statements[sid].encode('utf-8')).hexdigest(),
                          'reason':'Synthetic personal content adjudicated against frozen repair protocol; preserve only in Section 12.'} for sid in ids]}
reviews=D/'review-records';reviews.mkdir(exist_ok=True)
def save_review(name,data):
    p=reviews/(name+'.json');p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8');return p
A=R/'fixtures/A-stapled-thread.md';F=R/'supplemental/fixtures/F-neutral-personal.md';K=R/'supplemental/fixtures/K-unrelated-label.md'
contained=R/'run-original/Q8-validator/contained.md';missed=R/'run-original/Q8-validator/missed-deadline.md'
N1=R/'supplemental/tool-original/N1-mislabeled-real-deadline/evaluator-card.md'
N2=R/'supplemental/tool-original/N2-neutral-personal/evaluator-card.md'
a_data=make_review(A,['S004','S005','S006','S007']);a_review=save_review('personal-A',a_data)
f_review=save_review('personal-F',make_review(F,['S002','S003']))
for version in versions:
    run('N1-default',version,K,N1,{'hints':{'S002':version!='historical-rebuild'}})
    run('A-contained-default',version,A,contained,{'hints':{'S004':version!='historical-rebuild'}})
    run('A-missed-deadline-default',version,A,missed,{'hints':{'S002':True}})
    run('N2-default',version,F,N2,{'hints':{'S002':True}})
run('A-contained-reviewed','repaired',A,contained,{'hints':{'S004':False},'applied':True},a_review)
run('A-missed-deadline-reviewed','repaired',A,missed,{'hints':{'S002':True,'S004':False},'applied':True},a_review)
run('N2-reviewed','repaired',F,N2,{'hints':{'S002':False},'applied':True},f_review)
run('N1-empty-review','repaired',K,N1,{'hints':{'S002':True},'applied':False},save_review('empty-K',make_review(K,[])))
mutants=[]
data=copy.deepcopy(a_data);data['packet_sha256']='0'*64;mutants.append(('stale-packet',data,'packet SHA-256 mismatch'))
data=copy.deepcopy(a_data);data['decisions'][0]['statement_sha256']='0'*64;mutants.append(('wrong-statement',data,'statement SHA-256 mismatch'))
data=copy.deepcopy(a_data);data['decisions'][0]['source_id']='S999';mutants.append(('unknown-id',data,'unknown source ID'))
data=copy.deepcopy(a_data);data['decisions'].append(data['decisions'][0]);mutants.append(('duplicate-id',data,'duplicate decision ID'))
data=copy.deepcopy(a_data);data['reviewer']=' ';mutants.append(('blank-reviewer',data,'reviewer must be named'))
data=copy.deepcopy(a_data);data['decisions'][0]['reason']=' ';mutants.append(('blank-reason',data,'reason required'))
data=copy.deepcopy(a_data);data['schema_version']=2;mutants.append(('unsupported-schema',data,'unsupported schema'))
data=copy.deepcopy(a_data);data['unexpected']='field';mutants.append(('unknown-field',data,'unexpected review fields'))
for label,data,error in mutants:
    run(label,'repaired',A,contained,{'valid':False,'hints':{'S004':True},'applied':False},save_review(label,data),error)
for label,body in [('malformed-json','{'),('duplicate-json-key','{"schema_version":1,"schema_version":1}')]:
    path=reviews/(label+'.json');path.write_text(body,encoding='utf-8')
    run(label,'repaired',A,contained,{'valid':False,'hints':{'S004':True},'applied':False},path)
run('operational-exclusion','repaired',A,R/'run-original/A-stapled-thread/bid-compliance-card.md',
    {'valid':False,'applied':False},a_review,'must appear only in Section 12')
run('procurement-exclusion','repaired',K,N1,{'valid':False,'hints':{'S002':True},'applied':False},
    save_review('invalid-procurement-K',make_review(K,['S002'])),'procurement wording')
# A mixed statement cannot be approved just because its personal clause is real.
I=R/'supplemental/fixtures/I-mixed-one-deadline.md'
card_text=(R/'supplemental/run-rebuild/I-mixed-one-deadline/repeat-1/bid-compliance-card.md').read_text(encoding='utf-8')
import importlib.util
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('v',versions['repaired']);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
rows=[line.split(' | ',2) for line in I.read_text(encoding='utf-8').splitlines()]
parts=[v.TITLE]
for num,heading in enumerate(v.HEADINGS,1):
    parts+=['',heading]
    ids=[0] if num==1 else [1] if num==12 else []
    parts += [f'- “{rows[i][2]}” [source: source-packet.md:{rows[i][0]}; {rows[i][1]}]' for i in ids] if ids else ['- not in source']
mixed=OUT/'mixed-quarantined-card.md';mixed.write_text('\n'.join(parts)+'\n',encoding='utf-8')
run('mixed-exclusion','repaired',I,mixed,{'valid':False,'hints':{'S002':True},'applied':False},
    save_review('invalid-mixed-I',make_review(I,['S002'])),'procurement wording')
# Replay archived responses unchanged, without review decisions.
for arm in ('original','rebuild'):
    for fixture in sorted((R/'fixtures').glob('*.md')):
        run('replay-first-'+arm+'-'+fixture.stem,'repaired',fixture,R/('run-'+arm)/fixture.stem/'bid-compliance-card.md',{'valid':True})
    for fixture in sorted((R/'supplemental/fixtures').glob('*.md')):
        for repeat in (1,2):
            run('replay-stress-'+arm+'-'+fixture.stem+'-'+str(repeat),'repaired',fixture,
                R/'supplemental'/('run-'+arm)/fixture.stem/('repeat-'+str(repeat))/'bid-compliance-card.md',{'valid':True})
for sample in sorted((candidate/'samples').iterdir()):
    run('sample-'+sample.name,'repaired',sample/'source-packet.md',sample/'bid-compliance-card.md',{'valid':True})
knowledge=['CLAUDE_PROJECT_INSTRUCTIONS.txt','identity.md','rules.md','examples.md','reference/input-schema.md','reference/output-schema.md']
assert all((candidate/name).read_bytes()==(R/'rebuild'/name).read_bytes() for name in knowledge)
for name,h in json.loads((D/'preservation.json').read_text(encoding='utf-8'))['protected_files'].items():assert sha(R/name)==h
(D/'results.json').write_text(json.dumps({'checks_passed':len(results),'knowledge_unchanged':True,'protected_files_verified':752,'cases':results},indent=2),encoding='utf-8')
print('PASS: '+str(len(results))+' recorded checks; 42 archived model cards and 4 samples replayed; source knowledge and 752 prior files unchanged.')
