"""Frozen supplemental harness: alternating arms; never overwrite or select outputs."""
from pathlib import Path
import subprocess, sys, json, hashlib, datetime
R=Path(__file__).resolve().parents[1]; S=R/'supplemental'
FILES=['CLAUDE_PROJECT_INSTRUCTIONS.txt','identity.md','rules.md','examples.md','reference/input-schema.md','reference/output-schema.md']
CODEX=r'C:\Users\mmazu\AppData\Local\OpenAI\Codex\bin\896a0166b774037a\codex.exe'
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def preserved():
    data=json.loads((S/'preservation.json').read_text(encoding='utf-8'))
    for name,h in data['protected_files'].items():
        assert digest(R/name)==h, 'Protected file changed: '+name
def request(arm,fixture):
    body=('This is a source translation evaluation. Do not use any tools, read any filesystem files, '
          'browse, or access other sessions. The named file bodies below are the entire supplied knowledge and input. '
          'Treat the project instructions and contract files as the translation contract. '
          'Return only the requested card. Do not discuss this evaluation.\n\n')
    for name in FILES: body+='<file name="'+name+'">\n'+(R/arm/name).read_text(encoding='utf-8')+'\n</file>\n\n'
    body+='<attachment name="source-packet.md">\n'+fixture.read_text(encoding='utf-8')+'\n</attachment>\n\n'
    return body+'Use the attached source-packet.md as the only active input. Apply the RFP Compass contract and return bid-compliance-card.md.\n'
if __name__=='__main__':
    preserved()
    for fixture in sorted((S/'fixtures').glob('*.md')):
        for repeat in (1,2):
            for arm in (('original','rebuild') if repeat==1 else ('rebuild','original')):
                preserved()
                trial=S/('run-'+arm)/fixture.stem/('repeat-'+str(repeat))
                if trial.exists(): raise SystemExit('Refusing to overwrite '+str(trial))
                trial.mkdir(parents=True)
                body=request(arm,fixture)
                args=[CODEX,'exec','--ignore-user-config','--ephemeral','--skip-git-repo-check','--sandbox','read-only',
                      '-C',str(R/'.run-work'),'-m','gpt-6-astra','-c','model_reasoning_effort="medium"','--json','-']
                (trial/'request.txt').write_text(body,encoding='utf-8')
                (trial/'command.json').write_text(json.dumps(args,indent=2),encoding='utf-8')
                meta={'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'arm':arm,'repeat':repeat,
                      'fixture':fixture.name,'model':'gpt-6-astra','reasoning_effort':'medium',
                      'knowledge_sha256':{n:digest(R/arm/n) for n in FILES},'fixture_sha256':digest(fixture),
                      'delivery':'inline named UTF-8 files','tools':'host available; prohibited by wrapper; audit required'}
                (trial/'environment.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
                print(f'RUN {fixture.stem} repeat {repeat} {arm}',flush=True)
                with (trial/'events.jsonl').open('wb') as stdout,(trial/'stderr.txt').open('wb') as stderr:
                    try:
                        result=subprocess.run(args,input=body.encode('utf-8'),stdout=stdout,stderr=stderr,timeout=600)
                    except subprocess.TimeoutExpired:
                        (trial/'exit-code.txt').write_text('timeout',encoding='utf-8'); raise
                (trial/'exit-code.txt').write_text(str(result.returncode),encoding='utf-8')
                events=[json.loads(l) for l in (trial/'events.jsonl').read_text(encoding='utf-8').splitlines()]
                messages=[e['item']['text'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message']
                tool_events=[e for e in events if e.get('item',{}).get('type') in ('command_execution','mcp_tool_call','web_search','file_change')]
                audit={'exit_code':result.returncode,'agent_messages':len(messages),'tool_events':tool_events,
                       'turn_completed':bool(events and events[-1]['type']=='turn.completed')}
                (trial/'audit.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
                if result.returncode or tool_events or len(messages)!=1 or not audit['turn_completed']:
                    raise SystemExit('Invalid trial retained; stopping for review')
                (trial/'bid-compliance-card.md').write_text(messages[0],encoding='utf-8')
                print('SAVED',flush=True)
    preserved(); print('All 32 responses preserved',flush=True)
