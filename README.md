# RFP-COMPASS — Competition 15: The Rebuild

Local candidate, unpublished. Start with [feedback.md](feedback.md), [questions.md](questions.md), then [results.md](results.md).

The judged Comp #13 original is preserved byte-for-byte in original/, pinned at 92847d2a17250fa18914d932826db63d99dcb75c (tag judged-original-comp13). Source: https://github.com/BlkAdder72/RFP-COMPASS.

The judges asked for unrelated personal material only in Section 12 without false date warnings, consistent S133 contractual-expectation handling, explicit script-built sample provenance and raw noisy-input evidence. Frozen Q1–Q8 address those requests and precede the first rebuild. Current results report wins, ties, failures and intentionally unchanged behavior.

The October 26 review found four remaining warning issues. They were fixed and tested sequentially; all previous failed evidence is retained. Current report: results.md. Detailed stages and preservation: warning-final/. New paired raw runs: run-original/warning-final-* and run-rebuild/warning-final-*. Candidate folder: rebuild/. Exact packaged full-RFP raw evidence: rebuild/run-results/warning-final-full/.

Earlier acceptance reports describe their own recorded gates. red-team-oct26/REPORT.md and the failed boundary-repair/ and submission-repair/ comparisons remain preserved; they are not the current readiness status. Git history and before snapshots retain all earlier documents. Previously sealed packages remain unchanged.

Offline verification: python -B -X utf8 tools/verify_submission.py. It executes historical assertions unchanged at pinned commits, then evaluates current acceptance without model calls. Fresh runs use tools/run_arm.py and hardening/run_full.py with new output paths. Delivery: dist/warning-final-release/; read FINAL_VERIFICATION.json for actual fresh-clone status. Submission draft: SUBMISSION_COMMENT.md, unposted.

Finite test passes do not prove universal semantic routing or native-Claude acceptance. Premium/VIP eligibility and final public URL remain unverified. Nothing is published.
