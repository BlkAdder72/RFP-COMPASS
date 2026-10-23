"""Full-length paired harness with genuine, recorded session continuations."""
from pathlib import Path
import argparse,datetime,hashlib,importlib.util,json,shutil,subprocess,sys,tempfile
R=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('core',R/'tools/run_arm.py');core=importlib.util.module_from_spec(spec);spec.loader.exec_module(core)
p=argparse.ArgumentParser();p.add_argument('arm',choices=['original','rebuild']);p.add_argument('--preflight-only',action='store_true');p.add_argument('--output-dir',type=Path,help='entirely new destination; existing evidence is never reused');p.add_argument('--codex',help='explicit executable override; otherwise PATH');a=p.parse_args()
out=(a.output_dir or R/('run-'+a.arm)/'hardening-full').resolve()
if out.exists():raise SystemExit('Refusing existing output directory without changing it: '+str(out))
exe=a.codex or shutil.which('codex')
if not exe:raise SystemExit('Codex missing; no writes')
helptext=subprocess.check_output([exe,'exec','resume','--help'],text=True,encoding='utf-8')
assert all(x in helptext for x in ['SESSION_ID','--ignore-user-config','--json','--model'])
if a.preflight_only:print('PREFLIGHT PASS; no writes or model calls');raise SystemExit(0)
out.parent.mkdir(parents=True,exist_ok=True);out.mkdir();fixture=R/'hardening/fixtures/Z-full-length-noisy.md';body=core.request(R,a.arm,fixture)
core.write_new(out/'environment.json',json.dumps({'model':'gpt-6-astra','reasoning_effort':'medium','arm':a.arm,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'knowledge_sha256':{n:hashlib.sha256((R/a.arm/n).read_bytes()).hexdigest() for n in core.FILES},'fixture_sha256':hashlib.sha256(fixture.read_bytes()).hexdigest(),'sessions':'fresh persistent session; exact continue in same session, max eight parts; no retries','limitations':'host messages uncontrolled; same-session persistence differs from earlier ephemeral trials'},indent=2))
parent=R/'.run-work';parent.mkdir(exist_ok=True);parts=[];session=None
with tempfile.TemporaryDirectory(prefix='rfp-full-',dir=parent) as cwd:
 for n in range(1,9):
  part=out/f'part-{n}';part.mkdir();prompt=body if n==1 else 'continue';core.write_new(part/'request.txt',prompt)
  common=[exe,'exec','--ignore-user-config','--sandbox','read-only','-C',cwd]
  if n==1:cmd=common+['--skip-git-repo-check','-m','gpt-6-astra','-c','model_reasoning_effort="medium"','--json','-']
  else:cmd=common+['resume','--ignore-user-config','--skip-git-repo-check','-m','gpt-6-astra','-c','model_reasoning_effort="medium"','--json',session,'-']
  core.write_new(part/'command.json',json.dumps(cmd,indent=2));print(f'RUN {a.arm} full part {n}',flush=True)
  with (part/'events.jsonl').open('xb') as stdout,(part/'stderr.txt').open('xb') as stderr:
   try:r=subprocess.run(cmd,input=prompt.encode(),stdout=stdout,stderr=stderr,timeout=600)
   except (OSError,subprocess.TimeoutExpired) as e:core.write_new(part/'failure.txt',str(e));raise SystemExit('Failure retained; no retry')
  core.write_new(part/'exit-code.txt',str(r.returncode));events=[json.loads(l) for l in (part/'events.jsonl').read_text(encoding='utf-8').splitlines()]
  threads=[e['thread_id'] for e in events if e.get('type')=='thread.started']
  if n==1:session=threads[0] if len(threads)==1 else None
  messages=[e['item']['text'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message']
  tools=[e for e in events if e.get('item',{}).get('type') not in (None,'agent_message','reasoning')]
  audit={'exit_code':r.returncode,'session_id':session,'returned_sessions':threads,'messages':len(messages),'tools':tools,'turn_completed':bool(events and events[-1]['type']=='turn.completed')}
  core.write_new(part/'audit.json',json.dumps(audit,indent=2))
  if r.returncode or not session or tools or len(messages)!=1 or not audit['turn_completed'] or any(t!=session for t in threads):raise SystemExit('Invalid trial retained; no retry')
  core.write_new(part/'bid-compliance-card.md',messages[0]);parts.append(messages[0])
  if not messages[0].rstrip().endswith('<!-- RFP COMPASS: continued in next reply -->'):break
 else:core.write_new(out/'incomplete.txt','Eight-part limit reached; not retried.')
core.write_new(out/'bid-compliance-card.md','\n'.join(parts));print('SAVED '+str(len(parts))+' parts',flush=True)
