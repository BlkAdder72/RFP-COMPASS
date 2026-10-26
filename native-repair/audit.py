"""Offline evidence audit. Integrity and behavioral acceptance are separate results."""
from pathlib import Path
import hashlib, json, re, subprocess, sys, tempfile, zipfile

D=Path(__file__).resolve().parent
R=D.parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def write(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
checks={}
inputs=read(D/'final-inputs.json')
checks['prompt_frozen']=sha(D/'prompt.txt')==inputs['prompt']['sha256']
for arm,files in inputs['knowledge'].items():
    for name,h in files.items():
        p=D/'inputs'/('original' if arm=='original' else 'repaired')/'translation-contract.md' if name=='bundle_sha256' else R/arm/name
        checks[f'frozen:{arm}:{name}']=sha(p)==h
for key,info in inputs['fixtures'].items(): checks['source:'+key]=sha(D/'inputs'/key/'source-packet.md')==info['sha256']
checks['questions_unchanged']=(R/'questions.md').read_bytes()==subprocess.check_output(['git','show','bfdd812:questions.md'],cwd=R)
checks['required_competition_layout']=all((R/n).exists() for n in ['original','feedback.md','rebuild','results.md','questions.md','run-original','run-rebuild'])
checks['rebuild_folder_layout']=all((R/'rebuild'/n).exists() for n in ['identity.md','rules.md','examples.md','reference','README.md'])
checks['questions_committed_before_rebuild']=not subprocess.check_output(['git','ls-tree','--name-only','be4d956b','rebuild'],cwd=R)
checks['judged_tag']=subprocess.check_output(['git','rev-parse','judged-original-comp13'],cwd=R).decode().strip()=='92847d2a17250fa18914d932826db63d99dcb75c'
checks['report_matches_root']=(R/'results.md').read_bytes()==(D/'REPORT.md').read_bytes()
for n in ['PROTOCOL.md','expectations.json','full-expectations.json','inputs.json','prompt.txt']:
    checks['protocol:'+n]=(D/n).read_bytes()==subprocess.check_output(['git','show','473b87dd:native-repair/'+n],cwd=R)
for a,b in [('473b87dd','d3318dff'),('d3318dff','3fe49304'),('3fe49304','b7cff67d'),('b7cff67d','745159d9'),('745159d9','b8f37d6a')]:
    checks['chronology:'+a+':'+b]=subprocess.run(['git','merge-base','--is-ancestor',a,b],cwd=R).returncode==0
pres=read(D/'preservation.json'); changed=[]; missing=[]; bad_snapshots=[]
print('Checking prior tracked file hashes',flush=True)
work=R/'.run-work';work.mkdir(exist_ok=True)
archive=Path(tempfile.mkdtemp(prefix='preservation-',dir=work))/'baseline.zip'
subprocess.run(['git','archive','--format=zip','-o',str(archive),pres['target']],cwd=R,check=True)
with zipfile.ZipFile(archive) as z:
    baseline_hashes={name:hashlib.sha256(z.read(name)).hexdigest() for name in pres['tracked_sha256']}
checks['baseline_hashes_match_initial_inventory']=baseline_hashes==pres['tracked_sha256']
initial=read(D/'checkpoints/initial-full-file-preservation.json')
checks['initial_full_workspace_hash_audit_passed']=initial['passed'] and initial['prior_tracked_files_checked']==len(pres['tracked_sha256'])
diff_names=set(subprocess.check_output(['git','diff','--name-only','-z',pres['target'],'--'],cwd=R).decode().split('\0'))
for index,(name,h) in enumerate(pres['tracked_sha256'].items()):
    p=R/name
    if name in diff_names and not p.is_file(): missing.append(name); continue
    if name in diff_names:
        changed.append(name)
        before=D/'before'/name
        # Tools are preserved by the existing Git history; before/ holds product/docs.
        if name=='tools/verify_submission.py':
            old=subprocess.check_output(['git','show',pres['target']+':'+name],cwd=R)
            if hashlib.sha256(old).hexdigest()!=h: bad_snapshots.append(name)
        elif not before.is_file() or sha(before)!=h: bad_snapshots.append(name)
checks['prior_files_present']=not missing
checks['every_changed_prior_file_preserved']=not bad_snapshots
checks['old_evidence_unchanged']=not any(n.startswith(('original/','claude-native/','run-original/','run-rebuild/','warning-final/','dist/')) for n in changed)
pres_result={'method':'initial complete workspace SHA256 audit retained; all baseline Git blobs SHA256-checked against inventory; final git diff of index and working tree against baseline; every changed prior file verified against preserved before snapshot or Git','prior_source':pres['target'],'prior_tracked_files_checked':len(pres['tracked_sha256']),'unchanged':len(pres['tracked_sha256'])-len(changed)-len(missing),'changed_with_preserved_before_or_git':changed,'missing':missing,'unpreserved_changes':bad_snapshots,'passed':checks['baseline_hashes_match_initial_inventory'] and checks['initial_full_workspace_hash_audit_passed'] and not missing and not bad_snapshots and checks['old_evidence_unchanged']}
write(D/'preservation-check.json',pres_result)
print('Prior-file preservation checked',flush=True)
old=(D/'before/rebuild/tools/validate_packet.py').read_text(encoding='utf-8').split('def difference',1)[1]
new=(R/'rebuild/tools/validate_packet.py').read_text(encoding='utf-8').split('def difference',1)[1]
checks['strict_code_unchanged_except_advisory_call']=old==new.replace('likely_match(number, pattern, body)','pattern.search(body)')
inventory={}; chat_ids=[]
scores=read(D/'scores.json')
for arm in ('original','rebuild'):
    inventory[arm]={}
    for key in inputs['fixtures']:
        trial=D/'evidence'/arm/key
        trees='\n'.join(p.read_text(encoding='utf-8') for p in sorted(trial.glob('observed-tree*.txt')))
        ids=sorted(set(re.findall(r'https://claude.ai/chat/([a-f0-9-]+)',trees)))
        parts=sorted(trial.glob('raw-response-part-*.md')) or [trial/'raw-response.md']
        checks['trial:'+arm+':'+key]=len(ids)==1 and all(p.is_file() for p in parts)
        chat_ids.extend(ids)
        inventory[arm][key]={'chat_ids':ids,'raw_parts':[{'file':p.relative_to(D).as_posix(),'sha256':sha(p),'characters':len(p.read_text(encoding='utf-8')),'bullets':sum(l.startswith('- ') for l in p.read_text(encoding='utf-8').splitlines())} for p in parts]}
        score=scores['model_trials'][arm][key]
        checks['raw_status:'+arm+':'+key]=score['status'] in ('raw exported','refusal')
        derived=score['derived_export']
        if derived['strict_pass']:
            audit=read(trial/'derived-export/export-audit.json')
            checks['derived_raw_hash:'+arm+':'+key]=[x['raw_sha256'] for x in audit['parts']]==[sha(p) for p in parts]
            checks['derived_source_hash:'+arm+':'+key]=audit['source_sha256']==sha(D/'inputs'/key/'source-packet.md')
            checks['derived_same_routes:'+arm+':'+key]=derived['same_positions']
            checks['derived_output_hash:'+arm+':'+key]=all(sha(trial/'derived-export'/x['output'])==x['output_sha256'] for x in audit['parts'])
checks['20_unique_chats']=len(chat_ids)==20 and len(set(chat_ids))==20
checks['comparison_complete']=scores['comparison_complete']
checks['fresh_score_reproduction']=read(D/'reproducibility-check.json')['passed']
replays=read(D/'same-card-warning-replay.json')
checks['same_card_warning_repair']=len(replays)==4 and all(x['exit_code']==0 for x in replays) and all('S139' in x['stdout'] if x['version']=='before' else 'S139' not in x['stdout'] for x in replays)
checks['Q1_Q8_rebuild_pass']=all(v['verdict']=='pass' for v in scores['frozen_questions']['rebuild'].values())
for stage in ['C1-citation-retest','C4-final-export','C3-warning']:
    rows=read(D/'stages'/stage/'results.json'); checks['local:'+stage]=all(x['passed'] for x in rows)
sample=read(D/'stages/C2-sample-alignment/sample-validation.json')
checks['sample_alignment']=sample['exit_code']==0 and sample['roundtrip']
write(D/'trial-inventory.json',inventory)
result={'integrity_pass':all(checks.values()),'checks':checks,'behavioral_acceptance':all(x['semantic_pass'] and x['derived_export']['strict_pass'] for x in scores['model_trials']['rebuild'].values()),'raw_citation_perfection':all(x['strict_pass'] for x in scores['model_trials']['rebuild'].values()),'published':False}
write(D/'FINAL_CHECK.json',result)
print(json.dumps({'integrity_pass':result['integrity_pass'],'failed_integrity_checks':[k for k,v in checks.items() if not v],'behavioral_acceptance':result['behavioral_acceptance'],'raw_citation_perfection':result['raw_citation_perfection'],'prior_files_checked':len(pres['tracked_sha256']),'published':False},indent=2))
assert result['integrity_pass']
