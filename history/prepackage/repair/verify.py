"""Offline integrity and result audit; never overwrites historical evidence or reruns tests."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1];D=R/'repair'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
protected=json.loads((D/'preservation.json').read_text(encoding='utf-8'))['protected_files']
for name,h in protected.items():assert sha(R/name)==h,'Protected file changed: '+name
data=json.loads((D/'results.json').read_text(encoding='utf-8'))
assert len(data['cases'])==data['checks_passed']==75
for case in data['cases']:
    folder=D/'run'/case['label']/case['version']
    command=json.loads((folder/'command.json').read_text(encoding='utf-8'))
    assert sha(Path(command[3]))==case['validator_sha256']
    assert sha(R/case['source'])==case['source_sha256']
    assert sha(R/case['card'])==case['card_sha256']
    if case['review']:assert sha(R/case['review'])==case['review_sha256']
    stdout=(folder/'stdout.txt').read_text(encoding='utf-8')
    code=int((folder/'exit-code.txt').read_text(encoding='utf-8'))
    assert code==case['exit_code']
    assert (code==0)==case['expectation'].get('valid',True)
    hints=[l for l in stdout.splitlines() if 'REVIEW' in l and 'Section 6' in l]
    assert hints==case['section6_hints']
    for sid,wanted in case['expectation'].get('hints',{}).items():assert any(sid in l for l in hints)==wanted
    if 'applied' in case['expectation']:assert ('APPLIED EXCLUSIONS' in stdout)==case['expectation']['applied']
knowledge=['CLAUDE_PROJECT_INSTRUCTIONS.txt','identity.md','rules.md','examples.md','reference/input-schema.md','reference/output-schema.md']
for name in knowledge:assert (D/'candidate'/name).read_bytes()==(R/'rebuild'/name).read_bytes()
print(f'PASS: {len(protected)} historical files unchanged; 75 repair checks audited; six model knowledge files unchanged.')
