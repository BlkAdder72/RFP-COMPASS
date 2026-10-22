# Supplemental stress-test results

October 22, 2026. Local review draft; not published. **The model improvement held on the frozen checks, but the validator regressed. Repair that warning suppression before publishing.** Neither version was changed during this evaluation.

## What ran and what stayed preserved

Eight new synthetic fixtures, two fresh sessions per version per fixture: 32 raw responses, forming 16 paired comparisons. Each fixture ran original/rebuild in repeat 1 and rebuild/original in repeat 2. Protocol, fixtures, runner and scoring rules were committed as `b1f808c` before execution. Raw responses and tool evidence were committed as `a4d23ff` before this report.

The preservation audit verified 387 protected files unchanged, including both versions, first-pass inputs, questions, feedback, raw runs and the original results report. The original's 134-file judged export remains preserved. First-pass results are historical evidence and have not been rewritten to incorporate these findings.

## Model results

Both repeats gave the same core-check verdict in every fixture. The rebuild passed 16/16 trials; the original passed 10 and partially passed 6. This produces **six improved paired comparisons and ten ties**, with no regressed frozen model-placement subcheck. These are descriptive counts on eight designed cases, not a reliability estimate.

| Fixture | Original, repeats 1 / 2 | Rebuild, repeats 1 / 2 | Finding |
|---|---|---|---|
| F: neutral personal attachment | Partial / partial | Pass / pass | Improvement in both pairs. Dentist appointment and family party move from Section 6 to Section 12 even without an explicit unrelated label. Actual deadline remains in Section 6. |
| G: unknown attachment | Pass / pass | Pass / pass | Tie. Unknown meeting and required form stay under normal routing; neither model invents an authority determination. This preserves uncertain evidence, not proof that it belongs to the solicitation. |
| H: mixed email, separate statements | Partial / partial | Pass / pass | Improvement in both pairs. Real deadline and pricing sheet remain operational; recital and family picnic go only to Section 12. Shared thread anchors do not cause whole-thread quarantine. |
| I: mixed deadline/personal statement | Pass / pass | Pass / pass | Tie on preserving the requirement. Both include the birthday invitation alongside the deadline because the whole statement must be quoted. Personal isolation is not achieved. |
| J: personal-looking filename | Partial / partial | Pass / pass | Improvement in both pairs. Both preserve the explicit procurement clarification in Sections 6 and 11; only the rebuild sets the anniversary dinner aside. |
| K: misleading unrelated label | Pass / pass | Pass / pass | Tie. Both model versions retain the explicit procurement deadline despite the filename. This does not establish validator safety; see N1. |
| L: procurement site visit/lunch | Pass / pass | Pass / pass | Tie. The mandatory bidder event and signed confirmation remain usable; lunch is not mistaken for unrelated personal noise. |
| M: mixed form/personal statement | Pass / pass | Pass / pass | Tie on preserving the form. Both retain the family-party/cupcakes clause with the required pricing sheet in operational sections. Personal isolation is not achieved. |

All 32 cards pass their version's shape, exact quotation, citation and complete-coverage validation. Raw audits show one completed response per trial, no observed tool calls, and no task retries or best-of selection. G's absence of invented authority is supported by its exact-quotation/no-extra-prose checks and inspected card text.

### Variation outside the frozen minimum checks

The original's G repeat 1 also placed S003's form requirement in Section 6; its repeat 2 and both rebuild repeats omitted that additional placement. Required form placements in Sections 4 and 5 remained. The protocol did not require Section 6 for that sentence, so this is unscored routing variation, not silently counted as a win or a proven regression. All source-ID placement maps are retained in scores.json. Stable core verdicts do not mean every output placement is deterministic.

## A confirmed validator regression

**N1: real deadline, misleading anchor, wrong Section 12-only placement.** The same evaluator-built defective card puts the explicit RFP-26 deadline solely in Section 12. Its source filename is unrelated-background-notes.txt.

- [Original stdout](tool-original/N1-mislabeled-real-deadline/stdout.txt): correctly issues a Section 6 REVIEW identifying S002.
- [Rebuild stdout](tool-rebuild/N1-mislabeled-real-deadline/stdout.txt): issues no Section 6 warning.

This is a genuine regression in the warning layer. The rebuild uses the word unrelated in the anchor plus Section 12-only placement as grounds for suppression. A misleading filename can therefore silence the warning precisely when the model has misplaced a real deadline. The passing K model trials do not negate this result: they happened to place the deadline correctly; N1 tests what happens when that layer makes an error.

Both tools still return structural PASS/exit 0 because REVIEW is advisory. That exit status does not mean this semantic warning test passed. Tool-level verdicts are reported separately in tool-scores.json.

**N2: correct personal containment without an unrelated label.** Both validators warn that the personal appointment is missing from Section 6, despite correct Section 12 containment. This is a tied unresolved failure, not an improvement. See [original stdout](tool-original/N2-neutral-personal/stdout.txt) and [rebuild stdout](tool-rebuild/N2-neutral-personal/stdout.txt).

## Shared contract limit: indivisible mixed statements

I and M deliberately combine genuine requirements and personal clauses in a single packet statement. Both versions preserve the whole statement in the required operational section in all eight trials across these two fixtures. That avoids losing a deadline or attachment, but necessarily carries personal content with it.

Under the current whole-statement quotation contract, a model cannot both keep the exact complete requirement-bearing statement operational and put its personal clause only in Section 12. Calling these clean separation passes would be misleading. The frozen checks require preservation of the genuine requirement and record the unavoidable personal inclusion separately. Both checks passed; the broader containment ambition remains unmet.

Any future clause-level split would require a separate, explicit input/output contract decision and new traceability tests. It must not be patched silently into this evaluation or presented as a free routing fix.

## What should change before publication

First repair the validator so an untrusted label plus the card's own placement cannot suppress the warning that should detect a bad placement. Preserve these frozen versions and raw records. Test a separately versioned repair against N1, N2 and the first-pass hint case; do not claim that deleting all suppression resolves the original false-warning feedback.

The longer-term choice is how to represent excluded evidence in a way the checker can audit without trusting filenames or self-confirming card placement. That choice has not been implemented or owner-approved here. The existing model-routing improvements can be described with evidence, but the package should not be described as regression-free or as separating every possible mixed statement.

## Reproduce and limitations

Run `python supplemental/verify.py` with Python 3.10+. It checks protected first-pass bytes, the frozen protocol against Git commit b1f808c, exact supplied requests, knowledge/fixture hashes, raw-response extraction and tool-use audits, then regenerates supplemental scores. It does not rewrite first-pass evidence.

Every trial directory contains request.txt, command.json, environment.json, events.jsonl, stderr.txt, exit-code.txt, audit.json, bid-compliance-card.md, validation.txt and score.json. Tool cards are explicitly evaluator-built, not model outputs. See [protocol.md](protocol.md), [scores.json](scores.json), [tool-scores.json](tool-scores.json) and [verification.json](verification.json).

The model was OpenAI gpt-6-astra with medium reasoning through the same Codex harness as the first pass, not Claude. Host instructions and tool descriptions were not captured or held byte-identical; explicit knowledge, prompts, model, settings and source inputs were controlled. Named files were delivered inline. Two repeats per case and alternating arm order improve the record but do not establish statistical confidence or remove host variation. No blind external evaluator or real inbox corpus was used.

Provider-reported totals were 438,944 input / 7,517 output tokens for the original and 449,316 input / 7,403 output tokens for the rebuild. Host variation and differing reasoning/caching preclude a clean cost or speed conclusion. No latency benchmark was frozen.

The defensible claim is now narrower and stronger: the rebuild improved statement-level discrimination in the tested attachments, preserved genuine requirements in the ambiguous and mixed cases, and has a reproducible validator-warning regression that remains to be repaired.
