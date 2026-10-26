# RFP Compass — sequential warning repairs, 2026-10-26

**PASS all recorded gates; unpublished.** The four remaining finding families in red-team-oct26/REPORT.md were repaired separately, with each issue's tests and all previously solved boundaries passing before the next edit. The original questions, all earlier evidence and all old sealed packages remain preserved. This is finite measured acceptance, not a claim of perfect language understanding.

## What changed and why

1. **F1, dependency wording.** Attendance conditions expressed as “hinges on” or “is dependent on” now retain warning protection. Their corresponding negative/contraction forms are analyzed with negation tied to the dependency predicate. “Not payment” and “not only” are positive guards. This repairs missed date warnings without treating the word participation alone as an obligation.
2. **F2, relation binding.** An exclusion before a private heading must bind to the requirement scope: an explicit `from` object or a supported scope subject. Being excluded from an office-hours program or daytime schedule cannot cancel a separate compulsory event requirement. Real exclusions and local subsection boundaries remain supported.
3. **F3, worded shares.** A bounded compositional English amount grammar covers hundreds and thousands. Complete private-share phrases are treated as a single unit during clause analysis so the `and` inside an amount is not mistaken for an independent action. Only that matched phrase is replaced in an analysis copy; original quotations/citations are untouched. Genuine mixed return, payment and credential deadlines retain hints.
4. **F4, annotated private headings.** Explicit outside-procurement annotations are recognized only within the complete private-heading grammar. Their own negative annotation no longer supplies an affirmative procurement cue. This cannot erase explicit inherited inclusion, clinical requirements or a later genuine duty.

Only rebuild/tools/validate_packet.py changes product behavior. The entire implementation from `def difference` onward is byte-identical, including strict quotations, opaque anchors, IDs, coverage, headings, prose and continuation checks. All six model knowledge files are unchanged. Source data, frozen questions, source-hash-bound matrices and raw model outputs were not corrected or relaxed.

## Ordered tests before moving on

207 controls were frozen: the prior 162, all 18 October 26 review controls and 27 new safety controls. Each stage runs all 207 across original, before and current validators, preserving every stdout/stderr/command and the actual stage validator. Stage gates require the prior 162, common guards and every issue solved so far; later issue failures remain visible until their own repair. Baseline reproduces 18 failures. Stage results:

| Stage | Required gate | Remaining failing controls across all 207 |
|---|---|---|
| F1 | PASS | 12 |
| F2 | PASS | 9 |
| F3 | PASS | 4 |
| F4 | PASS | 0 |

Final controls: original 128/207; before 189/207; repaired 207/207. Against before: {'improved': 18, 'tied': 189, 'regressed': 0}. These controls include correct private cards, deliberately missed genuine dates and altered citations; all-12 deliberate omissions can pass structure while still requiring advisory hints. Structural PASS never proves semantic placement.

One patch-driver setup assertion stopped after the passing F1 commit, before any F2 product edit. Correcting the patch-string quoting resumed the sequence without repeating a model trial or replacing a validator result. DRIVER_FIRST_ATTEMPT.txt and DRIVER_NOTE.md retain that interruption.

## Frozen questions and fresh fair model comparison

Freeze 79257825; completed fresh original baseline d6833c94c89a0289172de299364d5bba1cc7a6d5; final validator candidate 225d921e91e1f476adf893429c98b1465624f116. Each fix is separately committed after passing its own gate. Q1–Q8 remain identical to bfdd812 and the initial competition chronology remains in Git history.

Same canonical runners, gpt-6-astra medium, six unchanged knowledge files, same core/new/full order and source packets, fresh sessions, expected answers excluded, exact `continue` turns for full RFP. No agent retry, raw correction or best-of selection. Automatic client transport retries are separately retained in SUMMARY.json; a transport retry is not claimed as a pristine identical request environment. Because this repair changes only a validator, different generated cards are sampling variation rather than a demonstrated causal improvement in the translator. Before/after replay of the exact same card isolates the actual warning repair.

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

Totals: {'improved': 5, 'tied': 3, 'regressed': 0}. Q8 uses default handling without an exclusion sidecar. Regressed subchecks, if any, remain in scores-final.json.

| Supplemental fixture | Original combined | Rebuild combined |
|---|---|---|
| A-obligation-and-retrospective-scope | FAIL | PASS |
| B-personal-boundaries | FAIL | PASS |
| C-opaque-citations | PASS | PASS |

original A-obligation-and-retrospective-scope: failed selected checks ['S006_required']; exact-copy mismatches []; private review hints [].

original B-personal-boundaries: failed selected checks ['S002_exclusive', 'S003_exclusive', 'S004_exclusive']; exact-copy mismatches []; private review hints [].

original C-opaque-citations: failed selected checks []; exact-copy mismatches []; private review hints [].

rebuild A-obligation-and-retrospective-scope: failed selected checks []; exact-copy mismatches []; private review hints [].

rebuild B-personal-boundaries: failed selected checks []; exact-copy mismatches []; private review hints [].

rebuild C-opaque-citations: failed selected checks []; exact-copy mismatches []; private review hints [].

## Fresh full-length noisy RFP

214 real TBRPC statements plus seven synthetic personal records. Fresh original and rebuilt sessions, full raw continuations retained.

| Gate | Original | Rebuild |
|---|---|---|
| exact_shape_quotes_coverage | True | True |
| exact_statement_text | True | True |
| exact_anchors | True | True |
| all_221_ids | True | True |
| noise_only12 | False | True |
| genuine_routing | False | True |
| forbidden_routing_clear | True | True |
| no_personal_review_hints | True | True |
| max150_bullets_per_reply | True | True |
| complete | True | True |

original: 5 parts, bullets [88, 67, 64, 141, 70]; quote mismatches []; anchor mismatches []; missing selected routes ['S133', 'S066', 'S083', 'S148']; private-only failures ['S216', 'S217', 'S218', 'S219', 'S220', 'S221'].

rebuild: 4 parts, bullets [109, 98, 141, 70]; quote mismatches []; anchor mismatches []; missing selected routes []; private-only failures [].

## Preserved failures, unchanged strengths and limitations

The exact failed October 26 B card formerly warned on private S002/S004; the repaired default validator now gives no REVIEW on that identical source/card. The full failed S100 citation from submission-repair is still rejected. Earlier failed boundary/submission comparisons and all later red-team reports remain untouched. Old seals remain byte-identical; a new release path is used. Original judged source remains untouched. Four packaged samples pass; historical controls pass rebuilt 73/73. Original historical failures are retained.

No changes to translator rules, S133 handling, script-built provenance, sparse Section 12, prompt-injection behavior, input drafting or PDF trace behavior were necessary for these warning fixes. Those established strengths remain in the frozen core checks and historical audits. Validator source matching is not independent PDF-source authentication; PDF tracing remains a separate check and dependency.

The warning filter is a bounded heuristic; selected semantic matrices are not exhaustive grading. These are targeted synthetic cases and one fresh sample per model case, not an independent population holdout or a reliability estimate. Native Claude/attachment acceptance and Premium/VIP eligibility remain unverified. The public submission URL remains a placeholder until an authorized publication step. Repeated language expansion cannot establish “perfect”; the defensible claim is closure of these measured findings without observed regression within the recorded gates.

## Submission layout and delivery

Read feedback.md → questions.md → results.md. Original, verbatim feedback, rebuild, frozen questions and both raw arms remain at the required root locations. Latest evidence is warning-final/ and run-original/warning-final-* / run-rebuild/warning-final-*. Exact latest rebuilt full-RFP raw copy is rebuild/run-results/warning-final-full/. Older files remain evidence, not the current readiness report. The three-sentence SUBMISSION_COMMENT.md is unposted.

Offline audit: python -B -X utf8 tools/verify_submission.py. Nine historical assertions run unchanged at pinned commits before the current gate; no model calls. Source ZIP and full-history bundle use dist/warning-final-release/. Read its FINAL_VERIFICATION.json for actual fresh-clone compliance status; do not infer delivery completion from this report. No publication.
