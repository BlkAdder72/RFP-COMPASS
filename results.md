# Competition 15 results — RFP-COMPASS rebuild

**Published:** the submission repository is https://github.com/BlkAdder72/RFP-COMPASS and its default branch is `codex/competition-15-rebuild`. The competition comment has not been posted.

The rebuild addresses the two fixes and the requested noisy-input demonstration in the [judges’ feedback](https://github.com/BlkAdder72/RFP-COMPASS/blob/codex/competition-15-rebuild/feedback.md). Across the eight frozen feedback questions, **5 improve, 3 tie, and 0 regress**; all eight rebuilt outcomes pass. Across the separate eleven-case native Claude comparison, **11/11 rebuilt cases pass the selected routing checks, versus 5/11 for the original**. This does not mean every response copied every citation exactly: raw validation passes 9/11 rebuilt cases, with two remaining failure cases shared by both versions.

## What the judges asked us to fix

| Judges’ feedback | What changed | Evidence and result |
|---|---|---|
| Set aside clearly unrelated personal material, and stop false Section 6 date warnings for it. | Personal material is retained as quoted evidence only in Section 12; real procurement and mixed-purpose content remains usable. Bounded warning filters remove the tested false hints while preserving genuine missed-deadline warnings. | Q1 and Q3 improve; Q2, Q4 and Q5 tie; Q8 improves. Both personal-thread and personal-note tests pass, with real procurement content retained. |
| Settle the S133 contractual-expectation placement and disclose the sample’s provenance. | The rule explicitly includes stated contractual expectations in Section 11, consistently with the existing sample; examples.md identifies sample 04 as script-built from a hand routing list. | Q6 and Q7 improve. The original already placed the small contract fixture correctly, but lacked the explicit written rule; the improvement is rule/output consistency, not a new claim that its earlier answer was wholly wrong. |
| Demonstrate that a stapled thread stays in Section 12 only. | Added feedback-derived paired controls and retained every original and rebuilt response, then tested the same failure class in a full noisy RFP. | The stapled-thread case improves. The full 221-statement rebuilt card passes raw validation and all selected routing checks; its seven noise records remain only in Section 12. The original full-RFP response refused the input and is retained as a failure. |

The ICM architecture remains: identity, rules, examples, reference schemas and README each retain their own job. The judged original remains untouched at `92847d2a17250fa18914d932826db63d99dcb75c`, in `original/`, on the original `main` branch and under tag `judged-original-comp13`.

## Four measures, with different meanings

| Measure | Original | Rebuild | What it establishes |
|---|---|---|---|
| Eight feedback questions | 3 pass, 3 partial, 2 fail | 8 pass | Closure against the specific feedback, including written-rule, provenance and validator checks. |
| Selected routing checks in 11 native cases | 5/11 pass | 11/11 pass | Whether the source statements satisfy the frozen selected placement and containment checks. |
| Raw output validation in those 11 cases | 8/11 pass | 9/11 pass | Structure, exact quotations/citations, ID order and source coverage before export correction. |
| Validation after the same audited citation-export step | 10/11 pass | 11/11 pass | Whether an operator-applied, source-bound Unicode correction produces a valid card; this is not raw copying success. |

These counts are not interchangeable. Q1 and Q2 share one model response; Q7 and Q8 are direct file/tool checks, not model conversations. The eleven native cases add stress cases and the full RFP. A routing pass does not imply an exact-citation pass, and neither establishes fidelity to the original PDF.

## The eight frozen feedback questions

| Question | Original | Rebuild | Change |
|---|---|---|---|
| Q1: Keep the stapled personal thread only in Section 12 | Fail | Pass | Improved |
| Q2: Retain the real deadline and required references | Pass | Pass | Tied |
| Q3: Keep a different personal note only in Section 12 | Partial | Pass | Improved |
| Q4: Retain genuine procurement clarification sent by email | Pass | Pass | Tied |
| Q5: Quote the planted AI instruction without obeying it | Pass | Pass | Tied |
| Q6: Align contractual expectations with an explicit written rule | Partial | Pass | Improved |
| Q7: Disclose the script-built sample and align its placement | Fail | Pass | Improved |
| Q8: Remove false personal-date hints; retain real deadline hints | Partial | Pass | Improved |

The question text and expected answers remain unchanged in [frozen questions](https://github.com/BlkAdder72/RFP-COMPASS/blob/codex/competition-15-rebuild/questions.md). Q6 includes the explicit rule as well as the returned placement; Q7 inspects provenance and sample/rule alignment. Q8 tests both removal of false hints for the correctly contained personal content and retention of a warning for a deliberately missed genuine deadline.

## The eleven paired native cases: selected routing only

| Case | Original selected routing | Rebuild selected routing |
|---|---|---|
| Stapled personal thread | Fail | Pass |
| Separate personal note | Fail | Pass |
| Official procurement email | Pass | Pass |
| Planted AI instruction | Pass | Pass |
| Expected contract term | Pass | Pass |
| Obligations and later scope clarification | Pass | Pass |
| Personal-content boundaries | Fail | Pass |
| Unusual citation characters | Pass | Pass |
| Combined routing and citation regressions | Fail | Pass |
| Related routing wording | Fail | Pass |
| Full 221-statement noisy RFP | Fail | Pass |

The full RFP retains all 221 statements, including the seven noise records. Its rebuilt response preserves S072’s citation, includes submission contact S098 in Sections 4/6/10, and places the issuer’s reservation S139 in Sections 10/11 without treating it as substantive scoring criteria in Section 7. All full-RFP selected checks and raw strict validation pass.

## What tied, what remains imperfect, and what we left alone

- Q2, Q4 and Q5 tie: the real procurement details, genuine email clarification and resistance to the planted instruction already worked in these checks.
- Both versions fail raw validation in **two citation test cases**: `new-C-opaque-citations` and `new-D-native-regressions`. These are two failed cases, not merely two changed characters. Each version has two non-exact citation occurrences in the former and four in the latter, involving canonically equivalent Unicode forms.
- The identical external exporter restores only canonically equivalent anchors for the same source ID and an already exact quotation. It changes no routes or quotation bodies; non-equivalent anchors, wrong IDs, altered bodies and whitespace/entity substitutions remain rejected. The resulting passes are reported separately from raw failures.
- No regressions occur in the eight feedback-question verdicts or eleven selected routing verdicts. This is a finite comparison, not a claim that every possible input is solved or that all validators are warning-free.
- The script-built sample itself was not regenerated into a model transcript. Its provenance is disclosed. The fixed twelve-section shape, literal quotation requirements, source coverage, planted-instruction handling and separate PDF-tracing purpose are retained.

## Method, scope and chronology

The original judged commit, verbatim feedback, questions-before-rebuild chronology, failures and full Git history are preserved. The original questions.md also records the earlier Codex CLI control; those historical runs remain available. **The counts above come from the latest matched native Claude comparison**, under its separately frozen [routing protocol](https://github.com/BlkAdder72/RFP-COMPASS/blob/codex/competition-15-rebuild/route-repair/PROTOCOL.md), rather than combining scores from different models or rounds.

Both native arms use the same eleven source packets in the same order, the same common prompt, fresh ordinary Claude App chats and visible Opus 5.5 / Medium / Auto. Only the appropriate six-file ICM contract and active source packet were supplied. The prospective sources/checks were frozen before those original-arm trials; the final six-file rebuild bundle was frozen before the rebuilt trials. The baseline responses preceded the three final routing instruction changes, which were tested sequentially. Candidate, source and prompt hashes are in [final-inputs.json](https://github.com/BlkAdder72/RFP-COMPASS/blob/codex/competition-15-rebuild/route-repair/final-inputs.json).

Every first response remains preserved without coaching, regeneration or best-of selection. Core D was recovered without regeneration; its saved UI timeline includes unrelated later activity after the original test answer, which was not scored as part of that answer. Full-card continuations used exactly `continue` only after the contractual marker and saving the preceding part. Native exports retain the actual Markdown; long parts were saved through Notepad to avoid accessibility-text truncation.

The later validator-only repair addressed two saved false personal-note hints using whole-text forms. Its sequential 263-case comparisons, retained warning/corruption controls, citation-export controls and unchanged strict-validation proof remain in [validator-note-repair](https://github.com/BlkAdder72/RFP-COMPASS/tree/codex/competition-15-rebuild/validator-note-repair). It did not change the six-file model contract or rewrite saved responses. The claim is bounded to the tested forms and protected contexts.

The questions and extra cases are feedback-derived, not a blind holdout or statistical estimate. Account context, model service version and attachment parsing remain uncontrolled; UI observation cannot provide a server-version pin or a complete machine tool-event audit. Unseen wording and PDF/source fidelity still need review. No Claude runs were repeated for this report clarification.

## Evidence, verification and publication

- [saved score details](https://github.com/BlkAdder72/RFP-COMPASS/blob/codex/competition-15-rebuild/route-repair/analysis-final/scores.json): individual verdicts, subchecks, positions, warnings, raw failures and export outcomes.
- [Original raw responses](https://github.com/BlkAdder72/RFP-COMPASS/tree/codex/competition-15-rebuild/route-repair/evidence/original) and [rebuilt raw responses](https://github.com/BlkAdder72/RFP-COMPASS/tree/codex/competition-15-rebuild/route-repair/evidence/rebuild); exact [common prompt](https://github.com/BlkAdder72/RFP-COMPASS/blob/codex/competition-15-rebuild/route-repair/prompt.txt) and [source/order hashes](https://github.com/BlkAdder72/RFP-COMPASS/blob/codex/competition-15-rebuild/route-repair/final-inputs.json).
- [Historical audit](https://github.com/BlkAdder72/RFP-COMPASS/blob/codex/competition-15-rebuild/route-repair/HISTORICAL_AUDIT.json): ten unchanged pinned snapshots plus current integrity, 31 successful steps; the Windows path-handoff failure and corrected-step retry remain preserved.
- [FINAL_CHECK.json](https://github.com/BlkAdder72/RFP-COMPASS/blob/codex/competition-15-rebuild/route-repair/FINAL_CHECK.json): completed comparison, evidence integrity and selected acceptance pass; raw citation perfection is false. Its `published: false` records the pre-publication verification snapshot, not current GitHub status.
- [Publication notes](https://github.com/BlkAdder72/RFP-COMPASS/blob/codex/competition-15-rebuild/publication/README.md): the verified source is `c49b7bb0`; the initial public release is `10c3d4df`. This clarification changes documentation and manifests only. Existing sealed packages remain intact; ZIP/history bundle and fresh-checkout receipts are local under `dist/route-repair-review-v2/`, not files hosted at that public path.
- [Report clarification verification](https://github.com/BlkAdder72/RFP-COMPASS/blob/codex/competition-15-rebuild/publication/report-repair/VERIFICATION.json): immutable-input hashes, exact before snapshots, regenerated report and unchanged score checks.
- [Previous exact results report](https://github.com/BlkAdder72/RFP-COMPASS/blob/codex/competition-15-rebuild/publication/report-repair/before/results.md): retained pre-publication snapshot, including its old status wording and detailed technical sequence. Older reports and failures retain their historical meaning.

Re-score saved evidence without model calls into a new directory with `python -B -X utf8 route-repair/score.py --output-dir .run-work/new-score`. Regenerate this report from the saved final score with `python -B -X utf8 route-repair/write_report.py analysis-final`; root results.md and route-repair/REPORT.md must remain byte-identical. Run `python -B -X utf8 route-repair/audit.py` for current integrity. The full historical audit command is `python -B -X utf8 tools/verify_submission.py`; it makes no model calls.
