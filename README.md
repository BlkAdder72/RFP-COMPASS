# RFP-COMPASS — Competition 15: The Rebuild

Unpublished review candidate. Start with [feedback.md](feedback.md), [questions.md](questions.md), then [results.md](results.md). VIP eligibility is user-confirmed.

The judged Comp #13 original remains untouched in original/, pinned at 92847d2a17250fa18914d932826db63d99dcb75c (tag judged-original-comp13). Source: https://github.com/BlkAdder72/RFP-COMPASS. Frozen Q1–Q8 were committed before the initial rebuild; every later repair and failed comparison remains in Git and on disk.

The judges asked for personal material only in section 12 without false date warnings, consistent contractual-expectation routing, visible script-built provenance, and noisy-input receipts. The latest twenty-trial native Claude comparison passes all eight feedback questions and the full-RFP selected checks. Broader acceptance remains failed: one combined-case route regresses, a contact-route omission remains, and both arms need the explicit audited export step for decomposed Unicode anchors. Read the report before treating a validator PASS as readiness.

Candidate: [rebuild/](rebuild/). Latest native evidence, frozen inputs and detailed stages: [native-repair/](native-repair/). [run-original/](run-original/) and [run-rebuild/](run-rebuild/) retain all comparisons and link to the native supplement. The older claude-native/ and warning-final/ reports describe their own versions; they are preserved evidence, not current acceptance.

Offline integrity check: `python -B -X utf8 native-repair/audit.py`. Reproduce scores: `python -B -X utf8 native-repair/score.py --output-dir .run-work/new-score`. Full historical-plus-current audit: `python -B -X utf8 tools/verify_submission.py`. Integrity and behavioral acceptance are reported separately. Full source ZIP and recoverable Git history: dist/native-repair-review/, with checksums and package verification. Submission draft: [SUBMISSION_COMMENT.md](SUBMISSION_COMMENT.md), unposted.

Finite passes do not prove perfect semantic routing or original-PDF fidelity. Nothing is published.
