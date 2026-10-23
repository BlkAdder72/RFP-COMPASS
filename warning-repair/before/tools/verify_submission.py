"""Offline audit: historical evidence at its sealed commit, then current repair. No model calls."""
from pathlib import Path
import json,subprocess,sys,tempfile,os
R=Path(__file__).resolve().parents[1]
records=[]
def run(label,cmd,cwd):
 r=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True,encoding='utf-8')
 records.append({'label':label,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
 if r.returncode:print(json.dumps(records,indent=2));raise SystemExit(r.returncode)
# Historical audits require their historical validator/knowledge. Execute them in a disposable
# private clone, never by weakening their assertions or rewriting current evidence.
work=(R/'.run-work').resolve();assert work.is_relative_to(R.resolve());work.mkdir(exist_ok=True)
temp=Path(tempfile.mkdtemp(prefix='ha-',dir=work)).resolve();assert temp.is_relative_to(work)
C=temp/'s'
run('clone-historical-tree',['git','-c','core.longpaths=true','clone','--quiet','--shared','--no-checkout',str(R),str(C)],R)
run('checkout-sealed',['git','-c','core.longpaths=true','checkout','--quiet','--detach','157d8fe22339ce5385b8291728c48f7141840206'],C)
script=str(C/'tools/verify_submission.py')
if os.name=='nt' and not script.startswith('\\\\?\\'):script='\\\\?\\'+script
# Launch by extended absolute filename so historical Path(__file__).resolve() keeps
# Windows long-path support. Keep scratch clones as ignored audit evidence.
run('historical-offline-audit',[sys.executable,'-B','-X','utf8',script],C)
current=str(R/'final-repair/verify.py')
if os.name=='nt' and not current.startswith('\\\\?\\'):current='\\\\?\\'+current
run('current-repair-audit',[sys.executable,'-B','-X','utf8',current],R)
print(json.dumps({'offline_audit':'PASS','real_model_calls':0,'published':False,'checks':records},indent=2))
