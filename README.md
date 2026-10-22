# RFP Compass — The Rebuild

**Latest review: [supplemental stress tests](supplemental/results.md) found a validator-warning regression.** The first-pass report below remains preserved. The supplemental model comparison produced six improved pairs and ten ties, but the package should not be published as regression-free. See the report for the defect and mixed-statement limits.

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

This verifies 134 preserved original files and the feedback hash, exact fixture delivery, contract hashes, raw-response extraction and absence of observed tool calls, then regenerates both score files. Semantic placement is scored separately from structural validation.

The model runner requires an authenticated Codex CLI with access to the recorded model; its executable path is specific to this Windows machine. Adapt and record that path for other systems. To rerun, use a separate checkout and archive the existing run directory first: tools/run_arm.py refuses to overwrite trials. Rerun both arms under the same environment. Do not supply questions or expected answers to the model.

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
