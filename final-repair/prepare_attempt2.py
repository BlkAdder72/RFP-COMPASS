from pathlib import Path
import hashlib,json,shutil
R=Path(__file__).resolve().parents[1];D=R/'final-repair';A=D/'attempt-1';A.mkdir(exist_ok=False)
files=['scores-final.json','new-results.json','full-length-results.json','full-length-results-original.json','score_core.py','score_new.py','score_full.py','write_reports.py','verify.py']
for name in files:shutil.copyfile(D/name,A/name)
knowledge=D/'attempt-1-knowledge'
for arm in ['original','rebuild']:
 for name in ['CLAUDE_PROJECT_INSTRUCTIONS.txt','identity.md','rules.md','examples.md','reference/input-schema.md','reference/output-schema.md','tools/validate_packet.py']:
  target=knowledge/arm/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(R/arm/name,target)
manifest={}
for folder in [A,knowledge,*[R/('run-'+a)/('final-repair-'+k) for a in ['original','rebuild'] for k in ['core','new','full']]]:
 for p in folder.rglob('*'):
  if p.is_file():manifest[str(p.relative_to(R)).replace('\\','/')]=hashlib.sha256(p.read_bytes()).hexdigest()
(A/'manifest.json').open('x').write(json.dumps(manifest,indent=2))
(A/'REPORT.md').open('x',encoding='utf-8').write('''# First final-repair attempt: retained failure
All three requested findings close on their frozen cases: S076 is in Sections 4 and 5, the graduation hint clears without losing genuine-event warnings, and strict quotations reject altered characters/delimiters. Core scores: five improvements, three ties. New fixtures: all three rebuilt passes.
However, the rebuilt full-length raw card changes S100’s Section 6 anchor from its own `TBRPC Auditing RFP p. 9 §7 Selection Process` to the next row’s `TBRPC Auditing RFP pp. 9-10 §7 Selection Process`. Validation correctly fails. All quotes are exact and seven personal rows remain only in Section 12. The original full card has exact anchors and S076 placement, but leaks six personal rows.
This is a new copying regression, not a pass. Raw runs remain at run-ARM/final-repair-{core,new,full}; snapshots and score/code hashes are retained here and in attempt-1-knowledge. The validator is not weakened. A separately frozen second attempt adds a general page-versus-range example and reruns both arms, preserving this failure.
''')
(D/'attempt-2-protocol.md').open('x',encoding='utf-8').write('''# Citation follow-up: second versioned attempt
The first repair run failed on one S100 anchor substitution. Preserve it and every score, prompt, raw event and exact knowledge snapshot. Do not retry the same candidate or select a better response.
Before the second knowledge change, run and commit a new original baseline on the same core A–E, then U/V/W, then unchanged full-length RFP. Then add a general single-page versus page-range citation safeguard and extend the synthetic worked example. No actual S100 identifier, TBRPC answer, source-specific matrix or repaired raw output enters model knowledge. Validators and all expectations remain unchanged from attempt 1.
Run the new rebuilt version on the identical cases/order, with the unchanged model, wrapper, runners and continuation policy. New output prefix final-repair-v2. One run per arm/fixture; no best-of or raw corrections. All earlier attempts count as failures and remain in the final report. Questions.md remains frozen. No publication.
''')
source=(D/'run_pair_arm.py').read_text().replace("'final-repair-'+kind","'final-repair-v2-'+kind").replace("arm+'-'+kind+","arm+'-v2-'+kind+")
(D/'run_attempt2_arm.py').open('x',encoding='utf-8').write(source)
# Additional mutable example file was already captured before the stage; do not alter the original manifest.
target=D/'history/rebuild/examples.md';target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(D/'baseline-knowledge/rebuild/examples.md',target)
(D/'additional-mutable-paths.json').open('x').write(json.dumps({'paths':['rebuild/examples.md'],'snapshot':'final-repair/history/rebuild/examples.md','sha256':hashlib.sha256(target.read_bytes()).hexdigest()},indent=2))
print('First failed attempt preserved; second protocol frozen')
