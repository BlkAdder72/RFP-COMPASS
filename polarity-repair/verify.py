from pathlib import Path
import hashlib,json,importlib.util,re,subprocess,sys
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[1];D=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((D/'preservation.json').read_text())
for n,h in m['tracked'].items():assert sha(D/'before'/n if n in m['mutable'] else R/n)==h,n
artifacts=[]
for n,h in m['artifacts'].items():
 if (R/n).exists():assert sha(R/n)==h;artifacts.append(n)
assert (R/'questions.md').read_bytes()==subprocess.check_output(['git','show','bfdd812:questions.md'],cwd=R)
a=(D/'before/rebuild/tools/validate_packet.py').read_bytes();b=(R/'rebuild/tools/validate_packet.py').read_bytes();assert a[a.index(b'def difference('):]==b[b.index(b'def difference('):]
ch=json.loads((D/'chronology.json').read_text())
for c in ch.values():assert subprocess.run(['git','merge-base','--is-ancestor',c,'HEAD'],cwd=R).returncode==0
assert subprocess.check_output(['git','show',ch['original_baseline']+':rebuild/tools/validate_packet.py'],cwd=R)==a
assert subprocess.check_output(['git','show',ch['candidate']+':rebuild/tools/validate_packet.py'],cwd=R)==b
for older,newer in [('freeze','original_baseline'),('original_baseline','candidate')]:assert subprocess.run(['git','merge-base','--is-ancestor',ch[older],ch[newer]],cwd=R).returncode==0
for record in subprocess.check_output(['git','ls-tree','-r','-z',ch['original_baseline']],cwd=R).split(b'\0'):
 if not record:continue
 meta,name=record.split(b'\t',1);n=name.decode()
 if n.startswith('run-original/polarity-repair-'):
  data=(R/n).read_bytes();assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==meta.decode().split()[2],n
for n in ['PROTOCOL.md','expectations.json','full-expectations.json','control-definitions.json',*[str(p.relative_to(D)).replace('\\','/') for p in (D/'fixtures').glob('*.md')]]:assert subprocess.check_output(['git','show',ch['freeze']+':polarity-repair/'+n],cwd=R)==(D/n).read_bytes()
spec=importlib.util.spec_from_file_location('runner',R/'tools/run_arm.py');runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)
turns=0
for arm in ['original','rebuild']:
 for kind,folder in [('core',R/'fixtures'),('new',D/'fixtures'),('full',R/'hardening/fixtures')]:
  base=R/('run-'+arm)/('polarity-repair-'+kind);env=json.loads((base/'environment.json').read_text());assert env['model']=='gpt-6-astra' and env['reasoning_effort']=='medium'
  for n,h in env['knowledge_sha256'].items():assert sha(R/arm/n)==h==m['tracked'][arm+'/'+n]
  ps=sorted(base.glob('part-*'),key=lambda p:int(p.name.split('-')[1])) if kind=='full' else [base/p.stem for p in sorted(folder.glob('*.md'))]
  if kind!='full':assert env['fixture_order']==[p.name for p in sorted(folder.glob('*.md'))]
  session=None
  for i,p in enumerate(ps):
   src=folder/('Z-full-length-noisy.md' if kind=='full' else p.name+'.md');prompt=runner.request(R,arm,src) if kind!='full' or i==0 else 'continue';assert (p/'request.txt').read_text(encoding='utf-8')==prompt
   cmd=json.loads((p/'command.json').read_text());assert '--ignore-user-config' in cmd and '--sandbox' in cmd and 'read-only' in cmd and 'gpt-6-astra' in cmd and 'model_reasoning_effort="medium"' in cmd
   events=[json.loads(l) for l in (p/'events.jsonl').read_text(encoding='utf-8').splitlines()];assert events[-1]['type']=='turn.completed';assert all(e.get('item',{}).get('type') in [None,'reasoning','agent_message'] for e in events)
   msgs=[e['item']['text'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message'];assert msgs==[(p/'bid-compliance-card.md').read_text(encoding='utf-8')];assert (p/'exit-code.txt').read_text()=='0'
   if kind=='full':
    ts=[e['thread_id'] for e in events if e.get('type')=='thread.started']
    if not i:assert len(ts)==1;session=ts[0]
    assert all(t==session for t in ts)
    if i:assert session in cmd
   turns+=1
  if kind=='full':assert env['fixture_sha256']==sha(R/'hardening/fixtures/Z-full-length-noisy.md');assert (base/'bid-compliance-card.md').read_text(encoding='utf-8')=='\n'.join((p/'bid-compliance-card.md').read_text(encoding='utf-8') for p in ps)
controls=json.loads((D/'control-results.json').read_text());defs=json.loads((D/'control-definitions.json').read_text(encoding='utf-8'))
assert len(defs)==116 and all(c['passed'] for c in controls if c['arm']=='rebuild')
for c in defs:
 f=D/'controls'/c['name'];assert (f/'source-packet.md').read_text(encoding='utf-8')==c['source'] and (f/'card.md').read_text(encoding='utf-8')==c['card']
 for arm in ['original','rebuild']:
  p=subprocess.run([sys.executable,'-B','-X','utf8',str(R/arm/'tools/validate_packet.py'),str(f/'source-packet.md'),str(f/'card.md')],capture_output=True,text=True,encoding='utf-8');w=any('REVIEW' in l and 'Section 6' in l and c['sid'] in l for l in p.stdout.splitlines());v=next(x for x in controls if x['case']==c['name'] and x['arm']==arm);assert v['valid']==(p.returncode==0) and v['warning']==w
replays=json.loads((D/'historical-control-replays.json').read_text());assert all(c['passed'] for c in replays if c['arm']=='rebuild')
same=json.loads((D/'same-card-warning-replay.json').read_text());assert 'S003, S006, S008' in same['before']['stdout'] and 'REVIEW' not in same['after']['stdout'];assert same['before']['source_sha256']==same['after']['source_sha256']==sha(R/'red-team-guard/fixtures/B-negated-scope-and-private-headings.md');assert same['before']['card_sha256']==same['after']['card_sha256']==sha(R/'red-team-guard/run-rebuild/B-negated-scope-and-private-headings/bid-compliance-card.md');assert same['after']['validator_sha256']==sha(R/'rebuild/tools/validate_packet.py')
base=R/'run-rebuild/polarity-repair-full';copy=R/'rebuild/run-results/polarity-repair-full'
for f in base.rglob('*'):
 if f.is_file():assert f.read_bytes()==(copy/f.relative_to(base)).read_bytes(),str(f)
assert (copy/'.gitattributes').read_text().strip()=='* -text'
plan=json.loads((D/'submission-plan.json').read_text(encoding='utf-8'));comment=(R/'SUBMISSION_COMMENT.md').read_text(encoding='utf-8').split('\n\n',1)[1].strip();assert comment==' '.join(plan['sentences']) and len(plan['sentences'])==3;assert len(re.findall(r'[.!?](?:[”\"])?(?=\s|$)',comment))==3
assert (D/'REPORT.md').read_bytes()==(R/'results.md').read_bytes()
print(json.dumps({'status':'PASS','prior_files_preserved':len(m['tracked']),'prior_sealed_artifacts_present_verified':len(artifacts),'raw_turns_verified':turns,'frozen_questions':'unchanged','strict_implementation':'unchanged','six_model_knowledge_files':'unchanged','warning_controls':116,'published':False},indent=2))
