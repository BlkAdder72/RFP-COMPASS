"""Portable fresh-session runner. Existing destinations are never changed."""
from pathlib import Path
import argparse,datetime,hashlib,json,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1]
FILES=['CLAUDE_PROJECT_INSTRUCTIONS.txt','identity.md','rules.md','examples.md','reference/input-schema.md','reference/output-schema.md']
def write_new(path,text):
    with path.open('x',encoding='utf-8',newline='\n') as stream:stream.write(text)
def request(root,arm,fixture):
    text=('This is a source translation evaluation. Do not use any tools, read any filesystem files, '
          'browse, or access other sessions. The named file bodies below are the entire supplied knowledge and input. '
          'Treat the project instructions and contract files as the translation contract. '
          'Return only the requested card. Do not discuss this evaluation.\n\n')
    for name in FILES:text+='<file name="'+name+'">\n'+(root/arm/name).read_text(encoding='utf-8')+'\n</file>\n\n'
    text+='<attachment name="source-packet.md">\n'+fixture.read_text(encoding='utf-8')+'\n</attachment>\n\n'
    return text+'Use the attached source-packet.md as the only active input. Apply the RFP Compass contract and return bid-compliance-card.md.\n'
def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('arm',choices=['original','rebuild'])
    parser.add_argument('--output-dir',type=Path,help='entirely new destination; defaults to run-ARM')
    parser.add_argument('--fixtures-dir',type=Path,default=ROOT/'fixtures')
    parser.add_argument('--codex',help='Codex executable; otherwise discover on PATH')
    parser.add_argument('--preflight-only',action='store_true',help='validate paths/CLI flags without writing or calling a model')
    args=parser.parse_args(argv)
    out=(args.output_dir or ROOT/('run-'+args.arm)).resolve()
    # This guard is deliberately first: refusal cannot mutate environment metadata.
    if out.exists():raise SystemExit('Refusing existing output directory without changing it: '+str(out))
    required=[ROOT/args.arm/name for name in FILES]
    if not all(p.is_file() for p in required):raise SystemExit('Missing model knowledge file; no output created')
    fixtures=sorted(args.fixtures_dir.glob('*.md')) if args.fixtures_dir.is_dir() else []
    if not fixtures:raise SystemExit('No fixture files; no output created')
    for fixture in fixtures:
        for n,line in enumerate(fixture.read_text(encoding='utf-8').splitlines(),1):
            if line and len(line.split(' | ',2))!=3:raise SystemExit(f'Invalid fixture {fixture}:{n}; no output created')
    executable=args.codex or shutil.which('codex')
    if not executable:raise SystemExit('Codex not found on PATH; use --codex; no output created')
    try:
        version=subprocess.run([executable,'--version'],capture_output=True,text=True,timeout=30)
        help_result=subprocess.run([executable,'exec','--help'],capture_output=True,text=True,timeout=30)
    except (OSError,subprocess.TimeoutExpired) as error:raise SystemExit('CLI preflight failed; no output created: '+str(error))
    flags=['--ignore-user-config','--ephemeral','--skip-git-repo-check','--sandbox','--json']
    if version.returncode or help_result.returncode or not all(f in help_result.stdout for f in flags):
        raise SystemExit('Unsupported CLI/version; no output created')
    if args.preflight_only:
        print('PREFLIGHT PASS: executable/flags, knowledge, fixtures, and new output path. No model call or writes. Authentication/model access will be tested by the first real trial.')
        return 0
    out.parent.mkdir(parents=True,exist_ok=True)
    out.mkdir(exist_ok=False)  # atomic claim; never reuse an old experiment
    meta={'provider':'OpenAI via authenticated Codex CLI','model':'gpt-6-astra','reasoning_effort':'medium',
          'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cli_version':version.stdout.strip(),
          'delivery':'UTF-8 stdin with inline named files','sessions':'fresh ephemeral session per fixture; user config ignored',
          'tools':'host tools may exist; prohibited by wrapper; audit required','limitations':'Host system messages are not held byte-identical; one response per trial, no best-of selection',
          'knowledge_sha256':{n:hashlib.sha256((ROOT/args.arm/n).read_bytes()).hexdigest() for n in FILES},
          'fixture_order':[p.name for p in fixtures]}
    write_new(out/'environment.json',json.dumps(meta,indent=2))
    work_parent=ROOT/'.run-work';work_parent.mkdir(exist_ok=True)
    for fixture in fixtures:
        trial=out/fixture.stem;trial.mkdir(exist_ok=False)
        body=request(ROOT,args.arm,fixture);write_new(trial/'request.txt',body)
        with tempfile.TemporaryDirectory(prefix='rfp-eval-',dir=work_parent) as cwd:
            command=[executable,'exec','--ignore-user-config','--ephemeral','--skip-git-repo-check','--sandbox','read-only',
                     '-C',cwd,'-m','gpt-6-astra','-c','model_reasoning_effort="medium"','--json','-']
            write_new(trial/'command.json',json.dumps(command,indent=2));print('RUN '+args.arm+' '+fixture.stem,flush=True)
            with (trial/'events.jsonl').open('xb') as stdout,(trial/'stderr.txt').open('xb') as stderr:
                try:result=subprocess.run(command,input=body.encode('utf-8'),stdout=stdout,stderr=stderr,timeout=600)
                except (OSError,subprocess.TimeoutExpired) as error:
                    write_new(trial/'failure.txt',str(error));raise SystemExit('Trial failed and retained; no retry')
        write_new(trial/'exit-code.txt',str(result.returncode))
        try:events=[json.loads(l) for l in (trial/'events.jsonl').read_text(encoding='utf-8').splitlines()]
        except ValueError:raise SystemExit('Invalid events retained; no retry')
        messages=[e['item']['text'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message']
        tool_events=[e for e in events if e.get('item',{}).get('type') not in (None,'agent_message','reasoning')]
        completed=bool(events and events[-1]['type']=='turn.completed')
        write_new(trial/'audit.json',json.dumps({'exit_code':result.returncode,'agent_messages':len(messages),'tool_events':tool_events,'turn_completed':completed},indent=2))
        if result.returncode or tool_events or len(messages)!=1 or not completed:raise SystemExit('Invalid trial retained; no retry')
        write_new(trial/'bid-compliance-card.md',messages[0]);print('SAVED',flush=True)
    return 0
if __name__=='__main__':raise SystemExit(main())
