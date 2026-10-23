from pathlib import Path
import importlib.util,json,subprocess,sys,hashlib
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[1];D=Path(__file__).resolve().parent;O=D/'controls';O.mkdir(exist_ok=False)
spec=importlib.util.spec_from_file_location('v',R/'original/tools/validate_packet.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
results=[]
def new(p,t):p.parent.mkdir(parents=True,exist_ok=True);p.open('x',encoding='utf-8',newline='\n').write(t)
def card(rows):
 out=[v.TITLE]
 for n,h in enumerate(v.HEADINGS,1):
  out.append(h);out.extend([f'- “{b}” [source: source-packet.md:S{i:03}; {a}]' for i,(a,b) in enumerate(rows,1)] if n==12 else ['- not in source'])
 return '\n'.join(out)+'\n'
def run(label,arm,source,parts,valid,warning=None,sid=None,section=6):
 folder=O/label/arm;folder.mkdir(parents=True);cmd=[sys.executable,'-B','-X','utf8',str(R/arm/'tools/validate_packet.py'),str(source),*[str(p) for p in parts]];r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8')
 for n,t in [('command.json',json.dumps(cmd)),('stdout.txt',r.stdout),('stderr.txt',r.stderr),('exit-code.txt',str(r.returncode))]:new(folder/n,t)
 observed=any('REVIEW' in l and f'Section {section}' in l and sid in l for l in r.stdout.splitlines()) if sid else None
 results.append({'label':label,'arm':arm,'expected_valid':valid,'exit_code':r.returncode,'expected_warning':warning,'observed_warning':observed,'passed':(r.returncode==0)==valid and (warning is None or observed==warning),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest()})
base=[('Memo p. 4 ¶2 [column A]','A background statement.')];exact=card(base)
cases=[('exact',base,exact,True),('zero-width',base,exact.replace('background','back\u200bground'),False),('straight',base,exact.replace('“','"').replace('”','"'),False),('changed-anchor',base,exact.replace('column A','column B'),False),('shortened-anchor',base,exact.replace(' ¶2 [column A]',''),False),('changed-quote',base,exact.replace('background','different'),False),('missing-coverage',base,exact.replace(next(l for l in exact.splitlines() if 'source:' in l),'- not in source'),False)]
for label,body in [('zero-width-source-exact','A back\u200bground statement.'),('internal-straight-quotes','The "draft" is background.')]:
 rows=[('Memo p. 4',body)];cases.append((label,rows,card(rows),True))
for name,body in [('nbsp','A background\u00a0statement.'),('decomposed','The cafe\u0301 is closed.'),('trailing-space','Background text. ')]:
 rows=[('Memo p. 4',body)];text=card(rows);cases.append((name+'-exact',rows,text,True))
 changed=text.replace('\u00a0',' ') if name=='nbsp' else text.replace('cafe\u0301','café') if name=='decomposed' else text.replace('text. ”','text.”')
 cases.append((name+'-changed',rows,changed,False))
for label,rows,text,valid in cases:
 source=O/label/'source-packet.md';new(source,''.join(f'S{i:03} | {a} | {b}\n' for i,(a,b) in enumerate(rows,1)));p=O/label/'card.md';new(p,text)
 for arm in ['original','rebuild']:run(label,arm,source,[p],valid)
# Existing cross-anchor, clinical, mandatory and ambiguous controls are reused unchanged.
spec=importlib.util.spec_from_file_location('cases',R/'hardening/check_cases.py');c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
guards=c.CASES+[
 ('graduation',[('Unrelated personal correspondence','My niece’s graduation celebration is November 19, 2026 at 7 PM.')],False),
 ('graduation-procurement',[('RFP p. 2','Mandatory bidder events:'),('RFP p. 3','My niece’s graduation celebration is November 19, 2026 at 7 PM.')],True),
 ('graduation-mixed',[('personal note','My niece’s graduation celebration is November 19, 2026 at 7 PM; bids are due at 8 PM.')],True),
 ('graduation-clinical',[('a','Required patient activity schedule:'),('b','Our graduation ceremony is November 19, 2026 at 7 PM.')],True),
 ('graduation-unknown',[('a','The celebration is November 19, 2026 at 7 PM.')],True)]
for label,rows,want in guards:
 label='guard-'+label;source=O/label/'source-packet.md';new(source,''.join(f'S{i:03} | {a} | {b}\n' for i,(a,b) in enumerate(rows,1)));p=O/label/'card.md';new(p,card(rows))
 for arm in ['original','rebuild']:run(label,arm,source,[p],True,want,f'S{len(rows):03}')
prior=json.loads((R/'revision/default-tests-v2-results.json').read_text())['cases']
for c in prior:
 want=False if c['label'] in ['generic-lunch-money','changed-quote'] and c['arm']=='rebuild' else c['expect_warning']
 run('prior-'+c['label'],c['arm'],R/c['source'],[R/c['card']],c['expect_valid'],want,c['sid'],c['section'])
for arm in ['original','rebuild']:
 run('preserved-S072-failure',arm,R/'hardening/fixtures/Z-full-length-noisy.md',sorted((R/'run-rebuild/hardening-full').glob('part-*/bid-compliance-card.md')),False)
new(D/'control-results.json',json.dumps({'cases':results,'count':len(results),'rebuild_failures':[x for x in results if x['arm']=='rebuild' and not x['passed']],'original_contract_gaps':[x for x in results if x['arm']=='original' and not x['passed']]},indent=2))
print(json.dumps({'count':len(results),'rebuild_failures':[x for x in results if x['arm']=='rebuild' and not x['passed']]},indent=2))
assert all(x['passed'] for x in results if x['arm']=='rebuild')
