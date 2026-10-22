"""Preserve every prior tracked file, then promote the tested repair without rewriting history."""
from pathlib import Path
import subprocess,hashlib,json,shutil
R=Path(__file__).resolve().parents[1];P=R/'packaging';H=R/'history/prepackage'
assert not H.exists(), 'Snapshot already exists; refusing to overwrite'
assert not subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=R).strip(), 'Tracked changes exist'
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()
names=[n for n in subprocess.check_output(['git','ls-files','-z'],cwd=R).decode().split('\0') if n]
manifest={'prepackage_commit':head,'files':{}}
for name in names:
    data=(R/name).read_bytes();dst=H/name;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(data)
    manifest['files'][name]=hashlib.sha256(data).hexdigest()
for name,digest in manifest['files'].items():
    assert hashlib.sha256((H/name).read_bytes()).hexdigest()==digest
(P/'preservation.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
shutil.copytree(R/'repair/candidate',R/'rebuild',dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
print(f'Preserved {len(names)} tracked files from {head}; promoted candidate to root rebuild/.')
