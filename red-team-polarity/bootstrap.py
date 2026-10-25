from pathlib import Path
import hashlib,json,subprocess,importlib.util
R=Path.cwd();D=R/'red-team-polarity';D.mkdir(exist_ok=False)
def put(p,t):
 p.parent.mkdir(parents=True,exist_ok=True);p.open('x',encoding='utf-8',newline='\n').write(t)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files=[n for n in subprocess.check_output(['git','ls-files','-z']).decode().split('\0') if n]
art={str(p.relative_to(R)).replace('\\','/'):sha(p) for f in ['','final-repair','final-repair-verified','release','warning-release','warning-release-verified','scope-release','scope-guard-release','polarity-release'] for p in (R/'dist'/f).glob('*') if p.is_file()}
put(D/'preservation.json',json.dumps({'target':subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),'files':{n:sha(R/n) for n in files},'artifacts':art},indent=2))
put(D/'reference/pre-polarity-validator.py',subprocess.check_output(['git','show','06e6a1384c94bd0c1298f0d50cfbe09ce3fc1bcf:rebuild/tools/validate_packet.py']).decode('utf-8'))
cases=[
 ('contracted-negation',['Private correspondence:','Participation doesn’t depend on attendance at our family reunion.','My birthday dinner is September 1, 2027 at 7 PM.'],False,'S003'),
 ('explicit-optional-attendance',['Private correspondence:','Attendance at these events is optional.','My graduation ceremony is September 2, 2027 at 2 PM.'],False,'S003'),
 ('no-attendance-condition',['Private correspondence:','There is no attendance condition for these events.','My birthday dinner is September 3, 2027 at 7 PM.'],False,'S003'),
 ('exclusion-other-program',['Companies must attend all events, including the subsection titled Private events:','The subsection titled Private events is not part of our office-hours program and remains compulsory for all companies.','Private events:','Our farewell dinner is September 4, 2027 at 7 PM.'],True,'S004'),
 ('not-included-other-schedule',['Companies must attend all events, including the subsection titled Private events:','The subsection titled Private events is not included in our daytime schedule and remains compulsory for all companies.','Private events:','Our baby shower is September 5, 2027 at 3 PM.'],True,'S004'),
 ('relative-clause-exclusion',['All companies must attend these events; the subsection titled Private correspondence, which is excluded from these activities, is unrelated personal correspondence.','Private correspondence:','My graduation ceremony is September 6, 2027 at 2 PM.'],False,'S003'),
 ('mixed-credential-deadline',['My birthday dinner is September 7, 2027 at 7 PM, with the official participation credential to reach the office by September 8, 2027 at 2 PM.'],True,'S001'),
 ('private-worded-share',['My birthday dinner is September 9, 2027 at 7 PM and my share is twenty dollars.'],False,'S001'),
 ('joint-private-activities',['My graduation ceremony and birthday dinner are September 10, 2027 at 7 PM.'],False,'S001'),
 ('parenthetical-private-heading',['Private calendar (unrelated personal correspondence):','My child’s christening ceremony is September 11, 2027 at 11 AM.'],False,'S002'),
 ('positive-dependency-guard',['Participation depends on attendance at these events.','Our farewell dinner is September 12, 2027 at 7 PM.'],True,'S002'),
 ('not-only-positive-guard',['Participation not only depends on attendance at these events but also on a signed declaration.','Our farewell dinner is September 13, 2027 at 7 PM.'],True,'S002'),
 ('direct-exclusion-guard',['All companies must attend these events; the subsection titled Private correspondence is excluded from these activities.','Private correspondence:','My graduation ceremony is September 14, 2027 at 2 PM.'],False,'S003'),
 ('mixed-must-guard',['My birthday dinner is September 15, 2027 at 7 PM and applicants must deliver the official participation credential by September 16, 2027 at 2 PM.'],True,'S001'),
 ('clinical-guard',['Clinical providers must attend these events:','Our family dinner is September 17, 2027 at 7 PM.'],True,'S002'),
 ('private-dollar-share-guard',['My birthday dinner is September 18, 2027 at 7 PM and my share is $20.'],False,'S001'),
 ('explicit-negative-dependency-guard',['Private correspondence:','Participation does not depend on attendance at our family reunion.','My birthday dinner is September 19, 2027 at 7 PM.'],False,'S003'),
]
a=cases[3][1]+['Separate requirement group:']+cases[4][1]+['Separate requirement group:']+cases[6][1]
b=cases[0][1]+cases[1][1]+cases[5][1]+cases[7][1]+cases[8][1]+cases[9][1]
anchors=['Annex A p.\u200a12','Annex A p.\u061c12','Annex A p.\u206612\u2069','Annex A p.&#32;12','Annex A p.12 non\u2010public','Annex A p.12； item A']
data={'A-exclusions-and-mixed-deadlines':[(f'Official instructions paragraph {i}',t) for i,t in enumerate(a,1)],'B-negation-and-private-content':[(f'Packet paragraph {i}',t) for i,t in enumerate(b,1)],'C-opaque-citation-variants':[(a,'Applicants must include a signed conflict disclosure.') for a in anchors]}
ex={}
for n,rs in data.items():
 p=D/'fixtures'/(n+'.md');put(p,''.join(f'S{i:03} | {a} | {b}\n' for i,(a,b) in enumerate(rs,1)));ex[n]={'source_sha256':sha(p),'required':{},'forbidden':{},'exclusive':{}}
ex['A-exclusions-and-mixed-deadlines']['required']={s:[6] for s in ['S004','S009','S011']};ex['A-exclusions-and-mixed-deadlines']['forbidden']={s:[12] for s in ['S004','S009','S011']}
ex['B-negation-and-private-content']['exclusive']={f'S{i:03}':[12] for i in [1,2,3,4,5,6,8,9,10,11,12,13]};ex['B-negation-and-private-content']['required']={'S007':[4]}
ex['C-opaque-citation-variants']['required']={f'S{i:03}':[4,5] for i in range(1,7)};put(D/'expectations.json',json.dumps(ex,indent=2))
s=importlib.util.spec_from_file_location('v',R/'rebuild/tools/validate_packet.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
def card(rows):
 ls=[v.TITLE]
 for n,h in enumerate(v.HEADINGS,1):
  ls.append(h);ls.extend([f'- “{body}” [source: source-packet.md:S{i:03}; {anchor}]' for i,(anchor,body) in enumerate(rows,1)] if n==12 else ['- not in source'])
 return '\n'.join(ls)+'\n'
cs=[]
for n,bs,w,sid in cases:
 rs=[(f'Document p. {i}',body) for i,body in enumerate(bs,1)];cs.append({'name':n,'source':''.join(f'S{i:03} | {a} | {b}\n' for i,(a,b) in enumerate(rs,1)),'card':card(rs),'valid':True,'warning':w,'sid':sid})
rs=data['C-opaque-citation-variants'];src=''.join(f'S{i:03} | {a} | {b}\n' for i,(a,b) in enumerate(rs,1));c=card(rs);cs.append({'name':'exact-new-anchors','source':src,'card':c,'valid':True,'warning':None,'sid':'S001'})
for n,x,y in [('hair-space-normalized','\u200a',' '),('arabic-mark-deleted','\u061c',''),('directional-isolates-deleted','\u2066',''),('numeric-entity-decoded','&#32;',' '),('unicode-hyphen-normalized','\u2010','-'),('fullwidth-semicolon-normalized','；',';')]:cs.append({'name':n,'source':src,'card':c.replace(x,y),'valid':False,'warning':None,'sid':'S001'})
put(D/'control-definitions.json',json.dumps(cs,ensure_ascii=False,indent=2))
for n in ['controls.py','score_models.py','audit_models.py','verify_preservation.py','recheck_full.py','audit_delivery.py']:
 t=(R/'red-team-guard'/n).read_text().replace('pre-guard','pre-polarity')
 if n=='verify_preservation.py':t=t.replace('3159bc2a93e7de52580c5445c15e7ac24d31eddd','06e6a1384c94bd0c1298f0d50cfbe09ce3fc1bcf')
 if n=='audit_delivery.py':t=t.replace('red-team-guard-clone','red-team-polarity-clone').replace('scope-guard-release','polarity-release').replace('06e6a1384c94bd0c1298f0d50cfbe09ce3fc1bcf','21dd85b40edf835870689c9f4a0b67ddc10de81a')
 if n=='audit_models.py':t=t.replace('B-negated-scope-and-private-headings','B-negation-and-private-content')
 if n=='recheck_full.py':t=t.replace('scope-guard-repair','polarity-repair')
 put(D/n,t)
put(D/'PROTOCOL.md','''# Frozen repaired-package red team — 2026-10-25
Review sealed target 21dd85b40edf835870689c9f4a0b67ddc10de81a; do not modify candidate, questions, earlier evidence or sealed artifacts. Freeze source-hash-bound selected expectations and controls before execution. Original A/B/C once, commit complete baseline, then rebuild A/B/C once; unchanged canonical tools/run_arm.py, gpt-6-astra medium, fresh sessions, no tools, retries, corrections or best-of selection. No expected answers supplied to models. Compare model citation fidelity, selected semantic placement and personal warning accuracy separately. Evaluator controls compare original, preceding rebuild 06e6a13 and current rebuild; this middle validator is not a third model arm. All-12 official cards deliberately omit operational dates; all-12 private cards are correct. Cover contracted/optional/no-condition negation, exclusion from a different program, relative exclusions, mixed credential deadlines, worded private shares, coordinated private activities, annotated private headings, six grammar-valid opaque anchors and six alterations that must fail. Positive obligations, direct exclusion, clinical and known personal controls guard the boundaries. Cases are targeted synthetic probes informed by prior findings, not an independent population holdout. Recheck existing latest full-RFP cards read-only with no new full-length model calls. Verify archive bytes and complete-history bundle in a fresh clone. Preserve failures; report both regressions and ties. Do not repair, repack or publish.
''')
put(D/'prepare.py',Path(__file__).read_text(encoding='utf-8'))
print(len(files),len(art),len(cs))
