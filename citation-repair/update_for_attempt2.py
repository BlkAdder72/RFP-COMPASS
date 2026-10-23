from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'citation-repair'
t=(D/'attempt-1/score_core.py').read_text(encoding='utf-8').replace("'citation-repair-core'","'citation-repair-v2-core'")
(D/'score_core.py').write_text(t,encoding='utf-8')
t=(D/'attempt-1/score_full.py').read_text(encoding='utf-8').replace("'citation-repair-full'","'citation-repair-v2-full'")
(D/'score_full.py').write_text(t,encoding='utf-8')
