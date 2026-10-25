# RFP-COMPASS — Competition 15: The Rebuild

Local candidate; unpublished. Read [feedback.md](feedback.md), [questions.md](questions.md), then [results.md](results.md).

The judged Comp #13 Translator original stays byte-for-byte under `original/`, pinned at `92847d2a17250fa18914d932826db63d99dcb75c` (tag `judged-original-comp13`). Source: https://github.com/BlkAdder72/RFP-COMPASS. All history, previous deliveries and failed evidence remain preserved.

The feedback asked for personal material only in Section 12 without false date hints, explicit contractual-expectation handling, honest script-built example provenance and raw noisy-input evidence. Frozen Q1–Q8 precede the first rebuild. The latest repair addresses the seven finding families in `red-team-polarity/REPORT.md`; current measured outcomes, ties, failed attempts and limits are in results.md.

| Material | Location |
|---|---|
| Judged original and verbatim feedback | `original/`, `feedback.md` |
| Frozen questions | `questions.md` |
| Candidate knowledge and strict validator | `rebuild/` |
| Latest protocol, before snapshots, controls and report | `boundary-repair/` |
| Fresh paired model runs | `run-original/boundary-repair-*`, `run-rebuild/boundary-repair-*` |
| Packaged full-RFP raw result | `rebuild/run-results/boundary-repair-full/` |
| Latest red-team findings, preserved | `red-team-polarity/REPORT.md` |
| Earlier repair trail | `polarity-repair/`, `red-team-polarity/`, `scope-guard-repair/`, `scope-repair/`, `warning-repair/`, `final-repair/` and earlier folders |
| Source ZIP and complete-history bundle | `dist/boundary-release/` (not sealed: semantic D failed) |
| Three-sentence submission draft | `SUBMISSION_COMMENT.md` |

Offline audit: `python -B -X utf8 tools/verify_submission.py`. Historical assertions run unchanged at their sealed commits in sibling clones, followed by current evidence checks; no model calls. In restricted Windows shells local Git execution may require permission. Fresh trials use unchanged tools/run_arm.py and hardening/run_full.py with entirely new output paths.

The release FINAL_VERIFICATION.json records actual fresh-clone delivery status. Packaging compliance and model performance are separate. This finite warning heuristic is not a complete semantic classifier. Premium/VIP eligibility is unverified; the public URL and publication remain pending. Nothing has been published.
