# Competition #15 — revised default-workflow results

Unpublished, October 22, 2026. The frozen questions, original entry and all prior evidence remain preserved. The final default workflow now closes Q8 without additional review input. The two runner defects are also repaired and tested.

## Same questions, fresh runs on both versions

Twenty fresh model sessions: five fixture conversions per version, repeated twice. Same prompts, files, order per arm, gpt-6-astra/medium settings and no-tools requirement. No retries or selected best outputs. Q7 is inspected; Q8 executes both default validators on identical frozen evaluator cards with no sidecar. The first original baseline preceded the validator change; the second repeat reversed arm order.

| Frozen question | Original repeat 1 / 2 | Rebuild repeat 1 / 2 | Comparison |
|---|---|---|---|
| Q1 Stapled personal thread | Fail / fail | Pass / pass | Improved twice |
| Q2 Preserve actual requirements | Pass / pass | Pass / pass | Two ties |
| Q3 Different personal note | Partial / partial | Pass / pass | Improved twice |
| Q4 Official clarification email | Pass / pass | Pass / pass | Two ties |
| Q5 Planted instruction boundary | Pass / pass | Pass / pass | Two ties |
| Q6 S133 explicit rule/placement | Partial / partial | Pass / pass | Improved twice |
| Q7 Script-built sample provenance | Fail / fail | Pass / pass | Improved twice |
| Q8 Default false-date/missed-deadline hints | Partial / partial | Pass / pass | Improved twice, no review records |

Ten improved paired question comparisons and six ties; no regressed scored subcheck. These are not independent samples or a reliability estimate. A produces two question results; Q7/Q8 are file/tool evidence. See [detailed subchecks](revision/scores.json) and the fresh raw arms under [run-original/revision-v2/](run-original/revision-v2/) and [run-rebuild/revision-v2/](run-rebuild/revision-v2/).

## Each feedback obligation

- **Fix 1:** the model routes clearly unrelated statements only to Section 12. The default checker now uses affirmative personal activity language in the source, plus Section 12-only placement, with procurement/requirement/context vetoes. Filename words and card placement alone cannot grant suppression. On unchanged Q8 inputs, personal S004 gets no Section 6 REVIEW while misplaced real S002 still does. Ordinary invocation; no operator decisions added to either arm.
- **Fix 2:** S133 follows the narrow explicit contractual-expectation trigger; examples.md discloses sample 04's script and hand routing list. Its reference-card placement agrees with the rule.
- **Tier request:** the stapled-thread before/after runs remain shipped. Fresh repeat evidence is in both root arms. Historical rebuilt A/B/C raw trials remain under rebuild/run-results/rebuild-noisy-input/; their six knowledge files match the final rebuild. Those copies are labeled historical, not new sessions.

## What tied, regressed, or remained unchanged

Preserving real requirements, official clarifications and injection boundaries already worked in the original and tied. Prior stress testing found a validator regression and the first repair required extra review input; both findings and outputs remain visible in historical reports. The new default repair supersedes the assisted-only closure, rather than rewriting that result.

The filter is a bounded, primarily English heuristic. Ambiguous statements keep conservative hints; generic lunch money still triggers a Section 8 hint. Personal-looking content that implies a genuine requirement without detectable language/context can still be misclassified. Conversely, personal wording mentioning obligations may keep a false warning. No universal semantic classifier, authenticated authority check or legal-correctness claim is made.

Whole-statement quotation remains unchanged: a genuine requirement combined with a personal clause in one indivisible statement retains both operationally. The twelve headings, exact source quotation, full coverage, no-advice boundary, conflict preservation, PDF tools and historical sample cards remain. The six model knowledge files did not change during this revision. No new full-PDF corpus/model run is claimed.

## Other checks and preservation

Seven model-free runner checks passed: refusal before mutation, exclusive destinations/metadata, portable executable selection and workspace creation. The corrected default checker suite passed 51/51; both validators structurally replayed 42 historical model cards and four samples (92 checks). Fake CLI outputs and evaluator cards are not model evidence. One initial adversarial assertion incorrectly required a date hint after missing headings caused early structural rejection; its 50/51 record is preserved, corrected criteria are documented, and no validator/frozen question changed to satisfy it.

All 2,756 pre-revision tracked files are protected by the revision manifest. Modified current files were preserved in revision/history/; every other earlier file, raw score, question and report remains in place. Git history and judged-original-comp13 at 92847d2a17250fa18914d932826db63d99dcb75c remain. Prior sealed artifacts are retained separately when the replacement package is created.

Host system context is not held byte-identical, and the tests use disclosed synthetic inputs and Codex rather than Claude. Two repeats and 62 total recorded model responses (42 prior plus 20 fresh) do not establish statistical confidence, independent blind validation or cost/latency superiority.

See [the resolution report](revision/report.md), [initial assertion correction](revision/TEST_CORRECTION.md), [red-team findings](red-team/REPORT.md), [supplemental results](supplemental/results.md), [earlier repair](repair/report.md) and [previous packaged results](revision/history/results.md). Run `python tools/verify_submission.py` for the current portable audit. Nothing has been published; public URL and Premium/VIP eligibility remain external gates.
