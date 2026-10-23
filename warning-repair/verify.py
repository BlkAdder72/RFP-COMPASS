from pathlib import Path
import hashlib,importlib.util,json,subprocess,sys
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[1];D=R/'warning-repair'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((D/'preservation.json').read_text())
for n,h in m['tracked'].items():assert sha(D/'before'/n if n in m['mutable'] else R/n)==h,n
assert (R/'questions.md').read_bytes()==subprocess.check_output(['git','show','bfdd812:questions.md'],cwd=R)
artifacts=[]
for n,h in m['artifacts'].items():
 if (R/n).exists():assert sha(R/n)==h;artifacts.append(n)
# Strict structural implementation after the warning filter is byte-identical.
a=(D/'before/rebuild/tools/validate_packet.py').read_text(encoding='utf-8');b=(R/'rebuild/tools/validate_packet.py').read_text(encoding='utf-8');assert a[a.index('def difference('):]==b[b.index('def difference('):]
spec=importlib.util.spec_from_file_location('core',R/'tools/run_arm.py');core=importlib.util.module_from_spec(spec);spec.loader.exec_module(core)
turns=0
for arm in ['original','rebuild']:
 for kind,folder in [('core',R/'fixtures'),('new',D/'fixtures'),('full',R/'hardening/fixtures')]:
  base=R/('run-'+arm)/('warning-repair-'+kind);env=json.loads((base/'environment.json').read_text());assert env['model']=='gpt-6-astra' and env['reasoning_effort']=='medium'
  for n,h in env['knowledge_sha256'].items():assert sha(R/arm/n)==h==m['tracked'][arm+'/'+n]
  parts=sorted(base.glob('part-*'),key=lambda p:int(p.name.split('-')[1])) if kind=='full' else [base/p.stem for p in sorted(folder.glob('*.md'))]
  if kind!='full':assert env['fixture_order']==[p.name for p in sorted(folder.glob('*.md'))]
  session=None
  for i,p in enumerate(parts):
   source=folder/('Z-full-length-noisy.md' if kind=='full' else p.name+'.md');prompt=core.request(R,arm,source) if kind!='full' or i==0 else 'continue'
   assert (p/'request.txt').read_text(encoding='utf-8')==prompt
   events=[json.loads(l) for l in (p/'events.jsonl').read_text(encoding='utf-8').splitlines()];assert events[-1]['type']=='turn.completed'
   assert all(e.get('item',{}).get('type') in [None,'agent_message','reasoning'] for e in events)
   messages=[e['item']['text'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message'];assert messages==[(p/'bid-compliance-card.md').read_text(encoding='utf-8')]
   cmd=json.loads((p/'command.json').read_text());assert cmd[cmd.index('-m')+1]=='gpt-6-astra' and cmd[cmd.index('-c')+1]=='model_reasoning_effort="medium"';assert (p/'exit-code.txt').read_text()=='0'
   if kind=='full':
    threads=[e['thread_id'] for e in events if e.get('type')=='thread.started']
    if i==0:assert len(threads)==1;session=threads[0]
    assert all(t==session for t in threads)
    if i:assert session in cmd
   turns+=1
  if kind=='full':assert (base/'bid-compliance-card.md').read_text(encoding='utf-8')=='\n'.join((p/'bid-compliance-card.md').read_text(encoding='utf-8') for p in parts)
controls=json.loads((D/'control-results.json').read_text());assert all(x['passed'] for x in controls if x['arm']=='rebuild')
replays=json.loads((D/'historical-control-replays.json').read_text());assert all(x['passed'] for x in replays if x['arm']=='rebuild')
print(json.dumps({'status':'PASS','preserved_prior_files':len(m['tracked']),'local_prior_artifacts_verified':len(artifacts),'raw_turns_verified':turns,'frozen_questions':'unchanged','strict_validation_implementation':'unchanged','six_model_knowledge_files_each_arm':'unchanged','published':False},indent=2))
