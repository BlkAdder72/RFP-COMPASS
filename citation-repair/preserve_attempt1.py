from pathlib import Path
import hashlib,json,shutil
R=Path(__file__).resolve().parents[1];D=R/'citation-repair';O=D/'attempt-1';O.mkdir(exist_ok=False)
for n in ['scores-final.json','full-length-results.json','score_core.py','score_full.py','verify.py','write_reports.py']:shutil.copyfile(D/n,O/n)
for arm in ('original','rebuild'):
 for n in ['CLAUDE_PROJECT_INSTRUCTIONS.txt','identity.md','rules.md','examples.md','reference/input-schema.md','reference/output-schema.md']:
  p=D/'attempt-1-knowledge'/arm/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(R/arm/n,p)
(O/'README.md').write_text('First repair attempt: general opaque-anchor instructions alone. Five fresh core model sessions per arm: five improved question results, three ties. Both fresh full-length model cards repeat S072 shortened anchors twice; both FAIL. Every quote text is exact, all 221 IDs present. Rebuild contains all seven personal statements only12; original leaks six. No validator, raw output, input or expected answer changed. Raw records remain under run-ARM/citation-repair-core and citation-repair-full. No best-of rerun: the next attempt changes general model knowledge and preserves this failure.\n',encoding='utf-8')
(O/'hashes.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in O.iterdir() if p.is_file()},indent=2),encoding='utf-8')
