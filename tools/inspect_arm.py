"""Mechanical tool checks and provenance observations; never a model translator."""
from pathlib import Path
import subprocess, sys, json, re, importlib.util
ROOT=Path(__file__).resolve().parents[1]
arm=sys.argv[1]; assert arm in ('original','rebuild')
out=ROOT/('run-'+arm); out.mkdir(exist_ok=True)
spec=importlib.util.spec_from_file_location('validator',ROOT/arm/'tools/validate_packet.py')
v=importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
rows={}
for line in (ROOT/'fixtures/A-stapled-thread.md').read_text(encoding='utf-8').splitlines():
    sid,anchor,text=line.split(' | ',2); rows[sid]=(anchor,text)
q8=out/'Q8-validator'; q8.mkdir(exist_ok=True)
mapping={1:['S001'],2:['S001'],5:['S003'],6:['S002'],12:['S004','S005','S006','S007']}
for label in ('contained','missed-deadline'):
    placements={k:list(ids) for k,ids in mapping.items()}
    if label=='missed-deadline': placements[6]=[]; placements[12]=['S002',*placements[12]]
    parts=[v.TITLE]
    for section,heading in enumerate(v.HEADINGS,1):
        parts+=['',heading]
        ids=placements.get(section,[])
        parts += [f'- “{rows[sid][1]}” [source: source-packet.md:{sid}; {rows[sid][0]}]' for sid in ids] if ids else ['- not in source']
    card=q8/(label+'.md'); card.write_text('\n'.join(parts)+'\n',encoding='utf-8')
    args=[sys.executable,'-X','utf8',str(ROOT/arm/'tools/validate_packet.py'),str(ROOT/'fixtures/A-stapled-thread.md'),str(card)]
    result=subprocess.run(args,capture_output=True,text=True,encoding='utf-8')
    (q8/(label+'-command.json')).write_text(json.dumps(args,indent=2),encoding='utf-8')
    (q8/(label+'-stdout.txt')).write_text(result.stdout,encoding='utf-8')
    (q8/(label+'-stderr.txt')).write_text(result.stderr,encoding='utf-8')
    (q8/(label+'-exit-code.txt')).write_text(str(result.returncode),encoding='utf-8')
(q8/'PROVENANCE.md').write_text('Both cards are evaluator-built fixtures, not model output. Their routing is fixed by questions.md. The second intentionally omits a real deadline from Section 6.\n',encoding='utf-8')
examples=(ROOT/arm/'examples.md').read_text(encoding='utf-8')
schema=(ROOT/arm/'reference/output-schema.md').read_text(encoding='utf-8')
card=(ROOT/arm/'samples/04-real-tbrpc-auditing-rfp/bid-compliance-card.md').read_text(encoding='utf-8')
section=0; places=[]
for line in card.splitlines():
    if m:=re.match(r'## (\d+)\.',line): section=int(m[1])
    if 'source-packet.md:S133;' in line: places.append(section)
report={'sample04_S133_sections':places,'examples_opening':examples.split('\n\n')[1],
        'section11_rule':schema.split('11. **')[1].split('12. **')[0],
        'note':'Inspect exact excerpts for provenance disclosure and rule alignment; no model inference.'}
(out/'Q7-provenance.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('Saved Q7 excerpts and Q8 tool runs for '+arm)
