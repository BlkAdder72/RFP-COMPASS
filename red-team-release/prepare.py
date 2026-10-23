from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parents[1];D=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,t):p.parent.mkdir(parents=True,exist_ok=True);p.open('x',encoding='utf-8',newline='\n').write(t)
files=[n for n in subprocess.check_output(['git','ls-files','-z'],cwd=R).decode().split('\0') if n]
artifacts={str(p.relative_to(R)).replace('\\','/'):sha(p) for folder in [R/'dist',R/'dist/final-repair',R/'dist/final-repair-verified',R/'dist/release'] for p in folder.iterdir() if p.is_file()}
new(D/'preservation.json',json.dumps({'target':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),'files':{n:sha(R/n) for n in files},'artifacts':artifacts},indent=2))
anchors=['Supplement β p.\u202fxi §IV(1)(l) [note a]','Supplement β p.\u202fxi §IV(1)(I) [note a]','Annex C p. 03, item (i); line 007','Annex C p. 3, item (i); line 007','Schedule D p. 5 n. ¹','Schedule D p. 5 n. 1','Exhibit E p. 6 §2`(b)` [column [B]]','Exhibit E p. 6 §2\u200b(b) [column [B]]']
rows=[(a,'Applicants must include a signed conflict disclosure.') for a in anchors]
datasets={'X-citation-microvariants':rows,'Y-routing-boundaries':[
 ('RFP §Applicant qualifications','Applicants must hold an active state audit license to qualify.'),
 ('RFP §Required response contents','The response shall provide a narrative of external inspection findings and any corrective measures.'),
 ('RFP §Required response contents','Include a summary of disciplinary proceedings with the proposal.'),
 ('RFP §Performance obligations','After award, the selected firm shall deliver quarterly performance reports.'),
 ('RFP §Performance obligations','During performance, the contractor shall maintain its business license at its own expense.'),
 ('RFP §Optional material','Applicants may attach a brochure.'),
 ('RFP §Commercial terms','It is expected that the contract shall use a fixed-price structure for two years.'),
 ('RFP §Required response contents','Provide the maximum price with the response.'),
 ('Addendum 2 vendor answer','The revised submission deadline is January 14, 2027 at 2 PM.')],
 'Z-personal-and-mandatory-events':[
 ('Private family correspondence, unrelated attachment','My child’s baptism ceremony is December 3, 2026 at 11 AM.'),
 ('Private family correspondence, unrelated attachment','My baby shower is December 4, 2026 at 3 PM.'),
 ('Private family correspondence, unrelated attachment','My graduation ceremony is December 5, 2026 at 2 PM.'),
 ('RFP §Participation instructions','All companies have to attend the following events:'),
 ('RFP §Participation instructions, next page','Our farewell dinner is December 6, 2026 at 7 PM.') ]}
expect={}
for name,rows in datasets.items():
 p=D/'fixtures'/(name+'.md');new(p,''.join(f'S{i:03} | {a} | {b}\n' for i,(a,b) in enumerate(rows,1)));expect[name]={'source_sha256':sha(p),'required':{},'forbidden':{},'exclusive':{}}
x=expect['X-citation-microvariants'];x['required']={f'S{i:03}':[4,5] for i in range(1,9)}
y=expect['Y-routing-boundaries'];y['required']={'S001':[3],'S002':[4,5],'S003':[4,5],'S004':[8],'S005':[8],'S007':[2,8,11],'S008':[4,5,8],'S009':[6,11]};y['forbidden']={'S001':[5],'S004':[3,5],'S005':[3,5],'S006':[5]}
z=expect['Z-personal-and-mandatory-events'];z['exclusive']={'S001':[12],'S002':[12],'S003':[12]};z['required']={'S005':[6]};z['forbidden']={'S005':[12]}
new(D/'expectations.json',json.dumps(expect,indent=2))
# These source-derived checks are explicitly retrospective review of the existing full cards.
new(D/'full-semantic-review-plan.json',json.dumps({'method':'Retrospective source review, not a new model trial or holdout. Selected after reading source; no old scores rewritten.','source_sha256':sha(R/'hardening/fixtures/Z-full-length-noisy.md'),'required':{'S046':[3],'S047':[3,4,5,10],'S048':[3,10],'S065':[4,5],'S066':[4,5],'S075':[4,5],'S076':[4,5],'S077':[4,5],'S079':[4,5,10],'S080':[4,5,10],'S081':[8],'S083':[4,5,8],'S089':[4,5],'S133':[2,8,11],'S148':[8,11],'S150':[8],'S152':[8]},'forbidden':{'S081':[3,5],'S152':[3,5]},'rationale':'Qualification requirements vs instructions to disclose information; compulsory response contents vs optional material and post-award deliverables. New rule explicitly includes mandatory response information without a named attachment.'},indent=2))
new(D/'protocol.md','''# Final sealed-release red team
Target 06fcebace08c19410b63f1cd8c2523f66822d18b. Review only; no candidate edits, publication or delivery replacement.
Preserve all pre-review tracked bytes and every sealed delivery. Freeze new fixtures/expected answers and warning/control definitions before execution. X has previously unused complete anchor strings: Roman-letter lookalikes, zero padding, superscripts, narrow NBSP, zero-width characters and nested/literal Markdown punctuation. Y tests required-response information, price, optional brochures, qualification vs post-award obligations, contract expectation and addenda. Z mixes clearly personal unfamiliar milestones with compulsory official events phrased without the literal word must.
Use unchanged tools/run_arm.py: original then rebuild once, X/Y/Z same order, gpt-6-astra medium, fresh sessions, identical wrapper, no tools, no retry/best-of or raw correction. No expected matrix or scorer supplied to the model. These synthetic fixtures are new, but test classes are informed by previous failures, so do not call this an independent real-world holdout or a statistical comparison.
Separately validate correct personal-only cards and deliberately misplaced official events using both default validators; no sidecar. Include must vs have-to, personal activity synonyms, mixed personal/required content, and exact/corrupted citation controls. Evaluator-built controls are not model output. Record original successes and rebuild losses honestly.
Review selected additional placements in existing final full-length raw cards against a source-hash-bound retrospective matrix; do not relabel this as prospective or replace the old frozen score. Freeze root questions unchanged. Inspect competition required layout/history, feedback closure, report disclosures and final delivered archive/bundle checks. Run offline audit in a new clone of sealed bundle using tested long-path/authorized Git execution. Retain every failure. Audit report/evidence are separate from the sealed package, which remains untouched.
''')
print('New red-team inputs, expectations, retrospective matrix and preservation manifest frozen')
