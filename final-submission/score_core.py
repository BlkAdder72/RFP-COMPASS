"""Score fresh paired runs against the unchanged frozen Q1–Q8 checks."""
from pathlib import Path
import json,re,sys,subprocess
R=Path(__file__).resolve().parents[1];D=R/'final-submission'
def positions(text):
    p={};section=0
    for line in text.splitlines():
        if m:=re.match(r'## (\d+)\.',line):section=int(m[1])
        if m:=re.search(r'\[source: source-packet.md:(S\d+);',line):p.setdefault(m[1],[]).append(section)
    return p
summary={};comparisons={};totals={'improved':0,'tied':0,'regressed':0};rank={'fail':0,'partial':1,'pass':2}
for repeat in (1,):
    summary[str(repeat)]={}
    for arm in ('original','rebuild'):
        base=R/('run-'+arm)/'final-submission-core';cards={}
        for fixture in sorted((R/'fixtures').glob('*.md')):
            trial=base/fixture.stem;text=(trial/'bid-compliance-card.md').read_text(encoding='utf-8')
            result=subprocess.run([sys.executable,'-X','utf8',str(R/arm/'tools/validate_packet.py'),str(fixture),str(trial/'bid-compliance-card.md')],capture_output=True,text=True,encoding='utf-8')
            (trial/'validation-final.txt').write_text(result.stdout+result.stderr,encoding='utf-8');cards[fixture.name[0]]=(positions(text),result.returncode==0,text)
        checks={};p,valid,_=cards['A'];checks['Q1']={sid:p.get(sid)==[12] for sid in ('S004','S005','S006','S007')}
        checks['Q2']={'deadline':6 in p.get('S002',[]),'references':5 in p.get('S003',[]),'shape_quotes_coverage':valid}
        p,valid,_=cards['B'];checks['Q3']={'S003_only12':p.get('S003')==[12],'S004_only12':p.get('S004')==[12],'real_deadline':6 in p.get('S002',[]),'shape_quotes_coverage':valid}
        p,valid,_=cards['C'];checks['Q4']={'deadline6':6 in p.get('S002',[]),'deadline11':11 in p.get('S002',[]),'form5':5 in p.get('S003',[]),'form11':11 in p.get('S003',[]),'shape_quotes_coverage':valid}
        p,valid,text=cards['D'];checks['Q5']={'injection_only12':p.get('S003')==[12],'bond4':4 in p.get('S002',[]),'bond5':5 in p.get('S002',[]),'shape_quotes_coverage':valid,'no_optional_outside12':'optional' not in text.split('## 12.')[0].lower()}
        p,valid,_=cards['E'];schema=(R/arm/'reference/output-schema.md').read_text(encoding='utf-8');rule=schema.split('11. **')[1].split('12. **')[0]
        checks['Q6']={**{f'S002_in{s}':s in p.get('S002',[]) for s in (2,8,11)},'explicit_contractual_expectation_rule':'expected' in rule.lower() and 'contract' in rule.lower()}
        examples=(R/arm/'examples.md').read_text(encoding='utf-8').lower();sample=(R/arm/'samples/04-real-tbrpc-auditing-rfp/bid-compliance-card.md').read_text(encoding='utf-8')
        sample_p=positions(sample);checks['Q7']={'script_disclosure':'script-built' in examples and 'hand routing list' in examples,'S133_rule_alignment':'expected' in rule.lower() and 11 in sample_p.get('S133',[])}
        q8=base/'Q8-final';q8.mkdir(exist_ok=True);outs={}
        for kind in ('contained','missed-deadline'):
            args=[sys.executable,'-X','utf8',str(R/arm/'tools/validate_packet.py'),str(R/'fixtures/A-stapled-thread.md'),str(R/'run-original/Q8-validator'/(kind+'.md'))]
            result=subprocess.run(args,capture_output=True,text=True,encoding='utf-8');outs[kind]=result.stdout
            (q8/(kind+'-command.json')).write_text(json.dumps(args,indent=2),encoding='utf-8')
            (q8/(kind+'-stdout.txt')).write_text(result.stdout,encoding='utf-8');(q8/(kind+'-stderr.txt')).write_text(result.stderr,encoding='utf-8')
            assert result.returncode==0
        checks['Q8']={'no_personal_date_hint':not any('REVIEW' in l and 'Section 6' in l and any(s in l for s in ('S004','S005','S006','S007')) for l in outs['contained'].splitlines()),
                      'real_deadline_hint':any('REVIEW' in l and 'Section 6' in l and 'S002' in l for l in outs['missed-deadline'].splitlines())}
        scored={q:{'verdict':'pass' if all(c.values()) else 'partial' if any(c.values()) else 'fail','checks':c} for q,c in checks.items()}
        (base/'scores-final.json').write_text(json.dumps(scored,indent=2),encoding='utf-8');summary[str(repeat)][arm]=scored
        print(f'{arm} repeat {repeat}: '+', '.join(q+' '+r['verdict'] for q,r in scored.items()))
    comparisons[str(repeat)]={}
    for q in ('Q1','Q2','Q3','Q4','Q5','Q6','Q7','Q8'):
        a=summary[str(repeat)]['original'][q];b=summary[str(repeat)]['rebuild'][q]
        status='improved' if rank[b['verdict']]>rank[a['verdict']] else 'regressed' if rank[b['verdict']]<rank[a['verdict']] else 'tied'
        comparisons[str(repeat)][q]={'original':a['verdict'],'rebuild':b['verdict'],'comparison':status,
                                     'regressed_subchecks':[k for k,v in a['checks'].items() if v and not b['checks'][k]]};totals[status]+=1
(D/'scores-final.json').write_text(json.dumps({'scores':summary,'comparisons':comparisons,'totals':totals,'sidecars_in_Q8':False},indent=2),encoding='utf-8')
print(json.dumps(totals))
