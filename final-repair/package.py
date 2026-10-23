"""Seal committed candidate and complete history without replacing any prior delivery."""
from pathlib import Path
import hashlib,json,subprocess,sys,zipfile
R=Path(__file__).resolve().parents[1];D=R/'dist/final-repair';assert not D.exists();D.mkdir()
assert not subprocess.check_output(['git','status','--porcelain'],cwd=R).strip(),'Commit all source/evidence before sealing'
commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip();records=[]
def run(label,cmd,cwd):
 r=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True,encoding='utf-8');records.append({'label':label,'command':cmd,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
 if r.returncode:
  (D/'FAILED_VERIFICATION.json').write_text(json.dumps(records,indent=2),encoding='utf-8');raise SystemExit(label+' failed; all evidence retained')
 return r
bundle=D/'RFP-COMPASS-Comp15.bundle';archive=D/'RFP-COMPASS-Comp15-source.zip'
run('bundle-create',['git','bundle','create',str(bundle),'--all'],R);run('bundle-verify',['git','bundle','verify',str(bundle)],R)
run('archive-create',['git','archive','--format=zip','--prefix=RFP-COMPASS-Comp15/','--output='+str(archive),'HEAD'],R)
tracked=[n for n in subprocess.check_output(['git','ls-tree','-r','--name-only','-z','HEAD'],cwd=R).decode().split('\0') if n]
with zipfile.ZipFile(archive) as z:
 assert {n.removeprefix('RFP-COMPASS-Comp15/') for n in z.namelist() if not n.endswith('/')}==set(tracked)
 for n in tracked:assert z.read('RFP-COMPASS-Comp15/'+n)==(R/n).read_bytes(),n
 E=D/'extracted';z.extractall(E)
 for n in tracked:assert (E/'RFP-COMPASS-Comp15'/n).read_bytes()==(R/n).read_bytes(),n
hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [bundle,archive]}
(D/'SHA256SUMS.txt').write_text(''.join(h+'  '+n+'\n' for n,h in hashes.items()),encoding='utf-8')
(D/'RELEASE.json').write_text(json.dumps({'commit':commit,'published':False,'source_archive_files_verified':len(tracked),'artifacts':list(hashes),'checksums':'SHA256SUMS.txt'},indent=2),encoding='utf-8')
C=D/'verification-clone';run('fresh-clone',['git','clone','--quiet',str(bundle),str(C)],R)
assert run('sealed-head',['git','rev-parse','HEAD'],C).stdout.strip()==commit
run('pristine-clone-byte-check',[sys.executable,'-B','-X','utf8','packaging/verify_index.py'],C)
for arm in ['original','rebuild']:
 for script,kind in [('tools/run_arm.py','core'),('hardening/run_full.py','full')]:run('preflight-'+kind+'-'+arm,[sys.executable,'-B','-X','utf8',script,arm,'--output-dir',str(C/'dist'/('unused-'+kind+'-'+arm)),'--preflight-only'],C)
run('portable-offline-audit',[sys.executable,'-B','-X','utf8','tools/verify_submission.py'],C)
result={'status':'PASS: fresh-clone compliance and exact source/archive bytes','commit':commit,'published':False,'real_model_calls_in_packaging':0,'source_files':len(tracked),'checksums':hashes,'checks':records}
(D/'FINAL_VERIFICATION.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
