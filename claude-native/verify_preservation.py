from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parent
p=json.loads((D/'preservation.json').read_text())
bad=[name for name,h in p['tracked_sha256'].items() if not (R/name).is_file() or hashlib.sha256((R/name).read_bytes()).hexdigest()!=h]
result={'prior_source':p['target'],'prior_tracked_files_checked':len(p['tracked_sha256']),'mismatches':bad,'passed':not bad}
(D/'preservation-check.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result));assert not bad
