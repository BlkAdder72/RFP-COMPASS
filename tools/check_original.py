"""Compare original bytes with the preserved judged Git archive, without extraction."""
from pathlib import Path
import hashlib, json, zipfile
root = Path(__file__).resolve().parents[1]
with zipfile.ZipFile(root / 'judged-source.zip') as archive:
    expected = {n: hashlib.sha256(archive.read(n)).hexdigest() for n in archive.namelist() if not n.endswith('/')}
actual = {str(p.relative_to(root / 'original')).replace('\\', '/'): hashlib.sha256(p.read_bytes()).hexdigest()
          for p in (root / 'original').rglob('*') if p.is_file()}
assert actual == expected, 'Original differs from judged archive'
feedback = root / 'feedback.md'
print(json.dumps({'judged_commit': '92847d2a17250fa18914d932826db63d99dcb75c', 'files_verified': len(actual),
                  'feedback_sha256': hashlib.sha256(feedback.read_bytes()).hexdigest(), 'files': actual}, indent=2))
