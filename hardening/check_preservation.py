from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1];D=R/'hardening';m=json.loads((D/'preservation.json').read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for n,h in m['files'].items():assert sha(D/'history'/n if n in m['mutable_paths'] else R/n)==h,n
for n,h in m['artifacts'].items():assert sha(R/'dist/prior-scope-hardening'/n)==h,n
report={'prior_tracked_files_preserved':len(m['files']),'prior_delivery_files_preserved':len(m['artifacts']),'status':'PASS'}
(D/'preservation-check.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report))
