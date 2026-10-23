from pathlib import Path
import hashlib,importlib.util,json,subprocess,sys
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[1];D=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((D/'preservation.json').read_text());assert m['target']=='09684fc7129b8ff4bcbefe4b749f644f8f23f50e'
for n,h in m['files'].items():assert sha(R/n)==h,n
for n,h in m['artifacts'].items():assert sha(R/n)==h,n
assert (R/'questions.md').read_bytes()==subprocess.check_output(['git','show','bfdd812:questions.md'])
assert (D/'reference/pre-warning-repair-validator.py').read_bytes()==subprocess.check_output(['git','show','06fcebace08c19410b63f1cd8c2523f66822d18b:rebuild/tools/validate_packet.py'])
spec=importlib.util.spec_from_file_location('runner',R/'tools/run_arm.py');runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)
turns=0
for arm in ['original','rebuild']:
 base=D/('run-'+arm);env=json.loads((base/'environment.json').read_text());assert env['model']=='gpt-6-astra' and env['reasoning_effort']=='medium';assert env['fixture_order']==[p.name for p in sorted((D/'fixtures').glob('*.md'))]
 for n,h in env['knowledge_sha256'].items():assert sha(R/arm/n)==h
 for fixture in sorted((D/'fixtures').glob('*.md')):
  trial=base/fixture.stem;assert (trial/'request.txt').read_text(encoding='utf-8')==runner.request(R,arm,fixture)
  cmd=json.loads((trial/'command.json').read_text());assert cmd[cmd.index('-m')+1]=='gpt-6-astra' and cmd[cmd.index('-c')+1]=='model_reasoning_effort="medium"'
  events=[json.loads(l) for l in (trial/'events.jsonl').read_text(encoding='utf-8').splitlines()];assert events[-1]['type']=='turn.completed';assert (trial/'exit-code.txt').read_text()=='0'
  msgs=[e['item']['text'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message'];assert msgs==[(trial/'bid-compliance-card.md').read_text(encoding='utf-8')];assert all(e.get('item',{}).get('type') in [None,'reasoning','agent_message'] for e in events);turns+=1
models=json.loads((D/'model-results.json').read_text());controls=json.loads((D/'control-results.json').read_text());delivery=json.loads((D/'delivery-summary.json').read_text());assert delivery['passed'] and not delivery['published']
regressions={a:[c['case'] for c in controls if c['arm']=='rebuild' and not c['passed'] and any(x['arm']==a and x['case']==c['case'] and x['passed'] for x in controls)] for a in ['original','pre-warning-repair']}
out={'integrity':'PASS','target':m['target'],'preserved_files':len(m['files']),'preserved_sealed_files':len(m['artifacts']),'new_model_replies':turns,'new_model_citation_pass':all(x['strict_fidelity_pass'] for a in models.values() for x in a.values()),'warning_regressions_against':regressions,'candidate_edited':False,'frozen_questions_unchanged':True,'sealed_delivery':delivery,'published':False}
(D/'verification.json').open('x').write(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
