"""Frozen supplemental checks; scores are regenerated without changing raw evidence."""
from pathlib import Path
import re, json, sys, subprocess, importlib.util
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[1]; S=R/'supplemental'
def positions(text):
    p={}; section=0
    for line in text.splitlines():
        if m:=re.match(r'## (\d+)\.',line): section=int(m[1])
        if m:=re.search(r'\[source: source-packet.md:(S\d+);',line):p.setdefault(m[1],[]).append(section)
    return p
def core_checks(key,p,valid):
    checks={'structure_exact_quotes_coverage':valid}
    def has(sid,*sections):return all(s in p.get(sid,[]) for s in sections)
    if key=='F': checks.update(real_deadline=has('S001',6),appointment_only12=p.get('S002')==[12],family_event_only12=p.get('S003')==[12])
    if key=='G': checks.update(uncertain_meeting_retained=has('S002',6),required_form_retained=has('S003',4,5))
    if key=='H': checks.update(real_deadline=has('S002',6),required_form=has('S003',5),recital_only12=p.get('S004')==[12],picnic_only12=p.get('S005')==[12])
    if key=='I': checks.update(mixed_real_deadline_retained=has('S002',6))
    if key=='J': checks.update(clarification_deadline=has('S002',6,11),personal_event_only12=p.get('S003')==[12])
    if key=='K': checks.update(real_deadline_despite_label=has('S002',6))
    if key=='L': checks.update(procurement_visit_retained=has('S002',4,6),attendance_form_retained=has('S003',4,5))
    if key=='M': checks.update(mixed_required_form_retained=has('S002',4,5))
    return checks
def score_models():
    result={}
    for arm in ('original','rebuild'):
        result[arm]={}
        for fixture in sorted((S/'fixtures').glob('*.md')):
            key=fixture.name[0]; result[arm][key]={}
            for repeat in (1,2):
                trial=S/('run-'+arm)/fixture.stem/('repeat-'+str(repeat))
                text=(trial/'bid-compliance-card.md').read_text(encoding='utf-8'); p=positions(text)
                cmd=[sys.executable,'-X','utf8',str(R/arm/'tools/validate_packet.py'),str(fixture),str(trial/'bid-compliance-card.md')]
                check=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8')
                (trial/'validation.txt').write_text(check.stdout+check.stderr,encoding='utf-8')
                checks=core_checks(key,p,check.returncode==0)
                verdict='pass' if all(checks.values()) else 'partial' if any(checks.values()) else 'fail'
                diagnostics={'placement':p}
                if key in ('I','M'):
                    diagnostics['inseparable_personal_text_in_operational_sections']=any(s<12 for s in p.get('S002',[]))
                    diagnostics['contract_tension']='Whole-statement preservation prevents isolating the personal clause while retaining the genuine requirement.'
                # G's no-added-authority property is inspected against exact raw text in the report.
                record={'verdict':verdict,'checks':checks,'diagnostics':diagnostics}
                (trial/'score.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
                result[arm][key][str(repeat)]=record
    compare={}; rank={'fail':0,'partial':1,'pass':2}; totals={'improved':0,'tied':0,'regressed':0}
    for key in result['original']:
        compare[key]={}
        for repeat in ('1','2'):
            a=result['original'][key][repeat]['verdict']; b=result['rebuild'][key][repeat]['verdict']
            status='improved' if rank[b]>rank[a] else 'regressed' if rank[b]<rank[a] else 'tied'
            # Even a verdict tie may have offsetting gains and losses; preserve check-level direction.
            ca=result['original'][key][repeat]['checks']; cb=result['rebuild'][key][repeat]['checks']
            compare[key][repeat]={'original':a,'rebuild':b,'comparison':status,
                                 'improved_checks':[k for k in ca if not ca[k] and cb[k]],
                                 'regressed_checks':[k for k in ca if ca[k] and not cb[k]]}
            totals[status]+=1
    report={'model_trials':result,'paired_comparisons':compare,'paired_totals':totals}
    (S/'scores.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps({'paired_comparisons':compare,'paired_totals':totals},indent=2))
def score_tools():
    report={}
    for arm in ('original','rebuild'):
        spec=importlib.util.spec_from_file_location('validator',R/arm/'tools/validate_packet.py')
        v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
        report[arm]={}
        for name,key,mapping in [('N1-mislabeled-real-deadline','K',{1:['S001'],2:['S001'],12:['S002']}),
                                 ('N2-neutral-personal','F',{6:['S001'],12:['S002','S003']})]:
            fixture=next((S/'fixtures').glob(key+'-*.md')); rows={}
            for line in fixture.read_text(encoding='utf-8').splitlines():
                sid,anchor,body=line.split(' | ',2);rows[sid]=(anchor,body)
            trial=S/('tool-'+arm)/name;trial.mkdir(parents=True,exist_ok=True)
            lines=[v.TITLE]
            for number,heading in enumerate(v.HEADINGS,1):
                lines+=['',heading]
                ids=mapping.get(number,[])
                lines += [f'- “{rows[sid][1]}” [source: source-packet.md:{sid}; {rows[sid][0]}]' for sid in ids] if ids else ['- not in source']
            card=trial/'evaluator-card.md';card.write_text('\n'.join(lines)+'\n',encoding='utf-8')
            cmd=[sys.executable,'-X','utf8',str(R/arm/'tools/validate_packet.py'),str(fixture),str(card)]
            check=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8')
            (trial/'command.json').write_text(json.dumps(cmd,indent=2),encoding='utf-8')
            (trial/'stdout.txt').write_text(check.stdout,encoding='utf-8');(trial/'stderr.txt').write_text(check.stderr,encoding='utf-8')
            (trial/'PROVENANCE.md').write_text('Evaluator-built card, not model output. Fixed construction and expectations in supplemental/protocol.md.\n',encoding='utf-8')
            hints=[l for l in check.stdout.splitlines() if 'REVIEW' in l and 'Section 6' in l]
            passed=any('S002' in l for l in hints) if key=='K' else not any(any(s in l for s in ('S002','S003')) for l in hints)
            report[arm][name]={'verdict':'pass' if passed else 'fail','validator_exit_code':check.returncode,'section6_hints':hints}
    (S/'tool-scores.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
if __name__=='__main__':
    if '--tools-only' not in sys.argv:score_models()
    score_tools()
