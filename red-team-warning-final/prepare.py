from pathlib import Path
import hashlib,importlib.util,json,subprocess
R=Path.cwd();D=R/'red-team-warning-final';assert not (D/'preservation.json').exists()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.open('x',encoding='utf-8',newline='\n').write(s)
files=[n for n in subprocess.check_output(['git','ls-files','-z']).decode().split('\0') if n]
artifacts={str(p.relative_to(R)).replace('\\','/'):sha(p) for folder in ['', 'final-repair','final-repair-verified','release','warning-release','warning-release-verified'] for p in (R/'dist'/folder).glob('*') if p.is_file()}
new(D/'preservation.json',json.dumps({'target':subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),'files':{n:sha(R/n) for n in files},'artifacts':artifacts},indent=2))
new(D/'reference/pre-warning-repair-validator.py',subprocess.check_output(['git','show','06fcebace08c19410b63f1cd8c2523f66822d18b:rebuild/tools/validate_packet.py']).decode('utf-8'))
anchors=['Annex Ω p.\u206012 §IV(a)','Annex Ω p.\u200e12 §IV(a)','Annexe\u0301 p. 12 §IV(a)','Annex E p. 12 &amp; exhibit A','Annex E p. 12 item non\u2011public','Annex E p. 12 literal \\[B\\]']
data={'A-obligation-paraphrases':[
('Official participation p. 1','All companies are to attend the following events:'),('Official participation p. 2','Our farewell dinner is January 5, 2027 at 7 PM.'),
('Official receipt instructions','Our farewell dinner is January 6, 2027 at 7 PM; offers are to reach the office by January 7, 2027 at 2 PM.'),
('Official participation p. 3','Attendance at the following activities is a condition of entry:'),('Official participation p. 4','Our baby shower is January 8, 2027 at 3 PM.')],
'B-private-obligations-and-milestones':[
('Unrelated private correspondence','Private correspondence:'),('Unrelated private correspondence','I have to attend my daughter’s birthday dinner on January 9, 2027 at 7 PM.'),
('Unrelated private correspondence','My graduation ceremony is January 10, 2027 at 2 PM.'),('Unrelated private correspondence','My child’s christening ceremony is January 11, 2027 at 11 AM.'),
('Unrelated private correspondence','My bridal shower is January 12, 2027 at 3 PM.'),('Unrelated private correspondence','I do not have to attend our family dinner on January 13, 2027 at 7 PM.'),
('Official response instructions','Proposals must arrive by January 14, 2027 at 2 PM.')],
'C-opaque-citation-variants':[(a,'Applicants must include a signed conflict disclosure.') for a in anchors]}
exp={}
for name,rows in data.items():
 p=D/'fixtures'/(name+'.md');new(p,''.join(f'S{i:03} | {a} | {b}\n' for i,(a,b) in enumerate(rows,1)));exp[name]={'source_sha256':sha(p),'required':{},'forbidden':{},'exclusive':{}}
exp['A-obligation-paraphrases']['required']={'S002':[6],'S003':[4,6],'S005':[6]};exp['A-obligation-paraphrases']['forbidden']={s:[12] for s in ['S002','S003','S005']}
exp['B-private-obligations-and-milestones']['exclusive']={f'S{i:03}':[12] for i in range(1,7)};exp['B-private-obligations-and-milestones']['required']={'S007':[6]}
exp['C-opaque-citation-variants']['required']={f'S{i:03}':[4,5] for i in range(1,7)}
new(D/'expectations.json',json.dumps(exp,indent=2))
spec=importlib.util.spec_from_file_location('v',R/'rebuild/tools/validate_packet.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
def card(rows):
 lines=[v.TITLE]
 for n,h in enumerate(v.HEADINGS,1):lines.append(h);lines.extend([f'- “{b}” [source: source-packet.md:S{i:03}; {a}]' for i,(a,b) in enumerate(rows,1)] if n==12 else ['- not in source'])
 return '\n'.join(lines)+'\n'
cases=[]
def add(name,bodies,want,sid='S001'):
 rows=[(f'Document p. {i}',b) for i,b in enumerate(bodies,1)];cases.append({'name':name,'source':''.join(f'S{i:03} | {a} | {b}\n' for i,(a,b) in enumerate(rows,1)),'card':card(rows),'valid':True,'warning':want,'sid':sid})
for name,heading in [('are-to','All companies are to attend the following events:'),('condition-of-entry','Attendance at the following activities is a condition of entry:'),('will-be-expected','All companies will be expected to attend the following events:'),('known-have-to','All companies have to attend the following events:')]:add(name,[heading,'Our farewell dinner is January 5, 2027 at 7 PM.'],True,'S002')
add('mixed-offers-to-reach',['Our farewell dinner is January 6, 2027 at 7 PM; offers are to reach the office by January 7, 2027 at 2 PM.'],True)
add('private-have-to',['I have to attend my daughter’s birthday dinner on January 9, 2027 at 7 PM.'],False)
add('private-obligation-pollutes-context',['I have to attend my daughter’s birthday dinner on January 9, 2027 at 7 PM.','My graduation ceremony is January 10, 2027 at 2 PM.'],False,'S002')
add('private-negated-have-to',['I do not have to attend our family dinner on January 13, 2027 at 7 PM.'],False)
for name,body in [('christening','My child’s christening ceremony is January 11, 2027 at 11 AM.'),('bridal-shower','My bridal shower is January 12, 2027 at 3 PM.'),('known-baptism','My child’s baptism ceremony is January 11, 2027 at 11 AM.')]:add(name,[body],False)
add('clinical-guard',['Our patients are to attend the following events:','Our farewell dinner is January 5, 2027 at 7 PM.'],True,'S002')
add('private-reset-control',['Companies have to attend the following events:','Private correspondence:','My graduation ceremony is January 10, 2027 at 2 PM.'],False,'S003')
rows=data['C-opaque-citation-variants'];src=''.join(f'S{i:03} | {a} | {b}\n' for i,(a,b) in enumerate(rows,1));text=card(rows)
cases.append({'name':'exact-opaque-anchors','source':src,'card':text,'valid':True,'warning':None,'sid':'S001'})
for name,a,b in [('word-joiner-deleted','p.\u206012','p.12'),('ltr-mark-deleted','p.\u200e12','p.12'),('accent-composed','Annexe\u0301','Annexé'),('entity-decoded','&amp;','&'),('hyphen-normalized','non\u2011public','non-public'),('backslashes-deleted','\\[B\\]','[B]')]:cases.append({'name':name,'source':src,'card':text.replace(a,b),'valid':False,'warning':None,'sid':'S001'})
cases.append({'name':'quote-word-joiner-inserted','source':src,'card':text.replace('signed conflict','signed\u2060 conflict'),'valid':False,'warning':None,'sid':'S001'})
new(D/'control-definitions.json',json.dumps(cases,ensure_ascii=False,indent=2))
new(D/'PROTOCOL.md','''# Repaired package adversarial review
Sealed target 09684fc7129b8ff4bcbefe4b749f644f8f23f50e. No candidate, frozen-question, previous-report, raw-run or delivery edits. New evidence only in this directory. Commit fixtures, source-bound expected checks and evaluator control definitions before execution. Same default validator invocation, no sidecars. Test original, repaired rebuild and a preserved pre-warning-repair validator snapshot (06fceba) to distinguish regressions introduced by the last repair from failures tied with original. The historical validator snapshot is for tool controls only, not a third model arm.
Run original A/B/C once, commit baseline, then rebuild A/B/C once through unchanged tools/run_arm.py with gpt-6-astra medium. Same wrapper/order/knowledge selection; fresh sessions, no tools, retries, corrections or best-of selection. Expected checks never supplied to models. New exact strings, but synthetic test classes informed by previous findings; no independent real-world holdout or reliability claim. Structural/citation, semantic routing and personal-warning checks remain separate.
A tests are-to, condition-of-entry and offer-receipt obligation wording. B tests unrelated private obligations, negative modality, unfamiliar personal milestones and a real deadline. C tests word joiners, direction marks, decomposed accents, HTML entity spelling, nonbreaking hyphens and literal backslashes in complete opaque anchors. Correct personal cards and deliberately misrouted official cards are evaluator-built, not model replies. Reinspect existing full-RFP evidence without rerunning or changing old scores. Verify sealed artifact hashes, complete archive bytes and bundle history; retain all failures. No publication or replacement delivery.
''')
print(len(files),len(artifacts),len(cases))
