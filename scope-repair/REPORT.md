# Obligation scope repair — paired results, 2026-10-23

Targeted warning controls closed; fresh selected model checks pass.

Local candidate; unpublished. This stage addresses all four findings in `red-team-warning-final/REPORT.md`: missed obligation warnings, private-duty/context false warnings, unfamiliar private milestones, and the four-sentence submission draft. Earlier failed evidence, including the S072/S100 citation failures and unsafe suppression witnesses, remains unchanged.

## Change and validation boundary

Only warning relevance and the submission draft changed. Procurement/clinical domain cues and genuine inherited context retain their vetoes. Obligation language is examined by clause: a narrowly supported first-person private duty, with affirmative personal ownership/activity and no extra or mixed clauses, does not itself create procurement scope. It cannot clear existing mandatory scope. Unknown event-list headings preserve warning context without depending on a particular modality keyword. Offer-receipt constructions retain warnings. Christening and bridal-shower bodies are recognized alongside earlier personal milestones. Unknown, mixed, clinical and genuinely required content remains conservative. No filenames, source IDs or expected placements are used to infer unrelatedness. The submission draft is exactly the three frozen sentences in `scope-repair/submission-plan.json`.

The implementation from `def difference` onward is byte-identical to the reviewed validator: exact quotations including invisible characters, exact complete anchors, trusted per-ID exclusions, heading/order/coverage/continuation checks and rejection behavior remain intact. A warning is a review aid, not proof of semantic correctness. The six model knowledge files in each arm are unchanged from the previous reviewed candidate. New model differences therefore reflect fresh-run variability, not a new routing-prompt repair.

## Frozen questions and sequence

`questions.md` is byte-identical to commit bfdd812. Model inputs, expected routing, the initial 56 warning controls and protocol were committed before the original baseline. Two evaluator-only safety addenda were frozen before their own executions; they did not change the model inputs or authorize retries. The original ran A–E, A/B/C/D and the unchanged full RFP first, and its complete baseline was committed before applying the candidate filter. Rebuild then used the same sources/order, unchanged runners, gpt-6-astra medium, fresh sessions and exact recorded continuations. No tools, retries, best-of selection, output corrections or evaluator answers were supplied. Exact requests, events, commands, hashes and card equality are audited. Host system instructions are not controlled.

A/B/C repeat the newest red-team sources; D is a new synthetic scope combination. These are disclosed regression tests, not unseen real-world validation or fresh Claude acceptance. The full source is the same 214 real TBRPC statements plus seven synthetic personal statements. Its expanded selected semantic matrix was frozen before this pair; it does not grade every possible semantic placement.

## Q1–Q8

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

Question totals: {'improved': 5, 'tied': 3, 'regressed': 0}. Default Q8 uses no reviewed-exclusion sidecar. Full individual subchecks: `scope-repair/scores-final.json`. Common strict core results: `scope-repair/core-common-strict.json`.

## Four-finding closure

F1: unseen event-heading and offer-receipt obligations retain date warnings on the frozen misrouted cards. F2: supported private self-duties do not create scope or contaminate later personal records; genuine inherited scope and mixed duties retain warnings. F3: private christening and bridal-shower dates suppress their false hints. F4: the draft equals the frozen three-sentence plan, including the exact motivating feedback excerpt. See scope-repair/verification.json and the per-case controls for the actual measured status.

An intermediate warning implementation passed the first 56 controls, but inspection found an escaped-regex defect and an omitted extra-clause check. Its code and results remain in scope-repair/attempt-1 and controls. A separately frozen safety addendum exposed two unsafe suppressions on mixed private/deposit statements; those failures remain in controls-addendum-initial and addendum-initial-results.json. That correction preceded all rebuilt model trials. A later validator-only safety check then found a false warning under Family events headings; its failure and pre-heading code are preserved in controls-heading-initial and attempt-1/pre-heading-validator.py. The final candidate passes the complete 60-case set. The final warning-tool revision postdates the start of the unchanged-knowledge model calls; all original/rebuilt replies are scored with the final tools. No model-input file, expected translation, source fixture or raw response changed and no model retry was performed.

## Warning and strict-validation controls

| Arm/state | Expectations met | Failures |
|---|---|---|
| Previous rebuild (saved pre-fix) | 43/56 | red-are-to, red-condition-of-entry, red-will-be-expected, red-mixed-offers-to-reach, red-private-have-to, red-private-obligation-pollutes-context, red-private-negated-have-to, red-christening, red-bridal-shower, unknown-event-heading, private-need-to, private-need-to-next, explicit-reset-self |
| Original | 40/60 | prior-baptism, prior-baby-shower, prior-graduation-control, prior-altered-zero-width-quotation, prior-straight-delimiters, prior-explicit-reset, prior-private-baptism, prior-private-shower, red-private-have-to, red-private-obligation-pollutes-context, red-private-negated-have-to, red-christening, red-bridal-shower, red-known-baptism, red-private-reset-control, red-quote-word-joiner-inserted, private-need-to, private-need-to-next, explicit-reset-self, explicit-family-event-heading |
| Repaired rebuild | 60/60 | None |

The current red-team unsafe-suppression, private-obligation, inherited-context and milestone cases are evaluated without sidecars. The earlier 27 controls are retained alongside the 21 red-team cases, eight new scope guards, two mixed-duty guards and two private/clinical-heading guards. See the complete per-case results, including original failures and any rebuilt failures, in scope-repair/control-results-release.json. Replaying the exact preserved earlier rebuilt B card with the before/after validators changes five personal warning IDs to zero; the source and raw card are identical in both executions (scope-repair/same-card-warning-replay.json). Exact new anchors remain accepted; altered citations and quotation text remain rejected. Original’s known permissive quotation behavior is disclosed rather than scored as fidelity success.

Historical replay executions: 143; repaired rebuild failures: 0. The same historical REVIEW lines and valid/invalid outcomes are required; old result files were not regenerated. The replay follows each original recorded command, including multipart cards. Prior failed replay-wrapper and delivery attempts remain in their original folders; this stage does not rewrite them.

## Fresh short model cases

| Case | Original strict / semantic / no false personal hints | Rebuild strict / semantic / no false personal hints |
|---|---|---|
| A-obligation-paraphrases | Pass / Pass / Pass | Pass / Pass / Pass |
| B-private-obligations-and-milestones | Pass / Fail / Pass | Pass / Pass / Pass |
| C-opaque-citation-variants | Pass / Pass / Pass | Pass / Pass / Pass |
| D-scope-boundaries | Pass / Fail / Pass | Pass / Pass / Pass |

A no-false-hints pass on an original card that misroutes private dates into Section 6 is not successful containment: the separate exclusive-placement checks still fail. Correct-card evaluator controls expose its false-warning behavior.

original B-private-obligations-and-milestones: failed semantic checks ['S002_exclusive', 'S003_exclusive', 'S004_exclusive', 'S005_exclusive', 'S006_exclusive']; citation mismatches []; personal hint lines [].

original D-scope-boundaries: failed semantic checks ['S001_exclusive', 'S002_exclusive', 'S003_exclusive']; citation mismatches []; personal hint lines [].

## Fresh full-length RFP

| Check | Original | Rebuild |
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

original: 4 replies, quoted bullets per reply [113, 80, 146, 70], 221 distinct IDs. Overall pass: False. Quote mismatches: []. Anchor mismatches: []. Failed routing: ['S066', 'S148']. Failed forbidden checks: []. Personal hint lines: [].

rebuild: 4 replies, quoted bullets per reply [111, 88, 140, 70], 221 distinct IDs. Overall pass: True. Quote mismatches: []. Anchor mismatches: []. Failed routing: []. Failed forbidden checks: []. Personal hint lines: [].

Full required Section 5 checks include S072 and S076; the source-bound expanded matrix distinguishes eligibility, required response information, optional material and post-award terms. All occurrences, not only selected IDs, are checked for exact quotation and complete anchor. Both arms face the same rebuilt strict structural gate. Actual reply boundaries are separately checked against the 150-bullet budget. Raw full rebuilt replies are copied byte-for-byte under `rebuild/run-results/scope-repair-full/` with local binary Git attributes.

## Preservation, remaining risk and delivery

Integrity audit: 12957 prior tracked files preserved (changed candidate/report paths have exact before snapshots). Original, verbatim feedback, frozen questions, all failed trials and previous review evidence are unchanged. All 30 existing local sealed artifact files retain their hashes. The complete Git history remains; no amend, reset, force push or history rewrite was used.

This closes the specified warning failures on the frozen controls; it does not establish a general personal-content classifier. New activity wording can still produce conservative false warnings; unfamiliar obligation wording can still escape a finite heuristic. The validator does not prove semantic routing, issuer authority, packet-to-PDF fidelity or authenticity. Context stays protected until an explicit private heading, which favors missed-risk detection and may over-warn on poorly separated attachments. Strict validation detects copying failures but cannot guarantee the model will not make them. One trial per source/arm is a receipt, not a reliability estimate. Original Claude Sonnet/Opus conditions are not reproduced. Eligibility remains unverified.

The prior warning-release delivery failure and repaired launcher proof remain unchanged under warning-repair/delivery-attempt-1 and dist/warning-release. Current offline audits execute the unchanged legacy, final-repair and warning-repair assertions at their own sealed commits in sibling clones, then run the current scope-repair audit.

Local package target: `dist/scope-release/`, including source ZIP, complete-history Git bundle, SHA256SUMS, RELEASE and fresh-clone FINAL_VERIFICATION. Packaging checks integrity/compliance separately from the measured performance above; a package audit pass does not erase a model failure. Older `dist/release/` and failed delivery attempts remain intact. `SUBMISSION_COMMENT.md` is still a draft; no public link, push or comment has been published.
