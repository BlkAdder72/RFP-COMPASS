# Current documentation and package index

**Documentation-aligned offline review; native acceptance remains incomplete. No Claude runs or publication.**

This update replaces stale current-status prose, not historical evidence or the ICM contract. Prior working versions are preserved in [before/](before/), canonical source hashes are pinned in [preservation.json](preservation.json), and earlier commits/packages remain recoverable.

## Start here

| Current entry point | Purpose |
|---|---|
| [Root README](../README.md) | Competition layout, current status and review commands. |
| [Inner README](../rebuild/README.md) | ICM file responsibilities, operation and measured limits. |
| [Results](../results.md) | Current question-by-question comparison; mirrored in [route report](../route-repair/REPORT.md). |
| [Compliance status](../packaging/COMPLIANCE.md) | Current HOLD and the boundary around older compliance receipts. |
| [Original run index](../run-original/README.md) / [Rebuild run index](../run-rebuild/README.md) | Links to saved controls and current native evidence. |
| [Candidate notes](../route-repair/CANDIDATE.md) / [Restart guide](../route-repair/RESUME.md) | Frozen model bundle and interrupted fourth-response state. |
| [Validator repair](../validator-note-repair/REPORT.md) | Two corrected warning predicates and preserved offline proof. |
| [Submission draft](../SUBMISSION_COMMENT.md) | Unposted, limited claims; public URL still requires verification. |

## Current facts

The required original/feedback/rebuild/results/questions/run-folder layout and the ICM identity/rules/examples/reference/README architecture remain. The six-file model contract, validator, exporter, source packets, questions, scores and raw responses are unchanged by this documentation-only update.

All 11 original native responses are exported. Three repaired responses are exported and pass strict validation and selected routing checks. Personal-thread and personal-note containment improve; official clarification ties. The fourth repaired response finished but its raw export is not verified. Seven subsequent cases remain unrun. In available current evidence, Q1–Q4/Q7/Q8 pass; Q5/Q6 remain pending. No older full-RFP result is substituted for a missing current trial.

The two saved personal-note advisory warnings were fixed in the preceding validator-only repair. It passed 263 differential cases per stage, 60 CLI comparisons, 216 retained warning/corruption controls and 17 export controls. Those are offline results on saved data, not new Claude acceptance. Unknown wording may still produce conservative hints.

## What changed

- Replaced older native-candidate claims in the inner README with the actual current counts, explicit ICM responsibilities and limits.
- Rewrote the restart/candidate entry points so they cannot imply no repaired trial was sent or authorize reruns of the interrupted response.
- Replaced the stale “PASS all recorded gates” compliance page; older JSON receipts and scripts retain their historical meaning.
- Added run-folder indexes, aligned root/report/draft package references, and updated the report generator so regeneration preserves these distinctions.
- Parameterized review packaging to create a separate documentation snapshot while retaining earlier verified and failed archives.

Historical protocols, reports, first-pass evidence and earlier compliance JSON are deliberately unchanged. They describe their own versions. The prior verified validator snapshot is dist/validator-note-repair-review-v2/ at commit 43108f35; the first failed archive remains dist/validator-note-repair-review/ with its error receipt.

## Verify and package

```text
python -B -X utf8 documentation-sync/verify.py --output .run-work/new-documentation-check.json
python -B -X utf8 validator-note-repair/package_review.py --package-dir dist/documentation-sync-review-v2 --checkout-dir NEW_ABSOLUTE_DIRECTORY --documentation-check
```

Output paths must be new. The current review snapshot is `dist/documentation-sync-review-v2/`, containing the source ZIP, full Git-history bundle, SHA256 checksums, package metadata and fresh-clone verification. Archive verification checks every Git-tracked source file and the canonical manifest; fresh-clone checks include documentation/ICM integrity, the 263-case validator regression suite, preservation and the retained submission HOLD. The existing Windows long-path handling and preserved canonical sample variant remain in effect.

This review package does not establish complete competition readiness. The latest native comparison and final submission audit remain incomplete, and nothing is published.

The first documentation snapshot remains preserved at dist/documentation-sync-review/ with FAILED.json. Its fresh documentation check falsely reported missing ../ links because Windows extended paths require lexical normalization; version 2 normalizes each target before checking it, with no checks removed. Version 2 also supplies the exact pre-update compliance page required by the older routing audit; no preservation assertion is relaxed.
