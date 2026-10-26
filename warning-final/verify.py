"""Current repair acceptance; historical gates run unchanged at their own commits."""
from pathlib import Path
import hashlib,json,subprocess,importlib.util,sys,re
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[1];D=R/'warning-final'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=read(D/'preservation.json')
for n,h in m['tracked'].items():assert sha(D/'before'/n if n in m['mutable'] else R/n)==h,n
for n,h in m['artifacts'].items():
 if (R/n).exists():assert sha(R/n)==h,n
assert (R/'questions.md').read_bytes()==subprocess.check_output(['git','show','bfdd812:questions.md'],cwd=R)
old=(D/'before/rebuild/tools/validate_packet.py').read_bytes();current=(R/'rebuild/tools/validate_packet.py').read_bytes();assert old!=current
assert old.split(b'def difference',1)[1]==current.split(b'def difference',1)[1]
ch=read(D/'chronology.json')
for c in ch.values():assert subprocess.run(['git','merge-base','--is-ancestor',c,'HEAD'],cwd=R).returncode==0
assert subprocess.run(['git','merge-base','--is-ancestor',ch['freeze'],ch['original_baseline']],cwd=R).returncode==0
assert subprocess.check_output(['git','show',ch['original_baseline']+':rebuild/tools/validate_packet.py'],cwd=R)==old
assert subprocess.check_output(['git','show',ch['candidate']+':rebuild/tools/validate_packet.py'],cwd=R)==current
for n in ['PROTOCOL.md','expectations.json','full-expectations.json','control-definitions.json',*[str(p.relative_to(D)).replace('\\','/') for p in (D/'fixtures').glob('*.md')]]:assert subprocess.check_output(['git','show',ch['freeze']+':warning-final/'+n],cwd=R)==(D/n).read_bytes()
for record in subprocess.check_output(['git','ls-tree','-r','-z',ch['original_baseline']],cwd=R).split(b'\0'):
 if not record:continue
 meta,name=record.split(b'\t',1);n=name.decode()
 if n.startswith('run-original/warning-final-'):
  data=(R/n).read_bytes();assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==meta.decode().split()[2]
spec=importlib.util.spec_from_file_location('runner',R/'tools/run_arm.py');runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)
turns=0;transport=[]
for arm in ['original','rebuild']:
 for kind,folder in [('core',R/'fixtures'),('new',D/'fixtures'),('full',R/'hardening/fixtures')]:
  base=R/('run-'+arm)/('warning-final-'+kind);env=read(base/'environment.json');assert env['model']=='gpt-6-astra' and env['reasoning_effort']=='medium'
  for n,h in env['knowledge_sha256'].items():assert sha(R/arm/n)==h==m['tracked'][arm+'/'+n]
  ps=sorted(base.glob('part-*'),key=lambda p:int(p.name.split('-')[1])) if kind=='full' else [base/p.stem for p in sorted(folder.glob('*.md'))]
  if kind!='full':assert env['fixture_order']==[p.name for p in sorted(folder.glob('*.md'))]
  session=None
  for i,p in enumerate(ps):
   src=folder/('Z-full-length-noisy.md' if kind=='full' else p.name+'.md');assert (p/'request.txt').read_text(encoding='utf-8')==(runner.request(R,arm,src) if kind!='full' or i==0 else 'continue')
   cmd=read(p/'command.json');assert all(x in cmd for x in ['--ignore-user-config','--sandbox','read-only','gpt-6-astra','model_reasoning_effort="medium"'])
   ev=[json.loads(l) for l in (p/'events.jsonl').read_text(encoding='utf-8').splitlines()];assert ev[-1]['type']=='turn.completed' and all(e.get('item',{}).get('type') in [None,'reasoning','agent_message'] for e in ev)
   assert [e['item']['text'] for e in ev if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message']==[(p/'bid-compliance-card.md').read_text(encoding='utf-8')];assert (p/'exit-code.txt').read_text()=='0'
   ts=[e['thread_id'] for e in ev if e.get('type')=='thread.started']
   if kind=='full':
    if not i:assert len(ts)==1;session=ts[0]
    assert all(t==session for t in ts)
    if i:assert session in cmd
   retries=[l for l in (p/'stderr.txt').read_text(encoding='utf-8').splitlines() if 'retrying sampling request' in l]
   if retries:transport.append({'path':str(p.relative_to(R)).replace('\\','/'),'client_transport_retries':retries})
   turns+=1
  if kind=='full':assert env['fixture_sha256']==sha(R/'hardening/fixtures/Z-full-length-noisy.md');assert (base/'bid-compliance-card.md').read_text(encoding='utf-8')=='\n'.join((p/'bid-compliance-card.md').read_text(encoding='utf-8') for p in ps)
defs=read(D/'control-definitions.json');assert len(defs)==207
for number in range(1,5):
 stage=D/'stages'/('F'+str(number));out=read(stage/'results.json');assert out['passed_required'] and not out['failures_in_required_gate'];assert sha(stage/'validator.py')==out['validator_sha256']
 for c in defs:
  f=D/'stages/baseline'/c['name'];assert (f/'source-packet.md').read_text(encoding='utf-8')==c['source'] and (f/'card.md').read_text(encoding='utf-8')==c['card']
  for arm in ['original','before','rebuild']:
   expected=next(x for x in out['results'] if x['case']==c['name'] and x['arm']==arm)
   valid=expected['exit_code']==0;w=any('REVIEW' in l and 'Section 6' in l and c['sid'] in l for l in expected['stdout'].splitlines())
   assert expected['valid']==valid and expected['warning']==w
   assert expected['passed']==(valid==c['valid'] and (c['warning'] is None or w==c['warning']))
final=read(D/'stages/F4/results.json');assert not final['all_remaining_failures'] and final['validator_sha256']==sha(R/'rebuild/tools/validate_packet.py')
assert all(x['passed'] for x in read(D/'historical-control-replays-release.json') if x['arm']=='rebuild')
assert all(x['passed_all_checks'] for x in read(D/'model-results.json')['rebuild'].values())
assert read(D/'full-length-results.json')['rebuild']['passed']
assert all(x['verdict']=='pass' for x in read(D/'scores-final.json')['scores']['1']['rebuild'].values())
assert all(x['exit_code']==0 for x in read(D/'core-common-strict.json'))
assert read(D/'packaged-samples-validation.json')['exit_code']==0
parts=sorted((R/'run-rebuild/submission-repair-full').glob('part-*/bid-compliance-card.md'),key=lambda p:int(p.parent.name.split('-')[1]))
rejected=subprocess.run([sys.executable,'-B','-X','utf8',str(R/'rebuild/tools/validate_packet.py'),str(R/'hardening/fixtures/Z-full-length-noisy.md'),*[str(p) for p in parts]],capture_output=True,text=True,encoding='utf-8');assert rejected.returncode!=0 and 'S100' in rejected.stdout
base=R/'run-rebuild/warning-final-full';copy=R/'rebuild/run-results/warning-final-full'
for p in base.rglob('*'):
 if p.is_file():assert p.read_bytes()==(copy/p.relative_to(base)).read_bytes()
assert (D/'REPORT.md').read_bytes()==(R/'results.md').read_bytes()
assert len(read(D/'submission-plan.json')['sentences'])==3
assert (R/'SUBMISSION_COMMENT.md').read_text(encoding='utf-8').split('\n\n',1)[1].strip()==' '.join(read(D/'submission-plan.json')['sentences'])
if '--preseal' not in sys.argv:
 manifest=read(D/'EVIDENCE_SHA256.json')
 assert set(manifest)=={str(p.relative_to(R)).replace('\\','/') for p in D.rglob('*') if p.is_file() and p.name!='EVIDENCE_SHA256.json'}
 for n,h in manifest.items():assert sha(R/n)==h,n
print(json.dumps({'status':'PASS','behavioral_acceptance':'all recorded repair gates pass','manifest_check':'pending sealing' if '--preseal' in sys.argv else 'PASS','sequential_issues_tested':4,'controls':207,'raw_turns_verified':turns,'prior_files_preserved':len(m['tracked']),'old_sealed_artifacts':len(m['artifacts']),'frozen_questions':'unchanged','six_model_knowledge_files':'unchanged','strict_checks':'byte-identical','automatic_transport_retries':transport,'published':False},indent=2))
