from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'hardening'
(D/'candidates/final.py').write_bytes((R/'rebuild/tools/validate_packet.py').read_bytes())
t=(D/'replay_controls.py').read_text(encoding='utf-8').replace("O=D/'prior-controls'","O=D/'final-prior-controls'").replace("D/'prior-controls.json'","D/'final-prior-controls.json'")
(D/'final_replay_controls.py').write_text(t,encoding='utf-8')
t=(D/'replay.py').read_text(encoding='utf-8').replace("O=D/'replays'","O=D/'final-replays'").replace("D/'replay-results.json'","D/'final-replay-results.json'")
(D/'final_replay.py').write_text(t,encoding='utf-8')
t=(D/'score_core.py').read_text(encoding='utf-8').replace("trial/'validation.txt'","trial/'validation-final.txt'").replace("base/'Q8-default'","base/'Q8-final'").replace("base/'scores.json'","base/'scores-final.json'").replace("D/'scores.json'","D/'scores-final.json'")
(D/'score_final_core.py').write_text(t,encoding='utf-8')
