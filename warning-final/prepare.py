from pathlib import Path
import json,hashlib,subprocess,shutil,importlib.util,sys
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[1];D=Path(__file__).resolve().parent
def put(p,t):p.parent.mkdir(parents=True,exist_ok=True);p.open('x',encoding='utf-8',newline='\n').write(t)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
mutable=['README.md','results.md','SUBMISSION_COMMENT.md','rebuild/README.md','rebuild/tools/validate_packet.py','tools/verify_submission.py','packaging/COMPLIANCE.md']
files=[n for n in subprocess.check_output(['git','ls-files','-z']).decode().split('\0') if n]
folders=['','final-repair','final-repair-verified','release','warning-release','warning-release-verified','scope-release','scope-guard-release','polarity-release','final-submission-release']
art={str(p.relative_to(R)).replace('\\','/'):sha(p) for f in folders for p in (R/'dist'/f).glob('*') if p.is_file()}
put(D/'preservation.json',json.dumps({'commit':subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),'tracked':{n:sha(R/n) for n in files},'mutable':mutable,'artifacts':art},indent=2))
for n in mutable:
 p=D/'before'/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(R/n,p)
cs=json.loads((R/'final-submission/control-definitions.json').read_text())
for c in cs:c['issue']='prior'
fresh=json.loads((R/'red-team-oct26/control-definitions.json').read_text())
families={'hinges-on-attendance':'F1','dependent-on-attendance':'F1','prefix-wrong-program-exclusion':'F2','hundred-dollar-private-share':'F3','hundred-and-five-private-share':'F3','outside-procurement-private-heading':'F4'}
for c in fresh:c['issue']=families.get(c['name'],'guard');c['name']='oct26-'+c['name'];cs.append(c)
spec=importlib.util.spec_from_file_location('v',R/'rebuild/tools/validate_packet.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
def add(name,bs,w,sid,issue):
 rows=[(f'Paragraph {i}',b) for i,b in enumerate(bs,1)];src=''.join(f'S{i:03} | {a} | {b}\n' for i,(a,b) in enumerate(rows,1));ls=[v.TITLE]
 for n,h in enumerate(v.HEADINGS,1):ls.append(h);ls.extend([f'- “{b}” [source: source-packet.md:S{i:03}; {a}]' for i,(a,b) in enumerate(rows,1)] if n==12 else ['- not in source'])
 cs.append({'name':name,'source':src,'card':'\n'.join(ls)+'\n','valid':True,'warning':w,'sid':sid,'issue':issue})
for predicate in ['does not hinge on','doesn’t hinge on','is not dependent on','is no longer dependent on']:
 add('negative-dependency-'+str(len(cs)),['Personal correspondence:',f'Participation {predicate} attendance at our family reunion.','My birthday dinner is November 20, 2027 at 7 PM.'],False,'S003','F1')
for subject in ['Participation, not payment, hinges on','Participation not only hinges on','Entry is dependent on']:
 add('positive-dependency-'+str(len(cs)),[subject+' attendance at our family reunion.','Our family reunion is November 21, 2027 at 7 PM.'],True,'S002','F1')
add('private-positive-self-attendance',['Personal correspondence:','My participation hinges on attendance at my birthday dinner.','My birthday dinner is November 22, 2027 at 7 PM.'],True,'S003','F1')
# Conservative affirmative conditions retain hints even in a private block. Negative relations do not.
for subject,warning in [('These mandatory activities',False),('The office-hours program',True),('Our daytime schedule',True)]:
 add('scope-subject-'+str(len(cs)),['Companies must attend all events, including the subsection titled Private events:',subject+' does not include the subsection titled Private events.','Private events:','Our farewell dinner is November 23, 2027 at 7 PM.'],warning,'S004','F2')
add('exclude-heading-from-wrong-program',['Companies must attend all events, including the subsection titled Private events:','We exclude the subsection titled Private events from our office-hours program.','Private events:','Our farewell dinner is November 24, 2027 at 7 PM.'],True,'S004','F2')
add('exclude-heading-from-requirements',['Companies must attend all events, including the subsection titled Private events:','We exclude the subsection titled Private events from these requirements.','Private events:','Our farewell dinner is November 24, 2027 at 7 PM.'],False,'S004','F2')
for amount in ['one hundred dollars','one hundred and five dollars','two thousand three hundred and five dollars','twenty-five dollars','zero dollars']:
 add('private-amount-'+str(len(cs)),[f'My birthday dinner is November 25, 2027 at 7 PM and my share is {amount}.'],False,'S001','F3')
for tail in ['my share is one hundred dollars and applicants must return the signed form by November 26, 2027','my share is one hundred dollars and my participation payment reaches the office by November 26, 2027','my share is one hundred dollars and a credential is to arrive by November 26, 2027']:
 add('mixed-amount-'+str(len(cs)),['My birthday dinner is November 25, 2027 at 7 PM and '+tail+'.'],True,'S001','F3')
for annotation in ['outside procurement','unrelated to the solicitation','not part of procurement']:
 add('private-annotation-'+str(len(cs)),[f'Personal correspondence ({annotation}):','My birthday dinner is November 27, 2027 at 7 PM.'],False,'S002','F4')
add('annotated-private-then-real-duty',['Personal correspondence (outside procurement):','Applicants must attend these events:','Our farewell dinner is November 28, 2027 at 7 PM.'],True,'S003','F4')
add('annotated-private-explicit-inclusion',['Applicants must attend all events, including the subsection titled Personal correspondence:','Personal correspondence (outside procurement):','Our farewell dinner is November 28, 2027 at 7 PM.'],True,'S003','F4')
add('annotated-private-clinical',['Clinical providers must attend all events, including the subsection titled Personal correspondence:','Personal correspondence (outside procurement):','Our farewell dinner is November 28, 2027 at 7 PM.'],True,'S003','F4')
put(D/'control-definitions.json',json.dumps(cs,ensure_ascii=False,indent=2))
shutil.copytree(R/'red-team-oct26/fixtures',D/'fixtures');shutil.copyfile(R/'red-team-oct26/expectations.json',D/'expectations.json');shutil.copyfile(R/'final-submission/full-expectations.json',D/'full-expectations.json')
for n in ['run_arm.py','score_core.py','score_core_strict.py','score_full.py','package.py','verify_delivery.py']:
 put(D/n,(R/'final-submission'/n).read_text().replace('final-submission','warning-final'))
# Adapt the selected new-model scorer to root run directories; definitions stay byte-identical.
t=(R/'red-team-oct26/score_models.py').read_text().replace("base=D/('run-'+arm)","base=R/('run-'+arm)/'warning-final-new'")
put(D/'score_models.py',t)
put(D/'PROTOCOL.md','''# Sequential warning repair — frozen 2026-10-26
Preserve all earlier evidence, frozen Q1–Q8, complete original Git history and all 53 sealed artifacts. Snapshot seven mutable files before repair. Freeze 180 prior controls plus new safety boundaries and the unchanged red-team A/B/C source-hash-bound expectations and full221 matrix. First run original core/new/full once with canonical gpt-6-astra medium runners; commit complete baseline before any validator edit.
Repair F1 dependency wording, test before moving to F2 relation binding, test before F3 worded shares/clause splitting, test before F4 private annotation. Retain every failed stage; do not relax frozen expectations. A stage passes when all162 older controls, common guards and that issue plus previously solved issues pass. All four must pass every frozen control at the end. Compare original, before and repaired validators. Warning analysis only; preserve the entire implementation from def difference onward byte-for-byte and all six knowledge files. After final candidate commit, run rebuilt core/new/full once under identical settings/order; do not correct model output, select best runs or silently retry. Retain and disclose automatic transport retries and failures. Score literal copying, selected routing and warning accuracy separately. Replay old controls and rejected S100 evidence. Keep every failure; a new failure blocks release acceptance. Update current report, entry navigation and three-sentence submission draft only after measurements. Produce a new release path; do not overwrite sealed packages or publish. Historical assertions execute unchanged at pinned commits, current gate evaluates new evidence.
''')
print(json.dumps({'prior_files':len(files),'sealed_artifacts':len(art),'frozen_controls':len(cs)}))
