from pathlib import Path
import hashlib,json,subprocess,importlib.util,sys
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[1];D=Path(__file__).resolve().parent
def put(p,t):
 p.parent.mkdir(parents=True,exist_ok=True);p.open('x',encoding='utf-8',newline='\n').write(t)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files=[n for n in subprocess.check_output(['git','ls-files','-z'],cwd=R).decode().split('\0') if n]
folders=['','final-repair','final-repair-verified','release','warning-release','warning-release-verified','scope-release','scope-guard-release','polarity-release','final-submission-release']
art={str(p.relative_to(R)).replace('\\','/'):sha(p) for f in folders for p in (R/'dist'/f).glob('*') if p.is_file()}
put(D/'preservation.json',json.dumps({'target':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),'files':{n:sha(R/n) for n in files},'artifacts':art},indent=2))
put(D/'reference/pre-repair-validator.py',subprocess.check_output(['git','show','21dd85b:rebuild/tools/validate_packet.py'],cwd=R).decode('utf-8'))
spec=importlib.util.spec_from_file_location('v',R/'rebuild/tools/validate_packet.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
cases=[
 ('hundred-dollar-private-share',['My birthday dinner is November 1, 2027 at 7 PM and my share is one hundred dollars.'],False,'S001'),
 ('hundred-and-five-private-share',['My birthday dinner is November 2, 2027 at 7 PM and my share is one hundred and five dollars.'],False,'S001'),
 ('numeric-private-share-guard',['My birthday dinner is November 3, 2027 at 7 PM and my share is $105.'],False,'S001'),
 ('hinges-on-attendance',['Participation hinges on attendance at our family reunion.','Our family reunion is November 4, 2027 at 7 PM.'],True,'S002'),
 ('dependent-on-attendance',['Entry is dependent on attendance at our family reunion.','Our family reunion is November 5, 2027 at 7 PM.'],True,'S002'),
 ('depends-on-guard',['Participation depends on attendance at our family reunion.','Our family reunion is November 6, 2027 at 7 PM.'],True,'S002'),
 ('prefix-wrong-program-exclusion',['Companies must attend all events, including the subsection titled Private events:','The office-hours program does not include the subsection titled Private events.','Private events:','Our farewell dinner is November 7, 2027 at 7 PM.'],True,'S004'),
 ('prefix-real-exclusion-guard',['Companies must attend all events, excluding the subsection titled Private events:','Private events:','Our farewell dinner is November 8, 2027 at 7 PM.'],False,'S003'),
 ('outside-procurement-private-heading',['Personal correspondence (outside procurement):','My birthday dinner is November 9, 2027 at 7 PM.'],False,'S002'),
 ('supported-private-heading-guard',['Personal correspondence:','My birthday dinner is November 10, 2027 at 7 PM.'],False,'S002'),
 ('negative-hinges-private',['Personal correspondence:','Participation does not hinge on attendance at our family reunion.','My birthday dinner is November 11, 2027 at 7 PM.'],False,'S003'),
 ('mixed-return-deadline-guard',['My birthday dinner is November 12, 2027 at 7 PM and applicants must return the participation certificate by November 13, 2027 at 2 PM.'],True,'S001'),
]
def source(rows):return ''.join(f'S{i:03} | {a} | {b}\n' for i,(a,b) in enumerate(rows,1))
def card(rows):
 ls=[v.TITLE]
 for n,h in enumerate(v.HEADINGS,1):
  ls.append(h);ls.extend([f'- “{b}” [source: source-packet.md:S{i:03}; {a}]' for i,(a,b) in enumerate(rows,1)] if n==12 else ['- not in source'])
 return '\n'.join(ls)+'\n'
cs=[]
for name,bs,w,sid in cases:
 rows=[(f'Document paragraph {i}',b) for i,b in enumerate(bs,1)];cs.append({'name':name,'source':source(rows),'card':card(rows),'valid':True,'warning':w,'sid':sid})
anchors=['Appendix p.\ufeff12','Appendix p.\u200f12','Appendix p.12 cafe\u0301','Appendix p.12 &apos;A&apos;','Appendix\tpage 12']
rs=[(a,'Applicants must include a signed declaration.') for a in anchors];src=source(rs);c=card(rs)
cs.append({'name':'exact-unseen-anchors','source':src,'card':c,'valid':True,'warning':None,'sid':'S001'})
for name,a,b in [('bom-deleted','\ufeff',''),('rtl-mark-deleted','\u200f',''),('combining-normalized','e\u0301','é'),('apostrophe-entity-decoded','&apos;',"'"),('tab-normalized','\t',' ')]:cs.append({'name':name,'source':src,'card':c.replace(a,b),'valid':False,'warning':None,'sid':'S001'})
put(D/'control-definitions.json',json.dumps(cs,ensure_ascii=False,indent=2))
fixtures={
 'A-obligation-and-retrospective-scope':[(f'Instructions paragraph {i}',b) for i,b in enumerate(['Participation hinges on attendance at our family reunion.','Our family reunion is November 14, 2027 at 7 PM.','Personal correspondence:','My birthday dinner is November 15, 2027 at 7 PM.','For this solicitation, applicants must attend the birthday dinner identified in the immediately preceding statement; attendance is an eligibility condition.','It is expected that the contract shall be a three-year fixed-price contract.'],1)],
 'B-personal-boundaries':[(f'Packet paragraph {i}',b) for i,b in enumerate(['Personal correspondence (outside procurement):','My birthday dinner is November 16, 2027 at 7 PM and my share is one hundred dollars.','Participation does not hinge on attendance at our family reunion.','My birthday dinner is November 17, 2027 at 7 PM.','End of personal correspondence.','Applicants must return the signed certificate by November 18, 2027 at 2 PM.'],1)],
 'C-opaque-citations':rs}
expect={}
for name,rows in fixtures.items():
 p=D/'fixtures'/(name+'.md');put(p,source(rows));expect[name]={'source_sha256':sha(p),'required':{},'forbidden':{},'exclusive':{}}
expect['A-obligation-and-retrospective-scope']['required']={'S002':[6],'S004':[6],'S005':[3],'S006':[11]};expect['A-obligation-and-retrospective-scope']['forbidden']={'S002':[12],'S004':[12]}
expect['B-personal-boundaries']['exclusive']={f'S{i:03}':[12] for i in range(1,5)};expect['B-personal-boundaries']['required']={'S006':[4,6]}
expect['C-opaque-citations']['required']={f'S{i:03}':[4,5] for i in range(1,6)}
put(D/'expectations.json',json.dumps(expect,indent=2))
put(D/'controls.py',(R/'red-team-polarity/controls.py').read_text().replace('pre-polarity','pre-repair'))
put(D/'score_models.py',(R/'red-team-polarity/score_models.py').read_text())
put(D/'PROTOCOL.md','''# Frozen review protocol, 2026-10-26
Target sealed 8e2afd4; reread packaging/competition-spec.txt and verbatim feedback.md before designing cases. Feedback priorities: unrelated personal material only12 without false date warnings; contractual expected wording consistently11; script-built example provenance; raw noisy evidence. No repairs, repackaging or publication. Preserve all tracked bytes and 53 sealed artifacts.
Freeze the 18 evaluator controls and three source-hash-bound selected model matrices before execution. All12 official cards deliberately miss dates and should warn; private cards are correct and should not warn. Compare original, pre-warning-repair21dd85b and current validators. Original model arm once for A/B/C, commit complete baseline, then current arm once with unchanged canonical runner/provider/model/settings/order; no retries, corrections or best-of. Semantic matrix, literal copying and warning accuracy are separate. Retrospective incorporation is explicit source evidence, not inferred context. These targeted synthetic cases are not a population holdout. Recheck the previous full-RFP evidence read-only rather than claiming a fresh full-length trial. Hash-check sealed delivery and previous evidence. Retain failures and distinguish longstanding gaps from regressions against21dd85b. New review is outside the unchanged sealed release.
''')
print(json.dumps({'prior_files':len(files),'sealed_artifacts':len(art),'controls':len(cs)}))
