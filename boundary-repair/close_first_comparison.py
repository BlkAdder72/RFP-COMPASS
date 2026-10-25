from pathlib import Path
import json,shutil
R=Path(__file__).resolve().parents[1];D=R/'boundary-repair'
def read(n):return json.loads((D/n).read_text(encoding='utf-8'))
scores=read('scores-final.json');model=read('model-results.json');full=read('full-length-results.json');controls=read('control-results.json');before=read('before-control-results.json')
text='''# Boundary warning repair — first comparison retained, 2026-10-25

**Hold: a new semantic failure was found. This is not the final submission candidate.** All seven warning finding families in `red-team-polarity/REPORT.md` are repaired in the frozen evaluator cases, but raw model fixture D incorrectly quarantines later genuine requirements after an initial private heading. The warning validator detects S008/S009; structural validation still passes because it does not prove routing. This failed comparison is preserved and motivates a separately frozen context-boundary repair in `submission-repair/`.

## What changed

The warning filter binds `not included in`/`not part of` to a requirement-scope object, recognizes relative exclusions, handles straight/curly contracted predicate negation without misreading `not payment`, avoids creating new event scope from explicit optionality/no-attendance conditions, supports complete worded private shares and coordinated birthday activities, recognizes bounded parenthetical private headings, and prevents a `with ... to <action>` adjunct borrowing personal evidence. Independent procurement/clinical duties still retain hints. Negative attendance cannot clear inherited duties. The exact-copy/structure implementation from `def difference` onward is byte-identical; all six model knowledge files are unchanged.

## Sequence and comparison

Cases, 162 controls and selected source-hash-bound routing expectations were frozen in 51d7cd5. Complete original core/supplemental/full baseline: 7eefb2d. Warning candidate: 0f1c29e, before every rebuilt call. Root questions remain identical to bfdd812. Both arms used canonical runners, gpt-6-astra medium, same ordered sources and six-file selection, fresh sessions and exact full-RFP continues. No tools, retries, best-of selection, evaluator answers in prompts or corrected raw outputs. The cases are targeted synthetic probes; host messages remain uncontrolled and inline files are not native Claude attachments.

## Recorded outcomes

'''
text+='| Frozen question | Original | Rebuild | Comparison |\n|---|---|---|---|\n'
for q,x in scores['comparisons']['1'].items():text+=f"| {q} | {x['original']} | {x['rebuild']} | {x['comparison']} |\n"
text+='\nQ1–Q8: five improvements, three ties, zero regressions. Q8 uses default invocation without a sidecar. Ten core cards pass common strict validation.\n\n'
text+='| Supplemental fixture | Original combined checks | Rebuild combined checks |\n|---|---|---|\n'
for n in model['original']:text+=f"| {n} | {'PASS' if model['original'][n]['passed_all_checks'] else 'FAIL'} | {'PASS' if model['rebuild'][n]['passed_all_checks'] else 'FAIL'} |\n"
text+='''
All eight supplemental cards preserve complete quotes and anchors. Original B leaks private content; rebuild B passes all selected placements and produces no false personal hints. C is an exact-citation pass/pass tie, not a new win.

**D must not be summarized only as FAIL/FAIL.** The original leaks private S002/S003/S004 operationally but retains genuine S008/S009 in Section 6. Rebuild D correctly contains those private statements, yet puts all nine IDs only in Section 12, losing genuine S008/S009 and violating their Section-12 exclusions. The four regressed subchecks are S008_required, S009_required, S008_forbidden_clear and S009_forbidden_clear. The repaired validator warns on both missed dates. The model knowledge was unchanged by the warning repair, so this fresh semantic difference is not evidence that warning-code changes caused routing behavior. Both the failure and the reason for a substantive knowledge correction remain visible.

Warning controls: original 104/162, preceding candidate 146/162, repaired candidate 162/162. This is sixteen improvements and 146 ties against the preceding tool, with no control regressions. It includes all ten previously reported failed controls plus six additional failing variations. The older 120 cases still pass. Historical replay: all 73 rebuilt executions pass; original retains four known permissive-quotation failures among 70 executions. Neither original failures nor earlier failed repairs were erased.

The exact prior rebuilt red-team B card was replayed unchanged: six false date IDs before, none after. Its source/card hashes are identical between runs. See same-card-warning-replay.json.

## Fresh full-length RFP

'''
text+='| Check | Original | Rebuild |\n|---|---|---|\n'
for n in full['original']['checks']:text+=f"| {n} | {full['original']['checks'][n]} | {full['rebuild']['checks'][n]} |\n"
text+=f"\nOriginal bullets per reply: {full['original']['bullets_per_part']}; rebuild: {full['rebuild']['bullets_per_part']}. Both have all 221 IDs and exact quotes/anchors. Original leaks six of seven synthetic private IDs and misses selected required placements for {[s for s,v in full['original']['genuine_routing'].items() if not v]}. Rebuild passes the selected matrix and contains all seven private IDs only in Section 12. The original's exact-copy improvement over a prior run is model variation, not a new original repair. Raw continuations and failures remain preserved.\n"
text+='''
## Preservation and release decision

All 27,828 prior tracked files and 47 sealed files are preserved; seven mutable files have exact before snapshots. The full rebuilt raw run is copied exactly under rebuild/run-results/boundary-repair-full/. Root results mirrors this report while this comparison is current. Integrity verification is distinct from behavioral acceptance. No release archive is created for this failed semantic candidate; final packaging waits for the separate context-boundary comparison. The unposted three-sentence draft, eligibility uncertainty, public-URL placeholder, finite-heuristic limits and lack of native-Claude acceptance remain explicit. Nothing is published.
'''
(D/'REPORT.md').open('x',encoding='utf-8',newline='\n').write(text);(R/'results.md').write_text(text,encoding='utf-8',newline='\n')
src=R/'run-rebuild/boundary-repair-full';dst=R/'rebuild/run-results/boundary-repair-full';shutil.copytree(src,dst);(dst/'.gitattributes').write_text('* -text\n',encoding='utf-8')
for n in ['README.md','packaging/COMPLIANCE.md']:
 p=R/n;t=p.read_text(encoding='utf-8').replace('`dist/boundary-release/`','`dist/boundary-release/` (not sealed: semantic D failed)');p.write_text(t,encoding='utf-8',newline='\n')
(D/'SUMMARY.json').open('x').write(json.dumps({'acceptance':'HOLD — semantic D fails; next frozen comparison required','core':scores['totals'],'controls':{a:sum(c['passed'] for c in controls if c['arm']==a) for a in ['original','rebuild']},'before_rebuild_controls':sum(c['passed'] for c in before if c['arm']=='rebuild'),'total_controls':162,'rebuild_full_pass':full['rebuild']['passed'],'D_regressed_subchecks':['S008_required','S009_required','S008_forbidden_clear','S009_forbidden_clear'],'published':False,'release_created':False},indent=2))
print('Preserved failed first comparison, exact full raw copy and honest report')
