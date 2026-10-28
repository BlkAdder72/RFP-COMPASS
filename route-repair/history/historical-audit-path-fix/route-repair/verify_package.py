"""Verify the review bundle in a fresh checkout and retain complete command results."""
from pathlib import Path, PureWindowsPath
import argparse,hashlib,json,subprocess,sys,os
R=Path(__file__).resolve().parents[1]; D=R/'dist/route-repair-review'
meta=json.loads((D/'PACKAGE.json').read_text()); records=[]
parser=argparse.ArgumentParser()
parser.add_argument('--checkout-dir',type=Path,default=R/'.run-work/route-review-verified')
C=parser.parse_args().checkout_dir.resolve()
assert not C.exists(),'Fresh checkout path must not exist'
C.parent.mkdir(exist_ok=True)
def run(label,cmd,cwd,expected=0):
    r=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True,encoding='utf-8')
    records.append({'label':label,'command':cmd,'exit_code':r.returncode,'expected_exit_code':expected,'stdout':r.stdout,'stderr':r.stderr})
    (D/'PACKAGE_VERIFICATION.json').write_text(json.dumps({'status':'in progress','checks':records,'published':False},ensure_ascii=False,indent=2),encoding='utf-8')
    assert r.returncode==expected,(label,r.stdout,r.stderr)
    return r
for line in (D/'SHA256SUMS.txt').read_text().splitlines():
    h,n=line.split('  ',1);assert hashlib.sha256((D/n).read_bytes()).hexdigest()==h
run('bundle structure',['git','bundle','verify',str(D/'RFP-COMPASS-Comp15.bundle')],R)
run('fresh clone',['git','-c','core.longpaths=true','clone','--quiet','--no-checkout',str(D/'RFP-COMPASS-Comp15.bundle'),str(C)],R)
run('long path configuration',['git','config','core.longpaths','true'],C)
run('pinned checkout',['git','checkout','--quiet','--detach',meta['commit']],C)
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=C).decode().strip()==meta['commit']
F=Path(chr(92)*2+'?'+chr(92)+str(C)) if os.name=='nt' else C
manifest=json.loads((F/'route-repair/EVIDENCE_SHA256.json').read_text())
assert set(manifest)=={p.relative_to(F/'route-repair').as_posix() for p in (F/'route-repair').rglob('*') if p.is_file() and p!=F/'route-repair/EVIDENCE_SHA256.json'}
assert all(hashlib.sha256((F/'route-repair'/n).read_bytes()).hexdigest()==h for n,h in manifest.items())
run('fresh evidence integrity',[sys.executable,'-u','-B','-X','utf8','route-repair/audit.py'],C)
audit=json.loads((C/'route-repair/FINAL_CHECK.json').read_text())
assert audit['integrity_pass'] and audit['behavioral_acceptance']==meta['behavioral_acceptance']
run('four shipped samples',[sys.executable,'-B','-X','utf8','rebuild/tools/validate_packet.py'],C)
for row in json.loads((C/'native-repair/stages/C4-final-export/results.json').read_text(encoding='utf-8')):
    old=row['command']; oldroot=PureWindowsPath(old[4]).parents[2]
    args=[]
    for arg in old[5:]:
        try:arg=str(C.joinpath(*PureWindowsPath(arg).relative_to(oldroot).parts))
        except ValueError:pass
        args.append(arg)
    out=C/'.run-work/package-export-controls'/row['name']
    args[-1]=str(out)
    run('export control '+row['name'],[sys.executable,'-B','-X','utf8','rebuild/tools/finalize_card.py',*args],C,row['exit_code'])
    if row['exit_code']:
        assert (out/'REJECTED.json').is_file() and not (out/'part-01.md').exists()
    else:assert (out/'export-audit.json').is_file()
run('unchanged source status',['git','status','--porcelain'],C)
assert not records[-1]['stdout'], 'Verification must not alter tracked source'
(D/'PACKAGE_VERIFICATION.json').write_text(json.dumps({'status':'PASS integrity and reproducibility; inspect behavioral acceptance and raw citation limits','source_commit':meta['commit'],'checks':records,'behavioral_acceptance':audit['behavioral_acceptance'],'published':False},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'verified_commands':len(records),'fresh_clone':str(C),'integrity_pass':True,'behavioral_acceptance':audit['behavioral_acceptance'],'published':False}))
