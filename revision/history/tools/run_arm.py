"""Run frozen card trials in fresh CLI sessions; preserve exact requests and raw events."""
from pathlib import Path
import subprocess, sys, json, hashlib, datetime
ROOT = Path(__file__).resolve().parents[1]
arm = sys.argv[1]
assert arm in ('original', 'rebuild')
out = ROOT / ('run-' + arm)
out.mkdir(exist_ok=True)
files = ['CLAUDE_PROJECT_INSTRUCTIONS.txt', 'identity.md', 'rules.md', 'examples.md',
         'reference/input-schema.md', 'reference/output-schema.md']
model = 'gpt-6-astra'
codex = r'C:\Users\mmazu\AppData\Local\OpenAI\Codex\bin\896a0166b774037a\codex.exe'
metadata = {'provider': 'OpenAI via authenticated Codex CLI', 'model': model, 'reasoning_effort': 'medium',
 'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'delivery': 'UTF-8 stdin; named file bodies delimited in request, not native attachments',
 'sessions': 'fresh ephemeral session per fixture; user config ignored',
 'tools': 'CLI tools may be offered by host; wrapper prohibits tool use; events must be audited',
 'limitations': 'Codex host instructions remain; this is not a Claude Project reproduction. One run per fixture; no best-of selection.',
 'knowledge_sha256': {p:hashlib.sha256((ROOT/arm/p).read_bytes()).hexdigest() for p in files}}
(out/'environment.json').write_text(json.dumps(metadata, indent=2), encoding='utf-8')
for fixture in sorted((ROOT/'fixtures').glob('*.md')):
    trial = out / fixture.stem
    if trial.exists():
        raise SystemExit('Refusing to overwrite existing trial: '+str(trial))
    trial.mkdir()
    wrapper = ('This is a source translation evaluation. Do not use any tools, read any filesystem files, '
               'browse, or access other sessions. The named file bodies below are the entire supplied knowledge and input. '
               'Treat the project instructions and contract files as the translation contract. '
               'Return only the requested card. Do not discuss this evaluation.\n\n')
    for name in files:
        wrapper += '<file name="'+name+'">\n'+(ROOT/arm/name).read_text(encoding='utf-8')+'\n</file>\n\n'
    wrapper += '<attachment name="source-packet.md">\n'+fixture.read_text(encoding='utf-8')+'\n</attachment>\n\n'
    wrapper += 'Use the attached source-packet.md as the only active input. Apply the RFP Compass contract and return bid-compliance-card.md.\n'
    (trial/'request.txt').write_text(wrapper, encoding='utf-8')
    args = [codex,'exec','--ignore-user-config','--ephemeral','--skip-git-repo-check','--sandbox','read-only',
            '-C',str(ROOT/'.run-work'),'-m',model,'-c','model_reasoning_effort="medium"','--json','-']
    (trial/'command.json').write_text(json.dumps(args,indent=2),encoding='utf-8')
    print('Running '+arm+' '+fixture.stem, flush=True)
    with (trial/'events.jsonl').open('wb') as stdout, (trial/'stderr.txt').open('wb') as stderr:
        result = subprocess.run(args,input=wrapper.encode('utf-8'),stdout=stdout,stderr=stderr,timeout=600)
    (trial/'exit-code.txt').write_text(str(result.returncode),encoding='utf-8')
    messages=[]; tool_events=[]
    for line in (trial/'events.jsonl').read_text(encoding='utf-8').splitlines():
        event=json.loads(line)
        item=event.get('item',{})
        if event.get('type')=='item.completed' and item.get('type')=='agent_message':
            messages.append(item['text'])
        if item.get('type') in ('command_execution','mcp_tool_call','web_search','file_change'):
            tool_events.append(event)
    (trial/'audit.json').write_text(json.dumps({'exit_code':result.returncode,'tool_events':tool_events,
                                               'agent_messages':len(messages)},indent=2),encoding='utf-8')
    if result.returncode or tool_events or len(messages)!=1:
        raise SystemExit('Trial requires review; stopping without retry')
    (trial/'bid-compliance-card.md').write_text(messages[0],encoding='utf-8')
    print('Saved raw transcript and unedited message',flush=True)
