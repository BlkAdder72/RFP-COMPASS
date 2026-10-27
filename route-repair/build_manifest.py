"""Hash tracked native evidence only. Stage new evidence before invoking this tool."""
from pathlib import Path
import hashlib,json,subprocess
D=Path(__file__).resolve().parent; R=D.parent
names=[n for n in subprocess.check_output(['git','ls-files','-z','--','route-repair'],cwd=R).decode().split('\0') if n and n!='route-repair/EVIDENCE_SHA256.json']
assert names
manifest={Path(n).relative_to('route-repair').as_posix():hashlib.sha256((R/n).read_bytes()).hexdigest() for n in sorted(names)}
(D/'EVIDENCE_SHA256.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
assert all(hashlib.sha256((D/n).read_bytes()).hexdigest()==h for n,h in manifest.items())
print(json.dumps({'tracked_files_verified':len(manifest),'ignored_cache_included':any('__pycache__' in n for n in manifest)}))
