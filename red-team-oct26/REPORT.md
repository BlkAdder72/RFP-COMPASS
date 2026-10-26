# Feedback-led red team — 2026-10-26

**HOLD for warning accuracy.** This review targets sealed candidate `8e2afd4e9963cf29fbcf32a874fd196a03a78a02`. It does not repair or replace that candidate, its report or its release. New tests expand coverage; they do not retroactively change the earlier recorded scores. Nothing is published.

## Spec and judges' feedback reviewed first

Read `packaging/competition-spec.txt` and `feedback.md` before designing tests. Both match the user's originally supplied files byte for byte (`delivery-checks.json`). The competition rewards closing the feedback gap, with the judged original untouched, feedback-derived questions frozen before rebuilding, paired raw runs, and honest ties/regressions. Literal citation stress is a preservation check, not a substitute for the personal-content fix.

The judges asked for unrelated personal records only in Section 12 without false Section 6 REVIEW hints; explicit treatment of contractual expectations such as S133; disclosure in examples.md that sample 04 is script-built; and raw noisy-input evidence in run-results. All have visible implementation and evidence. `rebuild/examples.md:3` discloses the hand routing list, and output-schema.md explicitly covers contractual expectations. The existing Q1–Q8 sequence and scores remain preserved. The issue is generalization of the first fix beyond the final repair's frozen cases.

## Findings

### F1 — missed attendance hints for unseen dependency wording (P2)

`rebuild/tools/validate_packet.py:74` recognizes a finite list of dependency predicates. An all-12 card containing “Participation hinges on attendance at our family reunion.” followed by its dated event gets no Section 6 REVIEW. “Entry is dependent on attendance…” has the same result. The filter explicitly excludes both records as personal. The matched “depends on” positive guard retains the date hint. This is a warning blind spot, not a validator quotation failure and not evidence that a correctly routed model card missed the event. The standalone controls express a participation condition; their public-procurement context is less explicit than the model fixture's later solicitation sentence. Do not infer relevance merely from these predicates in arbitrary private correspondence.

Evidence: `controls/hinges-on-attendance/`, `controls/dependent-on-attendance/`, and `controls/depends-on-guard/`. Repair should recognize supported affirmative dependency relations while preserving negative/private controls; never make every occurrence of “participation” procurement evidence.

### F2 — exclusion from the wrong program still clears compulsory scope (P2)

`rebuild/tools/validate_packet.py:154` binds an exclusion before a heading without checking the excluded relation's subject when no `from` suffix follows. “Companies must attend all events, including the subsection titled Private events:” is followed by “The office-hours program does not include the subsection titled Private events.” At the Private events heading, the filter clears the genuine inherited attendance requirement, and the following farewell date gets no REVIEW when deliberately omitted from Section 6. Being outside the office-hours program does not repeal the original attendance duty.

Evidence: `controls/prefix-wrong-program-exclusion/`. The genuine direct-exclusion guard passes. This is the prefix/subject counterpart to the previously repaired suffix/object failure. Bind the whole relation, not just proximity to the target heading; do not disable legitimate scope exclusions.

### F3 — ordinary worded private shares still produce false hints (P2)

`rebuild/tools/validate_packet.py:99` recognizes English amounts only through ninety-nine. “My birthday dinner is November 1, 2027 at 7 PM and my share is one hundred dollars.” is correctly all-12 but produces a Section 6 REVIEW. “One hundred and five dollars” also fails. The otherwise equivalent `$105` guard passes. This directly overlaps the judges' request to remove false date warnings on unrelated personal material. Bounded amount recognition plus clause splitting creates a brittle semantic boundary.

Evidence: `controls/hundred-dollar-private-share/`, `controls/hundred-and-five-private-share/`, and `controls/numeric-private-share-guard/`. Improve private cost-share handling without allowing arbitrary obligations or payment deadlines to borrow a personal cue.

### F4 — explicit private annotation causes false warning context (P2)

`rebuild/tools/validate_packet.py:89` accepts only a small annotation grammar, while `:174` treats the word procurement as an affirmative cue regardless of its negation/exclusion context. “Personal correspondence (outside procurement):” seeds protected context, so the next ordinary birthday date produces a false REVIEW despite correct all-12 containment. The simple “Personal correspondence:” guard passes.

Evidence: `controls/outside-procurement-private-heading/` and `controls/supported-private-heading-guard/`. Interpret an explicit outside-procurement annotation locally without allowing it to quarantine later genuine duties.

## Method, preservation and limits

| New review gate | Original | Rebuild |
|---|---|---|
| Eighteen warning/citation controls | 11/18 | 12/18 |
| Selected semantic checks across A/B/C | 1/3 fixtures pass | 3/3 fixtures pass |
| Exact quotes and anchors in fresh model cards | 3/3 | 3/3 |
| Combined selected semantics, fidelity and private hints | 1/3 | 2/3 |

The preceding rebuild `21dd85b` also passes 12/18 evaluator controls: **18 ties, zero improvements, zero regressions** against that comparator. The six failures form the four finding families above; they are remaining gaps, not newly introduced regressions against21dd85b. No fresh paired selected semantic or literal-copy regression against the judged original was observed. This does not establish equivalence across all meanings or against the prior candidate's model behavior, which was not rerun as a third model arm.

Fresh model A preserves the positive participation date, correctly applies an explicit later solicitation instruction to the earlier birthday date, and includes the exact S133 sentence in11. Original A misses that last placement. Fresh model B improves containment: all four selected private records are only12, and the genuine response deadline remains4/6; original B leaks three selected private records. However, the rebuilt validator still prints false date REVIEW for B's S002 and S004. The exact same raw rebuilt B card produces those hints with all three validators, isolating a remaining tool gap rather than a model-routing failure. C is a tie: both arms copy all five unseen anchor forms exactly, and both satisfy selected mandatory-document routing. All five altered-anchor evaluator cards are rejected by every validator. No new citation regression was found.

Freeze commit `b0553c95`; completed original-model baseline `ac42a324`, before rebuilt-model execution. Three fixtures in the same order, unchanged six-file canonical runner, gpt-6-astra medium, fresh sessions, expected answers excluded. No agent retry, output editing or best-of selection. The CLI's raw stderr records an automatic HTTP 429 transport retry during rebuilt B; this is a disclosed execution deviation from a literal zero-retry reading of the new protocol, not a clean identical transport environment. Retain it rather than silently rerunning or claiming zero retries of every kind. Exact counts/results are in SUMMARY.json and model-results.json.

Eighteen evaluator controls compare judged original, prior rebuild `21dd85b`, and current rebuild. Synthetic evaluator cards intentionally omit operational placement to isolate hints; structural PASS alone is expected and does not establish semantic correctness. Selected model matrices are not exhaustive semantic grading. Five unseen anchor variants include an interior BOM, right-to-left mark, decomposed accent, literal apostrophe entity, and tab. Exact copies must pass; each normalized/decoded alteration must fail.

The current acceptance audit rechecks its original finite gates successfully (`current-acceptance-recheck.json`), including 162 controls and 28 preserved raw turns. The existing full RFP is replayed read-only, not regenerated: rebuilt strict validation passes, all selected required placements hold, and all seven private records remain only12. Original retains its previously recorded citation/placement/noise failures (`full-recheck.json`). Historical failed S100 evidence remains rejected by the current acceptance audit.

All 37,090 prior tracked files and 53 sealed artifacts retain their bytes. The sealed ZIP still contains the exact 37,090 target source files. Frozen questions are unchanged. The release's earlier fresh-clone compliance result is historical; this review rechecks preservation/archive bytes and current acceptance locally, without claiming a new fresh-clone run. New review evidence is outside that unchanged sealed ZIP. It must be incorporated into any later release and current root navigation/report before submission.

## What could cost the win

1. The warning defects overlap the exact judges' first fix; more Unicode citation wins cannot compensate. Fix the four families and rerun both arms fairly on the frozen new cases before resealing.
2. The repository preserves extensive failed evidence but asks a judge to navigate 37,090 source files. Keep the entry point focused on feedback → Q1–Q8 → current paired evidence → explicit limits, while retaining the archive/history. The sealed report is accurate about its recorded gates but is no longer the complete current readiness account after this review.
3. Native Claude acceptance remains untested. The original judges used Sonnet/Opus; the automated comparison uses a different model and inline named files. Its results cannot establish native-attachment behavior or independent reliability over repeated trials.
4. Premium/VIP eligibility is unverified, the submission comment still has a public-URL placeholder, and the current review has not been added to the sealed release. These are completion items, not reasons to publish prematurely. The provided spec gives Wednesday October 28 at 11:59 PM EST; do not silently reinterpret its timezone label.

The S133 trigger, example provenance, preserved originals and raw noisy evidence remain strengths. The defensible claim is measured improvement against feedback with disclosed residual limits; the evidence does not support “perfect.”
