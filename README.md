# RFP-COMPASS — Competition 15: The Rebuild

**Unpublished; native comparison complete. Inspect final audit and package receipt before submission.** VIP eligibility is user-confirmed. Start with [judges' feedback](feedback.md), [frozen questions](questions.md), and [current results](results.md).

This rebuild addresses the judges' noisy-input failure: unrelated personal content belongs only in section 12, while genuine procurement content remains usable. It also makes contractual-expectation routing explicit, discloses the script-built sample, and passes the specified Q8 personal-date warning test while retaining genuine missed-deadline warnings. The two saved personal-note false warnings are repaired offline with preserved strict validation; finite warning coverage remains disclosed in the report.

The judged Comp #13 entry is untouched in [original/](original/), pinned at `92847d2a17250fa18914d932826db63d99dcb75c` (tag `judged-original-comp13`). Source: [BlkAdder72/RFP-COMPASS](https://github.com/BlkAdder72/RFP-COMPASS). Eight feedback questions were committed before the first rebuild. Historical reports, failures, raw evidence and Git history remain preserved.

## Current evidence

The latest candidate is [rebuild/](rebuild/). Its six-file ICM contract, frozen questions, sources and common prompt remain unchanged. All 11 original and 11 repaired native first-pass trials are exported. Core D was recovered without regeneration. Repaired frozen Q1–Q8 pass. Repaired results: 9/11 raw strict, 11/11 expanded selected semantics, 11/11 strict after the identical audited Unicode export. Raw citation failures remain failures; export does not change routing. See results.md for every paired result and any full-RFP failure.

The resumed run is authorized by the October 28 user instruction. Prior offline-only reports remain historical. No response was regenerated and no original trial was repeated.

## Review and reproduction

[Documentation and package index](documentation-sync/REPORT.md) identifies current entry points and preserved earlier packages. The [inner README](rebuild/README.md) explains the unchanged ICM file responsibilities.

- Current report: [results.md](results.md), mirrored in [route-repair/REPORT.md](route-repair/REPORT.md).
- Exact inputs, hashes and order: [final-inputs.json](route-repair/final-inputs.json); exact [prompt](route-repair/prompt.txt).
- Raw evidence: [original](route-repair/evidence/original/) and [rebuild](route-repair/evidence/rebuild/); control pointers in [run-original/](run-original/) and [run-rebuild/](run-rebuild/).
- Offline check: `python -B -X utf8 route-repair/offline_review.py --output-dir .run-work/new-offline-check`. Add `--require-complete` for a nonzero submission gate while native evidence is incomplete. Output directories must be new.
- Re-score existing evidence only: `python -B -X utf8 route-repair/score.py --output-dir .run-work/new-score`.
- Final submission audit: `python -B -X utf8 tools/verify_submission.py`. This intentionally returns HOLD while the final comparison is missing; passing offline checks alone cannot release the entry.

Final unpublished review artifacts are in `dist/route-repair-review-v2/`: source ZIP, complete Git-history bundle, SHA256 checksums and fresh-clone receipt. Earlier incomplete and failed archives remain preserved. The [submission comment](SUBMISSION_COMMENT.md) is an unposted draft. Inspect the final receipt before publishing; integrity and semantic acceptance are separate.
