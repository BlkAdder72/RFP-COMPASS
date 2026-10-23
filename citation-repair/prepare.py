"""One-shot preservation and challenge freeze before the citation repair."""
from pathlib import Path
import hashlib,json,shutil,subprocess
R=Path(__file__).resolve().parents[1];D=R/'citation-repair'
if (D/'preservation.json').exists():raise SystemExit('Refusing existing preservation manifest before writes')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
names=[n for n in subprocess.check_output(['git','ls-files','-z'],cwd=R).decode().split('\0') if n]
mutable=['rebuild/CLAUDE_PROJECT_INSTRUCTIONS.txt','rebuild/rules.md','rebuild/reference/output-schema.md','rebuild/README.md','README.md','results.md','SUBMISSION_COMMENT.md','tools/verify_submission.py','packaging/final_compliance.py','packaging/final-compliance.json','packaging/COMPLIANCE.md','revision/verify.py','revision/verification.json','hardening/verify.py','hardening/verification.json']
for n in mutable:
 p=D/'history'/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(R/n,p)
(D/'preservation.json').write_text(json.dumps({'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),'mutable_paths':mutable,'files':{n:sha(R/n) for n in names},'artifacts':{p.name:sha(p) for p in (R/'dist').iterdir() if p.is_file()}},indent=2),encoding='utf-8')
F=D/'fixtures';F.mkdir();shutil.copyfile(R/'hardening/fixtures/Z-full-length-noisy.md',F/'Z-full-length-noisy.md')
expected=json.loads((R/'hardening/full-length-expectations.json').read_text(encoding='utf-8'));expected['routing']['S072']=[4,5]
expected['additional_checks']=['every S072 occurrence uses its complete packet anchor','no anchor/quote mismatch anywhere, not merely S072','all raw parts and exact continue prompts preserved','same validator bytes as previous sealed candidate']
(D/'full-length-expectations.json').write_text(json.dumps(expected,indent=2),encoding='utf-8')
shutil.copyfile(R/'hardening/calendar.txt',D/'calendar.txt')
print('Preserved',len(names),'tracked files; frozen 221-statement input identical to prior failed trial.')
