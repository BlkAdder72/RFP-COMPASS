from pathlib import Path
import hashlib,json,subprocess,shutil,importlib.util
R=Path.cwd();D=R/'boundary-repair';D.mkdir(exist_ok=False)
def put(p,t):p.parent.mkdir(parents=True,exist_ok=True);p.open('x',encoding='utf-8',newline='\n').write(t)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
mutable=['rebuild/tools/validate_packet.py','tools/verify_submission.py','README.md','results.md','SUBMISSION_COMMENT.md','packaging/COMPLIANCE.md','rebuild/README.md']
files=[n for n in subprocess.check_output(['git','ls-files','-z']).decode().split('\0') if n]
for n in mutable:p=D/'before'/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(R/n,p)
art={str(p.relative_to(R)).replace('\\','/'):sha(p) for f in ['','final-repair','final-repair-verified','release','warning-release','warning-release-verified','scope-release','scope-guard-release','polarity-release'] for p in (R/'dist'/f).glob('*') if p.is_file()}
put(D/'preservation.json',json.dumps({'commit':subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),'tracked':{n:sha(R/n) for n in files},'mutable':mutable,'artifacts':art},indent=2))
shutil.copytree(R/'red-team-polarity/fixtures',D/'fixtures');ex=json.loads((R/'red-team-polarity/expectations.json').read_text())
rows=['Private calendar (unrelated personal correspondence):','Participation does not actually depend on attendance at our family reunion.','My graduation ceremony and birthday dinner are October 1, 2027 at 7 PM.','My birthday dinner is October 2, 2027 at 7 PM and my share is twenty-five dollars.','Companies must attend all events, including the subsection titled Private events:','The subsection titled Private events is not included in our daytime schedule and remains compulsory for all companies.','Private events:','Our farewell dinner is October 3, 2027 at 7 PM.','My birthday dinner is October 4, 2027 at 7 PM, with the official entry certificate to arrive at the office by October 5, 2027 at 2 PM.']
p=D/'fixtures/D-boundary-guards.md';put(p,''.join(f'S{i:03} | Packet paragraph {i} | {b}\n' for i,b in enumerate(rows,1)));ex[p.stem]={'source_sha256':sha(p),'required':{'S008':[6],'S009':[6]},'forbidden':{'S008':[12],'S009':[12]},'exclusive':{f'S{i:03}':[12] for i in [1,2,3,4]}};put(D/'expectations.json',json.dumps(ex,indent=2));shutil.copyfile(R/'polarity-repair/full-expectations.json',D/'full-expectations.json')
cs=[]
for folder,file,prefix in [('polarity-repair','control-definitions-release.json','prior-'),('red-team-polarity','control-definitions.json','red-')]:
 for c in json.loads((R/folder/file).read_text(encoding='utf-8')):c['name']=prefix+c['name'];cs.append(c)
s=importlib.util.spec_from_file_location('v',R/'rebuild/tools/validate_packet.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
def card(bs):
 ls=[v.TITLE]
 for n,h in enumerate(v.HEADINGS,1):ls.append(h);ls.extend([f'- “{b}” [source: source-packet.md:S{i:03}; Document p. {i}]' for i,b in enumerate(bs,1)] if n==12 else ['- not in source'])
 return '\n'.join(ls)+'\n'
date='Our farewell dinner is October 6, 2027 at 7 PM.'
extras=[
 ('straight-contraction',['Private correspondence:',"Participation doesn't depend on attendance at our family reunion.",'My birthday dinner is October 1, 2027 at 7 PM.'],False,'S003'),
 ('adverb-negation',rows[:3],False,'S003'),
 ('not-subject-qualifier',['Participation, not payment, depends on attendance at these events.',date],True,'S002'),
 ('optional-must-not-clear',['Companies must attend these events:','Attendance at these events is optional.',date],True,'S003'),
 ('negative-must-not-clear',['Companies must attend these events:',"Participation doesn’t depend on attendance at our family reunion.",date],True,'S003'),
 ('optional-with-independent-duty',['Private correspondence:','Attendance at these events is optional; companies must attend the dinner.',date],True,'S003'),
 ('relative-positive',['Companies must attend all events, including the subsection titled Private events, which is not excluded from these activities.','Private events:',date],True,'S003'),
 ('relative-exclusion-quoted',['Companies must attend all events; the subsection titled “Private correspondence”, which is excluded from these activities, contains private notes.','Private correspondence:','My birthday dinner is October 1, 2027 at 7 PM.'],False,'S003'),
 ('part-of-real-exclusion',['Companies must attend all events; the subsection titled Private correspondence is not part of these activities.','Private correspondence:','My birthday dinner is October 1, 2027 at 7 PM.'],False,'S003'),
 ('included-real-exclusion',['Companies must attend all events; the subsection titled Private correspondence is not included in these activities.','Private correspondence:','My birthday dinner is October 1, 2027 at 7 PM.'],False,'S003'),
 ('worded-share-hyphen',[rows[3]],False,'S001'),
 ('worded-share-unknown-action',['My birthday dinner is October 1, 2027 at 7 PM and my share is twenty dollars to fund the official participation credential.'],True,'S001'),
 ('coordinated-reversed',['My birthday dinner and graduation ceremony are October 1, 2027 at 7 PM.'],False,'S001'),
 ('coordinated-unknown-action',['My graduation ceremony and delivery of the sealed participation credential are October 1, 2027 at 7 PM.'],True,'S001'),
 ('parenthetical-clinical',['Private calendar (clinical visits for patients):',date],True,'S002'),
 ('parenthetical-included',['Companies must attend all events, including the subsection titled Private calendar:','Private calendar (unrelated personal correspondence):',date],True,'S003'),
 ('mixed-with-entry-certificate',[rows[-1]],True,'S001'),
 ('mixed-with-private-event',['My birthday dinner is October 1, 2027 at 7 PM with my graduation ceremony on October 2, 2027 at 2 PM.'],False,'S001'),
]
for n,bs,w,sid in extras:cs.append({'name':n,'source':''.join(f'S{i:03} | Document p. {i} | {b}\n' for i,b in enumerate(bs,1)),'card':card(bs),'valid':True,'warning':w,'sid':sid})
put(D/'control-definitions.json',json.dumps(cs,ensure_ascii=False,indent=2))
for n in ['run_arm.py','controls.py','score_core.py','score_core_strict.py','score_full.py','score_models.py','package.py','verify_delivery.py','preserve_prior.py']:
 put(D/n,(R/'polarity-repair'/n).read_text().replace('polarity-repair','boundary-repair').replace('polarity-release','boundary-release'))
put(D/'replay_controls.py',(R/'polarity-repair/replay_controls_release.py').read_text().replace('polarity-repair','boundary-repair'))
put(D/'submission-plan.json',(R/'polarity-repair/submission-plan.json').read_text(encoding='utf-8'))
put(D/'PROTOCOL.md','''# Frozen boundary repair protocol — 2026-10-25
Preserve every prior tracked file and all 47 sealed artifacts; snapshot seven mutable documents. Keep frozen root questions unchanged. Freeze 162 controls (120 prior, 24 new red-team, 18 safety/variation guards), source-bound expectations, supplemental A-D and unchanged full-RFP matrix before execution. Run original core A-E, supplemental A-D and full 221-statement RFP first and commit all raw baseline before candidate mutation. Commit candidate before rebuilt model calls. Use unchanged canonical runners, gpt-6-astra medium, the same ordered sources and six unchanged knowledge files; fresh sessions and exact full-RFP continues. No tools, retries, best-of selection, raw corrections or evaluator answers in model inputs. Repair seven warning finding families: scope-object exclusions, mixed credential deadlines, optional/no-condition event scope, coordinated private activities/shares, contracted negation, relative exclusions and parenthetical headings. Never clear an inherited duty merely because a later statement negates attendance; independent positive duties/clinical cues retain vetoes. Keep def difference onward byte-identical. Preserve intermediate failures and report every actual tie/regression. Targeted synthetic coverage is finite and does not prove perfect natural-language classification. Repackage only after fair checks and honest report; do not publish.
''')
print(len(files),len(art),len(cs))
