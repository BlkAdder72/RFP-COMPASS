"""Build local delivery artifacts from committed HEAD; do not publish."""
from pathlib import Path
import subprocess,hashlib,json
import zipfile
R=Path(__file__).resolve().parents[1];D=R/'dist';D.mkdir(exist_ok=True)
assert not subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=R).strip(),'Commit tracked changes first'
bundle=D/'RFP-COMPASS-Comp15.bundle';archive=D/'RFP-COMPASS-Comp15-source.zip'
assert not bundle.exists() and not archive.exists(),'Refusing to overwrite delivery artifacts'
subprocess.run(['git','bundle','create',str(bundle),'--all'],cwd=R,check=True)
subprocess.run(['git','bundle','verify',str(bundle)],cwd=R,check=True)
subprocess.run(['git','archive','--format=zip','--prefix=RFP-COMPASS-Comp15/','--output='+str(archive),'HEAD'],cwd=R,check=True)
tracked=[n for n in subprocess.check_output(['git','ls-tree','-r','--name-only','-z','HEAD'],cwd=R).decode().split('\0') if n]
with zipfile.ZipFile(archive) as z:
    actual={n.removeprefix('RFP-COMPASS-Comp15/') for n in z.namelist() if not n.endswith('/')}
    assert actual==set(tracked),'Archive file set mismatch'
    for name in tracked:assert z.read('RFP-COMPASS-Comp15/'+name)==(R/name).read_bytes(),'Archive bytes differ: '+name
lines=[hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name for p in (bundle,archive)]
(D/'SHA256SUMS.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(D/'RELEASE.json').write_text(json.dumps({'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),
                                        'published':False,'source_archive_files_verified':len(tracked),
                                        'artifacts':[p.name for p in (bundle,archive)],'checksums':'SHA256SUMS.txt'},indent=2),encoding='utf-8')
print('\n'.join(lines))
