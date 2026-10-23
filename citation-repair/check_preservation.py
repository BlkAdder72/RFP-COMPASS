from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1];D=R/'citation-repair'
m=json.loads((D/'preservation.json').read_text(encoding='utf-8'));extra=json.loads((D/'additional-mutable-paths.json').read_text(encoding='utf-8'))['paths']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for n,h in m['files'].items():assert sha(D/'history'/n if n in m['mutable_paths']+extra else R/n)==h,n
for n,h in m['artifacts'].items():assert sha(R/'dist/prior-citation-repair'/n)==h,n
for n,h in json.loads((D/'attempt-1/hashes.json').read_text(encoding='utf-8')).items():assert sha(D/'attempt-1'/n)==h,n
report={'status':'PASS','pre_stage_tracked_files_preserved':len(m['files']),'prior_delivery_files_preserved':len(m['artifacts']),'first_failed_attempt_snapshots':'PASS','both_validators_unchanged':all(sha(R/a/'tools/validate_packet.py')==m['files'][a+'/tools/validate_packet.py'] for a in ('original','rebuild'))}
(D/'preservation-check.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report))
