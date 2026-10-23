from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'citation-repair'
t=(R/'hardening/score_final_core.py').read_text(encoding='utf-8').replace("D=R/'hardening'","D=R/'citation-repair'").replace("/('run-'+arm)/'hardening'","/('run-'+arm)/'citation-repair-core'")
(D/'score_core.py').write_text(t,encoding='utf-8')
t=(R/'hardening/score_full.py').read_text(encoding='utf-8').replace("D=R/'hardening'","D=R/'citation-repair'").replace("/('run-'+arm)/'hardening-full'","/('run-'+arm)/'citation-repair-full'")
(D/'score_full.py').write_text(t,encoding='utf-8')
print('Scorers derived without changing earlier score scripts or evidence.')
