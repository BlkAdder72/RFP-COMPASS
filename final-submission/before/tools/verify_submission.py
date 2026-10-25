"""Offline audit: unchanged historical assertions in sibling clones, then current evidence."""
from pathlib import Path
import json,os,subprocess,sys,tempfile
R=Path(__file__).resolve().parents[1];records=[]
def gitpath(p):
 s=str(p)
 return s[4:] if os.name=='nt' and s.startswith('\\\\?\\') else s
def run(label,cmd,cwd):
 r=subprocess.run(cmd,cwd=gitpath(cwd),capture_output=True,text=True,encoding='utf-8');records.append({'label':label,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
 if r.returncode:print(json.dumps(records,indent=2));raise SystemExit(r.returncode)
def pythonpath(p):
 s=str(p)
 return '\\\\?\\'+s if os.name=='nt' and not s.startswith('\\\\?\\') else s
work=Path(tempfile.mkdtemp(prefix='rfp-comp15-historical-'))
# Do not invoke the older clone-launcher recursively: Git rejects its inherited
# extended-path destination. Keep all historical assertion code unchanged instead.
for name,commit,script in [('legacy','157d8fe22339ce5385b8291728c48f7141840206','tools/verify_submission.py'),('final-repair','06fcebace08c19410b63f1cd8c2523f66822d18b','final-repair/verify.py'),('warning-repair','09684fc7129b8ff4bcbefe4b749f644f8f23f50e','warning-repair/verify.py'),('scope-repair','3159bc2a93e7de52580c5445c15e7ac24d31eddd','scope-repair/verify.py'),('scope-guard-repair','06e6a1384c94bd0c1298f0d50cfbe09ce3fc1bcf','scope-guard-repair/verify.py'),('polarity-repair','21dd85b40edf835870689c9f4a0b67ddc10de81a','polarity-repair/verify.py'),('boundary-repair','118f24d3abf07b9cb736e1fd005ad40faf7fb58f','boundary-repair/verify.py')]:
 temp=Path(tempfile.mkdtemp(prefix='ha-',dir=work));C=temp/'s'
 run(name+'-clone',['git','-c','core.longpaths=true','clone','--quiet','--shared','--no-checkout',gitpath(R),gitpath(C)],R)
 run(name+'-checkout',['git','-c','core.longpaths=true','checkout','--quiet','--detach',commit],C)
 run(name+'-unchanged-audit',[sys.executable,'-B','-X','utf8',pythonpath(C/script)],C)
run('current-repair-audit',[sys.executable,'-B','-X','utf8',pythonpath(R/'submission-repair/verify.py')],R)
print(json.dumps({'offline_audit':'PASS','real_model_calls':0,'published':False,'checks':records},indent=2))
