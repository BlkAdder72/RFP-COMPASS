from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'final-submission'
for n in ['capture_preservation.py']:
 t=(R/'submission-repair'/n).read_text(encoding='utf-8').replace('submission-repair','final-submission');(D/n).open('x',encoding='utf-8',newline='\n').write(t)
t=(R/'submission-repair/verify.py').read_text(encoding='utf-8').replace('submission-repair','final-submission')
t=t.replace("assert not read(D/'model-results.json')['rebuild']['B-negation-and-private-content']['semantic_pass']","assert all(x['passed_all_checks'] for x in read(D/'model-results.json')['rebuild'].values())\nassert read(D/'full-length-results.json')['rebuild']['passed']\nassert all(x['verdict']=='pass' for x in read(D/'scores-final.json')['scores']['1']['rebuild'].values())\nassert read(D/'retained-S100-rejection.json')['passed']")
t=t.replace("assert read(D/'SUMMARY.json')['acceptance'].startswith('HOLD')","assert read(D/'SUMMARY.json')['acceptance'].startswith('PASS')")
t=t.replace("'status':'PASS preserved-failure integrity','behavioral_acceptance':'HOLD — B semantic failure preserved'","'status':'PASS','behavioral_acceptance':'PASS all final recorded gates'")
(D/'verify.py').open('x',encoding='utf-8',newline='\n').write(t)
print('Prepared final preservation and hard behavioral acceptance audit')
