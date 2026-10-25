from pathlib import Path
import json,shutil
R=Path(__file__).resolve().parents[1];D=R/'submission-repair'
def read(n):return json.loads((D/n).read_text(encoding='utf-8'))
scores=read('scores-final.json');models=read('model-results.json');full=read('full-length-results.json')
t='''# Context-boundary repair — second comparison retained, 2026-10-25

**HOLD: four private statements still leak in B. This is a preserved failed attempt, not the final candidate.** The two-file knowledge correction repairs the first attempt’s D over-quarantine and new E boundary variation, but B routes private S002/S003/S005/S006 into operational sections. All raw evidence and frozen expectations remain untouched. A third separately frozen comparison in final-submission addresses the classification order; no release is created for this failed candidate.

## Intervention and sequence

Protocol, same A-D sources plus new E, source-bound expected answers and unchanged 162 controls were frozen in b621c888. The first failed comparison and its report-byte correction were preserved in 118f24d. All 31,996 earlier tracked files and 47 sealed artifact files were then snapshotted/preserved, with nine mutable before files. Fresh original baseline 181fec3 precedes candidate 4431685. Only rules.md and reference/output-schema.md change among the six knowledge files; the entire warning/strict validator is unchanged from 0f1c29e. Canonical runners, gpt-6-astra medium, same ordered sources, fresh sessions and exact full-RFP continues; no tools, retries, best-of selection, expected-answer prompts or raw corrections. Host messages and native-Claude attachment behavior remain uncontrolled/unverified. Root Q1–Q8 remain identical to bfdd812.

The intended change was statement-level boundary handling: a private heading cannot quarantine genuine later procurement duties; inclusion/exclusion is local, and mixed statements retain whole quotations operationally. The intervention succeeded on D/E but did not adequately constrain classification of negative/optional personal relations in B. This is not universal closure.

## Recorded results

| Question | Original | Rebuild | Comparison |
|---|---|---|---|
'''
for q,x in scores['comparisons']['1'].items():t+=f"| {q} | {x['original']} | {x['rebuild']} | {x['comparison']} |\n"
t+='\nFive improvements, three ties, no frozen-question regressions. Q8 uses default warnings with no sidecar. All ten core cards pass common strict validation.\n\n| Supplemental case | Original combined | Rebuild combined |\n|---|---|---|\n'
for n in models['original']:t+=f"| {n} | {'PASS' if models['original'][n]['passed_all_checks'] else 'FAIL'} | {'PASS' if models['rebuild'][n]['passed_all_checks'] else 'FAIL'} |\n"
t+='''
All ten supplemental cards preserve exact quotations and anchors. C is a pass/pass tie. D now retains genuine S008/S009 and private S001–S004 correctly. E also passes. B still fails exclusive Section-12 checks for S002/S003/S005/S006: contracted negative dependency and optional attendance are treated as procurement context, contaminating the following personal dates. These four checks regressed relative to the first candidate’s B card; the original also fails them in this comparison. A FAIL/FAIL aggregate must not hide the contrast with the earlier candidate. No false personal date hints on the rebuilt B card is not success when it already leaks those records operationally.

The warning code remains 162/162, original 104/162; all 73 historical rebuilt executions pass while original retains four known permissive-copy failures out of 70. The causal warning replay remains boundary-repair/same-card-warning-replay.json: exact same raw card/source, six false date IDs before, none after. This later knowledge correction did not change that validator or cause those warning gains.

## Fresh full-length comparison

| Check | Original | Rebuild |
|---|---|---|
'''
for k in full['original']['checks']:t+=f"| {k} | {full['original']['checks'][k]} | {full['rebuild']['checks'][k]} |\n"
for a,x in full.items():t+=f"\n{a}: parts {x['parts']}, bullets {x['bullets_per_part']}, quote mismatches {x['quote_mismatches']}, anchor mismatches {x['anchor_mismatches']}, missing selected placements {[s for s,v in x['genuine_routing'].items() if not v]}, noise only12 {x['noise_only12']}.\n"
t+='''
The selected matrix is not exhaustive semantic grading. Synthetic cases and one model run per version do not establish general reliability or native-Claude acceptance. Both failed candidate comparisons remain visible, not replaced by a chosen successful response. The full raw rebuilt run is copied byte-for-byte under rebuild/run-results/submission-repair-full/.

## Acceptance and preservation

Historical integrity verification is separate from behavioral acceptance. verify_acceptance.py preserves the original stronger gate and would reject the failed B model result. No behavioral assertion is made true by changing a checker. The historical verify.py checks source, chronology, raw messages, frozen cases, exact-copy controls, preservation and unchanged validation; it does not label this comparison accepted. Root results mirrors this HOLD report while current. The prior newline-only verification failure and its correction remain preserved in boundary-repair. Membership and final public URL are unverified; the three-sentence draft is not posted. No release is created and nothing is published.
'''
(D/'REPORT.md').open('x',encoding='utf-8',newline='\n').write(t);(R/'results.md').write_text(t,encoding='utf-8',newline='\n')
src=R/'run-rebuild/submission-repair-full';dst=R/'rebuild/run-results/submission-repair-full';shutil.copytree(src,dst);(dst/'.gitattributes').write_text('* -text\n',encoding='utf-8')
(D/'SUMMARY.json').open('x',encoding='utf-8',newline='\n').write(json.dumps({'acceptance':'HOLD — B leaks S002/S003/S005/S006','core':scores['totals'],'controls':{'original':104,'rebuild':162,'total':162},'rebuild_full_pass':full['rebuild']['passed'],'rebuild_combined_supplemental':sum(x['passed_all_checks'] for x in models['rebuild'].values()),'supplemental_total':5,'published':False,'release_created':False},indent=2))
print('Retained second failed comparison and exact full raw copy')
