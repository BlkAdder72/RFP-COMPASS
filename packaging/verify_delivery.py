"""Verify sealed local artifacts in a fresh bundle clone; never publish or call a model."""
from pathlib import Path
import hashlib,json,subprocess,sys
R=Path(__file__).resolve().parents[1];D=R/'dist';C=D/'verification-scope-hardening';P=D/'FINAL_VERIFICATION.json'
assert not C.exists() and not P.exists(),'Refusing existing delivery proof/clone'
records=[]
def run(label,cmd,cwd):
 r=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True,encoding='utf-8');records.append({'label':label,'command':cmd,'cwd':str(cwd),'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
 assert r.returncode==0,(label,r.stdout,r.stderr)
 return r
hashes={}
for line in (D/'SHA256SUMS.txt').read_text(encoding='utf-8').splitlines():
 h,n=line.split('  ',1);assert hashlib.sha256((D/n).read_bytes()).hexdigest()==h;hashes[n]=h
release=json.loads((D/'RELEASE.json').read_text(encoding='utf-8'))
run('bundle-verify',['git','bundle','verify',str(D/'RFP-COMPASS-Comp15.bundle')],R)
run('fresh-clone',['git','clone','--quiet',str(D/'RFP-COMPASS-Comp15.bundle'),str(C)],R)
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=C).decode().strip()==release['commit']
run('clone-exact-working-bytes',[sys.executable,'-B','packaging/verify_index.py'],C)
before={str(p.relative_to(C)) for p in C.rglob('*') if p.is_file()}
for arm in ('original','rebuild'):
 for script,kind in [('tools/run_arm.py','core'),('hardening/run_full.py','full')]:
  out=C/'dist'/('reviewer-'+kind+'-'+arm)
  run('preflight-'+kind+'-'+arm,[sys.executable,'-B',script,arm,'--output-dir',str(out),'--preflight-only'],C)
  assert not out.exists()
assert before=={str(p.relative_to(C)) for p in C.rglob('*') if p.is_file()},'Preflight changed clone file inventory'
run('clone-offline-compliance',[sys.executable,'-B','-X','utf8','tools/verify_submission.py'],C)
proof={'status':'PASS: local delivery and evidence integrity','commit':release['commit'],'published':False,'real_model_calls_in_delivery_check':0,'checksums':hashes,'source_archive_files':release['source_archive_files_verified'],'preflight_clone_writes':False,'candidate_performance':'MIXED; raw full-length rebuild has two S072 anchor errors and is correctly rejected; no clean full-length pass claimed','checks':records}
P.write_text(json.dumps(proof,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in proof.items() if k!='checks'},indent=2))
