from pathlib import Path
import hashlib,json,subprocess,shutil,importlib.util
R=Path.cwd();D=R/'scope-guard-repair';D.mkdir(exist_ok=False)
def put(p,t):p.parent.mkdir(parents=True,exist_ok=True);p.open('x',encoding='utf-8',newline='\n').write(t)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
mutable=['rebuild/tools/validate_packet.py','tools/verify_submission.py','README.md','results.md','SUBMISSION_COMMENT.md','packaging/COMPLIANCE.md','rebuild/README.md']
files=[n for n in subprocess.check_output(['git','ls-files','-z']).decode().split('\0') if n]
for n in mutable:p=D/'before'/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(R/n,p)
art={str(p.relative_to(R)).replace('\\','/'):sha(p) for f in ['','final-repair','final-repair-verified','release','warning-release','warning-release-verified','scope-release'] for p in (R/'dist'/f).glob('*') if p.is_file()}
put(D/'preservation.json',json.dumps({'commit':subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),'tracked':{n:sha(R/n) for n in files},'mutable':mutable,'artifacts':art},indent=2))
shutil.copytree(R/'red-team-scope/fixtures',D/'fixtures');ex=json.loads((R/'red-team-scope/expectations.json').read_text())
rows=[('Official rules','Admission to these activities is contingent on attendance.'),('Official rules','Our farewell dinner is April 1, 2027 at 7 PM.'),('Unrelated private correspondence','My personal family calendar:'),('Unrelated private correspondence','My graduation ceremony is April 2, 2027 at 2 PM.'),('Official payment instructions','I have to attend my daughter’s birthday dinner on April 3, 2027 at 7 PM, then remit the official participation deposit by April 4, 2027 at 2 PM.'),('Unrelated private correspondence','Private correspondence:'),('Unrelated private correspondence','Our family dinner is April 5, 2027 at 7 PM; my graduation ceremony is April 6, 2027 at 2 PM.')]
p=D/'fixtures/D-additional-boundaries.md';put(p,''.join(f'S{i:03} | {a} | {b}\n' for i,(a,b) in enumerate(rows,1)));ex[p.stem]={'source_sha256':sha(p),'required':{'S002':[6],'S005':[6]},'forbidden':{'S002':[12],'S005':[12]},'exclusive':{'S003':[12],'S004':[12],'S006':[12],'S007':[12]}}
put(D/'expectations.json',json.dumps(ex,indent=2));shutil.copyfile(R/'scope-repair/full-expectations.json',D/'full-expectations.json')
cs=[]
for folder,file,prefix in [('scope-repair','control-definitions-release.json','prior-'),('red-team-scope','control-definitions.json','red-')]:
 for c in json.loads((R/folder/file).read_text(encoding='utf-8')):c['name']=prefix+c['name'];cs.append(c)
s=importlib.util.spec_from_file_location('v',R/'rebuild/tools/validate_packet.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
def card(bs):
 ls=[v.TITLE]
 for n,h in enumerate(v.HEADINGS,1):ls.append(h);ls.extend([f'- “{b}” [source: source-packet.md:S{i:03}; Document p. {i}]' for i,b in enumerate(bs,1)] if n==12 else ['- not in source'])
 return '\n'.join(ls)+'\n'
extras=[('conditional-admission',[rows[0][1],rows[1][1]],True,'S002'),('possessive-compound-private',[rows[2][1],rows[3][1]],False,'S002'),('two-personal-clauses',[rows[6][1]],False,'S001'),('unknown-second-clause',['Our farewell dinner is April 1, 2027 at 7 PM; collect the sealed attendance credential by April 2, 2027 at 2 PM.'],True,'S001'),('alternate-explicit-nested-label',['Companies must attend every activity, including the subsection titled Family activities:','Family activities:','Our farewell dinner is April 1, 2027 at 7 PM.'],True,'S003'),('unrelated-private-reset',['Companies must attend these events:','My family events:','My graduation ceremony is April 1, 2027 at 7 PM.'],False,'S003'),('clinical-private-heading',['Private events for patients:','Our farewell dinner is April 1, 2027 at 7 PM.'],True,'S002'),('private-year-comma',['I have to attend my daughter’s birthday dinner on April 1, 2027 at 7 PM.'],False,'S001')]
for n,bs,w,sid in extras:cs.append({'name':n,'source':''.join(f'S{i:03} | Document p. {i} | {b}\n' for i,b in enumerate(bs,1)),'card':card(bs),'valid':True,'warning':w,'sid':sid})
put(D/'control-definitions.json',json.dumps(cs,ensure_ascii=False,indent=2))
for n in ['run_arm.py','controls.py','score_core.py','score_core_strict.py','score_full.py','score_models.py','replay_controls.py']:
 put(D/n,(R/'scope-repair'/n).read_text().replace('scope-repair','scope-guard-repair'))
put(D/'PROTOCOL.md','''# Scope-guard repair frozen protocol - 2026-10-24
Preserve all prior tracked evidence, failed controls, snapshots, frozen questions and 35 sealed artifacts. Root mutable files snapshotted separately. Freeze original red-team A/B/C plus new D, source-bound selected expectations, unchanged full-RFP matrix and 82 controls before any run or code repair. Run original core A-E, supplemental A-D and full 221-statement RFP first with unchanged canonical runners; commit complete raw baseline before candidate mutation. Commit repaired candidate before rebuilt calls. Same ordered sources, gpt-6-astra medium, same six knowledge files, fresh sessions and exact full-RFP continuation; no tools, retries, corrections or best-of selection. Warning-only repair; def difference onward must stay byte-identical. A private nested heading explicitly referenced by inherited obligations must not reset; unrelated personal variants must reset; multi-clause personal evidence must not swallow unknown/official clauses; obligation dependency wording must preserve context. New eight safety controls cover private reset versus nested scope, conditional admission, mixed unknown clauses, two private clauses and clinical vetoes. Preserve all intermediate failures. Report ties/regressions and limits; model knowledge unchanged, so routing differences are fresh-run variability, not a prompt repair. Update report, package and three-sentence submission draft without publishing.
''');print(len(files),len(art),len(cs))
