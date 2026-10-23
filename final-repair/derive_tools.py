from pathlib import Path
R=Path(__file__).resolve().parents[1];D=Path(__file__).resolve().parent
def new(p,s):p.open('x',encoding='utf-8',newline='\n').write(s)
s=(R/'citation-repair/score_core.py').read_text(encoding='utf-8').replace("D=R/'citation-repair'","D=R/'final-repair'").replace('citation-repair-v2-core','final-repair-core');new(D/'score_core.py',s)
s=(R/'citation-repair/score_full.py').read_text(encoding='utf-8').replace("D=R/'citation-repair';source=D/'fixtures/Z-full-length-noisy.md'","D=R/'final-repair';source=R/'hardening/fixtures/Z-full-length-noisy.md'").replace('full-length-expectations.json','full-expectations.json').replace('citation-repair-v2-full','final-repair-full');new(D/'score_full.py',s)
s=(R/'hardening/replay.py').read_text(encoding='utf-8').replace("D=R/'hardening';O=D/'replays'","D=R/'final-repair';O=D/'historical-replays'");new(D/'replay.py',s)
print('Derived scorers retain old logic and add frozen S076 through expectations')
