from pathlib import Path
import hashlib,json,subprocess
R=Path.cwd();D=R/'scope-guard-repair';m=json.loads((D/'preservation.json').read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for n,h in m['tracked'].items():assert sha(D/'before'/n if n in m['mutable'] else R/n)==h,n
for n,h in m['artifacts'].items():assert sha(R/n)==h,n
assert (R/'questions.md').read_bytes()==subprocess.check_output(['git','show','bfdd812:questions.md'])
(D/'prior-preservation.json').open('x').write(json.dumps({'passed':True,'tracked_files_preserved':len(m['tracked']),'sealed_files_preserved':len(m['artifacts']),'mutable_files_snapshotted':len(m['mutable']),'frozen_questions_unchanged':True},indent=2));print('PASS all prior evidence preserved')
