# RFP-COMPASS — Competition 15: The Rebuild

Local candidate; not published. Start with [feedback.md](feedback.md), [questions.md](questions.md), then [results.md](results.md).

The Comp #13 Translator entry is preserved at judged commit `92847d2a17250fa18914d932826db63d99dcb75c` (tag `judged-original-comp13`) and byte-identical under `original/`. Source: https://github.com/BlkAdder72/RFP-COMPASS. Its Git history and every rebuild stage remain in this repository.

The feedback asked for unrelated personal material only in Section 12 without false Section 6 warnings; explicit contractual-expectation routing; honest script-built-example provenance; and a noisy-input run in `run-results/`. Frozen Q1–Q8 trace those requests and precede the first rebuild in Git.

Current repair: required response information is checked for Section 5, graduation notes no longer create the known false warning, and quotation validation is strictly character-exact. Read the actual outcomes and limits in [results.md](results.md).

| Material | Location |
|---|---|
| Judged original and verbatim feedback | `original/`, `feedback.md` |
| Frozen questions/expected answers | `questions.md` |
| Candidate knowledge, tools and operating guide | `rebuild/` |
| New exact prompts and unedited replies | `run-original/final-repair-v2-*`, `run-rebuild/final-repair-v2-*` |
| Current protocol, scores, controls, preservation and report | `final-repair/` |
| Previous red-team findings, including S076 regression | `red-team-citations/REPORT.md` |
| Previous citation failures and repairs | `citation-repair/`, `hardening/`, earlier `run-ARM/` folders |
| Earlier complete audit trail | `revision/`, `repair/`, `supplemental/`, `history/`, `packaging/` |
| Updated local ZIP and complete-history bundle | `dist/final-repair-verified/` (local delivery; not source-tracked) |

Offline audit from a Git clone: `python -B -X utf8 tools/verify_submission.py`. It runs historical assertions in a disposable clone of their sealed commit, then checks current repair evidence. It calls no model. Fresh controlled runs: `tools/run_arm.py` for core/new sources and `hardening/run_full.py` for the full fixture; always choose new output directories. Authentication/model access is required for real reruns. The stored trials prohibit tools and record any violations.

`SUBMISSION_COMMENT.md` remains a draft. Eligibility is unverified; public link and comment are pending. Do not publish without authorization.

The managed Windows process sandbox blocked Git's historical-clone helper during delivery checks. That failure is preserved; the same offline audit passed with authorized local Git execution. A restricted Codex shell may need that execution permission to rerun the audit.
