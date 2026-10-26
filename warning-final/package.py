from pathlib import Path
import hashlib,json,subprocess,zipfile
R=Path(__file__).resolve().parents[1];D=R/'dist/warning-final-release';D.mkdir(exist_ok=False)
assert json.loads((R/'warning-final/SUMMARY.json').read_text())['acceptance'].startswith('PASS'),'A failed gate blocks release sealing'
assert not subprocess.check_output(['git','status','--porcelain'],cwd=R),'Commit all evidence before sealing'
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()
for args in [['git','archive','--format=zip','--prefix=RFP-COMPASS-Comp15/','-o',str(D/'RFP-COMPASS-Comp15-source.zip'),head],['git','bundle','create',str(D/'RFP-COMPASS-Comp15.bundle'),'--all']]:subprocess.run(args,cwd=R,check=True)
names=[n for n in subprocess.check_output(['git','ls-tree','-r','--name-only','-z',head],cwd=R).decode().split('\0') if n]
with zipfile.ZipFile(D/'RFP-COMPASS-Comp15-source.zip') as z:
 assert {n.removeprefix('RFP-COMPASS-Comp15/') for n in z.namelist() if not n.endswith('/')}==set(names)
 for n in names:assert z.read('RFP-COMPASS-Comp15/'+n)==(R/n).read_bytes(),n
art=['RFP-COMPASS-Comp15.bundle','RFP-COMPASS-Comp15-source.zip']
(D/'SHA256SUMS.txt').open('x').write(''.join(hashlib.sha256((D/n).read_bytes()).hexdigest()+'  '+n+'\n' for n in art))
(D/'RELEASE.json').open('x').write(json.dumps({'commit':head,'published':False,'source_archive_files_verified':len(names),'artifacts':art,'checksums':'SHA256SUMS.txt'},indent=2));print(head,len(names))
