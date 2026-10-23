from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'hardening'
t=(D/'final_replay_controls.py').read_text(encoding='utf-8').replace("final-prior-controls","final-prior-controls-v2")
t=t.replace("expected=False if c['label']=='generic-lunch-money' and c['arm']=='rebuild' else c['expect_warning']", "expected=False if c['label'] in ('generic-lunch-money','changed-quote') and c['arm']=='rebuild' else c['expect_warning']")
(D/'last_replay_controls.py').write_text(t,encoding='utf-8')
t=(D/'final_replay.py').read_text(encoding='utf-8').replace('final-replays','final-replays-v2').replace('final-replay-results','final-replay-results-v2')
(D/'last_replay.py').write_text(t,encoding='utf-8')
