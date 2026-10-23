"""Point historical hash checks at preserved code; execute current checks in a new log directory."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1];D=R/'hardening'
current=(R/'rebuild/tools/validate_packet.py').read_bytes();C=D/'candidates';C.mkdir(exist_ok=True)
(C/'final.py').write_bytes(current)
initial=current.replace(b'activities|schedules?|calendars?',b'activities|schedule')
expected=next(c['validator_sha256'] for c in json.loads((D/'after/results.json').read_text())['cases'] if c['arm']=='rebuild')
assert hashlib.sha256(initial).hexdigest()==expected
(C/'initial.py').write_bytes(initial)
p=R/'revision/verify.py';t=p.read_text(encoding='utf-8')
t=t.replace("assert sha(R/case['arm']/'tools/validate_packet.py')==case['validator_sha256']", "assert sha((R/'hardening/history/rebuild/tools/validate_packet.py') if case['arm']=='rebuild' else R/'original/tools/validate_packet.py')==case['validator_sha256']")
p.write_text(t,encoding='utf-8')
p=R/'packaging/final_compliance.py';t=p.read_text(encoding='utf-8')
t=t.replace("assert sha(R/'rebuild/tools/validate_packet.py')==next", "assert sha(R/'hardening/history/rebuild/tools/validate_packet.py')==next")
t=t.replace("logs=P/'final-checks-v2'", "logs=P/'final-checks-v3'")
t=t.replace("(P/'final-compliance.json').write_text", "hardening_audit=subprocess.run([sys.executable,str(R/'hardening/verify.py')],cwd=R,capture_output=True,text=True,encoding='utf-8')\nassert hardening_audit.returncode==0,hardening_audit.stdout+hardening_audit.stderr\nresult['hardening']=json.loads((R/'hardening/verification.json').read_text(encoding='utf-8'))\nresult['total_raw_model_responses']+=result['hardening']['fresh_model_turns']\n(P/'final-compliance.json').write_text")
p.write_text(t,encoding='utf-8');(R/'tools/verify_submission.py').write_text(t,encoding='utf-8')
print('Historical hash checks now use byte-preserved prior code; no old test logs overwritten.')
