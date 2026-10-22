"""Offline audit of supplemental evidence and byte-preserved first-pass material."""
from pathlib import Path
import sys,json,subprocess,hashlib
sys.dont_write_bytecode=True
from run import preserved,request,FILES
R=Path(__file__).resolve().parents[1];S=R/'supplemental'
preserved()
protocol_paths=['supplemental/protocol.md','supplemental/run.py','supplemental/score.py']
protocol_paths += [str(p.relative_to(R)).replace('\\','/') for p in (S/'fixtures').glob('*.md')]
for name in protocol_paths:
    assert subprocess.check_output(['git','show','b1f808c:'+name],cwd=R)==(R/name).read_bytes(), 'Frozen protocol changed: '+name
counts=0;types=set();totals={a:{'input_tokens':0,'output_tokens':0} for a in ('original','rebuild')}
for arm in ('original','rebuild'):
    for fixture in sorted((S/'fixtures').glob('*.md')):
        for repeat in (1,2):
            trial=S/('run-'+arm)/fixture.stem/('repeat-'+str(repeat))
            assert (trial/'request.txt').read_text(encoding='utf-8')==request(arm,fixture)
            env=json.loads((trial/'environment.json').read_text(encoding='utf-8'))
            assert env['model']=='gpt-6-astra' and env['reasoning_effort']=='medium'
            for name in FILES:
                assert env['knowledge_sha256'][name]==hashlib.sha256((R/arm/name).read_bytes()).hexdigest()
            assert env['fixture_sha256']==hashlib.sha256(fixture.read_bytes()).hexdigest()
            cmd=json.loads((trial/'command.json').read_text(encoding='utf-8'))
            assert cmd[1:8]==['exec','--ignore-user-config','--ephemeral','--skip-git-repo-check','--sandbox','read-only','-C']
            assert cmd[cmd.index('-m')+1]=='gpt-6-astra'
            assert cmd[cmd.index('-c')+1]=='model_reasoning_effort="medium"'
            events=[json.loads(l) for l in (trial/'events.jsonl').read_text(encoding='utf-8').splitlines()]
            messages=[]
            for event in events:
                item=event.get('item',{});kind=item.get('type')
                if kind:types.add(kind)
                assert kind not in ('command_execution','mcp_tool_call','web_search','file_change')
                if event.get('type')=='item.completed' and kind=='agent_message':messages.append(item['text'])
            assert len(messages)==1 and messages[0]==(trial/'bid-compliance-card.md').read_text(encoding='utf-8')
            assert events[-1]['type']=='turn.completed' and (trial/'exit-code.txt').read_text(encoding='utf-8')=='0'
            for key in totals[arm]:totals[arm][key]+=events[-1]['usage'][key]
            counts+=1
assert types <= {'agent_message','reasoning'},'Unreviewed item types: '+str(types)
subprocess.run([sys.executable,str(S/'score.py')],check=True,stdout=subprocess.DEVNULL)
preserved()
report={'status':'pass','protected_first_pass_files':len(json.loads((S/'preservation.json').read_text(encoding='utf-8'))['protected_files']),
        'model_responses_verified':counts,'frozen_protocol_commit':'b1f808c','observed_item_types':sorted(types),
        'token_totals':totals,'note':'Explicit requests and knowledge verified; host system context was not captured.'}
(S/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
