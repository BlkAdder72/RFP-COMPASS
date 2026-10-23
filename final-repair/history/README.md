# RFP-COMPASS — Competition #15 candidate

Not published. The fresh rebuilt full-length card passes every frozen check, including exact S072 citations in Sections 4 and 5. The earlier failed card remains unchanged and still fails validation.

Start with [current results](results.md), [frozen questions](questions.md), [verbatim feedback](feedback.md) and [citation repair evidence](citation-repair/REPORT.md). Previous reports and all failed raw trials remain under `citation-repair/history/`, `hardening/`, `revision/`, `repair/` and `supplemental/`.

The judged original is pinned at `92847d2a17250fa18914d932826db63d99dcb75c` with tag `judged-original-comp13`, from [RFP-COMPASS](https://github.com/BlkAdder72/RFP-COMPASS). Its 134 files remain unchanged under `original/`. The usable project is `rebuild/`. The portable audit verifies the original Git tree, feedback, frozen questions, original-before-rebuild sequence, old and new raw sessions and the unchanged validators.

Run `python -X utf8 tools/verify_submission.py` for the offline audit (Git history required; ignored delivery binaries optional). For a fresh full-length comparison run `python hardening/run_full.py original --output-dir NEW_ORIGINAL_DIRECTORY`, then rebuild with a different new directory. For A–E use `python tools/run_arm.py original --output-dir NEW_CORE_DIRECTORY` and the corresponding rebuilt invocation. Existing destinations refuse before writes; `--preflight-only` calls no model; `--codex` supports an executable override. See `citation-repair/protocol.md` for comparison rules and limits.

The source ZIP contains current files; the Git bundle contains the complete preserved history and judged-original tag. Premium/VIP eligibility and the public submission link remain pending. A passing fresh trial is not a universal model reliability claim.
