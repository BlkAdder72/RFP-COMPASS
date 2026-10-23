from pathlib import Path
import importlib.util,json,subprocess,sys
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[1];D=Path(__file__).resolve().parent;O=D/'controls';O.mkdir(exist_ok=False)
spec=importlib.util.spec_from_file_location('v',R/'rebuild/tools/validate_packet.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
def new(p,t):p.parent.mkdir(parents=True,exist_ok=True);p.open('x',encoding='utf-8',newline='\n').write(t)
def card(rows):
 lines=[v.TITLE]
 for n,h in enumerate(v.HEADINGS,1):
  lines.append(h);lines.extend([f'- “{b}” [source: source-packet.md:S{i:03}; {a}]' for i,(a,b) in enumerate(rows,1)] if n==12 else ['- not in source'])
 return '\n'.join(lines)+'\n'
cases=[]
for label,body in [('baptism','My child’s baptism ceremony is December 3, 2026 at 11 AM.'),('baby-shower','My baby shower is December 4, 2026 at 3 PM.'),('graduation-control','My graduation ceremony is December 5, 2026 at 2 PM.')]:
 rows=[('Unrelated private family correspondence',body)];cases.append((label,rows,card(rows),True,False,'S001'))
for label,header in [('compulsory-have-to','All companies have to attend the following events:'),('mandatory-must-control','All companies must attend the following events:'),('clinical-control','All patients have to attend the following events:')]:
 rows=[('RFP participation p. 2',header),('RFP participation p. 3','Our farewell dinner is December 6, 2026 at 7 PM.')];cases.append((label,rows,card(rows),True,True,'S002'))
rows=[('RFP participation instructions','Our farewell dinner is December 6, 2026 at 7 PM; companies have to deliver their offers by December 7, 2026 at 2 PM.')];cases.append(('mixed-offer-deadline',rows,card(rows),True,True,'S001'))
src=(D/'fixtures/X-citation-microvariants.md').read_text(encoding='utf-8');rows=[tuple(l.split(' | ',2)[1:]) for l in src.splitlines()];text=card(rows)
cases.append(('exact-unseen-anchors',rows,text,True,None,None))
for label,a,b in [('narrow-nbsp-normalized','p.\u202fxi','p. xi'),('superscript-normalized','p. 5 n. ¹','p. 5 n. 1'),('zero-padding-normalized','p. 03,','p. 3,'),('zero-width-deleted','§2\u200b(b)','§2(b)'),('literal-backticks-deleted','§2`(b)`','§2(b)'),('roman-lookalike-swapped','§IV(1)(l)','§IV(1)(I)')]:cases.append((label,rows,text.replace(a,b),False,None,None))
cases.append(('altered-zero-width-quotation',rows,text.replace('conflict disclosure','conflict\u200b disclosure'),False,None,None))
cases.append(('straight-delimiters',rows,text.replace('“','"').replace('”','"'),False,None,None))
out=[]
for label,rows,text,want_valid,want_warning,sid in cases:
 folder=O/label;source=folder/'source-packet.md';target=folder/'card.md';new(source,''.join(f'S{i:03} | {a} | {b}\n' for i,(a,b) in enumerate(rows,1)));new(target,text)
 for arm in ['original','rebuild']:
  cmd=[sys.executable,'-B','-X','utf8',str(R/arm/'tools/validate_packet.py'),str(source),str(target)];r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8')
  for n,t in [('command.json',json.dumps(cmd)),('stdout.txt',r.stdout),('stderr.txt',r.stderr),('exit-code.txt',str(r.returncode))]:new(folder/arm/n,t)
  observed=any('REVIEW' in l and 'Section 6' in l and sid in l for l in r.stdout.splitlines()) if sid else None
  out.append({'case':label,'arm':arm,'expected_valid':want_valid,'exit_code':r.returncode,'expected_date_warning':want_warning,'observed_date_warning':observed,'passed':(r.returncode==0)==want_valid and (want_warning is None or observed==want_warning)})
new(D/'control-results.json',json.dumps(out,indent=2));print(json.dumps({'cases':len(out),'failures':[x for x in out if not x['passed']]},indent=2))
