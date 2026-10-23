from pathlib import Path
import hashlib,importlib.util,json,subprocess,sys
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[1];D=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((D/'preservation.json').read_text());assert m['target']=='06fcebace08c19410b63f1cd8c2523f66822d18b'
for n,h in m['files'].items():assert sha(R/n)==h,'Pre-review source/evidence changed: '+n
for n,h in m['artifacts'].items():assert sha(R/n)==h,'Sealed artifact changed: '+n
assert (R/'questions.md').read_bytes()==subprocess.check_output(['git','show','bfdd812:questions.md'],cwd=R)
spec=importlib.util.spec_from_file_location('runner',R/'tools/run_arm.py');runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)
turns=0
for arm in ['original','rebuild']:
 base=D/('run-'+arm);env=json.loads((base/'environment.json').read_text())
 for name,h in env['knowledge_sha256'].items():assert sha(R/arm/name)==h
 for fixture in sorted((D/'fixtures').glob('*.md')):
  trial=base/fixture.stem;assert (trial/'request.txt').read_text(encoding='utf-8')==runner.request(R,arm,fixture)
  cmd=json.loads((trial/'command.json').read_text());assert cmd[cmd.index('-m')+1]=='gpt-6-astra' and cmd[cmd.index('-c')+1]=='model_reasoning_effort="medium"'
  events=[json.loads(l) for l in (trial/'events.jsonl').read_text(encoding='utf-8').splitlines()];assert events[-1]['type']=='turn.completed';assert (trial/'exit-code.txt').read_text()=='0'
  msgs=[e['item']['text'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message'];assert msgs==[(trial/'bid-compliance-card.md').read_text(encoding='utf-8')]
  assert all(e.get('item',{}).get('type') in [None,'agent_message','reasoning'] for e in events);turns+=1
delivery=json.loads((D/'delivery-summary.json').read_text());assert delivery['passed'] and not delivery['published']
models=json.loads((D/'model-results.json').read_text());controls=json.loads((D/'control-results.json').read_text());semantics=json.loads((D/'full-semantic-results.json').read_text())
out={'evidence_integrity':'PASS','sealed_target':m['target'],'preserved_tracked_files':len(m['files']),'preserved_sealed_files':len(m['artifacts']),'frozen_questions_unchanged':True,'new_raw_model_replies':turns,'all_new_model_copies_exact':all(c['strict_fidelity_pass'] for a,d in models.items() for c in d.values()),'new_warning_regressions':[c['case'] for c in controls if c['arm']=='rebuild' and not c['passed'] and any(o['case']==c['case'] and o['arm']=='original' and o['passed'] for o in controls)],'remaining_rebuilt_failures':[c for c in controls if c['arm']=='rebuild' and not c['passed']],'retrospective_full_rebuild_missing_required':semantics['arms']['rebuild']['missing_required'],'new_semantic_full_regressions':semantics['new_regressions'],'delivery_compliance':delivery,'candidate_edited':False,'published':False}
(D/'verification.json').open('x',encoding='utf-8').write(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
