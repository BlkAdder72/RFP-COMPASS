# Current restart status — no Claude runs authorized

As of October 28, all eleven original first-pass native responses are preserved. Three repaired responses (core A, B and C) are fully exported and scored. The fourth, core-D-ai-instruction, was submitted once and finished; capture failed while verifying Copy, so its raw response is not saved. Seven later repaired cases have not run. The exact interrupted checkpoint is [RESUME-REPAIRED-PROGRESS-04.md](RESUME-REPAIRED-PROGRESS-04.md).

Do not regenerate, correct or start over with that fourth response. Do not rerun the original arm. The current user instruction excludes Claude runs and publication. Any future recovery must preserve the existing fourth response before proceeding and must follow the frozen order and prompt; this guide does not authorize resuming native input.

The six-file model bundle in inputs/rebuild/translation-contract.md and its hashes in final-inputs.json remain frozen. The subsequent offline-only validator warning repair is documented in [validator-note-repair/REPORT.md](../validator-note-repair/REPORT.md). It removes the two saved personal-note hints while retaining strict validation and procurement/clinical protections. It supplies no new model response or semantic-routing acceptance.

Current scores: [validator-note-repair/analysis/scores.json](../validator-note-repair/analysis/scores.json). Q1–Q4, Q7 and Q8 pass in the available evidence; Q5/Q6 remain pending. Current reports: [results.md](../results.md) and [REPORT.md](REPORT.md). Earlier baseline-only analyses, reports, failed trials and checkpoints remain historical.

Current documentation/package index: [documentation-sync/REPORT.md](../documentation-sync/REPORT.md). The newest offline review snapshot is dist/documentation-sync-review/, with source ZIP, full-history bundle, checksums and fresh-clone verification. Final competition packaging and submission stay on HOLD until the complete native evidence and final audit exist.

For offline reproduction, use new output paths with route-repair/score.py and validator-note-repair/test_repair.py --stage final. Do not overwrite old output directories or confuse local tests with model acceptance. Native window IDs and coordinates in older notes are stale and must never be reused without live observation if a later instruction authorizes recovery.
