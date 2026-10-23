from pathlib import Path
import hashlib,json,shutil
R=Path(__file__).resolve().parents[1];D=R/'final-repair/delivery-attempt-2';D.mkdir(exist_ok=False)
for n in ['FAILED_VERIFICATION.json','RELEASE.json','SHA256SUMS.txt']:shutil.copyfile(R/'dist/final-repair-verified'/n,D/n)
(D/'preservation.json').open('x').write(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'dist/final-repair-verified').iterdir() if p.is_file()},indent=2))
for name in ['README.md','results.md','packaging/COMPLIANCE.md','final-repair/REPORT.md','final-repair/write_reports.py','final-repair/package.py']:
 p=R/name;s=p.read_text(encoding='utf-8').replace('dist/final-repair-verified/','dist/release/').replace("R/'dist/final-repair-verified'","R/'dist/release'");p.write_text(s,encoding='utf-8',newline='\n')
note='\nThe second delivery attempt passed archive, clone-byte and preflight checks but exposed Windows path-length limits inside the nested historical clone. It is preserved at dist/final-repair-verified and final-repair/delivery-attempt-2. The historical Python entrypoint now uses an extended absolute Windows filename; Git long-path mode remains enabled. Scratch clones are kept under the verified ignored workspace path, so failed evidence is not removed by cleanup. No assertion, validator, model knowledge or model result changed.\n'
for name in ['final-repair/AUDIT_NOTES.md','results.md','final-repair/REPORT.md']:
 p=R/name;p.write_text(p.read_text(encoding='utf-8')+note,encoding='utf-8',newline='\n')
print('Second failed release preserved; current delivery path is dist/release')
