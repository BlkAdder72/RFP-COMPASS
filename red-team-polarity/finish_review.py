from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parents[1];D=Path(__file__).resolve().parent
def read(n):return json.loads((D/n).read_text(encoding='utf-8'))
def put(n,x):(D/n).open('x',encoding='utf-8').write(json.dumps(x,ensure_ascii=False,indent=2))
r=read('control-results.json');by={a:{x['case']:x for x in r if x['arm']==a} for a in ['original','pre-polarity','rebuild']}
assert len(r)==72 and all(len(v)==24 for v in by.values())
assert {a:sum(x['passed'] for x in v.values()) for a,v in by.items()}=={'original':14,'pre-polarity':18,'rebuild':14}
def comparison(a):
 c={'improved':[],'regressed':[],'tied':[]}
 for n,x in by['rebuild'].items():
  old=by[a][n]['passed'];new=x['passed'];c['tied' if old==new else 'improved' if new else 'regressed'].append(n)
 return c
assert len(comparison('pre-polarity')['regressed'])==6 and len(comparison('pre-polarity')['improved'])==2
assert len(comparison('original')['regressed'])==3 and len(comparison('original')['improved'])==3
models=read('model-results.json');assert all(x['strict_fidelity_pass'] for v in models.values() for x in v.values());assert all(x['semantic_pass'] for x in models['rebuild'].values())
assert all(sum(x['passed_all_checks'] for x in v.values())==2 for v in models.values())
old=read('prior-control-replay.json');assert old['passed'] and old['total']==120
for n in ['preservation-verification.json','frozen-and-baseline-verification.json','model-audit.json','delivery-summary.json']:assert read(n)['passed'],n
full=read('full-recheck.json');assert full['arms']['rebuild']['exit_code']==0 and not full['arms']['rebuild']['missing_required'] and not full['arms']['rebuild']['forbidden_found'] and all(full['arms']['rebuild']['noise_only12'].values())
changed=subprocess.check_output(['git','diff','--name-only','21dd85b'],cwd=R).decode().splitlines();assert all(n.startswith('red-team-polarity/') for n in changed),changed
put('SUMMARY.json',{'date':'2026-10-25','recommendation':'HOLD — seven open finding families; no repair or publication in this review','sealed_target':read('preservation.json')['target'],'freeze':'efb167b','original_baseline':'4569421','rebuild_raw':'ca72f84','new_controls':{a:{'passed':sum(x['passed'] for x in v.values()),'total':len(v)} for a,v in by.items()},'vs_preceding':comparison('pre-polarity'),'vs_original':comparison('original'),'new_failed_controls':[n for n,x in by['rebuild'].items() if not x['passed']],'prior_controls':{'passed':120,'total':120},'current_combined_controls':{'passed':134,'total':144},'fresh_model_turns':6,'model_strict_copy_all_pass':True,'model_selected_semantics':{'original':{'passed':2,'total':3},'rebuild':{'passed':3,'total':3}},'model_combined_checks':{'original':{'passed':2,'total':3},'rebuild':{'passed':2,'total':3}},'fresh_full_length_model_calls':0,'existing_rebuilt_full_read_only_replay_pass':True,'prior_tracked_files_preserved':27050,'sealed_files_preserved':47,'new_review_in_old_zip':False,'new_delivery_created':False,'sealed_delivery_audit_pass':True,'published':False})
manifest={str(p.relative_to(D)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(D.rglob('*')) if p.is_file()}
put('EVIDENCE_SHA256.json',{'algorithm':'sha256','scope':'Every red-team-polarity file except this manifest itself; earlier files and sealed artifacts are independently covered by preservation.json','files':manifest})
print('PASS final review assertions and evidence manifest:',len(manifest),'files')
