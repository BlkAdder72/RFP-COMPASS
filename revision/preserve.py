from pathlib import Path
import subprocess,json,hashlib,shutil
R=Path(__file__).resolve().parents[1];D=R/'revision';target=D/'preservation.json'
assert not target.exists(),'Preservation already recorded'
names=[n for n in subprocess.check_output(['git','ls-files','-z'],cwd=R).decode().split('\0') if n]
mutable=['README.md','results.md','tools/run_arm.py','tools/verify_submission.py','packaging/final_compliance.py','packaging/COMPLIANCE.md',
         'rebuild/tools/validate_packet.py','rebuild/README.md','rebuild/REVIEWED_EXCLUSIONS.md','rebuild/run-results/rebuild-noisy-input/README.md',
         'SUBMISSION_COMMENT.md']
for name in mutable:
    dst=D/'history'/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(R/name,dst)
records={n:hashlib.sha256((R/n).read_bytes()).hexdigest() for n in names}
artifacts={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'dist').glob('*') if p.is_file()}
target.write_text(json.dumps({'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),
                             'mutable_paths':mutable,'files':records,'artifact_sha256':artifacts},indent=2),encoding='utf-8')
print(f'Preserved {len(records)} tracked-file hashes and {len(mutable)} working-file snapshots.')
