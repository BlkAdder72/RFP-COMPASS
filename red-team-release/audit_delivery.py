from pathlib import Path
import hashlib,json,subprocess,sys,zipfile
R=Path(__file__).resolve().parents[1];D=Path(__file__).resolve().parent;C=R/'dist/red-team-release-clone';assert not C.exists()
records=[]
def run(label,cmd,cwd):
 r=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True,encoding='utf-8');records.append({'label':label,'command':cmd,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr});(D/'delivery-checks.json').write_text(json.dumps(records,indent=2),encoding='utf-8');assert r.returncode==0,(label,r.stdout[-4000:],r.stderr[-4000:])
release=json.loads((R/'dist/release/RELEASE.json').read_text());assert release['commit']=='06fcebace08c19410b63f1cd8c2523f66822d18b' and not release['published']
for line in (R/'dist/release/SHA256SUMS.txt').read_text().splitlines():
 h,n=line.split('  ',1);assert hashlib.sha256((R/'dist/release'/n).read_bytes()).hexdigest()==h
names=[n for n in subprocess.check_output(['git','ls-tree','-r','--name-only','-z',release['commit']],cwd=R).decode().split('\0') if n]
with zipfile.ZipFile(R/'dist/release/RFP-COMPASS-Comp15-source.zip') as z:
 assert {n.removeprefix('RFP-COMPASS-Comp15/') for n in z.namelist() if not n.endswith('/')}==set(names)
 for n in names:assert z.read('RFP-COMPASS-Comp15/'+n)==(R/n).read_bytes(),n
run('bundle-verify',['git','bundle','verify',str(R/'dist/release/RFP-COMPASS-Comp15.bundle')],R)
run('fresh-clone',['git','-c','core.longpaths=true','clone','--quiet',str(R/'dist/release/RFP-COMPASS-Comp15.bundle'),str(C)],R)
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=C).decode().strip()==release['commit']
run('pristine-index-bytes',[sys.executable,'-B','-X','utf8','packaging/verify_index.py'],C)
for arm in ['original','rebuild']:run('preflight-'+arm,[sys.executable,'-B','-X','utf8','tools/run_arm.py',arm,'--output-dir',str(C/'dist'/('unused-'+arm)),'--preflight-only'],C)
run('offline-compliance',[sys.executable,'-B','-X','utf8','tools/verify_submission.py'],C)
(D/'delivery-summary.json').open('x').write(json.dumps({'passed':True,'sealed_target':release['commit'],'archive_files_checked':len(names),'real_model_calls':0,'published':False},indent=2));print('PASS: sealed archive/bundle bytes, pristine clone, runner preflights and offline compliance')
