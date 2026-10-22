"""Independent Q8, context and fresh-text probes; no edits to the package."""
from pathlib import Path
import subprocess,hashlib,json,sys,importlib.util,shutil
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[1];D=R/'red-team-final';O=D/'evidence';assert not O.exists();O.mkdir()
names=[n for n in subprocess.check_output(['git','ls-files','-z'],cwd=R).decode().split('\0') if n]
before={n:hashlib.sha256((R/n).read_bytes()).hexdigest() for n in names}
artifacts={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'dist').glob('*') if p.is_file()}
spec=importlib.util.spec_from_file_location('v',R/'rebuild/tools/validate_packet.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
results=[]
def run(label,arm,source,card,sid='S002',expected_warning=None):
    folder=O/label/arm;folder.mkdir(parents=True)
    cmd=[sys.executable,'-X','utf8',str(R/arm/'tools/validate_packet.py'),str(source),str(card)]
    result=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8')
    for name,body in [('command.json',json.dumps(cmd,indent=2)),('stdout.txt',result.stdout),('stderr.txt',result.stderr),('exit-code.txt',str(result.returncode))]:
        (folder/name).write_text(body,encoding='utf-8')
    warning=any('REVIEW' in l and 'Section 6' in l and sid in l for l in result.stdout.splitlines())
    record={'case':label,'arm':arm,'exit_code':result.returncode,'warning_for':sid,'warning_emitted':warning,
            'expected_warning':expected_warning,'meets_expectation':warning==expected_warning if expected_warning is not None else None,
            'source':str(source.relative_to(R)).replace('\\','/'),'card':str(card.relative_to(R)).replace('\\','/'),
            'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'card_sha256':hashlib.sha256(card.read_bytes()).hexdigest()}
    results.append(record)
for arm in ('original','rebuild'):
    run('frozen-Q8-contained',arm,R/'fixtures/A-stapled-thread.md',R/'run-original/Q8-validator/contained.md','S004',arm=='original')
    run('frozen-Q8-real-deadline',arm,R/'fixtures/A-stapled-thread.md',R/'run-original/Q8-validator/missed-deadline.md','S002',True)
def fixture(name,rows,placement):
    folder=D/'inputs'/name;folder.mkdir(parents=True);source=folder/'source-packet.md';card=folder/'card.md'
    source.write_text('\n'.join(' | '.join(row) for row in rows)+'\n',encoding='utf-8')
    lines=[v.TITLE]
    for n,heading in enumerate(v.HEADINGS,1):
        lines+=['',heading];ids=placement.get(n,[])
        lines += [f'- “{rows[i][2]}” [source: source-packet.md:{rows[i][0]}; {rows[i][1]}]' for i in ids] if ids else ['- not in source']
    card.write_text('\n'.join(lines)+'\n',encoding='utf-8');return source,card
for label,header_anchor,body_anchor in [
    ('required-event-same-anchor','RFP p. 3 events','RFP p. 3 events'),
    ('required-event-different-lines','RFP p. 3 line 10','RFP p. 3 line 11'),
    ('required-event-different-paragraphs','RFP p. 3 paragraph 1','RFP p. 3 paragraph 2')]:
    source,card=fixture(label,[('S001',header_anchor,'Mandatory bidder events:'),
                               ('S002',body_anchor,'Our holiday potluck is January 12, 2027, at 1:30 PM.')],{4:[0],12:[1]})
    for arm in ('original','rebuild'):run(label,arm,source,card,'S002',True)
personal=[('retirement-lunch','Our retirement lunch is February 3, 2027, at 12:00 PM.'),
          ('private-therapy','My physical therapy appointment is March 4, 2027, at 9:00 AM.'),
          ('family-reunion','Our family reunion is April 5, 2027, at 4:00 PM.')]
for label,text in personal:
    source,card=fixture(label,[('S001','attached personal note line 1',text)],{12:[0]})
    for arm in ('original','rebuild'):run(label,arm,source,card,'S001',False)
for label,body in [('unknown-meeting','The meeting is May 6, 2027, at 2:00 PM.'),
                   ('mixed-requirement','Our retirement lunch is June 7, 2027, at noon; proposals are due at 3:00 PM.')]:
    source,card=fixture(label,[('S001','attachment.txt line 1',body)],{12:[0]})
    for arm in ('original','rebuild'):run(label,arm,source,card,'S001',True)
# Refusal must protect existing files before any CLI attempt or knowledge reading.
box=D/'refusal-sandbox';(box/'tools').mkdir(parents=True);shutil.copyfile(R/'tools/run_arm.py',box/'tools/run_arm.py')
out=box/'existing';out.mkdir();(out/'environment.json').write_text('PRESERVE SENTINEL',encoding='utf-8')
snapshot={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir()}
refused=subprocess.run([sys.executable,str(box/'tools/run_arm.py'),'original','--output-dir',str(out)],capture_output=True,text=True)
(O/'refusal-stdout.txt').write_text(refused.stdout,encoding='utf-8');(O/'refusal-stderr.txt').write_text(refused.stderr,encoding='utf-8')
unchanged=snapshot=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir()}
assert refused.returncode!=0 and unchanged and 'Refusing existing output' in refused.stderr
for name,h in before.items():assert hashlib.sha256((R/name).read_bytes()).hexdigest()==h,'Prior source/evidence changed: '+name
for name,h in artifacts.items():assert hashlib.sha256((R/'dist'/name).read_bytes()).hexdigest()==h
report={'target_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),'validator_probes':results,
        'runner_refusal':{'passed':True,'environment_unchanged':unchanged,'model_called':False},
        'preserved_tracked_files':len(before),'sealed_artifact_sha256':artifacts}
(D/'results.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'runner_refusal':report['runner_refusal'],'probes':[{k:r[k] for k in ('case','arm','warning_emitted','meets_expectation')} for r in results]},indent=2))
