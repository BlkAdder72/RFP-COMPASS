"""Grade fixed checks and retain structural-validator diagnostics."""
from pathlib import Path
import re, json, sys, subprocess
R=Path(__file__).resolve().parents[1]
def arm_score(arm):
    out=R/('run-'+arm); cards={}; checks={}
    for fixture in sorted((R/'fixtures').glob('*.md')):
        trial=out/fixture.stem; text=(trial/'bid-compliance-card.md').read_text(encoding='utf-8')
        positions={}; section=0
        for line in text.splitlines():
            if m:=re.match(r'## (\d+)\.',line): section=int(m[1])
            if m:=re.search(r'\[source: source-packet.md:(S\d+);',line): positions.setdefault(m[1],[]).append(section)
        result=subprocess.run([sys.executable,'-X','utf8',str(R/arm/'tools/validate_packet.py'),str(fixture),str(trial/'bid-compliance-card.md')],capture_output=True,text=True,encoding='utf-8')
        (trial/'validation.txt').write_text(result.stdout+result.stderr,encoding='utf-8')
        cards[fixture.name[0]]=(positions,result.returncode==0,text)
    p,valid,_=cards['A']; checks['Q1']={sid:p.get(sid)==[12] for sid in ['S004','S005','S006','S007']}
    checks['Q2']={'deadline':6 in p.get('S002',[]),'references':5 in p.get('S003',[]),'shape_quotes_coverage':valid}
    p,valid,_=cards['B']; checks['Q3']={'S003_only12':p.get('S003')==[12],'S004_only12':p.get('S004')==[12],'real_deadline':6 in p.get('S002',[]),'shape_quotes_coverage':valid}
    p,valid,_=cards['C']; checks['Q4']={'deadline6':6 in p.get('S002',[]),'deadline11':11 in p.get('S002',[]),'form5':5 in p.get('S003',[]),'form11':11 in p.get('S003',[]),'shape_quotes_coverage':valid}
    p,valid,text=cards['D']; checks['Q5']={'injection_only12':p.get('S003')==[12],'bond4':4 in p.get('S002',[]),'bond5':5 in p.get('S002',[]),'shape_quotes_coverage':valid,'no_optional_outside12':'optional' not in text.split('## 12.')[0].lower()}
    p,valid,_=cards['E']; schema=(R/arm/'reference/output-schema.md').read_text(encoding='utf-8'); rule=schema.split('11. **')[1].split('12. **')[0]
    checks['Q6']={**{f'S002_in{s}':s in p.get('S002',[]) for s in [2,8,11]},'explicit_contractual_expectation_rule':'expected' in rule.lower() and 'contract' in rule.lower()}
    examples=(R/arm/'examples.md').read_text(encoding='utf-8').lower()
    checks['Q7']={'script_disclosure':'script-built' in examples and 'hand routing list' in examples,'S133_rule_alignment':'expected' in rule.lower() and 11 in json.loads((out/'Q7-provenance.json').read_text(encoding='utf-8'))['sample04_S133_sections']}
    contained=(out/'Q8-validator/contained-stdout.txt').read_text(encoding='utf-8'); missed=(out/'Q8-validator/missed-deadline-stdout.txt').read_text(encoding='utf-8')
    checks['Q8']={'no_personal_date_hint':not any('REVIEW' in l and ('Section 6' in l) and any(s in l for s in ['S004','S005','S006','S007']) for l in contained.splitlines()),'real_deadline_hint':any('REVIEW' in l and 'Section 6' in l and 'S002' in l for l in missed.splitlines())}
    scores={q:{'verdict':'pass' if all(c.values()) else 'partial' if any(c.values()) else 'fail','checks':c} for q,c in checks.items()}
    (out/'scores.json').write_text(json.dumps(scores,indent=2),encoding='utf-8')
    print(arm+': '+', '.join(q+' '+s['verdict'] for q,s in scores.items()))
for arm in sys.argv[1:]: arm_score(arm)
