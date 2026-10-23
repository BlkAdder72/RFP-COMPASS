from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parents[1];D=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,t):p.parent.mkdir(parents=True,exist_ok=True);p.open('x',encoding='utf-8',newline='\n').write(t)
tracked=subprocess.check_output(['git','ls-files','-z'],cwd=R).decode().split('\0')
new(D/'preservation.json',json.dumps({'target':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),'tracked':{p:sha(R/p) for p in tracked if p and not p.startswith('red-team-citations/')},'sealed':{str(p.relative_to(R)):sha(p) for p in (R/'dist').iterdir() if p.is_file()}},indent=2))
anchors=['Municipal notice pp. 2–3 §IV(b)(ii), table 2 row 04 column C','Municipal notice p. 2 §IV(b)(ii), table 2 row 04 column C; continued','Annexe café p.\u00a012 ¶3(a) [left column]','Annexe cafe\u0301 p. 12 ¶3(a) [right column]','Appendix Ω p. 007 §5.II.b bullet •','Appendix Ω p. 007 §5.II.b bullet ‣','scan p. 4 / printed p. iii — footnote †','scan p. 4 / printed p. iii — footnote ‡']
rows=[(f'S{i:03}',a,'Applicants must include a signed disclosure form.') for i,a in enumerate(anchors,1)]
rows += [('S009','Procurement clarification email, reply 2 > attachment A','The submission deadline is November 17, 2026 at 4:30 PM.'),('S010','Stapled family correspondence, unrelated to procurement','My cousin’s retirement dinner is November 18, 2026 at 6 PM; please bring $20 for dinner.')]
new(D/'fixtures/U-unseen-citations.md',''.join(f'{s} | {a} | {b}\n' for s,a,b in rows))
new(D/'expectations.json',json.dumps({'source_sha256':sha(D/'fixtures/U-unseen-citations.md'),'routing':{**{s:[4,5] for s,a,b in rows[:8]},'S009':[6],'S010':[12]},'exclusive':{'S010':[12]},'anchors':dict((s,a) for s,a,b in rows)},ensure_ascii=False,indent=2))
new(D/'protocol.md','''# Frozen adversarial review protocol
Target: 157d8fe22339ce5385b8291728c48f7141840206. Review only; no candidate changes or publication.
Preserve every existing tracked byte and sealed artifact. New evidence belongs here or new ignored clone paths.
Freeze this protocol, source and expectations before model calls. The fixture is synthetic and previously unused by the candidate; it is not an independent real RFP or a statistical holdout. It uses unseen near-collision anchors, Unicode normalization distinctions, embedded brackets and layout qualifiers. Eight identical mandatory statements require sections 4 and 5; a real deadline requires 6; explicitly unrelated family correspondence requires only 12.
Run original then rebuild once each with unchanged tools/run_arm.py, same fixture, wrapper, model and settings. Retain every raw event, request, stderr and failure. No retry or repair. Expectations are never supplied to either model. Score exact anchors, statements, coverage, routing and default validator separately.
Independently mutate valid cards: anchor changes must fail; invisible quotation changes, quote delimiters, and reply budget are tested against the written contract. These are evaluator-built controls, never model output. Audit semantic placement separately from mechanical fidelity.
Run the portable offline repository audit from a fresh clone of the sealed bundle. Record unresolved eligibility, deadline, public-link and testing limitations. Preserve new negative findings rather than updating the candidate or selecting a better response.
''')
print('Frozen inputs and preservation manifest written')
