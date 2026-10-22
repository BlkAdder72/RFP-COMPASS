"""Offline verification of preserved bytes, fixed inputs, transcript extraction and grading."""
from pathlib import Path
import sys, subprocess, json, re
R=Path(__file__).resolve().parents[1]
subprocess.run([sys.executable,str(R/'tools/check_original.py')],check=True,stdout=subprocess.DEVNULL)
for arm in ('original','rebuild'):
    env=json.loads((R/('run-'+arm)/'environment.json').read_text(encoding='utf-8'))
    assert env['model']=='gpt-6-astra' and env['reasoning_effort']=='medium'
    for fixture in sorted((R/'fixtures').glob('*.md')):
        trial=R/('run-'+arm)/fixture.stem
        request=(trial/'request.txt').read_text(encoding='utf-8')
        assert '<attachment name="source-packet.md">\n'+fixture.read_text(encoding='utf-8')+'\n</attachment>' in request
        assert request.endswith('Use the attached source-packet.md as the only active input. Apply the RFP Compass contract and return bid-compliance-card.md.\n')
        for name,digest in env['knowledge_sha256'].items():
            import hashlib
            body=(R/arm/name).read_text(encoding='utf-8')
            assert hashlib.sha256((R/arm/name).read_bytes()).hexdigest()==digest
            assert '<file name="'+name+'">\n'+body+'\n</file>' in request
        events=[json.loads(l) for l in (trial/'events.jsonl').read_text(encoding='utf-8').splitlines()]
        msgs=[e['item']['text'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message']
        assert len(msgs)==1 and msgs[0]==(trial/'bid-compliance-card.md').read_text(encoding='utf-8')
        assert events[-1]['type']=='turn.completed'
        assert not any(e.get('item',{}).get('type') in ('command_execution','mcp_tool_call','web_search','file_change') for e in events)
        assert (trial/'exit-code.txt').read_text(encoding='utf-8')=='0'
subprocess.run([sys.executable,str(R/'tools/score.py'),'original','rebuild'],check=True)
print('PASS: original and feedback integrity; ten raw model responses; exact inputs and knowledge; no observed tool use; grading regenerated.')
