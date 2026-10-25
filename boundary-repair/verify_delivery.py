from pathlib import Path
import hashlib,json,subprocess,sys,zipfile
R=Path(__file__).resolve().parents[1];D=R/'dist/boundary-release';C=R/'dist/boundary-release-clone';assert not C.exists() and not (D/'FINAL_VERIFICATION.json').exists()
checks=[]
def run(label,cmd):
 p=subprocess.run(cmd,cwd=C if C.exists() and label not in ['bundle-verify','fresh-clone'] else R,capture_output=True,text=True,encoding='utf-8');checks.append({'label':label,'command':cmd,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr});(D/'DELIVERY_PROGRESS.json').write_text(json.dumps(checks,indent=2),encoding='utf-8');assert p.returncode==0,(label,p.stdout[-5000:],p.stderr[-5000:])
release=json.loads((D/'RELEASE.json').read_text())
for line in (D/'SHA256SUMS.txt').read_text().splitlines():
 h,n=line.split('  ',1);assert hashlib.sha256((D/n).read_bytes()).hexdigest()==h
run('bundle-verify',['git','bundle','verify',str(D/'RFP-COMPASS-Comp15.bundle')]);run('fresh-clone',['git','-c','core.longpaths=true','clone','--quiet',str(D/'RFP-COMPASS-Comp15.bundle'),str(C)])
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=C).decode().strip()==release['commit']
run('pristine-index-bytes',[sys.executable,'-B','-X','utf8','packaging/verify_index.py'])
for arm in ['original','rebuild']:
 for script,kind in [('tools/run_arm.py','core'),('hardening/run_full.py','full')]:run('preflight-'+arm+'-'+kind,[sys.executable,'-B','-X','utf8',script,arm,'--output-dir',str(C/'dist'/('unused-'+arm+'-'+kind)),'--preflight-only'])
run('offline-compliance',[sys.executable,'-B','-X','utf8','tools/verify_submission.py'])
with zipfile.ZipFile(D/'RFP-COMPASS-Comp15-source.zip') as z:
 names=[n for n in z.namelist() if not n.endswith('/')];assert len(names)==release['source_archive_files_verified']
 for n in names:assert z.read(n)==(C/n.removeprefix('RFP-COMPASS-Comp15/')).read_bytes(),n
(D/'FINAL_VERIFICATION.json').open('x',encoding='utf-8').write(json.dumps({'status':'PASS: fresh-clone compliance and exact archive/source bytes','commit':release['commit'],'source_archive_files_verified':len(names),'published':False,'real_model_calls':0,'checks':checks},indent=2));print('PASS new delivery')
