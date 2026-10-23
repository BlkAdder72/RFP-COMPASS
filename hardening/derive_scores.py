from pathlib import Path
R=Path(__file__).resolve().parents[1]
t=(R/'revision/score.py').read_text(encoding='utf-8').replace("D=R/'revision'","D=R/'hardening'").replace('for repeat in (1,2):','for repeat in (1,):').replace("/'revision-v2'/('repeat-'+str(repeat))","/'hardening'")
(R/'hardening/score_core.py').write_text(t,encoding='utf-8')
(R/'hardening/replay.py').write_text((R/'revision/replay.py').read_text(encoding='utf-8').replace("D=R/'revision'","D=R/'hardening'"),encoding='utf-8')
