"""Freeze prior bytes and the new challenge before changing the candidate."""
from pathlib import Path
import hashlib,json,subprocess,shutil
R=Path(__file__).resolve().parents[1];D=R/'hardening'
if (D/'preservation.json').exists():raise SystemExit('Refusing existing preservation manifest before any writes')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
names=subprocess.check_output(['git','ls-files','-z'],cwd=R).decode().split('\0');names=[n for n in names if n]
mutable=['rebuild/tools/validate_packet.py','rebuild/README.md','README.md','results.md','packaging/COMPLIANCE.md','tools/verify_submission.py','packaging/final_compliance.py','packaging/final-compliance.json','revision/verify.py','revision/verification.json','SUBMISSION_COMMENT.md']
for n in mutable:
 p=D/'history'/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(R/n,p)
(D/'preservation.json').write_text(json.dumps({'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),'mutable_paths':mutable,'files':{n:sha(R/n) for n in names},'artifacts':{p.name:sha(p) for p in (R/'dist').iterdir() if p.is_file()}},indent=2),encoding='utf-8')
base=R/'original/samples/04-real-tbrpc-auditing-rfp/source-packet.md';F=D/'fixtures';F.mkdir()
noise=[('calendar.txt line 1','Personal calendar:'),('calendar.txt line 2','Our retirement lunch is February 3, 2027, at 12:00 PM.'),('calendar.txt line 3','My physical therapy appointment is March 4, 2027, at 9:00 AM.'),('calendar.txt line 4','Our family reunion is April 5, 2027, at 4:00 PM.'),('calendar.txt line 5','My birthday dinner is May 6, 2027, at 7:00 PM; my share is $20.'),('calendar.txt line 6','For my birthday dinner, email me at alex@example.net.'),('calendar.txt line 7','My dentist appointment is June 7, 2027, at 10:00 AM.')]
(D/'calendar.txt').write_text('\n'.join(b for a,b in noise)+'\n',encoding='utf-8')
(F/'Z-full-length-noisy.md').write_bytes(base.read_bytes()+('\n'+'\n'.join(f'S{215+i:03d} | {a} | {b}' for i,(a,b) in enumerate(noise))+'\n').encode())
(D/'full-length-expectations.json').write_text(json.dumps({'base_packet':str(base.relative_to(R)),'base_sha256':sha(base),'original_statements':214,'total_statements':221,'noise_source':'hardening/calendar.txt','noise_only12':[f'S{i:03d}' for i in range(215,222)],'routing':{'S089':[5],'S103':[7],'S114':[6],'S133':[2,8,11],'S209':[9]},'checks':['all 221 exact statements covered','all twelve headings and exact anchors','continuations preserved; no repairing outputs','no personal date, money or contact REVIEW hints'],'provenance':'214 original packet statements unchanged; seven synthetic calendar statements appended. Not a new real-world attachment or independent holdout.'},indent=2),encoding='utf-8')
print('Frozen',len(names),'prior tracked files; full fixture SHA256',sha(F/'Z-full-length-noisy.md'))
