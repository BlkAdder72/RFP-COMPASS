# RFP-COMPASS — Competition #15 rebuild

Local candidate; not published. **Open full-length regression: two model-generated S072 anchors are wrong and correctly rejected; no clean full-length pass is claimed.** Start with [current results](results.md), [frozen questions](questions.md), and [final hardening evidence](hardening/REPORT.md). The judged original is unchanged under `original/`; verbatim feedback is `feedback.md`; the usable project is under `rebuild/`.

Judged original pin: `judged-original-comp13` at `92847d2a17250fa18914d932826db63d99dcb75c`, from [RFP-COMPASS](https://github.com/BlkAdder72/RFP-COMPASS). The offline verifier checks all 134 original files against that Git tree and verifies that the frozen questions and baseline precede the first rebuild.

Run `python -X utf8 tools/verify_submission.py` for the portable offline audit (Git history required; delivery binaries are optional). For a fresh core comparison use `python tools/run_arm.py original --output-dir NEW_DIRECTORY`, then the same command for rebuild with a different new directory. For the full-length continuation comparison use `python hardening/run_full.py original --output-dir NEW_FULL_DIRECTORY`, then rebuild with another new directory. Existing destinations refuse before writes; `--codex` supports an explicit executable override. See `hardening/protocol.md`; `run_full_frozen.py` preserves the exact harness used in the recorded trials. The later output-path flags allow new trials without editing tracked evidence and do not change the recorded prompts/model/session logic.

The final warning repair passes cross-anchor protection and the retained controls. Every earlier source, prompt, model response, failure and report remains available. Frozen questions are unchanged. Full-length test results and any limitations are reported without repairing model outputs. The source ZIP provides current files; the Git bundle preserves history and the judged-original tag. Membership eligibility and public submission remain pending.

---

The [previous package guide](hardening/history/README.md) and [previous results](hardening/history/results.md) are preserved as historical evidence. Earlier `revision/`, `repair/`, `supplemental/` and red-team directories retain their original status and failures; use the current report above for release readiness.

