from pathlib import Path
import json,shutil
R=Path(__file__).resolve().parents[1];D=R/'final-submission'
def read(n):return json.loads((D/n).read_text(encoding='utf-8'))
scores=read('scores-final.json');models=read('model-results.json');full=read('full-length-results.json');m=read('preservation.json');ch=read('chronology.json');cs=read('control-results.json');hist=read('historical-control-replays-release.json')
assert all(x['passed_all_checks'] for x in models['rebuild'].values()) and full['rebuild']['passed']
assert all(x['verdict']=='pass' for x in scores['scores']['1']['rebuild'].values())
assert len(cs)==324 and all(c['passed'] for c in cs if c['arm']=='rebuild') and all(c['passed'] for c in hist if c['arm']=='rebuild')
t='''# RFP Compass — final measured repair, 2026-10-25

**PASS on all final recorded behavioral gates; local candidate, unpublished.** The seven warning finding families are repaired in the frozen controls, and the final model comparison passes the retained semantic failures, the context variation and the full noisy RFP. Two failed candidate comparisons remain preserved below. These finite results are not a claim of perfect natural-language classification or native-Claude acceptance.

## Changes tied to the findings

| Finding | Implemented repair and preserved boundary |
|---|---|
| F1: exclusion from a different program hid compulsory dates | Exclusion predicates bind to their scope object. Being outside a different schedule does not waive a still-compulsory duty. Positive inclusion and negated exclusion retain scope. |
| F2: mixed personal/credential deadline lost its hint | An action-bearing `with ... to <action>` adjunct cannot borrow a preceding personal cue. Mixed statements retain their whole quote and genuine operational placements. |
| F3: optional/no-condition events polluted private context | Explicit optionality/no-attendance conditions do not create unknown-event scope. They cannot erase an inherited or independent genuine duty. |
| F4: private coordination/shares produced false warnings | Complete birthday activity fragments and bounded worded dollar shares are recognized; unknown actions and independent procurement/clinical cues keep hints. |
| F5: contracted negation was affirmative | Negation is expanded only in analysis and must modify the dependency predicate. `Not payment` does not negate attendance dependence; `not only` remains affirmative. |
| F6: relative exclusion did not release a private subsection | Local heading relations recognize relative copulas and quoted labels while binding exclusion to its named subsection and scope. |
| F7: parenthetical private heading became event scope | Parentheses are accepted only around a supported private annotation. Explicit inclusion or clinical/procurement context keeps warning protection. |

The warning implementation was committed in 0f1c29e after the first original baseline. Its complete code is unchanged in the final comparison. Strict quotation, opaque-anchor, ID/coverage/order, heading, extra-prose and continuation checks remain byte-identical to the pre-repair implementation from `def difference` onward. No source IDs, filenames or benchmark answer tables are classification rules; quotations and source anchors are never rewritten by warning analysis.

The warning-only model attempt then over-quarantined later genuine duties. A second knowledge candidate fixed that but leaked negative/optional personal records and altered one full-RFP citation. The final knowledge repair makes relevance decisions in source order, requires affirmative source support before private dates become operational, prevents later duties from retroactively contaminating unrelated private records, resumes ordinary routing for genuine later requirements and their explicitly included subsections, and retrieves literal source-row fields per emitted occurrence. Only rules.md and reference/output-schema.md change among the six knowledge files in the final comparison; the other four and the entire validator are unchanged. Exact output structure and whole-statement quotation obligations are retained.

## Frozen sequence and fair comparison

'''
t+=f"Final source/expectation freeze: {ch['freeze']}. Citation safeguard addendum: {ch['citation_addendum']}. Completed fresh original baseline: {ch['original_baseline']}. Final knowledge candidate: {ch['candidate']}, before every final rebuilt model call. The second failed comparison is preserved at {ch['preserved_second_comparison']}. Root questions.md remains identical to bfdd812 and its original feedback-derived chronology is preserved.\n\n"
t+='''All three comparisons used unchanged canonical runners, gpt-6-astra medium, the same six-file selection, the same ordered relevant sources and fresh sessions. The full RFP uses a fresh persistent session and exact `continue` turns. No tools, retries, best-of selection, evaluator answers in prompts or raw-output corrections. Each substantive candidate was committed after its own fresh original baseline. Final A-E sources and expectations, the 162 controls and full source were not relaxed after failures. Host system instructions remain uncontrolled; UTF-8 inline named files are not native Claude attachments. Cases are targeted synthetic probes informed by feedback and prior failures, not an independent population holdout.

## Frozen feedback questions

| Question | Original | Rebuild | Comparison |
|---|---|---|---|
'''
for q,x in scores['comparisons']['1'].items():t+=f"| {q} | {x['original']} | {x['rebuild']} | {x['comparison']} |\n"
t+=f"\nTotals: {scores['totals']}. Q8 uses ordinary default warning handling with no exclusion sidecar. Individual checks and regressed subchecks remain in scores-final.json. Ten core cards are also checked with the same strict rebuilt validator.\n\n"
t+='''## Supplemental paired model cases

| Fixture | Original combined checks | Rebuild combined checks |
|---|---|---|
'''
for n in models['original']:t+=f"| {n} | {'PASS' if models['original'][n]['passed_all_checks'] else 'FAIL'} | {'PASS' if models['rebuild'][n]['passed_all_checks'] else 'FAIL'} |\n"
for arm,data in models.items():
 for n,x in data.items():
  bad=[k for k,v in x['semantic_checks'].items() if not v]
  if bad or x['mismatches'] or x['personal_review_hints']:t+=f"\n{arm} {n}: failed selected checks {bad}; exact-copy differences {x['mismatches']}; personal review hints {x['personal_review_hints']}.\n"
t+='''
These checks separate literal copying, selected placements, private-only containment and warning accuracy. No false warning is claimed as a success when a model already leaked the date into an operational section. Model C’s exact citation behavior is a tie when both versions pass. It includes six new opaque Unicode/entity anchors, not new evidence for every possible citation encoding. All six altered-anchor controls are still rejected. Selected matrices are not exhaustive semantic grading.

## Fresh full-length noisy RFP

The unchanged source contains 214 real TBRPC statements plus seven synthetic private records. All parts, exact continuation prompts and raw event streams are preserved.

| Check | Original | Rebuild |
|---|---|---|
'''
for k in full['original']['checks']:t+=f"| {k} | {full['original']['checks'][k]} | {full['rebuild']['checks'][k]} |\n"
for arm,x in full.items():t+=f"\n{arm}: {x['parts']} parts, bullet counts {x['bullets_per_part']}; {x['cited_distinct_ids']} distinct source IDs; quote differences {x['quote_mismatches']}; anchor differences {x['anchor_mismatches']}; missing selected placements {[s for s,v in x['genuine_routing'].items() if not v]}; private-only-12 checks {x['noise_only12']}.\n"
t+='''
The final rebuilt raw run is copied byte-for-byte under rebuild/run-results/final-submission-full/. All 221 IDs, every quote/anchor occurrence and the selected semantic matrix are gated separately. Original changes across repeated baselines are model variability, not repairs to the pinned original; none of those baselines is discarded. One successful final comparison does not establish a statistical reliability rate.

## Warning and validation controls

'''
for a in ['original','rebuild']:t+=f"- {a}: {sum(x['passed'] for x in cs if x['arm']==a)}/162 frozen controls.\n"
t+='''
The initial candidate was 146/162 on this same expanded suite; its sixteen failures remain in boundary-repair/before-control-results.json. The warning repair reaches 162/162: sixteen improvements, 146 ties and no control regressions against that tool baseline. All older 120 cases still pass. The final knowledge-only change does not earn a second warning improvement: the warning implementation stays unchanged and ties the passing warning candidate. Original strict-copy tolerance failures remain visible; native original validation alone never grades the rebuilt routing or exact-copy contract.

Historical replay remains in historical-control-replays-release.json: all 73 rebuilt executions pass; original retains four known permissive-copy failures among 70 executions. Default packaged-sample validation is recorded separately. The exact same old rebuilt B card/source still produces six false date IDs before the warning fix and none after; source/card hashes in boundary-repair/same-card-warning-replay.json are identical between arms. The final validator hash equals that repaired tool. This comparison isolates warning-code behavior from model variability.

The second candidate’s failed full card is not repaired or hidden: retained-S100-rejection.json records rejection of its altered S100 anchor, and the current offline verifier rechecks its source/part hashes and reruns strict rejection. Successful new output does not overwrite this failed evidence or weaken the anchor gate.

## Failed attempts, ties and regressions retained

1. **boundary-repair/REPORT.md:** the warning-only candidate passed 162 controls and the full RFP, but D put every statement only in Section 12. Genuine S008/S009 disappeared operationally, creating four regressed subchecks against the original despite improved private containment. The validator correctly warned on the omissions. No failed response was corrected. The six knowledge files were unchanged, so the model difference cannot be attributed causally to warning code.
2. **submission-repair/REPORT.md:** the two-file context correction passed D/E but B leaked private S002/S003/S005/S006, regressing four containment checks against the preceding candidate. Its full run also replaced S100’s literal single-page anchor with a neighboring page range. Strict validation rejected it. Both original and rebuilt full runs, complete failed raw copies, first report drafts and score files remain preserved. Its historical integrity PASS is explicitly HOLD on behavioral acceptance; verify_acceptance.py retains its stronger, unsatisfied gate.
3. **Mechanical verification failure:** the first report mirror had identical text with different Windows line endings. The failed assertion and original CRLF report are preserved in boundary-repair; only report bytes were aligned. No raw response, source, score or failed check changed.

No candidate is described as better at everything. Final unchanged-behavior ties include literal-citation checks that both arms pass, preserved output structure, injected-instruction handling and official email handling where the frozen results tie. The judged original, PDF/source tools, source statements and original provenance remain intact. Final differences do not erase earlier model regressions or prove that all unseen language variants are resolved.

## Preservation, package and submission state

'''
t+=f"All {len(m['tracked'])} earlier tracked files and {len(m['artifacts'])} old sealed artifacts are preserved. Nine mutable files have exact before snapshots; other earlier files remain byte-identical. Full Git history and the judged original tag remain available. verification.json records current source, chronology, canonical requests, complete tool-free raw turns, frozen controls and hard behavioral acceptance checks. Root results.md is an exact mirror of this report.\n\n"
t+='''One current evidence map in README.md points to these final results and both failed comparisons; the rebuilt operating guide is shortened with the prior versions preserved. The submission comment remains an unposted three-sentence draft with a public-URL placeholder. Premium/VIP eligibility and native-Claude acceptance remain unverified. No external action is authorized or performed.

The source ZIP and complete-history Git bundle are created only after the current source and evidence are committed cleanly. The sealed target, checksums and actual fresh-clone compliance result live in dist/final-submission-release/RELEASE.json, SHA256SUMS.txt and FINAL_VERIFICATION.json. Do not infer delivery success from this report if the final receipt is absent or failed. Packaging compliance and measured behavioral success are separate gates; neither establishes universal semantic perfection. Publication remains on hold until the user authorizes it and the public URL/eligibility are settled.
'''
(D/'REPORT.md').open('x',encoding='utf-8',newline='\n').write(t);(R/'results.md').write_text(t,encoding='utf-8',newline='\n')
src=R/'run-rebuild/final-submission-full';dst=R/'rebuild/run-results/final-submission-full';shutil.copytree(src,dst);(dst/'.gitattributes').write_text('* -text\n',encoding='utf-8')
(D/'SUMMARY.json').open('x',encoding='utf-8',newline='\n').write(json.dumps({'acceptance':'PASS all final recorded behavioral gates; unpublished','core':scores['totals'],'controls':{a:sum(x['passed'] for x in cs if x['arm']==a) for a in ['original','rebuild']},'total_controls':162,'model_combined':{a:sum(x['passed_all_checks'] for x in v.values()) for a,v in models.items()},'model_cases':5,'rebuild_full_pass':full['rebuild']['passed'],'prior_files_preserved':len(m['tracked']),'old_sealed_files_preserved':47,'failed_candidates_preserved':['boundary-repair','submission-repair'],'strict_validator_unchanged':True,'published':False},indent=2));print('Final measured report, summary and exact full raw copy created')
