from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parents[1];D=Path(__file__).resolve().parent
p=json.loads((D/'preservation.json').read_text())
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
bad=[n for n,h in {**p['files'],**p['artifacts']}.items() if not (R/n).is_file() or sha(R/n)!=h]
assert not bad,bad
assert (R/'questions.md').read_bytes()==subprocess.check_output(['git','show','bfdd812:questions.md'],cwd=R)
assert (D/'reference/pre-scope-validator.py').read_bytes()==subprocess.check_output(['git','show','09684fc7129b8ff4bcbefe4b749f644f8f23f50e:rebuild/tools/validate_packet.py'],cwd=R)
(D/'preservation-verification.json').open('x').write(json.dumps({'passed':True,'prior_tracked_files':len(p['files']),'sealed_files':len(p['artifacts']),'target':p['target'],'frozen_questions_unchanged':True,'preceding_validator_exact':True,'mismatches':bad},indent=2))
print('PASS preservation')
