from pathlib import Path
import hashlib,json,subprocess,shutil
R=Path.cwd();D=R/'submission-repair'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
mutable=['rebuild/tools/validate_packet.py','tools/verify_submission.py','README.md','results.md','SUBMISSION_COMMENT.md','packaging/COMPLIANCE.md','rebuild/README.md','rebuild/rules.md','rebuild/reference/output-schema.md']
files=[n for n in subprocess.check_output(['git','ls-files','-z']).decode().split('\0') if n]
for n in mutable:p=D/'before'/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(R/n,p)
art={str(p.relative_to(R)).replace('\\','/'):sha(p) for f in ['','final-repair','final-repair-verified','release','warning-release','warning-release-verified','scope-release','scope-guard-release','polarity-release'] for p in (R/'dist'/f).glob('*') if p.is_file()}
(D/'preservation.json').open('x',encoding='utf-8').write(json.dumps({'commit':subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),'tracked':{n:sha(R/n) for n in files},'mutable':mutable,'artifacts':art},indent=2));print(len(files),len(art),len(mutable))
