from pathlib import Path
import hashlib,json,subprocess,importlib.util
R=Path.cwd();D=R/'red-team-scope';D.mkdir(exist_ok=False)
def put(p,t):p.parent.mkdir(parents=True,exist_ok=True);p.open('x',encoding='utf-8',newline='\n').write(t)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files=subprocess.check_output(['git','ls-files','-z']).decode().strip('\0').split('\0')
art={str(p.relative_to(R)):sha(p) for f in ['','final-repair','final-repair-verified','release','warning-release','warning-release-verified','scope-release'] for p in (R/'dist'/f).glob('*') if p.is_file()}
put(D/'preservation.json',json.dumps({'target':subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),'files':{n:sha(R/n) for n in files},'artifacts':art},indent=2))
put(D/'reference/pre-scope-validator.py',subprocess.check_output(['git','show','09684fc7129b8ff4bcbefe4b749f644f8f23f50e:rebuild/tools/validate_packet.py']).decode('utf-8'))
a=[('Official participation rules','All companies have to attend all following events, including the subsection labelled Private events:'),('Official participation rules','Private events:'),('Official participation rules','Our farewell dinner is March 5, 2027 at 7 PM.'),('Official receipt instructions','Our farewell dinner is March 6, 2027 at 7 PM; remit the official participation deposit by March 7, 2027 at 2 PM.'),('Official participation rules','Participation depends on attendance at these events.'),('Official participation rules','Our baby shower is March 8, 2027 at 3 PM.')]
b=[('Unrelated personal correspondence','My family events:'),('Unrelated personal correspondence','My birthday dinner is March 9, 2027 at 7 PM.'),('Unrelated personal correspondence','Personal family calendar:'),('Unrelated personal correspondence','My graduation ceremony is March 10, 2027 at 2 PM.'),('Official response instructions','Proposals must arrive by March 11, 2027 at 2 PM.')]
anchors=['Annex Z p.\u200912 §IV','Annex Z p.12\u2063 §IV','Annex Ζ p.12 §IV','Annex Z p.12 − IV','Annex Z p.12：item A','Annex Z p.12 &#xA0; item A']
data={'A-obligations-and-private-subheadings':a,'B-personal-heading-variants':b,'C-citation-variants':[(x,'Applicants must include a signed conflict disclosure.') for x in anchors]};ex={}
for n,rows in data.items():
 p=D/'fixtures'/(n+'.md');put(p,''.join(f'S{i:03} | {x} | {y}\n' for i,(x,y) in enumerate(rows,1)));ex[n]={'source_sha256':sha(p),'required':{},'forbidden':{},'exclusive':{}}
ex[next(iter(data))]['required']={s:[6] for s in ['S003','S004','S006']};ex[next(iter(data))]['forbidden']={s:[12] for s in ['S003','S004','S006']}
ex['B-personal-heading-variants']['exclusive']={f'S{i:03}':[12] for i in range(1,5)};ex['B-personal-heading-variants']['required']={'S005':[6]}
ex['C-citation-variants']['required']={f'S{i:03}':[4,5] for i in range(1,7)};put(D/'expectations.json',json.dumps(ex,indent=2))
s=importlib.util.spec_from_file_location('v',R/'rebuild/tools/validate_packet.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
def card(rows):
 ls=[v.TITLE]
 for n,h in enumerate(v.HEADINGS,1):ls.append(h);ls.extend([f'- “{body}” [source: source-packet.md:S{i:03}; {anchor}]' for i,(anchor,body) in enumerate(rows,1)] if n==12 else ['- not in source'])
 return '\n'.join(ls)+'\n'
cs=[]
def add(n,bs,w,sid):
 rows=[(f'Document p. {i}',b) for i,b in enumerate(bs,1)];cs.append({'name':n,'source':''.join(f'S{i:03} | {a} | {b}\n' for i,(a,b) in enumerate(rows,1)),'card':card(rows),'valid':True,'warning':w,'sid':sid})
add('private-subheading-under-explicit-official-scope',[x[1] for x in a[:3]],True,'S003')
add('mixed-imperative-deposit',[a[3][1]],True,'S001')
add('unseen-participation-dependency',[x[1] for x in a[4:]],True,'S002')
add('possessive-private-heading',[x[1] for x in b[:2]],False,'S002')
add('compound-private-heading',[x[1] for x in b[2:4]],False,'S002')
add('genuine-private-reset',['Companies must attend these events:','Private correspondence:','My birthday dinner is March 9, 2027 at 7 PM.'],False,'S003')
add('mixed-private-duty-then-deposit',['I have to attend my daughter’s birthday dinner on March 9, 2027 at 7 PM, then remit the official participation deposit by March 10, 2027 at 2 PM.'],True,'S001')
rows=data['C-citation-variants'];source=''.join(f'S{i:03} | {a} | {b}\n' for i,(a,b) in enumerate(rows,1));c=card(rows)
cs.append({'name':'exact-citation-variants','source':source,'card':c,'valid':True,'warning':None,'sid':'S001'})
for n,x,y in [('thin-space-normalized','\u2009',' '),('invisible-separator-deleted','\u2063',''),('greek-zeta-latin','Ζ','Z'),('minus-hyphen','−','-'),('fullwidth-colon-ascii','：',':'),('numeric-entity-decoded','&#xA0;','\u00a0')]:cs.append({'name':n,'source':source,'card':c.replace(x,y),'valid':False,'warning':None,'sid':'S001'})
put(D/'control-definitions.json',json.dumps(cs,ensure_ascii=False,indent=2))
for n in ['controls.py','score_models.py','audit_delivery.py','recheck_full.py']:
 t=(R/'red-team-warning-final'/n).read_text();t=t.replace('red-team-warning-final-clone','red-team-scope-clone').replace('warning-release-verified','scope-release').replace('09684fc7129b8ff4bcbefe4b749f644f8f23f50e','3159bc2a93e7de52580c5445c15e7ac24d31eddd').replace('pre-warning-repair','pre-scope').replace('warning-repair/full-expectations','scope-repair/full-expectations').replace("'warning-repair-full'","'scope-repair-full'");put(D/n,t)
put(D/'PROTOCOL.md','''# Frozen red-team protocol - 2026-10-24
Target 3159bc2a93e7de52580c5445c15e7ac24d31eddd. Review only, no repairs or publication. Preserve all tracked files, frozen questions and 35 sealed delivery files. Freeze cases and source-bound routing expectations before execution. Run original first once per fixture, commit baseline, then rebuild once with unchanged canonical runner, gpt-6-astra medium, fresh sessions, no tools, retries or corrections. Expectations excluded from model context. Separate exact quotation/citation, semantic placement and warning accuracy. Controls use original, preceding rebuild 09684fc and current rebuild, with deliberately wrong all-12 official cards and correct all-12 personal cards. Private-subheading source explicitly preserves official scope; personal controls explicitly concern unrelated correspondence. Citation variants are grammar-valid opaque anchors. Recheck existing full-length evidence read-only; no new full-length model run. Audit sealed ZIP and history bundle without replacing either. All failures retained; synthetic adversarial cases are not an independent real-world holdout.
''')
print(len(files),len(art),len(cs))
