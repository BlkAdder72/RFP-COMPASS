"""Verify the completed native supplement without changing any model response."""
from pathlib import Path
import hashlib, json

D=Path(__file__).resolve().parent
R=D.parent
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
inputs=json.loads((D/'inputs.json').read_text(encoding='utf-8'))
checks={}
checks['frozen:prompt_file']=sha(D/'prompt.txt')==inputs['prompt']['sha256']
for arm, files in inputs['knowledge'].items():
    for name, digest in files.items():
        path=D/'inputs'/arm/'translation-contract.md' if name=='bundle_sha256' else R/arm/name
        checks[f'frozen:{arm}:{name}']=sha(path)==digest
for key, info in inputs['fixtures'].items():
    checks[f'frozen:{key}']=sha(D/'inputs'/key/'source-packet.md')==info['sha256']
scores=json.loads((D/'scores.json').read_text(encoding='utf-8'))
inventory=json.loads((D/'trial-inventory.json').read_text(encoding='utf-8'))
checks['18_trials_complete']=scores['comparison_complete'] and sum(len(v) for v in inventory.values())==18
for arm,trials in inventory.items():
    for key,trial in trials.items():
        checks[f'chat_identity:{arm}:{key}']=len(trial['chat_ids'])==1
        for part in trial['raw_parts']:
            checks['raw:'+part['file']]=sha(D/part['file'])==part['sha256']
checks['rebuilt_frozen_questions_pass']=all(v['verdict']=='pass' for v in scores['frozen_questions']['rebuild'].values())
full=scores['model_trials']['rebuild']['full-Z-full-length-noisy']
checks['full_strict_pass']=full['strict_pass'] and not full['literal_mismatches']
checks['full_failures_honestly_retained']={k for k,v in full['semantic_checks'].items() if not v}=={'S047_required','S048_required','S148_required'}
checks['citation_failures_honestly_retained']=all(not scores['model_trials'][arm]['new-C-opaque-citations']['strict_pass'] for arm in ('original','rebuild'))
checks['prior_preservation_pass']=json.loads((D/'preservation-check.json').read_text())['passed']
result={'checks':checks,'integrity_pass':all(checks.values()),'acceptance_pass':False,'publication':False}
(D/'FINAL_CHECK.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
assert result['integrity_pass'], [k for k,v in checks.items() if not v]
manifest={str(p.relative_to(D)).replace('\\','/'):sha(p) for p in sorted(D.rglob('*')) if p.is_file() and p!=D/'EVIDENCE_SHA256.json'}
(D/'EVIDENCE_SHA256.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
assert all(sha(D/name)==digest for name,digest in manifest.items())
print(json.dumps({'integrity_pass':True,'checks':len(checks),'manifest_files':len(manifest),'acceptance_pass':False,'published':False}))
