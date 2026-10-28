"""Offline documentation, ICM and history checks; no model calls or output edits."""
from pathlib import Path
import argparse,hashlib,json,os,re,subprocess
R=Path(__file__).resolve().parents[1];D=R/'documentation-sync'
p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);a=p.parse_args();assert not a.output.exists()
cwd=str(R)[4:] if os.name=='nt' and str(R).startswith('\\\\?\\') else str(R)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old=json.loads((D/'preservation.json').read_text());checks={};allowed=set(old['before_documents'])
for arm,items in old['model_contract'].items():
 for n,h in items.items():
  path=R/'route-repair/inputs'/arm/'translation-contract.md' if n=='bundle_sha256' else R/arm/n
  checks['frozen_model:'+arm+':'+n]=sha(path)==h
checks['validator_unchanged']=sha(R/'rebuild/tools/validate_packet.py')==old['validator_sha256']
checks['exporter_unchanged']=sha(R/'rebuild/tools/finalize_card.py')==old['exporter_sha256']
tree={}
for row in subprocess.check_output(['git','ls-tree','-r','-z',old['prior_commit']],cwd=cwd).split(b'\0'):
 if row:
  meta,n=row.split(b'\t',1);tree[n.decode()]=meta.decode().split()[2]
checks['prior_inventory_exact']=set(tree)==set(old['canonical_tracked_sha256'])
# Verify all pinned baseline blobs once, deduplicating repeated historical files.
ids=list(dict.fromkeys(tree.values()));raw=subprocess.run(['git','cat-file','--batch'],cwd=cwd,input=''.join(h+'\n' for h in ids).encode(),capture_output=True,check=True).stdout
hashes={};pos=0
for oid in ids:
 end=raw.index(b'\n',pos);header=raw[pos:end].split();size=int(header[2]);pos=end+1;blob=raw[pos:pos+size];pos+=size+1
 assert header[0].decode()==oid and header[1]==b'blob';hashes[oid]=hashlib.sha256(blob).hexdigest()
checks['all_prior_canonical_blobs_preserved']=all(hashes[tree[n]]==h for n,h in old['canonical_tracked_sha256'].items())
changed=[n for n in subprocess.check_output(['git','diff','--name-only','-z',old['prior_commit'],'--'],cwd=cwd).decode().split('\0') if n in tree]
checks['only_authorized_current_docs_and_packaging_changed']=set(changed)<=allowed
before_ok=True
for n in changed:
 snapshot=D/'before'/n
 prior=subprocess.check_output(['git','show',old['prior_commit']+':'+n],cwd=cwd)
 before_ok=before_ok and snapshot.is_file() and snapshot.read_bytes().replace(b'\r\n',b'\n')==prior.replace(b'\r\n',b'\n')
checks['every_changed_file_has_exact_before_version']=before_ok
checks['historical_reports_and_raw_untouched']=not any(n.startswith(('original/','native-repair/','claude-native/','warning-final/','route-repair/evidence/','route-repair/offline-review-2026-10-28/')) for n in changed)
checks['required_layout']=all((R/n).exists() for n in ['original','rebuild','feedback.md','questions.md','results.md','run-original','run-rebuild'])
checks['report_mirror']=(R/'results.md').read_bytes()==(R/'route-repair/REPORT.md').read_bytes()
scores=json.loads((R/'validator-note-repair/analysis/scores.json').read_text());completed={arm:sum(v['status'] in ('raw exported','refusal') for v in rows.values()) for arm,rows in scores['model_trials'].items()}
checks['documented_export_counts']=completed=={'original':11,'rebuild':3} and not scores['comparison_complete']
checks['documented_question_verdicts']={k:v['verdict'] for k,v in scores['frozen_questions']['rebuild'].items()}=={k:('pending' if k in ('Q5','Q6') else 'pass') for k in ['Q'+str(i) for i in range(1,9)]}
docs=['README.md','rebuild/README.md','route-repair/RESUME.md','route-repair/CANDIDATE.md','results.md','route-repair/REPORT.md','packaging/COMPLIANCE.md','SUBMISSION_COMMENT.md','run-original/README.md','run-rebuild/README.md','validator-note-repair/REPORT.md','documentation-sync/REPORT.md']
bad_links=[]
for n in docs:
 path=R/n;text=path.read_text(encoding='utf-8')
 for target in re.findall(r'\]\(([^)]+)\)',text):
  if target.startswith(('https://','http://')):continue
  target=target.split('#',1)[0]
  if target and not(path.parent/target).exists():bad_links.append({'document':n,'target':target})
checks['current_document_links_exist']=not bad_links
inner=(R/'rebuild/README.md').read_text(encoding='utf-8')
checks['icm_responsibilities_explicit']=all(n in inner for n in ['identity.md','rules.md','examples.md','reference/','outside the model'])
checks['stale_current_claims_removed']=all(s not in (R/n).read_text(encoding='utf-8') for n,s in [('rebuild/README.md','Q1–Q8 and the full-RFP selected checks pass'),('route-repair/RESUME.md','No repaired-arm trial was sent'),('packaging/COMPLIANCE.md','PASS all recorded gates'),('route-repair/CANDIDATE.md','Validator and citation export are byte-identical')])
gate=subprocess.run([__import__('sys').executable,'-B','-X','utf8',str(R/'tools/verify_submission.py')],cwd=cwd,capture_output=True,text=True,encoding='utf-8')
checks['submission_gate_retains_hold']=gate.returncode==2
result={'passed':all(checks.values()),'checks':checks,'prior_commit':old['prior_commit'],'prior_files_checked':len(tree),'changed_prior_files':changed,'bad_links':bad_links,'completed_exports':completed,'model_calls':0,'published':False,'submission_ready':False,'submission_gate':{'exit_code':gate.returncode,'stdout':gate.stdout,'stderr':gate.stderr}}
a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_bytes(json.dumps(result,ensure_ascii=False,indent=2).encode());print(json.dumps({k:v for k,v in result.items() if k not in ('checks','submission_gate')}));assert result['passed'],[k for k,v in checks.items() if not v]
