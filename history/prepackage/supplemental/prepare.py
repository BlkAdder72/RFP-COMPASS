"""Freeze first-pass hashes before supplemental trials; refuse to overwrite."""
from pathlib import Path
import subprocess, json, hashlib
R=Path(__file__).resolve().parents[1]; S=R/'supplemental'
target=S/'preservation.json'
assert not target.exists(), 'Preservation manifest already exists'
tracked=subprocess.check_output(['git','ls-files','-z'],cwd=R).decode().split('\0')
protected={n:hashlib.sha256((R/n).read_bytes()).hexdigest() for n in tracked if n and
           (n.startswith(('original/','rebuild/','run-original/','run-rebuild/','fixtures/')) or
            n in ('questions.md','feedback.md','results.md','original-integrity.json','original-integrity-recheck.json'))}
target.write_text(json.dumps({'baseline_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),
                             'protected_files':protected},indent=2),encoding='utf-8')
print('Frozen '+str(len(protected))+' first-pass/source files')
