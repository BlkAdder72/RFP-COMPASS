"""Audit preserved competition evidence; acceptance is distinct from integrity."""
from pathlib import Path
import json,hashlib,subprocess,re,zipfile,sys
D=Path(__file__).resolve().parent;R=D.parent
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
write=lambda p,v:p.write_text(json.dumps(v,indent=2,ensure_ascii=False),encoding='utf-8')
x=read(D/'final-inputs.json'); checks={};pres=read(D/'preservation.json')
for n in ['PROTOCOL.md','expectations.json','full-expectations.json','inputs.json','prompt.txt']:
 checks['frozen_protocol:'+n]=(D/n).read_bytes()==subprocess.check_output(['git','show','83da4078:route-repair/'+n],cwd=R)
checks['questions_unchanged']=(R/'questions.md').read_bytes()==subprocess.check_output(['git','show','bfdd812:questions.md'],cwd=R)
checks['questions_before_rebuild']=not subprocess.check_output(['git','ls-tree','--name-only','be4d956b','rebuild'],cwd=R)
checks['judged_original_pin']=subprocess.check_output(['git','rev-parse','judged-original-comp13'],cwd=R).decode().strip()=='92847d2a17250fa18914d932826db63d99dcb75c'
checks['required_layout']=all((R/n).exists() for n in ['original','feedback.md','questions.md','rebuild','results.md','run-original','run-rebuild'])
for arm,files in x['knowledge'].items():
 for name,h in files.items():checks['candidate:'+arm+':'+name]=sha(D/'inputs'/arm/'translation-contract.md' if name=='bundle_sha256' else R/arm/name)==h
for key,v in x['fixtures'].items():checks['source:'+key]=sha(D/'inputs'/key/'source-packet.md')==v['sha256']
checks['prompt']=sha(D/'prompt.txt')==x['prompt']['sha256']
checks['unchanged:tools/finalize_card.py']=(R/'rebuild/tools/finalize_card.py').read_bytes()==(D/'before/rebuild/tools/finalize_card.py').read_bytes()
proof=read(R/'validator-note-repair/FINAL_INTEGRITY.json')
checks['authorized_validator_only_delta']=proof['passed'] and proof['checks']['only_new_private_patterns_and_support_changed'] and proof['after_sha256']==sha(R/'rebuild/tools/validate_packet.py') and proof['before_sha256']==sha(D/'before/rebuild/tools/validate_packet.py')
for stage in ['R1-reservations','R2-submission-contacts','R3-commercial-forms']:checks['stage:'+stage]=read(D/'stages'/stage/'checks.json')['passed']
for a,b in [('83da4078','a9cc5cca'),('a9cc5cca','0d71781c'),('0d71781c','cdd3df64')]:checks['chronology:'+a+':'+b]=subprocess.run(['git','merge-base','--is-ancestor',a,b],cwd=R).returncode==0
work=R/'.run-work';work.mkdir(exist_ok=True);archive=work/'route-preservation-baseline.zip'
subprocess.run(['git','archive','--format=zip','-o',str(archive),pres['target']],cwd=R,check=True)
with zipfile.ZipFile(archive) as z:checks['all_baseline_git_hashes']=all(hashlib.sha256(z.read(n)).hexdigest()==h for n,h in pres['tracked_sha256'].items())
changed=[n for n in subprocess.check_output(['git','diff','--name-only','-z',pres['target'],'--'],cwd=R).decode().split('\0') if n in pres['tracked_sha256']];bad=[]
for n in changed:
 p=D/'before'/n
 if not p.is_file() or sha(p)!=pres['tracked_sha256'][n]:bad.append(n)
checks['every_changed_prior_file_preserved']=not bad
checks['old_evidence_unchanged']=not any(n.startswith(('original/','claude-native/','native-repair/','warning-final/','hardening/','run-original/','run-rebuild/','dist/')) for n in changed)
# Only new pointer subdirectories under run-* may be added; historical files must not change.
write(D/'preservation-check.json',{'method':'all baseline Git blobs SHA256 checked against frozen inventory; Git diff detects changed prior files; changed files match before snapshots; old evidence unchanged','prior_source':pres['target'],'prior_tracked_files_checked':len(pres['tracked_sha256']),'changed_with_preserved_before':changed,'unpreserved':bad,'passed':checks['all_baseline_git_hashes'] and checks['every_changed_prior_file_preserved'] and checks['old_evidence_unchanged']})
s=read(D/'analysis-final/scores.json');inventory={};ids=[]
for arm in ['original','rebuild']:
 inventory[arm]={}
 for key in x['fixtures']:
  t=D/'evidence'/arm/key;parts=sorted(t.glob('raw-response-part-*.md')) or ([t/'raw-response.md'] if (t/'raw-response.md').exists() else []);trees='\n'.join(p.read_text(encoding='utf-8') for p in t.glob('observed-tree*.txt'));chats=sorted(set(re.findall(r'https://claude.ai/chat/([a-f0-9-]+)',trees)));ids+=chats
  checks['trial:'+arm+':'+key]=len(chats)==1 and bool(parts)
  inventory[arm][key]={'chat_ids':chats,'raw_parts':[{'file':p.relative_to(D).as_posix(),'sha256':sha(p),'characters':len(p.read_text(encoding='utf-8')),'bullets':sum(l.startswith('- ') for l in p.read_text(encoding='utf-8').splitlines())} for p in parts]}
  result=s['model_trials'][arm][key];de=result.get('derived_export',{})
  if de.get('strict_pass'):
   p=D/'analysis-final/evidence'/arm/key/'derived-export';a=read(p/'export-audit.json');checks['export:'+arm+':'+key]=de['same_positions'] and a['source_sha256']==sha(D/'inputs'/key/'source-packet.md') and [v['raw_sha256'] for v in a['parts']]==[sha(f) for f in parts] and all(sha(p/v['output'])==v['output_sha256'] for v in a['parts'])
checks['22_unique_chats']=len(ids)==22 and len(set(ids))==22
checks['comparison_complete']=s['comparison_complete']
checks['score_reproducible']=read(D/'reproducibility-check.json')['passed']
for kind in ['export','warning']:checks['retained_controls:'+kind]=all(v['passed'] for v in read(D/'stages/R4-retained-validation'/(kind+'-results.json')))
checks['report_matches_root']=(D/'REPORT.md').read_bytes()==(R/'results.md').read_bytes()
write(D/'trial-inventory.json',inventory)
res={'integrity_pass':all(checks.values()),'checks':checks,'comparison_complete':s['comparison_complete'],'behavioral_acceptance':s['comparison_complete'] and all(v.get('expanded_semantic_pass',False) and v.get('derived_export',{}).get('strict_pass',False) for v in s['model_trials']['rebuild'].values()),'raw_citation_perfection':all(v.get('strict_pass',False) for v in s['model_trials']['rebuild'].values()),'published':False}
write(D/'FINAL_CHECK.json',res);print(json.dumps({k:v for k,v in res.items() if k!='checks'}));print('Failed integrity checks:',[k for k,v in checks.items() if not v]);assert res['integrity_pass']
