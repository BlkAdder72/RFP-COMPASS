from pathlib import Path
import hashlib,json,subprocess,sys,shutil
R=Path(__file__).resolve().parents[1];D=R/'red-team';O=D/'evidence'
assert not O.exists(),'Refusing to overwrite audit evidence'
O.mkdir()
names=[n for n in subprocess.check_output(['git','ls-files','-z'],cwd=R).decode().split('\0') if n]
before={n:hashlib.sha256((R/n).read_bytes()).hexdigest() for n in names}
artifacts=[R/'dist/RFP-COMPASS-Comp15.bundle',R/'dist/RFP-COMPASS-Comp15-source.zip']
artifact_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in artifacts}
def execute(label,args,cwd=R):
    target=O/label;target.mkdir()
    (target/'command.json').write_text(json.dumps(args,indent=2),encoding='utf-8')
    result=subprocess.run(args,cwd=cwd,capture_output=True,text=True,encoding='utf-8')
    (target/'stdout.txt').write_text(result.stdout,encoding='utf-8');(target/'stderr.txt').write_text(result.stderr,encoding='utf-8')
    (target/'exit-code.txt').write_text(str(result.returncode),encoding='utf-8');return result
results={}
for arm in ('original','rebuild'):
    for kind in ('contained','missed-deadline'):
        label=arm+'-'+kind+'-default'
        result=execute(label,[sys.executable,'-X','utf8',str(R/arm/'tools/validate_packet.py'),str(R/'fixtures/A-stapled-thread.md'),str(R/'run-original/Q8-validator'/(kind+'.md'))])
        hints=[l for l in result.stdout.splitlines() if 'REVIEW' in l and 'Section 6' in l]
        results[label]={'exit_code':result.returncode,'section6_hints':hints,
                        'frozen_check_pass':not any('S004' in l for l in hints) if kind=='contained' else any('S002' in l for l in hints)}
for kind in ('contained','missed-deadline'):
    label='rebuild-'+kind+'-with-additional-review'
    result=execute(label,[sys.executable,'-X','utf8',str(R/'rebuild/tools/validate_packet.py'),str(R/'fixtures/A-stapled-thread.md'),str(R/'run-original/Q8-validator'/(kind+'.md')),'--reviewed-exclusions',str(R/'repair/review-records/personal-A.json')])
    results[label]={'exit_code':result.returncode,'section6_hints':[l for l in result.stdout.splitlines() if 'REVIEW' in l and 'Section 6' in l]}
# Minimal isolated copy of the real runner. Its existing first trial must stop execution before any CLI invocation.
box=D/'sandbox';(box/'tools').mkdir(parents=True);(box/'fixtures').mkdir()
shutil.copyfile(R/'tools/run_arm.py',box/'tools/run_arm.py')
for name in ('CLAUDE_PROJECT_INSTRUCTIONS.txt','identity.md','rules.md','examples.md','reference/input-schema.md','reference/output-schema.md'):
    dst=box/'rebuild'/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(R/'rebuild'/name,dst)
shutil.copyfile(R/'fixtures/A-stapled-thread.md',box/'fixtures/A-stapled-thread.md')
(box/'run-rebuild/A-stapled-thread').mkdir(parents=True)
env=box/'run-rebuild/environment.json';env.write_text('{"preserved_evidence":"MUST NOT CHANGE ON REFUSAL"}\n',encoding='utf-8')
old=env.read_bytes();(O/'runner-environment-before.bin').write_bytes(old)
refused=execute('runner-refusal',[sys.executable,str(box/'tools/run_arm.py'),'rebuild'],box)
new=env.read_bytes();(O/'runner-environment-after.bin').write_bytes(new)
assert 'Refusing to overwrite existing trial' in refused.stderr
results['runner-refusal']={'exit_code':refused.returncode,'model_called':False,'environment_changed':old!=new,
                           'before_sha256':hashlib.sha256(old).hexdigest(),'after_sha256':hashlib.sha256(new).hexdigest()}
for n,h in before.items():assert hashlib.sha256((R/n).read_bytes()).hexdigest()==h,'Existing tracked file changed: '+n
for p in artifacts:assert hashlib.sha256(p.read_bytes()).hexdigest()==artifact_hashes[p.name]
results['preservation']={'tracked_files_unchanged':len(before),'delivery_sha256':artifact_hashes}
(D/'results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps(results,indent=2))
