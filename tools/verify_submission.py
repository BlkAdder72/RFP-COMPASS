"""Offline audit: historical evidence at its sealed commit, then current repair. No model calls."""
from pathlib import Path
import json,subprocess,sys,tempfile
R=Path(__file__).resolve().parents[1]
records=[]
def run(label,cmd,cwd):
 r=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True,encoding='utf-8')
 records.append({'label':label,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
 if r.returncode:print(json.dumps(records,indent=2));raise SystemExit(r.returncode)
# Historical audits require their historical validator/knowledge. Execute them in a disposable
# private clone, never by weakening their assertions or rewriting current evidence.
work=(R/'.run-work').resolve();assert work.is_relative_to(R.resolve());work.mkdir(exist_ok=True)
with tempfile.TemporaryDirectory(prefix='rfp-history-audit-',dir=work) as temp:
 assert Path(temp).resolve().is_relative_to(work)
 C=Path(temp)/'sealed'
 run('clone-historical-tree',['git','-c','core.longpaths=true','clone','--quiet','--shared','--no-checkout',str(R),str(C)],R)
 run('checkout-sealed',['git','-c','core.longpaths=true','checkout','--quiet','--detach','157d8fe22339ce5385b8291728c48f7141840206'],C)
 run('historical-offline-audit',[sys.executable,'-B','-X','utf8','tools/verify_submission.py'],C)
run('current-repair-audit',[sys.executable,'-B','-X','utf8','final-repair/verify.py'],R)
print(json.dumps({'offline_audit':'PASS','real_model_calls':0,'published':False,'checks':records},indent=2))
