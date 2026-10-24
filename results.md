# Polarity and mixed-clause repair — paired results, 2026-10-24

Local candidate; unpublished. This stage addresses all five findings in red-team-guard/REPORT.md. Closure claims below apply to the recorded cases and guards, not every possible wording. All earlier evidence, failures and deliveries remain preserved.

## Changes tied to the findings

F1: unknown nonprivate event statements retain warning scope without a particular modal phrase, colon or all-capital heading. This covers the reverse-prerequisite and implicit attendance conditions without adding only those phrases to a vocabulary list. Explicit private headings and negated dependency statements are handled separately.

F2: coordinating conjunctions delimit warning-analysis clauses with or without a comma. Each clause needs affirmative private support before the statement can be exempted. Narrow calendar/activity fragments can share ownership within the same statement, and a private cost-sharing clause remains bounded. Official participation-payment cues and unknown extra actions retain hints. A private self-duty is assessed per duty clause; an additional demonstrably private clause does not itself create procurement scope.

F3: dependency matches respect negation, while not-only constructions remain affirmative. Negated dependency language alone does not create or clear inherited requirement scope. Other procurement/clinical vetoes remain.

F4: subsection references are evaluated locally by clause and heading, with the latest applicable relation controlling inclusion. An excluded or unrelated private subsection is not held inside a requirement merely because its name occurs there. Another subsection’s exclusion cannot cancel an included subsection. Positive inclusion and a negated exclusion remain conservative.

F5: narrowly supported private annotations following a dash or colon are recognized along with possessive/compound headings. Clinical or procurement wording retains its veto, and an explicitly included private-looking subsection retains inherited scope.

The exact-copy/structural implementation from def difference onward is byte-identical to the preceding candidate: complete anchors, invisible characters, statement text, coverage, order, headings, continuations, trusted exclusion checks and rejection behavior are unchanged. Warning analysis never alters the source statement or output quotation. No source IDs or filenames are relevance rules. A validator PASS still does not prove semantic placement.

## Frozen sequence and fair comparison

Inputs, 116 controls, three prior red-team fixtures plus new D and source-bound expected checks were frozen in 3bbb5a7. Root questions.md remains byte-identical to bfdd812. The original ran frozen core A-E, supplemental A-D, and the unchanged 221-statement full RFP first; its complete baseline was committed in eb10487 before mutating the candidate. Candidate 3539ec4 preceded every rebuilt model call.

Both arms used unchanged canonical runners and gpt-6-astra medium, the same ordered sources and six-file knowledge selection. Core/supplemental trials used fresh ephemeral sessions; the full run used a fresh persistent session and exact continue turns. No tools, retries, best-of selection, raw-output corrections or evaluator answers in model inputs. Host system instructions remain uncontrolled. The six knowledge files in each arm are unchanged, so fresh routing differences do not establish a new routing-prompt repair.

These are targeted synthetic regression/safety cases informed by prior findings, not independent real-world validation or fresh Claude acceptance. The full source contains 214 real TBRPC statements plus seven synthetic personal records, with a selected semantic matrix. The first implementation passed 116 controls and the rebuilt historical replay, but inspection led to four further safety cases frozen in f017ceb before execution. Two exposed unsafe suppression when outside/unrelated described time or subject matter rather than exclusion from scope. Their failures and initial code remain preserved. The correction preceded all rebuilt model calls; the final 120 controls pass. See REPAIR_NOTES.md, attempt-1 and relation-addendum-before for the failed evidence.

## Frozen questions

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

Totals: {'improved': 5, 'tied': 3, 'regressed': 0}. Q8 runs default warning handling without a reviewed-exclusion sidecar. All subchecks and regressed subchecks remain in polarity-repair/scores-final.json; core-common-strict.json applies the same strict gate to both arms.

## Supplemental paired cases

| Case | Original all checks | Rebuild all checks |
|---|---|---|
| A-unseen-obligations-and-mixed-conjunction | PASS | PASS |
| B-negated-scope-and-private-headings | FAIL | PASS |
| C-new-citation-variants | PASS | PASS |
| D-polarity-and-coordination | FAIL | PASS |

original B-negated-scope-and-private-headings: failed selected semantic checks ['S002_exclusive', 'S003_exclusive', 'S006_exclusive', 'S008_exclusive']; exact-copy mismatches []; personal false hints [].

original D-polarity-and-coordination: failed selected semantic checks ['S002_exclusive', 'S003_exclusive', 'S007_exclusive']; exact-copy mismatches []; personal false hints [].

Citation C is scored as a tie whenever both arms pass. Full positions, mismatches and raw validation output: polarity-repair/model-results.json. All native and common strict results remain beside the raw cards. Selected checks are not exhaustive semantic grading.

## Fresh full-length RFP

| Check | Original | Rebuild |
|---|---|---|
| exact_shape_quotes_coverage | False | True |
| exact_statement_text | True | True |
| exact_anchors | False | True |
| all_221_ids | True | True |
| noise_only12 | False | True |
| genuine_routing | False | True |
| forbidden_routing_clear | True | True |
| no_personal_review_hints | True | True |
| max150_bullets_per_reply | True | True |
| complete | True | True |

**original: FAIL**, 4 parts, 221 distinct source IDs; per-reply bullets [90, 108, 99, 139].
Quote mismatches: []; anchor mismatches: [{'sid': 'S072', 'section': 4, 'actual': 'TBRPC Auditing RFP p. 7 §5.II.b', 'expected': 'TBRPC Auditing RFP p. 7 §5.II.b bullet'}, {'sid': 'S072', 'section': 5, 'actual': 'TBRPC Auditing RFP p. 7 §5.II.b', 'expected': 'TBRPC Auditing RFP p. 7 §5.II.b bullet'}, {'sid': 'S092', 'section': 6, 'actual': 'TBRPC Auditing RFP p. 9 §6.II Questions', 'expected': 'TBRPC Auditing RFP p. 9 §6.I Questions'}].
Missing selected placements: ['S133', 'S066', 'S083', 'S148']; personal containment failures: ['S216', 'S217', 'S218', 'S219', 'S220', 'S221']; false personal hints: [].

**rebuild: PASS**, 3 parts, 221 distinct source IDs; per-reply bullets [128, 123, 141].
Quote mismatches: []; anchor mismatches: [].
Missing selected placements: []; personal containment failures: []; false personal hints: [].

Raw full evidence is under run-original/polarity-repair-full and run-rebuild/polarity-repair-full. The new rebuilt full run is also copied byte-for-byte to rebuild/run-results/polarity-repair-full with binary attributes. Scores: polarity-repair/full-length-results.json. All older failed full runs, including S072/S100 anchor errors, remain unchanged. No failed output was corrected.

## Warning and strict controls

| Arm | Passed | Total |
|---|---:|---:|
| original | 80 | 120 |
| rebuild | 120 | 120 |

The 120 controls comprise the previous 87, all 17 latest red-team controls, 12 additional positive/negative scope, coordination, latest-reference and clinical guards, and four further scope-relation safety cases. Deliberately misrouted official cards test advisory warnings; correct all-12 personal cards test false warnings. They are evaluator cards, not model replies. Every changed-citation/quotation control retains its original exact rejection expectation. Original’s known permissive quotation tolerances count as failures rather than copying wins.

Historical replay counts: {'original': {'pass': 66, 'total': 70}, 'rebuild': {'pass': 73, 'total': 73}}. Complete command/stdout/stderr/exit evidence is retained.

The exact preserved red-team rebuilt B card is replayed without a model rerun in same-card-warning-replay-release.json. Before has false warning IDs S003/S006/S008; after is checked for zero REVIEW warnings, with identical source/card hashes and both structural exits preserved. This isolates warning-tool behavior from model variability.

## Ties, regressions, untouched behavior and limits

Question-by-question ties/regressions and full-RFP fidelity ties or failures are shown above. Model knowledge, frozen questions, source packets, original evidence, example provenance and strict validation were deliberately left unchanged. Fresh-model routing improvements are variable observations, not causal evidence of a new prompt repair. In this full-RFP draw the original has three anchor errors (S072 twice and S092), whereas the preceding original draw copied its anchors exactly; that deterioration is retained as evidence of variability. The warning-only change cannot cause better model copying. See REPAIR_NOTES.md for every intermediate failure and correction in this stage.

The classifier remains a finite local warning heuristic, not a complete semantic parser. It can still misread novel negation, scope references, ambiguous ownership, mixed clauses or annotated headings. Unknown event text is treated conservatively, which can retain warnings where a human may conclude unrelatedness. Single paired runs and selected matrices do not establish reliability on every real-world attachment, Unicode form or judge environment. Human semantic review and fresh Claude acceptance remain open. No universal conservative-behavior claim is made.

## Competition layout, history and delivery

The judged original remains pinned at 92847d2a17250fa18914d932826db63d99dcb75c. Required root layout, verbatim feedback, frozen questions and historical original-before-rebuild sequence remain retained. The new report is also root results.md. All 22,013 prior tracked files and 41 sealed artifact files are preserved; seven mutable documents have exact before snapshots. Preservation and chronology records bind old evidence, frozen cases, baseline bytes, current candidate and raw model events.

New local delivery: dist/polarity-release with source ZIP, complete-history bundle, SHA256SUMS and RELEASE.json. Its FINAL_VERIFICATION.json records actual fresh-clone compliance once built; prior deliveries remain intact. Packaging compliance is separate from model quality. The updated submission body is exactly the three frozen sentences in submission-plan.json and includes the verbatim motivating feedback line. Premium/VIP eligibility and a valid public repository URL remain unverified. Nothing has been published.
