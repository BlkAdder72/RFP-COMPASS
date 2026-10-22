"""Immutable default-workflow checker evidence; no review sidecars supplied."""
from pathlib import Path
import subprocess,json,sys,hashlib,importlib.util
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[1];D=R/'revision';O=D/(sys.argv[1] if len(sys.argv)>1 else 'default-tests');assert not O.exists();O.mkdir()
spec=importlib.util.spec_from_file_location('v',R/'rebuild/tools/validate_packet.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
results=[]
def execute(label,arm,source,card,section,sid,warn,valid=True,filter_expected=None):
    folder=O/label/arm;folder.mkdir(parents=True)
    command=[sys.executable,'-X','utf8',str(R/arm/'tools/validate_packet.py'),str(source),str(card)]
    (folder/'command.json').write_text(json.dumps(command,indent=2),encoding='utf-8')
    result=subprocess.run(command,capture_output=True,text=True,encoding='utf-8')
    (folder/'stdout.txt').write_text(result.stdout,encoding='utf-8');(folder/'stderr.txt').write_text(result.stderr,encoding='utf-8')
    (folder/'exit-code.txt').write_text(str(result.returncode),encoding='utf-8')
    hints=[l for l in result.stdout.splitlines() if 'REVIEW' in l and f'Section {section}' in l]
    observed=any(sid in l for l in hints)
    checks={'validity':(result.returncode==0)==valid,'hint':observed==warn}
    if filter_expected is not None:checks['filter_presence']=('PERSONAL HINT FILTER' in result.stdout)==filter_expected
    record={'label':label,'arm':arm,'command':command,'source':str(source.relative_to(R)).replace('\\','/'),
            'card':str(card.relative_to(R)).replace('\\','/'),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'card_sha256':hashlib.sha256(card.read_bytes()).hexdigest(),'validator_sha256':hashlib.sha256((R/arm/'tools/validate_packet.py').read_bytes()).hexdigest(),
            'section':section,'sid':sid,'expect_warning':warn,'observed_warning':observed,'expect_valid':valid,'exit_code':result.returncode,
            'checks':checks,'passed':all(checks.values())}
    (folder/'audit.json').write_text(json.dumps(record,indent=2),encoding='utf-8');results.append(record)
def render(rows,placements):
    lines=[v.TITLE]
    for n,heading in enumerate(v.HEADINGS,1):
        lines+=['',heading];ids=placements.get(n,[])
        lines += [f'- “{rows[i][2]}” [source: source-packet.md:{rows[i][0]}; {rows[i][1]}]' for i in ids] if ids else ['- not in source']
    return '\n'.join(lines)+'\n'
for case in json.loads((D/'default-cases.json').read_text(encoding='utf-8')):
    folder=O/'inputs'/case['name'];folder.mkdir(parents=True)
    rows=[];anchor=case.get('anchor','attachment.txt paragraph 1')
    if 'header' in case:rows.append(('S001',anchor,case['header']))
    sid=f'S{len(rows)+1:03d}';rows.append((sid,anchor,case['body']))
    source=folder/'source-packet.md';source.write_text('\n'.join(' | '.join(row) for row in rows)+'\n',encoding='utf-8')
    card=folder/'card.md';card.write_text(render(rows,{12:list(range(len(rows)))}),encoding='utf-8')
    for arm in ('original','rebuild'):
        execute(case['name'],arm,source,card,case.get('section',6),sid,True if arm=='original' else not case['exclude'])
A=R/'fixtures/A-stapled-thread.md';K=R/'supplemental/fixtures/K-unrelated-label.md';F=R/'supplemental/fixtures/F-neutral-personal.md'
for arm in ('original','rebuild'):
    execute('Q8-contained',arm,A,R/'run-original/Q8-validator/contained.md',6,'S004',arm=='original')
    execute('Q8-real-deadline',arm,A,R/'run-original/Q8-validator/missed-deadline.md',6,'S002',True)
    execute('N1-misleading-anchor',arm,K,R/'supplemental/tool-original/N1-mislabeled-real-deadline/evaluator-card.md',6,'S002',True)
    execute('N2-neutral-personal',arm,F,R/'supplemental/tool-original/N2-neutral-personal/evaluator-card.md',6,'S002',arm=='original')
# An operational duplicate cannot be used as evidence for automatic exclusion.
folder=O/'inputs/operational-duplicate';folder.mkdir(parents=True)
rows=[('S001','attachment.txt','Our birthday party is March 10, 2028, at 6:00 PM; bring $20 for dinner.')]
source=folder/'source-packet.md';source.write_text(' | '.join(rows[0])+'\n',encoding='utf-8')
card=folder/'card.md';card.write_text(render(rows,{6:[0],12:[0]}),encoding='utf-8')
execute('operational-duplicate','rebuild',source,card,8,'S001',True,filter_expected=False)
for label,text in [('changed-quote',(R/'run-original/Q8-validator/contained.md').read_text(encoding='utf-8').replace('November 20','November 21')),
                   ('missing-heading',(R/'run-original/Q8-validator/contained.md').read_text(encoding='utf-8').replace('## 3. Eligibility and qualifications stated',''))]:
    path=O/'inputs'/(label+'.md');path.write_text(text,encoding='utf-8')
    execute(label,'rebuild',A,path,6,'S004',label!='missing-heading',valid=False,filter_expected=False)
report={'count':len(results),'passed':sum(r['passed'] for r in results),'cases':results,'review_records_supplied':False}
(D/('default-results.json' if O.name=='default-tests' else O.name+'-results.json')).write_text(json.dumps(report,indent=2),encoding='utf-8')
failed=[r['label']+'/'+r['arm'] for r in results if not r['passed']]
print(json.dumps({'count':len(results),'passed':report['passed'],'failed':failed},indent=2))
if failed:raise SystemExit(1)
