from pathlib import Path
import shutil,json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'hardening';O=D/'full-first-pass';O.mkdir(exist_ok=False)
names=['hardening/full-length-results.json','hardening/REPORT.md','results.md','README.md','SUBMISSION_COMMENT.md','packaging/COMPLIANCE.md','rebuild/README.md']
for arm in ('original','rebuild'):
 names += ['run-'+arm+'/hardening-full/'+n for n in ['validation-command.json','validation.txt','validation-stderr.txt','validation-exit.txt']]
for n in names:
 p=O/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(R/n,p)
shutil.copyfile(R/'rebuild/tools/validate_packet.py',D/'candidates/third.py')
(O/'AUDIT-NOTE.md').write_text('First-pass complete paired full-length test: original exact structure PASS, six personal leaks; rebuild all personal only12 but S072 anchor wrong in two citations. Both FAIL cases and reports preserved before separating personal hint trust by statement. The earlier combined audit correctly refused its then-assumption that the full rebuilt card passed. No raw model response is repaired or retried.\n',encoding='utf-8')
(O/'hashes.json').write_text(json.dumps({n:hashlib.sha256((R/n).read_bytes()).hexdigest() for n in names},indent=2),encoding='utf-8')
