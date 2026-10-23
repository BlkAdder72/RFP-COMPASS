from pathlib import Path
import json,subprocess,sys,shutil
R=Path(__file__).resolve().parents[1];D=R/'final-repair';C=R/'dist/portability-probe-with-deliberately-long-name/verification-clone';assert not C.exists()
out=[]
def run(label,cmd,cwd):
 r=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True,encoding='utf-8');out.append({'label':label,'command':cmd,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr});(D/'deep-audit-probe.json').write_text(json.dumps(out,indent=2),encoding='utf-8');assert r.returncode==0,(label,r.stdout[-4000:],r.stderr[-4000:])
run('clone-prototype',['git','-c','core.longpaths=true','clone','--quiet',str(R/'dist/final-repair-verified/RFP-COMPASS-Comp15.bundle'),str(C)],R)
# Prototype differs from its retained sealed archive only by the proposed auditor.
shutil.copyfile(R/'tools/verify_submission.py',C/'tools/verify_submission.py')
run('deep-path-audit',[sys.executable,'-B','-X','utf8','tools/verify_submission.py'],C)
print('PASS: full offline audit at deliberately deep clone path; prototype and all logs retained')
