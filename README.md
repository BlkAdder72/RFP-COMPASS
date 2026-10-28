# RFP-COMPASS — Competition 15: The Rebuild

**Unpublished; the latest native comparison and final submission audit remain incomplete.** VIP eligibility is user-confirmed. Start with [judges' feedback](feedback.md), [frozen questions](questions.md), and [current results](results.md).

This rebuild addresses the judges' noisy-input failure: unrelated personal content belongs only in section 12, while genuine procurement content remains usable. It also makes contractual-expectation routing explicit, discloses the script-built sample, and passes the specified Q8 personal-date warning test while retaining genuine missed-deadline warnings. The two saved personal-note false warnings are repaired offline with preserved strict validation; finite warning coverage remains disclosed in the report.

The judged Comp #13 entry is untouched in [original/](original/), pinned at `92847d2a17250fa18914d932826db63d99dcb75c` (tag `judged-original-comp13`). Source: [BlkAdder72/RFP-COMPASS](https://github.com/BlkAdder72/RFP-COMPASS). Eight feedback questions were committed before the first rebuild. Historical reports, failures, raw evidence and Git history remain preserved.

## Current evidence

The latest candidate is [rebuild/](rebuild/). Its six-file ICM model contract remains frozen for the [route-repair protocol](route-repair/PROTOCOL.md); later documentation and the authorized validator-only repair are versioned separately. All 11 original native first-pass responses are preserved. Three repaired responses are fully exported and pass strict validation and selected routing checks: personal thread and personal note improve; official clarification ties. Local provenance and default warning checks pass. A fourth repaired response finished but its raw export is blocked; seven subsequent cases remain unrun. These gaps include remaining routing regressions, citation variants and the full-length noisy RFP.

The October 28 update makes no Claude calls and changes no frozen model contract, question, fixture or raw response. The subsequent authorized validator-only fix is separately versioned in validator-note-repair/. See [validator repair](validator-note-repair/REPORT.md) and the [earlier offline review](route-repair/offline-review-2026-10-28/review.json) and [restart checkpoint](route-repair/RESUME-REPAIRED-PROGRESS-04.md). Do not regenerate the fourth response.

## Review and reproduction

[Documentation and package index](documentation-sync/REPORT.md) identifies current entry points and preserved earlier packages. The [inner README](rebuild/README.md) explains the unchanged ICM file responsibilities.

- Current report: [results.md](results.md), mirrored in [route-repair/REPORT.md](route-repair/REPORT.md).
- Exact inputs, hashes and order: [final-inputs.json](route-repair/final-inputs.json); exact [prompt](route-repair/prompt.txt).
- Raw evidence: [original](route-repair/evidence/original/) and [rebuild](route-repair/evidence/rebuild/); control pointers in [run-original/](run-original/) and [run-rebuild/](run-rebuild/).
- Offline check: `python -B -X utf8 route-repair/offline_review.py --output-dir .run-work/new-offline-check`. Add `--require-complete` for a nonzero submission gate while native evidence is incomplete. Output directories must be new.
- Re-score existing evidence only: `python -B -X utf8 route-repair/score.py --output-dir .run-work/new-score`.
- Final submission audit: `python -B -X utf8 tools/verify_submission.py`. This intentionally returns HOLD while the final comparison is missing; passing offline checks alone cannot release the entry.

Older `native-repair/`, `claude-native/` and `dist/` packages describe earlier candidates. No final `dist/route-repair-review/` package has been sealed. The current `dist/documentation-sync-review/` is an explicitly incomplete offline review snapshot, with its own checksums and full Git-history bundle; it is not a submission-ready release. The [submission comment](SUBMISSION_COMMENT.md) is an unposted draft. The review ZIP/history bundle pass their offline and fresh-clone checks; complete the retained native comparison and final submission audit before claiming release readiness. Integrity, raw citation accuracy and semantic routing are separate checks; finite passes do not prove perfection or original-PDF fidelity.
