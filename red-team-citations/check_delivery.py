from pathlib import Path
import hashlib,json,subprocess,sys
R=Path(__file__).resolve().parents[1];D=Path(__file__).resolve().parent;C=R/'dist/redteam-unseen-pristine'
assert not C.exists()
records=[]
def run(label,args,cwd):
 r=subprocess.run(args,cwd=cwd,capture_output=True,text=True,encoding='utf-8');records.append({'label':label,'command':args,'cwd':str(cwd),'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr});assert r.returncode==0,(label,r.stdout,r.stderr)
run('fresh-clone',['git','clone','--quiet',str(R/'dist/RFP-COMPASS-Comp15.bundle'),str(C)],R)
run('sealed-head',['git','rev-parse','HEAD'],C);assert records[-1]['stdout'].strip()=='157d8fe22339ce5385b8291728c48f7141840206'
run('pristine-index-before-audit',[sys.executable,'-B','-X','utf8','packaging/verify_index.py'],C)
for arm in ['original','rebuild']:run('preflight-'+arm,[sys.executable,'-B','-X','utf8','tools/run_arm.py',arm,'--output-dir',str(C/'dist'/('unused-'+arm)),'--preflight-only'],C)
m=json.loads((D/'preservation.json').read_text(encoding='utf-8'));bad=[]
for group in ['tracked','sealed']:
 for p,h in m[group].items():
  if hashlib.sha256((R/p).read_bytes()).hexdigest()!=h:bad.append(p)
assert not bad,bad
out={'sealed_target':m['target'],'all_preexisting_files_unchanged':True,'tracked_files_verified':len(m['tracked']),'sealed_files_verified':len(m['sealed']),'checks':records,'offline_audit_exit':int((D/'clone-audit-exit.txt').read_text().strip()),'sequence_correction':'An index-byte check was initially run after the offline audit on the first clone. It failed on citation-repair/verification.json because the audit rewrites derived verification metadata. That sequencing failure is retained in post-audit-index-failure.txt. A second untouched clone passed the index-byte check before any audit.'}
(D/'delivery-review.json').open('x',encoding='utf-8').write(json.dumps(out,indent=2));print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2))
