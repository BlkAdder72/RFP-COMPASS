# RFP Compass — The Rebuild

**Unpublished revised package: default Q8 and both runner defects are fixed.** Start with [results.md](results.md), [the resolution report](revision/report.md) and [the final compliance record](packaging/final-compliance.json). The fresh paired comparison used twenty model sessions plus file/tool checks; the rebuild passed Q1–Q8 in both repeats, and Q8 used no review record. The original, feedback, frozen questions and both raw run arms remain at the required root paths. [SUBMISSION_COMMENT.md](SUBMISSION_COMMENT.md) is a draft only.

All 1,287 prepackaging files remain in [history/prepackage/](history/prepackage/README.md). The new preservation manifest covers all 2,756 pre-revision tracked files; changed entry points/reports were copied to revision/history/ before editing. Earlier stage and red-team reports remain unchanged historical records. Default hint filtering is now bounded and source-text based; do not claim universal noise classification or mixed-statement isolation.

**A stapled personal email became an RFP deadline. This rebuild keeps it as evidence without promoting it into a requirement.**

Competition #15 local review draft. First-pass results: **five improved questions, three ties, no observed regression on the scored checks.** Read [feedback.md](feedback.md), [questions.md](questions.md), then [results.md](results.md).

Compare the [original noisy-input card](run-original/A-stapled-thread/bid-compliance-card.md) with the [rebuild card](run-rebuild/A-stapled-thread/bid-compliance-card.md). Personal events move out of Section 6 and lunch money moves out of Section 8; all remain quoted in Section 12.

The original is the complete export of BlkAdder72/RFP-COMPASS at judged commit `92847d2a17250fa18914d932826db63d99dcb75c`. Files under `original/` must remain byte-identical to that export. Its historical results describe the old entry, not this competition's outcomes.

`feedback.md` is the judges' file, copied verbatim. `questions.md` fixes the evaluation before any rebuild exists. `fixtures/` holds synthetic evaluation inputs, not official procurement documents and not recovered judge inputs.

Required sequence: preserve original and feedback → commit questions and fixtures → run original and commit raw evidence → create rebuild → run identical questions → commit raw evidence → write results including ties and regressions.

## Verify offline

Python 3.10+, no third-party dependencies for this comparison:

```text
python tools/verify_submission.py
```

This checks the layout, 134 original files against judged Git objects, feedback, Git sequence, 42 historical plus 20 fresh model responses, 75 historical repair expectations and prior evidence. It audits the new default-Q8 comparison, 51 corrected checker cases, 92 structural replays and seven model-free runner tests. It never regenerates historical scores. Current root-validator logs are under packaging/final-checks-v2/; older final-checks/ remains unchanged. Historical verifiers assume their stage's old paths; use this supported entry point.

New runs require an authenticated Codex CLI with access to gpt-6-astra. The runner discovers codex on PATH; use --codex for an explicit executable path. It creates its working directory and refuses existing output destinations before writes. Use new labels below, and never supply expected answers or feedback to translation sessions.

```text
python tools/run_arm.py original --output-dir experiments/new-label/original --preflight-only
python tools/run_arm.py rebuild --output-dir experiments/new-label/rebuild --preflight-only
python tools/run_arm.py original --output-dir experiments/new-label/original
python tools/run_arm.py rebuild --output-dir experiments/new-label/rebuild
```

Preflight checks flags/local inputs, not account access; an actual access failure is retained in the new experiment directory. Latest runs are under run-original/revision-v2/ and run-rebuild/revision-v2/. Q8 passes with ordinary commands, without additional review input. [Review records](rebuild/REVIEWED_EXCLUSIONS.md) remain optional, outside the default comparison.

## Git sequence

| Commit | Evidence |
|---|---|
| be4d956 | Original, feedback, questions and inputs; no rebuild |
| bfdd812 | Harness and integrity manifest frozen before trials |
| 045e74e | Original raw runs committed; still no rebuild |
| c97a79c | Focused rebuild created |
| f10babd | Rebuild raw runs and checks committed before conclusions |

Eight questions do not represent eight independent model trials: five fresh sessions per arm produce six question results, and two questions inspect files/tools. The inputs are synthetic; host-context variation and other limitations are disclosed in results.md. Historical claims inside the original and rebuild folders describe the old project unless explicitly identified as new evidence.

Original project by Matthew Mazur / BlkAdder72. The original license is retained. Work performed October 22, 2026. No external submission has been made.
