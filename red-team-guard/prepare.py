from pathlib import Path
import hashlib,json,subprocess,importlib.util
R=Path.cwd();D=R/'red-team-guard';D.mkdir(exist_ok=False)
def put(p,t):p.parent.mkdir(parents=True,exist_ok=True);p.open('x',encoding='utf-8',newline='\n').write(t)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files=[n for n in subprocess.check_output(['git','ls-files','-z']).decode().split('\0') if n]
art={str(p.relative_to(R)).replace('\\','/'):sha(p) for f in ['','final-repair','final-repair-verified','release','warning-release','warning-release-verified','scope-release','scope-guard-release'] for p in (R/'dist'/f).glob('*') if p.is_file()}
put(D/'preservation.json',json.dumps({'target':subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),'files':{n:sha(R/n) for n in files},'artifacts':art},indent=2))
put(D/'reference/pre-guard-validator.py',subprocess.check_output(['git','show','3159bc2a93e7de52580c5445c15e7ac24d31eddd:rebuild/tools/validate_packet.py']).decode('utf-8'))
a=[('Official participation instructions','Attendance at these activities is a prerequisite for entry.'),('Official participation instructions','Our farewell dinner is August 1, 2027 at 7 PM.'),('Official payment instructions','Our family reunion is August 2, 2027 at 7 PM and remit the official participation deposit by August 3, 2027 at 2 PM.'),('Official participation instructions','Only those who attend these events may take part.'),('Official participation instructions','Our baby shower is August 4, 2027 at 3 PM.')]
b=[('Unrelated personal correspondence','Private correspondence:'),('Unrelated personal correspondence','Participation does not depend on attendance at our family reunion.'),('Unrelated personal correspondence','My birthday dinner is August 5, 2027 at 7 PM.'),('Official participation instructions','All companies must attend the following events; the subsection titled Private correspondence is unrelated and excluded from these activities.'),('Unrelated personal correspondence','Private correspondence:'),('Unrelated personal correspondence','My graduation ceremony is August 6, 2027 at 2 PM.'),('Unrelated personal correspondence','Private calendar — unrelated personal correspondence:'),('Unrelated personal correspondence','My child’s christening ceremony is August 7, 2027 at 11 AM.'),('Official response instructions','Proposals must arrive by August 8, 2027 at 2 PM.')]
anchors=['Annex A p.12 item A\ufe0f','Annex A p.1\u034f2','Annex A p.\u202f12','Annex A p.12 &quot;A&quot;','Annex A p.12 non\u00adpublic','Annex Ａ p.12 [source: note]']
data={'A-unseen-obligations-and-mixed-conjunction':a,'B-negated-scope-and-private-headings':b,'C-new-citation-variants':[(a,'Applicants must include a signed conflict disclosure.') for a in anchors]};ex={}
for n,rs in data.items():
 p=D/'fixtures'/(n+'.md');put(p,''.join(f'S{i:03} | {a} | {b}\n' for i,(a,b) in enumerate(rs,1)));ex[n]={'source_sha256':sha(p),'required':{},'forbidden':{},'exclusive':{}}
ex['A-unseen-obligations-and-mixed-conjunction']['required']={s:[6] for s in ['S002','S003','S005']};ex['A-unseen-obligations-and-mixed-conjunction']['forbidden']={s:[12] for s in ['S002','S003','S005']}
ex['B-negated-scope-and-private-headings']['exclusive']={f'S{i:03}':[12] for i in [1,2,3,5,6,7,8]};ex['B-negated-scope-and-private-headings']['required']={'S004':[4],'S009':[6]}
ex['C-new-citation-variants']['required']={f'S{i:03}':[4,5] for i in range(1,7)};put(D/'expectations.json',json.dumps(ex,indent=2))
s=importlib.util.spec_from_file_location('v',R/'rebuild/tools/validate_packet.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
def card(rows):
 ls=[v.TITLE]
 for n,h in enumerate(v.HEADINGS,1):ls.append(h);ls.extend([f'- “{body}” [source: source-packet.md:S{i:03}; {anchor}]' for i,(anchor,body) in enumerate(rows,1)] if n==12 else ['- not in source'])
 return '\n'.join(ls)+'\n'
cs=[]
def add(n,bs,w,sid):
 rs=[(f'Document p. {i}',body) for i,body in enumerate(bs,1)];cs.append({'name':n,'source':''.join(f'S{i:03} | {a} | {b}\n' for i,(a,b) in enumerate(rs,1)),'card':card(rs),'valid':True,'warning':w,'sid':sid})
add('reverse-prerequisite',[a[0][1],a[1][1]],True,'S002')
add('only-attendees-may-participate',[a[3][1],a[4][1]],True,'S002')
add('mixed-and-without-comma',[a[2][1]],True,'S001')
add('negated-dependency-pollutes-private',[x[1] for x in b[:3]],False,'S003')
add('explicitly-excluded-private-reference',[x[1] for x in b[3:6]],False,'S003')
add('annotated-private-heading',[x[1] for x in b[6:8]],False,'S002')
add('positive-dependency-guard',['Participation depends on attendance at these events.','Our farewell dinner is August 1, 2027 at 7 PM.'],True,'S002')
add('positive-nested-reference-guard',['Companies must attend all events, including the subsection titled Private correspondence:','Private correspondence:','Our farewell dinner is August 1, 2027 at 7 PM.'],True,'S003')
add('genuine-private-reset',['Companies must attend these events:','My private family calendar:','My graduation ceremony is August 6, 2027 at 2 PM.'],False,'S003')
add('private-share-control',['My birthday dinner is August 5, 2027 at 7 PM; my share is $20.'],False,'S001')
rs=data['C-new-citation-variants'];src=''.join(f'S{i:03} | {a} | {b}\n' for i,(a,b) in enumerate(rs,1));c=card(rs);cs.append({'name':'exact-new-anchors','source':src,'card':c,'valid':True,'warning':None,'sid':'S001'})
for n,x,y in [('variation-selector-deleted','\ufe0f',''),('grapheme-joiner-deleted','\u034f',''),('narrow-space-normalized','\u202f',' '),('quote-entity-decoded','&quot;','"'),('soft-hyphen-deleted','\u00ad',''),('fullwidth-letter-normalized','Ａ','A')]:cs.append({'name':n,'source':src,'card':c.replace(x,y),'valid':False,'warning':None,'sid':'S001'})
put(D/'control-definitions.json',json.dumps(cs,ensure_ascii=False,indent=2))
for n in ['controls.py','score_models.py','audit_models.py','verify_preservation.py','recheck_full.py','audit_delivery.py']:
 t=(R/'red-team-scope'/n).read_text();t=t.replace('pre-scope','pre-guard').replace('09684fc7129b8ff4bcbefe4b749f644f8f23f50e','3159bc2a93e7de52580c5445c15e7ac24d31eddd')
 if n=='audit_delivery.py':t=t.replace('red-team-scope-clone','red-team-guard-clone').replace('scope-release','scope-guard-release').replace('3159bc2a93e7de52580c5445c15e7ac24d31eddd','06e6a1384c94bd0c1298f0d50cfbe09ce3fc1bcf')
 if n=='audit_models.py':t=t.replace('B-personal-heading-variants','B-negated-scope-and-private-headings')
 if n=='recheck_full.py':t=t.replace('scope-repair','scope-guard-repair')
 put(D/n,t)
put(D/'PROTOCOL.md','''# Frozen repaired-package red team - 2026-10-24
Review sealed target 06e6a1384c94bd0c1298f0d50cfbe09ce3fc1bcf without modifying candidate, frozen questions, prior evidence or deliveries. Preserve all tracked bytes and 41 sealed files. Freeze cases, source-hash-bound selected routing expectations and controls before execution. Run original A/B/C once, commit complete baseline, then rebuild A/B/C once with unchanged canonical tools/run_arm.py, gpt-6-astra medium, fresh sessions, no tools, retries, corrections or best-of selection. No expected answers supplied to models. Separate exact copying, selected semantic placement and warning accuracy. Compare evaluator cards under original, preceding rebuild 3159bc2 and current rebuild; the middle version is not a third model arm. All-12 official cards deliberately omit operational dates; all-12 personal cards are correct. Cases include reverse/implicit obligation wording, mixed conjunction without punctuation, negated dependency, explicit exclusion of a private referenced subsection, annotated private heading, six grammar-valid opaque citation variants and altered-anchor rejection guards. These targeted synthetic cases are informed by previous findings, not an independent real-world holdout. Recheck current existing full-RFP evidence read-only, without new full-length model calls. Audit sealed ZIP and complete-history bundle in a new clone. Retain failures; do not repair or publish.
''');print(len(files),len(art),len(cs))
