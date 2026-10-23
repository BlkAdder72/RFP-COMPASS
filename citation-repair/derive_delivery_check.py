from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'citation-repair'
t=(R/'packaging/verify_delivery.py').read_text(encoding='utf-8').replace("C=D/'verification-scope-hardening'","C=D/'verification-citation-repair'")
needle='P.write_text(json.dumps(proof,indent=2),encoding=\'utf-8\')'
assert needle in t
t=t.replace(needle,"current=json.loads((R/'citation-repair/verification.json').read_text(encoding='utf-8'))\nproof['candidate_performance']=current['performance_summary']\nproof['both_validators_byte_identical']=current['both_validators_byte_identical']\n"+needle)
(D/'verify_delivery.py').write_text(t,encoding='utf-8')
