"""Package an explicitly incomplete offline review snapshot, never a release."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,zipfile
R=Path(__file__).resolve().parents[1];D=R/'validator-note-repair';P=R/'dist/validator-note-repair-review'
p=argparse.ArgumentParser();p.add_argument('--checkout-dir',required=True,type=Path);a=p.parse_args();C=a.checkout_dir.resolve()
assert not P.exists() and not C.exists(),'Preserve earlier archives and checkouts'
assert not subprocess.check_output(['git','status','--porcelain'],cwd=R),'Commit the source and evidence first'
proof=json.loads((D/'FINAL_INTEGRITY.json').read_text());assert proof['passed'] and proof['after_sha256']==hashlib.sha256((R/'rebuild/tools/validate_packet.py').read_bytes()).hexdigest()
P.mkdir(parents=True);head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip();records=[]
def run(label,args,cwd=R,expected=0):
 v=subprocess.run(args,cwd=cwd,capture_output=True,text=True,encoding='utf-8');records.append({'label':label,'command':args,'exit_code':v.returncode,'stdout':v.stdout,'stderr':v.stderr})
 (P/'VERIFICATION.json').write_bytes(json.dumps({'status':'in progress','checks':records,'published':False},indent=2).encode())
 assert v.returncode==expected,(label,v.stdout,v.stderr)
 return v
source=P/'RFP-COMPASS-offline-review-source.zip';bundle=P/'RFP-COMPASS-full-history.bundle'
run('source archive',['git','archive','--format=zip','--prefix=RFP-COMPASS/','-o',str(source),head])
run('full Git history',['git','bundle','create',str(bundle),'--all'])
blobs={}
for row in subprocess.check_output(['git','ls-tree','-r','-z',head],cwd=R).split(b'\0'):
 if row:
  meta,name=row.split(b'\t',1);blobs[name.decode()]=meta.decode().split()[2]
with zipfile.ZipFile(source) as z:
 assert z.testzip() is None
 assert {n.removeprefix('RFP-COMPASS/') for n in z.namelist() if not n.endswith('/')}==set(blobs)
 for n,h in blobs.items():
  v=z.read('RFP-COMPASS/'+n);assert hashlib.sha1(b'blob '+str(len(v)).encode()+b'\0'+v).hexdigest()==h,n
run('bundle verify',['git','bundle','verify',str(bundle)])
run('independent full-history clone',['git','-c','core.longpaths=true','clone','--quiet','--no-checkout',str(bundle),str(C)])
run('long paths',['git','config','core.longpaths','true'],C)
run('exact checkout',['git','checkout','--quiet','--detach',head],C)
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=C,text=True).strip()==head
manifest=json.loads((C/'validator-note-repair/EVIDENCE_SHA256.json').read_text())
assert all(hashlib.sha256((C/n).read_bytes()).hexdigest()==h for n,h in manifest.items())
run('fresh differential cases',[sys.executable,'-B','-X','utf8','validator-note-repair/test_repair.py','--stage','final','--output-dir','.run-work/fresh-warning-check'],C)
run('fresh delta and preservation integrity',[sys.executable,'-B','-X','utf8','validator-note-repair/verify_integrity.py','--output','.run-work/fresh-integrity.json'],C)
run('submission still blocked',[sys.executable,'-B','-X','utf8','tools/verify_submission.py'],C,2)
run('clean checkout',['git','status','--porcelain'],C);assert not records[-1]['stdout']
arts=[source.name,bundle.name]
(P/'SHA256SUMS.txt').write_bytes(''.join(hashlib.sha256((P/n).read_bytes()).hexdigest()+'  '+n+'\n' for n in arts).encode())
(P/'PACKAGE.json').write_bytes(json.dumps({'commit':head,'kind':'incomplete offline review snapshot; NOT a submission-ready release','submission_ready':False,'native_comparison_complete':False,'published':False,'new_Claude_runs':0,'source_files_verified':len(blobs),'manifest_files_verified':len(manifest),'artifacts':arts,'remaining':'Fourth response export and seven repaired native cases remain pending; no new native acceptance is claimed'},indent=2).encode())
(P/'VERIFICATION.json').write_bytes(json.dumps({'status':'PASS offline archive, fresh-clone differential and preservation checks; HOLD submission','checks':records,'source_commit':head,'published':False,'submission_ready':False},indent=2).encode())
print(json.dumps({'package':str(P),'commit':head,'source_files_verified':len(blobs),'fresh_clone':str(C),'submission_ready':False,'published':False}))
