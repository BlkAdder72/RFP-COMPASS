"""Check the frozen candidate and available evidence without calling any model.

PASS here means offline integrity only. Incomplete native trials always block
submission readiness. All output is written into a new directory.
"""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,zipfile
R=Path(__file__).resolve().parents[1];D=R/'route-repair'
p=argparse.ArgumentParser();p.add_argument('--output-dir',required=True,type=Path)
p.add_argument('--require-complete',action='store_true');args=p.parse_args()
O=args.output_dir.resolve();O.mkdir(parents=True,exist_ok=False)
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
x=read(D/'final-inputs.json');checks={};commands=[]
def run(label,cmd):
 v=subprocess.run(cmd,cwd=R,capture_output=True,text=True,encoding='utf-8')
 commands.append(dict(label=label,command=cmd,exit_code=v.returncode,stdout=v.stdout,stderr=v.stderr))
 checks[label]=v.returncode==0
 return v
for arm,files in x['knowledge'].items():
 for n,h in files.items():
  checks['frozen:'+arm+':'+n]=sha(D/'inputs'/arm/'translation-contract.md' if n=='bundle_sha256' else R/arm/n)==h
for k,v in x['fixtures'].items():
 checks['fixture:'+k]=sha(D/'inputs'/k/'source-packet.md')==v['sha256'] and sha(R/v['source'])==v['sha256']
for n in ['PROTOCOL.md','expectations.json','full-expectations.json','inputs.json','prompt.txt']:
 checks['protocol:'+n]=(D/n).read_bytes()==subprocess.check_output(['git','show','83da4078:route-repair/'+n],cwd=R)
checks['questions_frozen']=(R/'questions.md').read_bytes()==subprocess.check_output(['git','show','bfdd812:questions.md'],cwd=R)
checks['questions_before_rebuild']=not subprocess.check_output(['git','ls-tree','--name-only','be4d956b','rebuild'],cwd=R)
checks['judged_pin']=subprocess.check_output(['git','rev-parse','judged-original-comp13'],cwd=R).decode().strip()=='92847d2a17250fa18914d932826db63d99dcb75c'
checks['exporter_unchanged']=(R/'rebuild/tools/finalize_card.py').read_bytes()==(D/'before/rebuild/tools/finalize_card.py').read_bytes()
proof=read(R/'validator-note-repair/FINAL_INTEGRITY.json')
checks['authorized_validator_only_delta']=proof['passed'] and proof['checks']['only_new_private_patterns_and_support_changed'] and proof['after_sha256']==sha(R/'rebuild/tools/validate_packet.py') and proof['before_sha256']==sha(D/'before/rebuild/tools/validate_packet.py')
checks['feedback_unchanged']=(R/'feedback.md').read_bytes()==subprocess.check_output(['git','show','5e30129b:feedback.md'],cwd=R)
pres=read(D/'preservation.json')
run('baseline_archive',['git','archive','--format=zip','-o',str(O/'baseline.zip'),pres['target']])
with zipfile.ZipFile(O/'baseline.zip') as z:
 checks['all_baseline_blobs']=all(hashlib.sha256(z.read(n)).hexdigest()==h for n,h in pres['tracked_sha256'].items())
 checks['original_worktree_untouched']=all((R/n).is_file() and sha(R/n)==h for n,h in pres['tracked_sha256'].items() if n.startswith('original/'))
changed=[n for n in subprocess.check_output(['git','diff','--name-only','-z',pres['target'],'--'],cwd=R).decode().split('\0') if n in pres['tracked_sha256']]
checks['changed_prior_files_preserved']=all((D/'before'/n).is_file() and sha(D/'before'/n)==pres['tracked_sha256'][n] for n in changed)
checks['historical_evidence_untouched']=not any(n.startswith(('original/','claude-native/','native-repair/','warning-final/','hardening/','run-original/','run-rebuild/','dist/')) for n in changed)
run('samples',[sys.executable,'-B','-X','utf8','rebuild/tools/validate_packet.py'])
run('score',[sys.executable,'-B','-X','utf8','route-repair/score.py','--output-dir',str(O/'analysis')])
run('controls',[sys.executable,'-B','-X','utf8','route-repair/run_validations.py','--output-dir',str(O/'controls')])
for kind,count in [('export',17),('warning',216)]:
 rows=read(O/'controls'/(kind+'-results.json'))
 checks[kind+'_controls']=len(rows)==count and all(v['passed'] for v in rows)
s=read(O/'analysis/scores.json')
completed={a:sum(v['status'] in ('raw exported','refusal') for v in vs.values()) for a,vs in s['model_trials'].items()}
result=dict(scope='offline integrity and available evidence only; no native model acceptance implied',offline_integrity_pass=all(checks.values()),submission_ready=False,comparison_complete=s['comparison_complete'],completed_exports=completed,checks=checks,commands=commands,published=False,real_model_calls=0,baseline_files_checked=len(pres['tracked_sha256']),remaining=['Export existing fourth repaired response without regeneration','Seven further repaired native trials remain excluded by current instruction','Update final paired report and seal/verify final competition package after complete evidence'])
(O/'review.json').write_bytes(json.dumps(result,ensure_ascii=False,indent=2).encode('utf-8'))
print(json.dumps({k:v for k,v in result.items() if k not in ('checks','commands')},indent=2))
print('Failed offline checks:',[k for k,v in checks.items() if not v])
raise SystemExit(1 if not result['offline_integrity_pass'] else 2 if args.require_complete and not s['comparison_complete'] else 0)
