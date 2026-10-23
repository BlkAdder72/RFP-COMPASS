from pathlib import Path
import shutil
R=Path(__file__).resolve().parents[1];D=R/'final-repair';E=D/'attempt-2';E.mkdir(exist_ok=False)
for name in ['score_core.py','score_new.py','score_full.py']:
 s=(D/name).read_text(encoding='utf-8').replace('parents[1]','parents[2]').replace("D=R/'final-repair'","D=R/'final-repair/attempt-2'").replace('final-repair-core','final-repair-v2-core').replace('final-repair-new','final-repair-v2-new').replace('final-repair-full','final-repair-v2-full')
 (E/name).open('x',encoding='utf-8').write(s)
for name in ['full-expectations.json','expectations.json']:shutil.copyfile(D/name,E/name)
shutil.copytree(D/'fixtures',E/'fixtures')
p=D/'write_reports.py';s=p.read_text(encoding='utf-8')
s=s.replace("core=json.loads((D/'scores-final.json')","E=D/'attempt-2'\ncore=json.loads((E/'scores-final.json')").replace("full=json.loads((D/'full-length-results.json')","full=json.loads((E/'full-length-results.json')").replace("new=json.loads((D/'new-results.json')","new=json.loads((E/'new-results.json')")
s=s.replace('final-repair-{{core,new,full}}','final-repair-v2-{{core,new,full}}').replace('final-repair/new-results.json','final-repair/attempt-2/new-results.json').replace('final-repair/full-length-results.json','final-repair/attempt-2/full-length-results.json')
s=s.replace('Identity, input schema and worked examples were not altered for this repair.','Identity and input schema were not altered. The second attempt extends the general synthetic anchor example with single-page/page-range near-collisions; that example was chosen after inspecting the new failure.')
s=s.replace('This is a targeted repair with one fresh pair per fixture and one fresh full-length pair, after inspecting failures.','This repair had two versioned attempts. The first failed full-length citation validation; the second has one fresh pair per fixture and one fresh full-length pair after that failure.')
s=s.replace('## Frozen questions','''## First attempt: failed and preserved

The initial final-repair candidate passed Q1–Q8, all three new cases, the S076 placement check and personal containment, but changed one S100 Section 6 anchor from its own single-page citation to the next statement’s page range. The unchanged strict validator rejected it. Original copied all anchors exactly. This was a real copying regression; it is not counted as a pass or replaced by the later run.

Exact first-attempt knowledge, scores, scorers and hashes remain in `final-repair/attempt-1/` and `attempt-1-knowledge/`; all raw runs remain at `run-ARM/final-repair-*`. Before the second knowledge change, a new protocol was frozen and a new original baseline was committed. The second version adds a general p.-versus-pp. safeguard and four-row synthetic near-collision example; it adds no S100 or actual RFP answer. Both arms then rerun all cases and the full input in the same order. The validator and expectations are unchanged between attempts.

## Frozen questions''')
s=s.replace("'rebuild/run-results/final-repair-full'","'rebuild/run-results/final-repair-v2-full'").replace("'run-rebuild/final-repair-full'","'run-rebuild/final-repair-v2-full'").replace('`run-results/final-repair-full/`','`run-results/final-repair-v2-full/`').replace('run-rebuild/final-repair-full.','run-rebuild/final-repair-v2-full.')
s=s.replace('`run-original/final-repair-*`, `run-rebuild/final-repair-*`','`run-original/final-repair-v2-*`, `run-rebuild/final-repair-v2-*`')
p.write_text(s,encoding='utf-8',newline='\n')
p=D/'package.py';s=p.read_text(encoding='utf-8').replace("R/'final-repair/full-length-results.json'","R/'final-repair/attempt-2/full-length-results.json'");p.write_text(s,encoding='utf-8',newline='\n')
print('Second-version scorers and honest report template prepared; model knowledge unchanged')
