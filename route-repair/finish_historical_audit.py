from pathlib import Path
import ast,json,subprocess,sys,hashlib
R=Path.cwd();D=R/'route-repair';old=(D/'history/historical-audit-path-fix/tools/verify_submission.py').read_text(encoding='utf8');new=(R/'tools/verify_submission.py').read_text(encoding='utf8')
assert old.replace("pythonpath(R/'route-repair/audit.py')","gitpath(R/'route-repair/audit.py')")==new
prior=json.loads((D/'historical-audit-wrapper-failure.json').read_text(encoding='utf8'));assert len(prior)==31 and all(x['exit_code']==0 for x in prior[:-1]);assert prior[-1]['label']=='current-route-repair-integrity' and prior[-1]['exit_code']==1
names=[x['label'] for x in prior[:-1] if x['label'].endswith('unchanged-audit')];assert len(names)==10
records=prior[:-1]
tree=ast.parse(new);gitpath_node=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='gitpath');current=next(x for x in tree.body if isinstance(x,ast.Expr) and isinstance(x.value,ast.Call) and isinstance(x.value.func,ast.Name) and x.value.func.id=='run' and x.value.args and isinstance(x.value.args[0],ast.Constant) and x.value.args[0].value=='current-route-repair-integrity')
import os
ns={'os':os,'sys':sys,'R':Path(chr(92)*2+'?'+chr(92)+str(R)) if os.name=='nt' else R}
exec(compile(ast.Module(body=[gitpath_node],type_ignores=[]),'tools/verify_submission.py','exec'),ns)
def run(label,cmd,cwd):
 p=subprocess.run(cmd,cwd=ns['gitpath'](cwd),capture_output=True,text=True,encoding='utf8');records.append({'label':label,'command':cmd,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr});assert p.returncode==0,(p.stdout,p.stderr)
ns['run']=run
exec(compile(ast.Module(body=[current],type_ignores=[]),'tools/verify_submission.py','exec'),ns)
proof={'offline_audit':'PASS','method':'Ten unchanged historical audits reused from successful exact pinned-clone steps; only failed final Windows path handoff rerun through the corrected wrapper AST under an extended-path entry. No historical assertion or model input changed.','historical_snapshots_passed':len(names),'path_fix_only':True,'runner_sha256':hashlib.sha256((R/'tools/verify_submission.py').read_bytes()).hexdigest(),'current_audit_sha256':hashlib.sha256((D/'audit.py').read_bytes()).hexdigest(),'preserved_failed_attempt':'historical-audit-wrapper-failure.json','real_model_calls':0,'published':False,'checks':records}
(D/'HISTORICAL_AUDIT.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({k:v for k,v in proof.items() if k!='checks'}))
