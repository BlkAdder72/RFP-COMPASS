# RFP Compass — The Rebuild

**Unpublished competition package: root rebuild/ is the repaired version.** Start with [results.md](results.md) and [the final compliance record](packaging/final-compliance.json). The judged original, verbatim feedback, precommitted questions and both raw run arms are at the root as required. [SUBMISSION_COMMENT.md](SUBMISSION_COMMENT.md) is a draft only.

All 1,287 prepackaging tracked files are preserved byte for byte in [history/prepackage/](history/prepackage/README.md), and all Git commits remain. That snapshot contains the historical rebuild and all earlier reports/verifiers in their original context. The [supplemental report](supplemental/results.md) and [repair report](repair/report.md) remain historical, unchanged records; their statements about the root layout describe their stage, before this packaging step. Do not claim automatic noise suppression or universal mixed-statement isolation.

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

This checks the required layout, the 134 original files against the judged Git objects, verbatim feedback, pre-rebuild Git sequence, all 42 raw model responses, 75 historical repair expectations and preservation of prior evidence. It executes the final root validator on 42 archived cards, four reference cards and four critical repair cases; it does not regenerate historical scores. The portable package verifier replaces the old entry point, which remains preserved in history/prepackage/tools/verify_submission.py. Historical verifiers assume their stage's old paths; use the final verifier after packaging.

New model runs require an authenticated Codex CLI with access to the recorded model; runner executable paths are specific to the original Windows machine. Rerun both arms in a separate checkout and preserve the existing run directories; never overwrite trials or supply expected answers to the model. The final validator's selected review records add an operator-adjudication step; see [rebuild/REVIEWED_EXCLUSIONS.md](rebuild/REVIEWED_EXCLUSIONS.md).

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
