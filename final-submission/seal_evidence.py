from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1];D=R/'final-submission'
def read(n):return json.loads((D/n).read_text(encoding='utf-8'))
assert read('verification.json')['status']=='PASS'
assert read('SUMMARY.json')['acceptance'].startswith('PASS')
assert read('packaged-samples-validation.json')['exit_code']==0
assert read('retained-S100-rejection.json')['passed']
assert (D/'REPORT.md').read_bytes()==(R/'results.md').read_bytes()
files={str(p.relative_to(D)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(D.rglob('*')) if p.is_file()}
(D/'EVIDENCE_SHA256.json').open('x',encoding='utf-8',newline='\n').write(json.dumps({'algorithm':'sha256','scope':'Every final-submission file except this manifest itself; earlier tracked files and old sealed artifacts are independently covered by preservation.json and Git history','files':files},indent=2));print('PASS final evidence manifest:',len(files),'files')
