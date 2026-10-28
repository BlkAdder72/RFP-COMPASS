"""Seal an unpublished review archive; never treat integrity as behavioral acceptance."""
from pathlib import Path
import hashlib,json,subprocess,zipfile,argparse
R=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--package-dir',type=Path,default=R/'dist/route-repair-review-v2');D=parser.parse_args().package_dir.resolve()
assert not subprocess.check_output(['git','status','--porcelain'],cwd=R),'Commit all evidence before packaging'
audit=json.loads((R/'route-repair/FINAL_CHECK.json').read_text())
assert audit.get('comparison_complete'), 'Complete both native arms before sealing this package'
assert audit['integrity_pass'], 'Integrity failures block even a review archive'
assert not D.exists(),'Preserve existing archives; choose a new output path'
D.mkdir(parents=True)
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()
for args in [['git','archive','--format=zip','--prefix=RFP-COMPASS-Comp15/','-o',str(D/'RFP-COMPASS-Comp15-source.zip'),head],['git','bundle','create',str(D/'RFP-COMPASS-Comp15.bundle'),'--all']]: subprocess.run(args,cwd=R,check=True)
blobs={}
for record in subprocess.check_output(['git','ls-tree','-r','-z',head],cwd=R).split(b'\0'):
    if record:
        fields,name=record.split(b'\t',1);blobs[name.decode()]=fields.decode().split()[2]
names=list(blobs)
with zipfile.ZipFile(D/'RFP-COMPASS-Comp15-source.zip') as z:
    assert z.testzip() is None
    assert {n.removeprefix('RFP-COMPASS-Comp15/') for n in z.namelist() if not n.endswith('/')}==set(names)
    for n in names:
        data=z.read('RFP-COMPASS-Comp15/'+n)
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==blobs[n],n
arts=['RFP-COMPASS-Comp15.bundle','RFP-COMPASS-Comp15-source.zip']
(D/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256((D/n).read_bytes()).hexdigest()+'  '+n+'\n' for n in arts))
(D/'PACKAGE.json').write_text(json.dumps({'commit':head,'kind':'unpublished review archive','published':False,'behavioral_acceptance':audit['behavioral_acceptance'],'raw_citation_perfection':audit['raw_citation_perfection'],'source_archive_files_verified':len(names),'artifacts':arts,'checksums':'SHA256SUMS.txt','status':'UNPUBLISHED: inspect route-repair/REPORT.md and FINAL_CHECK.json for behavioral and raw-copy limits'},indent=2))
print(json.dumps({'commit':head,'files_verified':len(names),'package':str(D),'published':False,'behavioral_acceptance':audit['behavioral_acceptance']}))
