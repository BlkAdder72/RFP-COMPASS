from pathlib import Path
import json,hashlib,subprocess,sys
D=Path(__file__).resolve().parent;R=D.parent
stage=sys.argv[1]; O=D/'stages'/stage;O.mkdir(parents=True,exist_ok=False)
names=['CLAUDE_PROJECT_INSTRUCTIONS.txt','rules.md','reference/output-schema.md']
for n in names:
 p=O/'candidate'/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((R/'rebuild'/n).read_bytes())
checks={}
for n in ['tools/validate_packet.py','tools/finalize_card.py']:
 checks['byte_identical:'+n]=(R/'rebuild'/n).read_bytes()==(D/'before/rebuild'/n).read_bytes()
schema=(R/'rebuild/reference/output-schema.md').read_text(encoding='utf-8');rules=(R/'rebuild/rules.md').read_text(encoding='utf-8');main=(R/'rebuild/CLAUDE_PROJECT_INSTRUCTIONS.txt').read_text(encoding='utf-8')
checks['private_exceptions_retained']='Section 12-only exceptions' in schema and 'private self-duties' in rules
checks['reservation_route']=all('issuer reservations' in s for s in [schema,rules,main]) and 'not evidence that a change has already occurred' in schema
if stage>='R2':checks['submission_contact_route']=all('submission recipients' in s for s in [schema,rules,main]) and 'personal contacts remain' in schema
if stage>='R3':checks['commercial_response_route']=all('required pricing forms' in s for s in [schema,rules,main]) and 'technical narrative alone' in schema
commands=[]
def run(label,args,expected):
 cmd=[sys.executable,'-B','-X','utf8',str(R/'rebuild/tools/validate_packet.py'),*map(str,args)]
 p=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8');commands.append({'label':label,'command':cmd,'exit_code':p.returncode,'expected_exit_code':expected,'stdout':p.stdout,'stderr':p.stderr});checks[label]=p.returncode==expected
run('four_shipped_samples',[],0)
source=R/'fixtures/C-official-email.md';raw=D/'evidence/original/core-C-official-email/raw-response.md';text=raw.read_text(encoding='utf-8')
for label,mut in [('altered_quote',text.replace('signed pricing sheet','unsigned pricing sheet',1)),('altered_anchor',text.replace('RFP-17 p. 1','RFP-17 p. 999',1))]:
 p=O/(label+'.md');p.write_text(mut,encoding='utf-8');assert mut!=text;run(label,[source,p],1)
result={'kind':'offline contract consistency and unchanged strict-validation controls; not model routing acceptance','checks':checks,'commands':commands,'hashes':{n:hashlib.sha256((R/'rebuild'/n).read_bytes()).hexdigest() for n in names},'passed':all(checks.values())}
(O/'checks.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8');print(json.dumps({'stage':stage,'checks':checks,'passed':result['passed']}));assert result['passed']
