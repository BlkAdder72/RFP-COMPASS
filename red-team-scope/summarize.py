from pathlib import Path
import json,subprocess
D=Path(__file__).resolve().parent;R=D.parent
cs=json.loads((D/'control-results.json').read_text());ms=json.loads((D/'model-results.json').read_text())
x={'date':'2026-10-24','target':'3159bc2a93e7de52580c5445c15e7ac24d31eddd','verdict':'HOLD','findings':4,'current_failed_controls':[c['case'] for c in cs if c['arm']=='rebuild' and not c['passed']],'controls':{a:{'passed':sum(c['passed'] for c in cs if c['arm']==a),'total':14} for a in ['original','pre-scope','rebuild']},'models':{a:{'selected_semantics_pass':sum(t['semantic_pass'] for t in v.values()),'strict_fidelity_pass':sum(t['strict_fidelity_pass'] for t in v.values()),'all_checks_pass':sum(t['passed_all_checks'] for t in v.values()),'total':3} for a,v in ms.items()},'freeze_commit':'2666b8c','original_baseline_commit':'ebc22cf','candidate_changed':False,'published':False,'sealed_delivery_replaced':False}
(D/'SUMMARY.json').open('x').write(json.dumps(x,indent=2))
assert subprocess.check_output(['git','diff','3159bc2','--','original','rebuild','questions.md','results.md','README.md','SUBMISSION_COMMENT.md','tools'],cwd=R)==b''
print(json.dumps(x,indent=2))
