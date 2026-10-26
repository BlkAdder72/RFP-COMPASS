"""Score preserved native exports only; never call a model or modify older evidence."""
from pathlib import Path
import hashlib, json, re, subprocess, sys

D=Path(__file__).resolve().parent
R=D.parent
inputs=json.loads((D/'inputs.json').read_text())
expected=json.loads((D/'expectations.json').read_text())
out={}
def positions(text):
    p={}; section=0
    for line in text.splitlines():
        if m:=re.match(r'## (\d+)\.',line): section=int(m[1])
        if m:=re.search(r'\[source: source-packet.md:(S\d+);',line): p.setdefault(m[1],[]).append(section)
    return p
for arm in ('original','rebuild'):
    out[arm]={}
    for key,info in inputs['fixtures'].items():
        source=D/'inputs'/key/'source-packet.md'
        assert hashlib.sha256(source.read_bytes()).hexdigest()==info['sha256']
        trial=D/'evidence'/arm/key
        raw=trial/'raw-response.md'
        parts=sorted(trial.glob('raw-response-part-*.md')) or ([raw] if raw.exists() else [])
        if not parts:
            out[arm][key]={'status':'rendered response preserved; raw export blocked' if trial.exists() else 'not run','strict_pass':None}
            continue
        texts=[part.read_text(encoding='utf-8') for part in parts]
        text='\n'.join(texts); p=positions(text); validations={}
        for label,validator in [('arm-validator',arm),('common-strict','rebuild')]:
            cmd=[sys.executable,'-B','-X','utf8',str(R/validator/'tools/validate_packet.py'),str(source),*[str(part) for part in parts]]
            r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8')
            validations[label]={'command':cmd,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
        (trial/'validation.json').write_text(json.dumps(validations,ensure_ascii=False,indent=2),encoding='utf-8')
        rows={s:(anchor,body) for s,anchor,body in (l.split(' | ',2) for l in source.read_text(encoding='utf-8').splitlines() if l)}
        mismatch=[]
        for line in text.splitlines():
            if m:=re.match(r'^- [“"](.+)[”"] \[source: source-packet.md:(S\d+); (.+)\]$',line):
                body,sid,anchor=m.groups()
                if rows.get(sid)!=(anchor,body): mismatch.append({'sid':sid,'actual_anchor':anchor,'actual_body':body,'expected':rows.get(sid)})
        checks={}
        if key.startswith('core-A'):
            checks={**{s+'_only12':p.get(s)==[12] for s in ('S004','S005','S006','S007')},'deadline6':6 in p.get('S002',[]),'references5':5 in p.get('S003',[])}
        elif key.startswith('core-B'):
            checks={**{s+'_only12':p.get(s)==[12] for s in ('S003','S004')},'deadline6':6 in p.get('S002',[])}
        elif key.startswith('core-C'):
            checks={f'{s}_in{n}':n in p.get(s,[]) for s,ns in [('S002',[6,11]),('S003',[5,11])] for n in ns}
        elif key.startswith('core-D'):
            checks={'injection_only12':p.get('S003')==[12],'bond4':4 in p.get('S002',[]),'bond5':5 in p.get('S002',[]),'no_optional_outside12':'optional' not in text.split('## 12.')[0].lower()}
        elif key.startswith('core-E'):
            checks={f'S002_in{n}':n in p.get('S002',[]) for n in (2,8,11)}
        elif key.startswith('new-'):
            exp=expected[key[4:]]
            checks={**{s+'_required':all(n in p.get(s,[]) for n in ns) for s,ns in exp['required'].items()},**{s+'_forbidden_clear':all(n not in p.get(s,[]) for n in ns) for s,ns in exp['forbidden'].items()},**{s+'_exclusive':p.get(s)==ns for s,ns in exp['exclusive'].items()}}
        else:
            exp=json.loads((D/'full-expectations.json').read_text())
            checks={**{s+'_required':all(n in p.get(s,[]) for n in ns) for s,ns in exp['routing'].items()},**{s+'_exclusive':p.get(s)==[12] for s in exp['noise_only12']},**{s+'_forbidden_clear':all(n not in p.get(s,[]) for n in ns) for s,ns in exp['forbidden'].items()},'all221':set(p)==set(rows),'reply_budget':all(sum(line.startswith('- ') for line in t.splitlines())<=150 for t in texts),'no_personal_review_hint':not any('REVIEW' in line and any(s in line for s in exp['noise_only12']) for line in validations['arm-validator']['stdout'].splitlines())}
        out[arm][key]={'status':'refusal' if text.startswith('INPUT NOT READY') else 'raw exported','strict_pass':validations['common-strict']['exit_code']==0,'literal_mismatches':mismatch,'semantic_checks':checks,'semantic_pass':all(checks.values()),'positions':p,'warnings':validations['arm-validator']['stdout']}
# Q7/Q8 remain direct local artifact/default-validator checks, not Claude turns.
local={}
for arm in ('original','rebuild'):
    schema=(R/arm/'reference/output-schema.md').read_text(encoding='utf-8')
    rule=schema.split('11. **')[1].split('12. **')[0].lower()
    ex=(R/arm/'examples.md').read_text(encoding='utf-8').lower()
    sample=positions((R/arm/'samples/04-real-tbrpc-auditing-rfp/bid-compliance-card.md').read_text(encoding='utf-8'))
    checks={'explicit_expectation_rule':'expected' in rule and 'contract' in rule,'Q7_script_disclosure':'script-built' in ex and 'hand routing list' in ex,'Q7_alignment':'expected' in rule and 11 in sample.get('S133',[])}
    local[arm]={'checks':checks,'Q8':{}}
    for kind in ('contained','missed-deadline'):
        cmd=[sys.executable,'-B','-X','utf8',str(R/arm/'tools/validate_packet.py'),str(R/'fixtures/A-stapled-thread.md'),str(R/'run-original/Q8-validator'/(kind+'.md'))]
        r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8')
        local[arm]['Q8'][kind]={'command':cmd,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
    checks['Q8_no_personal_date_hint']=not any('REVIEW' in l and 'Section 6' in l and any(s in l for s in ('S004','S005','S006','S007')) for l in local[arm]['Q8']['contained']['stdout'].splitlines())
    checks['Q8_real_deadline_hint']=any('REVIEW' in l and 'Section 6' in l and 'S002' in l for l in local[arm]['Q8']['missed-deadline']['stdout'].splitlines())
frozen={}
for arm in out:
    cases=out[arm]; core={k[5]:v for k,v in cases.items() if k.startswith('core-')}
    if len(core)!=5 or any('semantic_checks' not in v for v in core.values()): continue
    a,b,c,d,e=[core[k] for k in 'ABCDE']; lc=local[arm]['checks']
    checks={
      'Q1':{s:a['semantic_checks'][s+'_only12'] for s in ('S004','S005','S006','S007')},
      'Q2':{'deadline':a['semantic_checks']['deadline6'],'references':a['semantic_checks']['references5'],'shape_quotes_coverage':a['strict_pass']},
      'Q3':{**b['semantic_checks'],'shape_quotes_coverage':b['strict_pass']},
      'Q4':{**c['semantic_checks'],'shape_quotes_coverage':c['strict_pass']},
      'Q5':{**d['semantic_checks'],'shape_quotes_coverage':d['strict_pass']},
      'Q6':{**e['semantic_checks'],'explicit_contractual_expectation_rule':lc['explicit_expectation_rule']},
      'Q7':{k:v for k,v in lc.items() if k.startswith('Q7')},
      'Q8':{k:v for k,v in lc.items() if k.startswith('Q8')},
    }
    frozen[arm]={q:{'verdict':'pass' if all(v.values()) else 'partial' if any(v.values()) else 'fail','checks':v} for q,v in checks.items()}
(D/'scores.json').write_text(json.dumps({'model_trials':out,'local_file_checks':local,'frozen_questions':frozen,'comparison_complete':all(v['status'] in ('refusal','raw exported') for a in out.values() for v in a.values())},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({a:{k:{n:v[n] for n in ('status','strict_pass','semantic_pass') if n in v} for k,v in d.items()} for a,d in out.items()},indent=2))
