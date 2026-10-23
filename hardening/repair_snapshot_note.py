from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parents[1];D=R/'hardening/full-first-pass'
expected=json.loads((D/'hashes.json').read_text(encoding='utf-8'))['README.md']
source=subprocess.check_output(['git','show','HEAD:README.md'],cwd=R)
assert hashlib.sha256(source).hexdigest()==expected,'Pinned first-pass README does not match manifest'
with (D/'AUDIT-NOTE.md').open('xb') as f:f.write((D/'README.md').read_bytes())
(D/'README.md').write_bytes(source)
print('Recovered exact first-pass README from committed Git blob; descriptive note preserved separately.')
