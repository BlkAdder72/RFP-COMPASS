# Final local competition compliance check

October 22, 2026. Unpublished package. **Local layout, preservation, sequence and recorded-evidence checks passed.** This is not a prediction of the judges' rerun results.

| Requirement | Result | Evidence |
|---|---|---|
| Root original/, feedback.md, rebuild/, results.md | PASS | Required root paths present; repaired validator promoted into rebuild/. |
| Original pinned and untouched | PASS | All 134 files match the actual judged Git tree at 92847d2a17250fa18914d932826db63d99dcb75c; local tag judged-original-comp13 preserves that commit and ancestry. |
| Feedback verbatim | PASS | SHA-256 equals the original supplied feedback file's recorded hash. |
| Five to ten precommitted feedback-derived questions | PASS | Eight questions; both fixes and tier request are mapped in results.md. Questions and harness were committed before the first rebuild. |
| Original run committed before rebuild | PASS | 045e74e precedes c97a79c; the preceding commits contain no rebuild tree. Git ancestry verified. |
| Identical model questions/input order and raw evidence | PASS for supplied harness | Both arms preserve exact prompts, knowledge hashes and raw events. Five first-pass sessions per arm; eight supplemental fixtures, two repeats per arm. Final six knowledge files match the tested rebuild. Host-system variation remains disclosed. |
| Noisy thread test shipped under run-results | PASS | Rebuild A/B/C raw trial copies and source packets are included under rebuild/run-results/rebuild-noisy-input/ and match root run-rebuild bytes. |
| Ties, regressions and deliberate nonchanges reported | PASS | Root results synthesizes all stages, retains the validator regression and conditional repair, and discloses the indivisible mixed-statement limit. |
| Validator repair evidence | PASS | 75 recorded repair expectations audited; final root checker reruns 42 archived cards, four reference cards and four critical cases (50 checks). Explicit review records remain necessary for suppression. |
| All previous evidence and Git history retained | PASS | 1,287 prior tracked files retained in history/prepackage/ with hashes; stage reports/raw evidence unchanged; local stage history and judged-source ancestry retained. |
| Public repo URL and submission comment | NOT PUBLISHED, as instructed | SUBMISSION_COMMENT.md is a three-sentence draft with a URL placeholder. No push, post or external submission was performed. |
| Premium/VIP eligibility | NOT VERIFIED | Owner/account confirmation is still needed before entry. |

Run `python tools/verify_submission.py` from a checkout with Git history and Python 3.10+. No third-party Python packages are needed for this audit. It writes current checks only under packaging/ and never regenerates historical scores. The detailed machine-readable record is final-compliance.json; final root-validator stdout/stderr is under final-checks/.

Historical verifiers were written for earlier root paths and some contain the original machine's absolute execution paths. They are preserved as evidence. The final verifier resolves those stages through history/prepackage/ and is the supported packaged entry point. Fresh model execution still needs an authenticated model runner; no new model rerun is required for this offline evidence audit.

## Local delivery files

The source ZIP is a convenience copy of the committed tree; it does not carry .git. The companion Git bundle preserves all local refs, competition-stage commits and the judged-source tag. For a full-history copy, use `git clone RFP-COMPASS-Comp15.bundle RFP-COMPASS-Comp15` and run the verifier there. SHA256SUMS.txt accompanies the local artifacts. No hosting or public repository destination has been selected or changed.

The deadline is quoted by the supplied brief as Wednesday, October 28th, 11:59 PM EST. No timezone reinterpretation or independently verified eligibility claim is made here. The original brief is preserved in competition-spec.txt.
