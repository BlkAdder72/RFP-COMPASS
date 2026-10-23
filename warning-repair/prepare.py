from pathlib import Path
import hashlib,json,subprocess,shutil
R=Path.cwd();D=R/'warning-repair'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
tracked=subprocess.check_output(['git','ls-files','-z']).decode().split('\0');tracked=[n for n in tracked if n]
mutable=['rebuild/tools/validate_packet.py','tools/verify_submission.py','README.md','results.md','SUBMISSION_COMMENT.md','packaging/COMPLIANCE.md','rebuild/README.md']
for n in mutable:
 p=D/'before'/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(R/n,p)
artifacts={str(p.relative_to(R)):h(p) for p in [p for name in ['', 'release','final-repair','final-repair-verified'] for p in (R/'dist'/name).glob('*')] if p.is_file() and p.parent.name in ['dist','release','final-repair','final-repair-verified'] and p.suffix in ['.zip','.bundle','.json','.txt']}
(D/'preservation.json').write_text(json.dumps({'commit':subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),'tracked':{n:h(R/n) for n in tracked},'mutable':mutable,'artifacts':artifacts},indent=2))
shutil.copytree(R/'red-team-release/fixtures',D/'fixtures')
exp=json.loads((R/'red-team-release/expectations.json').read_text())
rows=[('Private family correspondence','My baby shower is December 12, 2026 at 3 PM.'),('Private family correspondence','Our child’s baptism ceremony is December 13, 2026 at 11 AM.'),('Participation p. 1','All companies have to attend the following events:'),('Participation p. 2','Our farewell dinner is December 14, 2026 at 7 PM.'),('Participation p. 3','Our farewell dinner is December 15, 2026 at 7 PM; companies have to deliver their offers by December 16, 2026 at 2 PM.')]
p=D/'fixtures/W-warning-obligations.md';p.write_text(''.join(f'S{i:03} | {a} | {b}\n' for i,(a,b) in enumerate(rows,1)),encoding='utf-8')
exp['W-warning-obligations']={'source_sha256':h(p),'required':{'S004':[6],'S005':[4,6]},'forbidden':{'S004':[12],'S005':[12]},'exclusive':{'S001':[12],'S002':[12]}}
(D/'expectations.json').write_text(json.dumps(dict(sorted(exp.items())),indent=2))
full=json.loads((R/'final-repair/attempt-2/full-expectations.json').read_text());plan=json.loads((R/'red-team-release/full-semantic-review-plan.json').read_text());full['routing'].update(plan['required']);full['forbidden']=plan['forbidden'];full['additional_checks']=['All prior exact citation and per-reply budget checks retained','17 previously retrospective semantic checks now frozen prospectively for this paired trial']
(D/'full-expectations.json').write_text(json.dumps(full,indent=2))
s=(R/'final-repair/run_attempt2_arm.py').read_text().replace('final-repair/fixtures','warning-repair/fixtures').replace('final-repair-v2-','warning-repair-').replace("R/'final-repair'","R/'warning-repair'").replace("arm+'-v2-'","arm+'-'")
(D/'run_arm.py').write_text(s)
(D/'PROTOCOL.md').write_text('Warning-only repair. Freeze this protocol, source hashes and expectations before original trials. Original core, W/X/Y/Z and unchanged 221-statement full RFP run first; commit baseline before validator change. Candidate six model knowledge files remain unchanged. Then run rebuild in identical order using unchanged runners, gpt-6-astra medium, fresh sessions, no tools, no retries or output edits. X/Y/Z are known red-team regressions; W is a new combination, not independent real-world holdout. Both arms use native and common strict checks. Structural fidelity and semantic routing are separate. Freeze control definitions before implementation. Preserve every failure and all old files/deliveries. No publication.\n')
# Frozen evaluator control definitions: actual red-team cases plus paraphrases and context boundaries.
cases=[]
for name in ['baptism','baby-shower','graduation-control','compulsory-have-to','mandatory-must-control','clinical-control','mixed-offer-deadline','exact-unseen-anchors','narrow-nbsp-normalized','superscript-normalized','zero-padding-normalized','zero-width-deleted','literal-backticks-deleted','roman-lookalike-swapped','altered-zero-width-quotation','straight-delimiters']:
 old=R/'red-team-release/controls'/name
 result=next(x for x in json.loads((R/'red-team-release/control-results.json').read_text()) if x['case']==name)
 cases.append({'name':name,'source':(old/'source-packet.md').read_text(encoding='utf-8'),'card':(old/'card.md').read_text(encoding='utf-8'),'valid':result['expected_valid'],'warning':result['expected_date_warning'],'sid':'S002' if name in ['compulsory-have-to','mandatory-must-control','clinical-control'] else 'S001'})
for name,bodies,want,sid in [
 ('has-to-context',['Each company has to attend the following events:','Our farewell dinner is December 6, 2026 at 7 PM.'],True,'S002'),
 ('need-to-context',['All companies need to attend the following events:','Our farewell dinner is December 6, 2026 at 7 PM.'],True,'S002'),
 ('obliged-context',['All firms are obliged to attend the following events:','Our baby shower is December 6, 2026 at 7 PM.'],True,'S002'),
 ('offer-without-have-to',['Our baby shower is December 6, 2026 at 7 PM; deliver offers by December 7, 2026 at 2 PM.'],True,'S001'),
 ('clinical-baptism',['Our patient baptism ceremony is December 6, 2026 at 7 PM.'],True,'S001'),
 ('mandatory-shower',['Our baby shower attendance is mandatory on December 6, 2026 at 7 PM.'],True,'S001'),
 ('ambiguous-meeting',['Our meeting is December 6, 2026 at 7 PM.'],True,'S001'),
 ('explicit-reset',['Companies have to attend the following events:','Private correspondence:','My baby shower is December 6, 2026 at 7 PM.'],False,'S003'),
 ('unknown-no-reset',['Companies have to attend the following events:','Unrelated note','My baby shower is December 6, 2026 at 7 PM.'],True,'S003'),
 ('private-baptism',['My daughter’s baptism is December 6, 2026 at 7 PM.'],False,'S001'),
 ('private-shower',['Our baby shower is December 6, 2026 at 7 PM.'],False,'S001')]:
 source=''.join(f'S{i:03} | Document p. {i} | {b}\n' for i,b in enumerate(bodies,1))
 # Use trusted all-12 card shape from red-team template; no model-generated evidence.
 import importlib.util
 spec=importlib.util.spec_from_file_location('v',R/'rebuild/tools/validate_packet.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
 lines=[v.TITLE]
 for n,heading in enumerate(v.HEADINGS,1):lines.append(heading);lines.extend([f'- “{b}” [source: source-packet.md:S{i:03}; Document p. {i}]' for i,b in enumerate(bodies,1)] if n==12 else ['- not in source'])
 cases.append({'name':name,'source':source,'card':'\n'.join(lines)+'\n','valid':True,'warning':want,'sid':sid})
(D/'control-definitions.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2),encoding='utf-8')
print(len(tracked),len(artifacts),len(cases))

