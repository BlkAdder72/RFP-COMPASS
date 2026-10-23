from pathlib import Path
import hashlib,json,shutil,subprocess
R=Path.cwd();D=R/'scope-repair';assert not (D/'preservation.json').exists()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.open('x',encoding='utf-8',newline='\n').write(s)
mutable=['rebuild/tools/validate_packet.py','tools/verify_submission.py','README.md','results.md','SUBMISSION_COMMENT.md','packaging/COMPLIANCE.md','rebuild/README.md']
files=[n for n in subprocess.check_output(['git','ls-files','-z']).decode().split('\0') if n]
for n in mutable:p=D/'before'/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(R/n,p)
artifacts={str(p.relative_to(R)).replace('\\','/'):sha(p) for folder in ['', 'final-repair','final-repair-verified','release','warning-release','warning-release-verified'] for p in (R/'dist'/folder).glob('*') if p.is_file()}
new(D/'preservation.json',json.dumps({'commit':subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),'tracked':{n:sha(R/n) for n in files},'mutable':mutable,'artifacts':artifacts},indent=2))
shutil.copytree(R/'red-team-warning-final/fixtures',D/'fixtures');exp=json.loads((R/'red-team-warning-final/expectations.json').read_text())
rows=[('Unrelated private correspondence','I need to attend my daughter’s birthday dinner on February 1, 2027 at 7 PM.'),('Unrelated private correspondence','My graduation ceremony is February 2, 2027 at 2 PM.'),('Unrelated private correspondence','My child’s christening ceremony is February 3, 2027 at 11 AM.'),('Official participation p. 1','Admission depends on attendance at these events:'),('Official participation p. 2','Our farewell dinner is February 4, 2027 at 7 PM.')]
p=D/'fixtures/D-scope-boundaries.md';new(p,''.join(f'S{i:03} | {a} | {b}\n' for i,(a,b) in enumerate(rows,1)));exp[p.stem]={'source_sha256':sha(p),'required':{'S005':[6]},'forbidden':{'S005':[12]},'exclusive':{f'S{i:03}':[12] for i in range(1,4)}}
new(D/'expectations.json',json.dumps(exp,indent=2));shutil.copyfile(R/'warning-repair/full-expectations.json',D/'full-expectations.json')
cases=[]
for folder,prefix in [('warning-repair','prior-'),('red-team-warning-final','red-')]:
 for c in json.loads((R/folder/'control-definitions.json').read_text(encoding='utf-8')):c['name']=prefix+c['name'];cases.append(c)
import importlib.util
spec=importlib.util.spec_from_file_location('v',R/'rebuild/tools/validate_packet.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
def card(rows):
 lines=[v.TITLE]
 for n,h in enumerate(v.HEADINGS,1):lines.append(h);lines.extend([f'- “{b}” [source: source-packet.md:S{i:03}; Document p. {i}]' for i,b in enumerate(rows,1)] if n==12 else ['- not in source'])
 return '\n'.join(lines)+'\n'
for name,bs,warn,sid in [
 ('unknown-event-heading',['Admission depends on attendance at these events:','Our farewell dinner is February 4, 2027 at 7 PM.'],True,'S002'),
 ('private-need-to',['I need to attend my daughter’s birthday dinner on February 1, 2027 at 7 PM.'],False,'S001'),
 ('private-need-to-next',['I need to attend my daughter’s birthday dinner on February 1, 2027 at 7 PM.','My graduation ceremony is February 2, 2027 at 2 PM.'],False,'S002'),
 ('private-mixed-real',['I have to attend my daughter’s birthday dinner on February 1, 2027 at 7 PM; offers are to reach the office by February 2, 2027 at 2 PM.'],True,'S001'),
 ('private-mixed-companies',['I have to attend my daughter’s birthday dinner on February 1, 2027 at 7 PM; all companies are to attend our farewell dinner at 8 PM.'],True,'S001'),
 ('clinical-self-obligation',['I have to attend my physical therapy appointment for patients on February 1, 2027 at 7 PM.'],True,'S001'),
 ('required-context-self',['Mandatory bidder events:','I have to attend my daughter’s birthday dinner on February 1, 2027 at 7 PM.'],True,'S002'),
 ('explicit-reset-self',['Mandatory bidder events:','Private correspondence:','I have to attend my daughter’s birthday dinner on February 1, 2027 at 7 PM.'],False,'S003')]:cases.append({'name':name,'source':''.join(f'S{i:03} | Document p. {i} | {b}\n' for i,b in enumerate(bs,1)),'card':card(bs),'valid':True,'warning':warn,'sid':sid})
new(D/'control-definitions.json',json.dumps(cases,ensure_ascii=False,indent=2))
s=(R/'warning-repair/run_arm.py').read_text().replace('warning-repair','scope-repair');new(D/'run_arm.py',s)
for name in ['controls.py','score_core.py','score_core_strict.py','score_full.py','score_models.py','replay_controls.py']:
 s=(R/'warning-repair'/name).read_text().replace('warning-repair','scope-repair');new(D/name,s)
new(D/'PROTOCOL.md','''# Obligation scope repair
Freeze sources, matrices and 56 controls before original core/new/full baseline. Core uses unchanged frozen Q1–Q8. Supplemental A/B/C are prior red-team regressions; D is a new synthetic combination, not an independent holdout. Same 221-statement full RFP and prior frozen expanded routing matrix. Run original core A–E, new A–D, full; commit complete raw baseline before candidate changes. Then commit warning-only candidate and run rebuild same order/model/settings through unchanged runners (gpt-6-astra medium). Fresh sessions, exact continues for full, no tools, retries, output correction or best-of selection. Six model knowledge files stay unchanged in each arm.
Scope repair must retain hard procurement/clinical vetoes and inherited mandatory context. A narrowly supported private self-obligation must not create procurement scope or reset genuine inherited scope. Unknown event headings keep warnings. Offer-receipt obligations remain protected. Christening/bridal-shower private wording is covered. Structural implementation from def difference onward stays byte-identical; exact anchors/quotes and trust checks unchanged. Preserve all previous files/deliveries, failed evidence and frozen questions. New source-bound controls include mixed private/real duties and clinical/mandatory guards. Submission draft must have exactly three identified sentences and the verbatim motivating feedback excerpt. Record all regressions, ties and remaining finite-heuristic limits. No publication.
''')
print(len(files),len(artifacts),len(cases))
