# Sealed-package red team — 2026-10-24

**Verdict: hold publication. Four actionable warning findings remain.** Target: `3159bc2a93e7de52580c5445c15e7ac24d31eddd`. Review only; candidate, root results, frozen questions, prior evidence and sealed delivery were not edited. This report is new evidence outside the existing ZIP.

## Findings

### F1 — High: a private subheading clears explicitly compulsory scope

`rebuild/tools/validate_packet.py:107–114`: the full-match private heading resets `protected` even when the preceding instruction explicitly makes that subsection compulsory. Frozen control `private-subheading-under-explicit-official-scope` says all companies have to attend all following events, including the subsection labelled Private events. After `Private events:`, the farewell dinner date can be placed only in Section 12 without the missing-Section-6 review warning. Original and preceding rebuild warn; current rebuild suppresses it. This is a new regression against both. The actual A model replies routed the tested dates correctly: this is an evaluator blind spot, not an observed model omission in this pair.

Repair acceptance: inherited explicit mandatory scope must survive a private-looking nested heading; a demonstrably unrelated private correspondence block must still reset scope. Preserve exact quotation/citation gates.

### F2 — High: mixed personal/procurement clauses still suppress a real deadline

`rebuild/tools/validate_packet.py:95–105`: personal recognition plus an incomplete procurement-cue vocabulary excludes a whole statement containing `Our farewell dinner ...; remit the official participation deposit by ...`. No recognized duty phrase means the extra-clause guard never applies. Original warns; both preceding and current rebuild suppress. A second frozen witness, `I have to attend my daughter’s birthday dinner ... , then remit the official participation deposit by ...`, is a new current-versus-preceding regression: the private-duty exception does not reject the extra comma/then obligation, because its connective guard only lists and/but/while/also. Both deliberately misplaced cards retain structurally valid exact quotations.

Repair acceptance: a private clause must not exempt a procurement deadline elsewhere in the same source statement. Add both witnesses without widening quote normalization or using IDs/filenames as relevance authority. The actual A model reply handled the semicolon variant correctly; no new model trial was run for the evaluator-only comma/then witness.

### F3 — Medium: unseen obligation wording without a heading marker loses context

`rebuild/tools/validate_packet.py:105–111`: `Participation depends on attendance at these events.` has neither a recognized obligation phrase nor a colon/uppercase heading shape. The following personal-style official baby-shower date is suppressed when wrongly retained only in Section 12. Original warns; preceding and current rebuild suppress. This is a remaining regression relative to original, not newly introduced by the last repair. The A model replies correctly placed this date in Section 6.

Repair acceptance: required participation dependencies must preserve the warning context across records without requiring a punctuation pattern or one short list of modal verbs. Bound the behavior with unrelated personal controls.

### F4 — Medium: unfamiliar personal headings reintroduce false warnings

`rebuild/tools/validate_packet.py:80,107–112`: `My family events:` and `Personal family calendar:` fail the private-heading full match but match the unknown-event-heading branch. Their unrelated birthday/graduation dates become protected. Both original and current rebuild warn on correct all-12 personal cards; preceding rebuild suppresses. These are two new regressions versus the preceding rebuild, tied with original. This is also reproduced in the fresh rebuilt B model reply: S002/S004 are correctly only in Section 12, yet the validator prints a Section-6 REVIEW note.

The exact same raw B card, unchanged, was replayed under all three validators in `same-card-warning-replay.json`; preceding has no REVIEW note and current has one containing S002/S004. This causal comparison avoids attributing the warning change to model variability. Repair acceptance must cover personal heading variants and the contrary explicitly compulsory nested-heading case together.

## Frozen method and measured results

Fixtures, source-hash-bound expectations, controls and protocol were committed in `2666b8c` before execution. Three original trials completed and were committed in `ebc22cf` before the three rebuild trials. Unchanged canonical runner; gpt-6-astra medium; same fixtures/order and six-file knowledge selection; fresh sessions; no tools, retries, corrections or best-of selection. Canonical requests, metadata and event/raw-card equality are verified in `model-audit.json` and `model-results.json`. Expected answers were never supplied to models. Host system instructions are not held byte-identical. These are synthetic targeted cases informed by prior failures, not a statistically independent real-world holdout.

| Fixture | Original | Rebuild | Interpretation |
|---|---|---|---|
| A: unseen obligations, nested private heading, mixed deposit | Selected routing and fidelity pass | Selected routing and fidelity pass | Tie on tested model behavior; warning controls still expose blind spots |
| B: unrelated private heading variants plus real deadline | Personal S002/S004 leak to Section 6 | Personal S001–S004 only in 12; real S005 in 6; false hints S002/S004 | Routing improves, warning accuracy fails; neither arm passes every check |
| C: six opaque citation variants | Exact copies and required 4/5 routing pass | Exact copies and required 4/5 routing pass | Tie; no observed citation regression |

All six model replies pass common strict quotation/citation/shape validation. Selected semantic checks pass 2/3 original and 3/3 rebuild; all combined checks pass 2/3 in each arm. This combined tie must not conceal the different reasons B fails. No claim of exhaustive semantic grading: header placement and all possible additional sections were not comprehensively scored.

| Validator controls | Pass | Fail |
|---|---:|---:|
| original | 11/14 | 3 |
| pre-scope | 12/14 | 2 |
| rebuild | 8/14 | 6 |

The six current failures span four findings: F1 one, F2 two, F3 one, F4 two. Four controls regress against preceding rebuild (F1, comma/then F2, both F4). Four unsafe suppression controls regress against original (F1, both F2, F3). Evaluator cards intentionally misroute official dates; warnings are advisory, so exit code 0 alone is not semantic success.

All three validators accept the exact citation control and reject all six mutations: thin-space replacement, invisible-separator deletion, Greek-zeta/Latin-Z substitution, minus/hyphen substitution, fullwidth/ASCII colon substitution, and numeric-entity decoding. This round finds no citation weakness on these cases; it does not prove universal copying reliability. Controls and all stdout/stderr/exit codes are preserved under `controls/`.

## Existing full RFP and competition compliance

Read-only replay of the existing scope-repair full-RFP cards preserves the prior result: both arms pass native structural checks; rebuild meets every selected required/forbidden routing check and holds S215–S221 only in Section 12. Original still misses S066 in 5 and S148 in 11 and leaks six personal records. No new full-RFP model call or rewritten historical score was made. See `full-recheck.json`. Prior frozen-question wins/ties are historical evidence, not a fresh rerun in this review.

The competition rewards feedback closure, not general polish. The feedback explicitly calls for stapled personal material only in Section 12 without spurious procurement warnings. F4 therefore directly weakens that closure claim; F1–F3 weaken confidence that the filter remains conservative around actual obligations. The sealed report’s broad statement that unknown/mixed content remains conservative is not supported by these new witnesses. Keep its original dated evidence intact, but reconcile the next submission report with this review before releasing.

No new formal layout/sequence defect is asserted. Frozen questions remain byte-identical to bfdd812; prior original pin and sequence are checked by the portable offline audit. The current submission body is three sentences, within the spec’s 2–3 sentence requirement. Public repository URL and Premium/VIP eligibility still require actual confirmation before submission; neither is established by local packaging. Nothing was published.

## What could cost the win

1. Warning correctness still fails the same feedback area despite narrower control passes. A judge can reproduce F4 on an actual fresh model card, not only on constructed output.
2. Overconfidence in the passing strict validator: its PASS establishes fidelity/shape, while advisory relevance checks can miss real dates or invent false concerns.
3. The tested model knowledge is unchanged from the preceding repair. Better outcomes on a new draw are not evidence of an improved routing prompt. One trial per fixture and a selected routing matrix cannot establish reliability.
4. Review burden: the sealed source has 17,372 tracked files with extensive historical evidence. A short evidence map and accurate current verdict matter; new review evidence is not yet in that sealed ZIP.
5. Administrative release conditions remain open: valid public link, membership eligibility and timely submission under the supplied spec.

## Evidence integrity and delivery audit

`preservation-verification.json` verifies all 17,372 prior tracked files and 35 sealed delivery files unchanged, plus frozen questions and byte-identical preceding validator snapshot. Exact model replies, prompts, events, failures, definitions and scoring outputs remain in this review directory. `delivery-summary.json` records the fresh sealed archive/bundle audit when complete; inspect `delivery-checks.json` for every command and any failure. The reviewed ZIP/bundle are unchanged; this review was not repackaged into them. No fixes or publication were performed.

Final delivery result: PASS. All 17,372 sealed archive files matched exactly; bundle verification, pristine clone index bytes, both runner preflights and portable offline compliance passed. See delivery-summary.json and delivery-checks.json. These mechanical compliance passes do not resolve F1–F4.
