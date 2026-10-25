# Context-boundary repair — second comparison retained, 2026-10-25

**HOLD: four private statements still leak in B, and the full run has a rejected S100 citation. This is a preserved failed attempt, not the final candidate.** The two-file knowledge correction repairs the first attempt’s D over-quarantine and new E boundary variation, but B routes private S002/S003/S005/S006 into operational sections. All raw evidence and frozen expectations remain untouched. A third separately frozen comparison in final-submission addresses the classification order; no release is created for this failed candidate.

## Intervention and sequence

Protocol, same A-D sources plus new E, source-bound expected answers and unchanged 162 controls were frozen in b621c888. The first failed comparison and its report-byte correction were preserved in 118f24d. All 31,996 earlier tracked files and 47 sealed artifact files were then snapshotted/preserved, with nine mutable before files. Fresh original baseline 181fec3 precedes candidate 4431685. Only rules.md and reference/output-schema.md change among the six knowledge files; the entire warning/strict validator is unchanged from 0f1c29e. Canonical runners, gpt-6-astra medium, same ordered sources, fresh sessions and exact full-RFP continues; no tools, retries, best-of selection, expected-answer prompts or raw corrections. Host messages and native-Claude attachment behavior remain uncontrolled/unverified. Root Q1–Q8 remain identical to bfdd812.

The intended change was statement-level boundary handling: a private heading cannot quarantine genuine later procurement duties; inclusion/exclusion is local, and mixed statements retain whole quotations operationally. The intervention succeeded on D/E but did not adequately constrain classification of negative/optional personal relations in B. This is not universal closure.

The fresh full rebuilt run also substitutes a neighboring `pp. 9-10` anchor for S100’s literal `p. 9` in Section 6. The unchanged strict validator rejects this occurrence. This is a new exact-anchor regression relative to the first comparison’s rebuilt full run and the current original full run. The failed raw parts, first report draft and full score are preserved; no output is corrected. The third comparison’s pre-candidate citation addendum addresses source-row retrieval without relaxing the universal exact-anchor gate.

## Recorded results

| Question | Original | Rebuild | Comparison |
|---|---|---|---|
| Q1 | fail | pass | improved |
| Q2 | pass | pass | tied |
| Q3 | partial | pass | improved |
| Q4 | pass | pass | tied |
| Q5 | pass | pass | tied |
| Q6 | partial | pass | improved |
| Q7 | fail | pass | improved |
| Q8 | partial | pass | improved |

Five improvements, three ties, no frozen-question regressions. Q8 uses default warnings with no sidecar. All ten core cards pass common strict validation.

| Supplemental case | Original combined | Rebuild combined |
|---|---|---|
| A-exclusions-and-mixed-deadlines | PASS | PASS |
| B-negation-and-private-content | FAIL | FAIL |
| C-opaque-citation-variants | PASS | PASS |
| D-boundary-guards | FAIL | PASS |
| E-context-boundary-variation | FAIL | PASS |

All ten supplemental cards preserve exact quotations and anchors. C is a pass/pass tie. D now retains genuine S008/S009 and private S001–S004 correctly. E also passes. B still fails exclusive Section-12 checks for S002/S003/S005/S006: contracted negative dependency and optional attendance are treated as procurement context, contaminating the following personal dates. These four checks regressed relative to the first candidate’s B card; the original also fails them in this comparison. A FAIL/FAIL aggregate must not hide the contrast with the earlier candidate. No false personal date hints on the rebuilt B card is not success when it already leaks those records operationally.

The warning code remains 162/162, original 104/162; all 73 historical rebuilt executions pass while original retains four known permissive-copy failures out of 70. The causal warning replay remains boundary-repair/same-card-warning-replay.json: exact same raw card/source, six false date IDs before, none after. This later knowledge correction did not change that validator or cause those warning gains.

## Fresh full-length comparison

| Check | Original | Rebuild |
|---|---|---|
| exact_shape_quotes_coverage | True | False |
| exact_statement_text | True | True |
| exact_anchors | True | False |
| all_221_ids | True | True |
| noise_only12 | False | True |
| genuine_routing | False | True |
| forbidden_routing_clear | True | True |
| no_personal_review_hints | True | True |
| max150_bullets_per_reply | True | True |
| complete | True | True |

original: parts 5, bullets [83, 79, 66, 138, 68], quote mismatches [], anchor mismatches [], missing selected placements ['S066', 'S083', 'S148'], noise only12 {'S215': True, 'S216': False, 'S217': False, 'S218': False, 'S219': False, 'S220': False, 'S221': False}.

rebuild: parts 4, bullets [111, 94, 142, 71], quote mismatches [], anchor mismatches [{'sid': 'S100', 'section': 6, 'actual': 'TBRPC Auditing RFP pp. 9-10 §7 Selection Process', 'expected': 'TBRPC Auditing RFP p. 9 §7 Selection Process'}], missing selected placements [], noise only12 {'S215': True, 'S216': True, 'S217': True, 'S218': True, 'S219': True, 'S220': True, 'S221': True}.

The selected matrix is not exhaustive semantic grading. Synthetic cases and one model run per version do not establish general reliability or native-Claude acceptance. Both failed candidate comparisons remain visible, not replaced by a chosen successful response. The full raw rebuilt run is copied byte-for-byte under rebuild/run-results/submission-repair-full/.

## Acceptance and preservation

Historical integrity verification is separate from behavioral acceptance. verify_acceptance.py preserves the original stronger gate and would reject the failed B model result. No behavioral assertion is made true by changing a checker. The historical verify.py checks source, chronology, raw messages, frozen cases, exact-copy controls, preservation and unchanged validation; it does not label this comparison accepted. Root results mirrors this HOLD report while current. The prior newline-only verification failure and its correction remain preserved in boundary-repair. Membership and final public URL are unverified; the three-sentence draft is not posted. No release is created and nothing is published.
