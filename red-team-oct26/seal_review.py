from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parents[1];D=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
# Validate the complete original baseline against Git, including every raw event.
count=0
for record in subprocess.check_output(['git','ls-tree','-r','-z','ac42a324','red-team-oct26/run-original'],cwd=R).split(b'\0'):
 if not record:continue
 meta,name=record.split(b'\t',1);data=(R/name.decode()).read_bytes()
 assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==meta.decode().split()[2]
 count+=1
assert count==22
audit=json.loads((D/'current-acceptance-recheck.json').read_text());assert audit['status']=='PASS'
assert json.loads((D/'delivery-checks.json').read_text())['all_prior_tracked_preserved']==37090
cases=json.loads((D/'control-results.json').read_text());assert len(cases)==54
summary=json.loads((D/'SUMMARY.json').read_text());assert summary['controls_vs_pre_repair']=={'improved':0,'tied':18,'regressed':0}
assert sum(not c['passed'] for c in cases if c['arm']=='rebuild')==6
manifest={str(p.relative_to(R)).replace('\\','/'):sha(p) for p in sorted(D.rglob('*')) if p.is_file() and p.name!='EVIDENCE_SHA256.json'}
(D/'EVIDENCE_SHA256.json').open('x',encoding='utf-8').write(json.dumps(manifest,indent=2))
for n,h in manifest.items():assert sha(R/n)==h
print(json.dumps({'review_files_verified':len(manifest),'original_baseline_files_unchanged':count,'candidate_and_prior_evidence':'preserved','publication':False}))
