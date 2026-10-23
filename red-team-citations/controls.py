from pathlib import Path
import importlib.util,json,subprocess,sys
R=Path(__file__).resolve().parents[1];D=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('validator',R/'rebuild/tools/validate_packet.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
def new(p,t):p.parent.mkdir(parents=True,exist_ok=True);p.open('x',encoding='utf-8',newline='\n').write(t)
def card(rows,placement):
 out=[v.TITLE]
 for section,heading in enumerate(v.HEADINGS,1):
  out.append(heading);out.extend([f'- “{b}” [source: source-packet.md:{s}; {a}]' for s,a,b in rows if section in placement[s]] or ['- not in source'])
 return '\n'.join(out)+'\n'
base=[('S001','New appendix p. 3 ¶2 [column A]','Applicants must include a signed disclosure form.')]
good=card(base,{'S001':[4,5]})
cases=[('exact-bracket-anchor',base,good,True),('changed-anchor',base,good.replace('column A','column B'),False),('zero-width-inserted',base,good.replace('signed','sig\u200bned'),False),('straight-delimiters',base,good.replace('“','"').replace('”','"'),False)]
nbsp=[('S001','Attachment p. 1 row 3','Applicants must include a signed\u00a0disclosure form.')]
cases.append(('nbsp-normalized',nbsp,card(nbsp,{'S001':[4,5]}).replace('\u00a0',' '),False))
many=[(f'S{i:03}','Register row '+str(i),'Background statement '+str(i)+'.') for i in range(1,152)]
cases.append(('151-bullets-single-reply',many,card(many,{s:[12] for s,a,b in many}),False))
personal=[('S001','Unrelated personal correspondence, attached in error','My niece’s graduation celebration is November 19, 2026 at 7 PM.')]
cases.append(('unrelated-graduation',personal,card(personal,{'S001':[12]}),True))
result=[]
for label,rows,text,want in cases:
 folder=D/'controls'/label;new(folder/'source-packet.md',''.join(f'{s} | {a} | {b}\n' for s,a,b in rows));new(folder/'card.md',text)
 for arm in ['original','rebuild']:
  cmd=[sys.executable,'-B','-X','utf8',str(R/arm/'tools/validate_packet.py'),str(folder/'source-packet.md'),str(folder/'card.md')]
  r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8')
  new(folder/(arm+'-stdout.txt'),r.stdout);new(folder/(arm+'-stderr.txt'),r.stderr)
  result.append({'case':label,'arm':arm,'written_contract_valid':want,'exit_code':r.returncode,'acceptance_matches_contract':(r.returncode==0)==want,'review_notes':[l for l in r.stdout.splitlines() if 'REVIEW' in l]})
new(D/'control-results.json',json.dumps(result,indent=2));print(json.dumps(result,indent=2))
