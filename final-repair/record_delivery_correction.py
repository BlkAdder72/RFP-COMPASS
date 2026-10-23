from pathlib import Path
import hashlib,json,shutil
R=Path(__file__).resolve().parents[1];D=R/'final-repair/delivery-attempt-1';D.mkdir(exist_ok=False)
names=['FAILED_VERIFICATION.json','RELEASE.json','SHA256SUMS.txt']
for n in names:shutil.copyfile(R/'dist/final-repair'/n,D/n)
m={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'dist/final-repair').iterdir() if p.is_file()};(D/'preservation.json').open('x').write(json.dumps(m,indent=2))
for name in ['README.md','results.md','packaging/COMPLIANCE.md','final-repair/REPORT.md','final-repair/write_reports.py','final-repair/package.py']:
 p=R/name;s=p.read_text(encoding='utf-8');s=s.replace('dist/final-repair/', 'dist/final-repair-verified/').replace("R/'dist/final-repair'", "R/'dist/final-repair-verified'")
 if name in ['results.md','final-repair/REPORT.md']:
  s+='\nThe first delivery attempt passed source/archive bytes, pristine clone bytes and preflights, but its offline audit could not create a historical scratch clone in the sandbox system temp directory. That failed delivery and raw error are preserved under `dist/final-repair/` and `final-repair/delivery-attempt-1/`. The audit now uses a verified workspace scratch path; no test assertion or model result changed. Current delivery is `dist/final-repair-verified/`.\n'
 p.write_text(s,encoding='utf-8',newline='\n')
p=R/'final-repair/AUDIT_NOTES.md';s=p.read_text(encoding='utf-8');s+='\nThe first sealed delivery at 4222f35 passed exact archive/pristine-clone checks and four runner preflights. Its offline audit failed before starting the historical checkout because the sandbox denied Git access to the system temporary directory; cleanup was also denied there. The complete failure JSON and old delivery remain untouched. Scratch work is now constrained to the clone’s verified .run-work directory with long-path Git support. No validation assertion is relaxed and no model is rerun. A new delivery path preserves the failed release rather than replacing it.\n';p.write_text(s,encoding='utf-8',newline='\n')
print('Preserved failed release and updated scratch-path audit/delivery references')
