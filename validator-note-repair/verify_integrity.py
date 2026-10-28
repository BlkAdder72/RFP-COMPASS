"""Verify the authorized validator-only delta and preserve all prior evidence."""
from pathlib import Path
import argparse,ast,copy,hashlib,json,os,subprocess
R=Path(__file__).resolve().parents[1];D=R/'validator-note-repair'
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
assert not a.output.exists(),'Do not overwrite a verification receipt'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
before=D/'before/rebuild/tools/validate_packet.py';after=R/'rebuild/tools/validate_packet.py'
b=ast.parse(before.read_text(encoding='utf-8'));n=ast.parse(after.read_text(encoding='utf-8'))
added={'OWNERLESS_DENTIST_APPOINTMENT','PRIVATE_BIRTHDAY_CONTACT'}
def reduced(tree):
 tree=copy.deepcopy(tree)
 tree.body=[v for v in tree.body if not(isinstance(v,ast.Assign) and any(isinstance(t,ast.Name) and t.id in added for t in v.targets))]
 for v in tree.body:
  if isinstance(v,ast.FunctionDef) and v.name=='personal_hint_exclusions':
   v.body=[x for x in v.body if not(isinstance(x,ast.FunctionDef) and x.name=='personal_support')]
 return ast.dump(tree,include_attributes=False)
checks={'only_new_private_patterns_and_support_changed':reduced(b)==reduced(n),'exporter_unchanged':(R/'rebuild/tools/finalize_card.py').read_bytes()==(D/'before/rebuild/tools/finalize_card.py').read_bytes()}
x=json.loads((R/'route-repair/final-inputs.json').read_text())
for arm,files in x['knowledge'].items():
 for name,h in files.items():checks['model_contract:'+arm+':'+name]=sha(R/'route-repair/inputs'/arm/'translation-contract.md' if name=='bundle_sha256' else R/arm/name)==h
pres=json.loads((D/'preservation.json').read_text());changed=[];unpreserved=[]
portable=json.loads((D/'portability.json').read_text())['variants']
portable_ok=True
for name,v in portable.items():
 canonical=subprocess.check_output(['git','show',pres['commit']+':'+name],cwd=str(R)[4:] if os.name=='nt' and str(R).startswith('\\\\?\\') else R)
 snapshot=R/v['working_snapshot']
 portable_ok=portable_ok and sha(snapshot)==pres['tracked_sha256'][name]==v['prior_working_sha256'] and hashlib.sha256(canonical).hexdigest()==v['git_canonical_sha256'] and snapshot.read_bytes().replace(b'\r\n',b'\n')==canonical.replace(b'\r\n',b'\n')
 portable_ok=portable_ok and not name.startswith(('route-repair/evidence/','native-repair/evidence/','claude-native/evidence/'))
checks['canonical_variants_exactly_verified']=portable_ok
# Compare all prior tracked files in the working tree, including ignored-looking
# evidence paths. Allow changes only with their exact pre-update snapshot.
for name,h in pres['tracked_sha256'].items():
 if not(R/name).is_file() or sha(R/name) not in {h,portable.get(name,{}).get('git_canonical_sha256')}:
  changed.append(name)
  if not(D/'before'/name).is_file() or sha(D/'before'/name)!=h:unpreserved.append(name)
checks['every_changed_prior_file_preserved']=not unpreserved
checks['historical_and_raw_evidence_unchanged']=not any(v.startswith(('original/','claude-native/','native-repair/','warning-final/','route-repair/evidence/','route-repair/offline-review-2026-10-28/')) for v in changed)
for stage in ['baseline','stage-1-dentist','stage-2-contact']:
 s=json.loads((D/stage/'results.json').read_text());checks['stage:'+stage]=s['passed'] and len(s['records'])==263
 if stage!='baseline':checks['snapshot:'+stage]=sha(D/stage/'validate_packet.py')==s['validators']['candidate']['sha256']
for name in ['cli-comparison.json','historical-native-replay.json','reproducibility.json']:
 checks['supplement:'+name]=json.loads((D/name).read_text())['passed']
checks['report_mirror']=(R/'results.md').read_bytes()==(R/'route-repair/REPORT.md').read_bytes()
controls=D/'retained-controls'
for kind,count in [('export',17),('warning',216)]:
 rows=json.loads((controls/(kind+'-results.json')).read_text());checks['controls:'+kind]=len(rows)==count and all(v['passed'] for v in rows)
result={'passed':all(checks.values()),'checks':checks,'before_sha256':sha(before),'after_sha256':sha(after),'prior_commit':pres['commit'],'prior_files_checked':len(pres['tracked_sha256']),'changed_prior_files':changed,'unpreserved':unpreserved,'model_calls':0,'published':False,'submission_ready':False}
a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_bytes(json.dumps(result,indent=2).encode())
print(json.dumps({k:v for k,v in result.items() if k!='checks'}));assert result['passed'],[k for k,v in checks.items() if not v]
