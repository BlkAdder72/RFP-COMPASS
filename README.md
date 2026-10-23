# RFP-COMPASS — Competition #15 rebuild

Local candidate; not published. Start with [current results](results.md), [frozen questions](questions.md), and [final hardening evidence](hardening/REPORT.md). The judged original is unchanged under `original/`; verbatim feedback is `feedback.md`; the usable project is under `rebuild/`.

Run `python -X utf8 tools/verify_submission.py` for the portable offline audit (Git history required; delivery binaries are optional). For a fresh core comparison use `python tools/run_arm.py original --output-dir NEW_DIRECTORY`, then the same command for rebuild with a different new directory. Existing destinations refuse before writes. For the full-length continuation protocol see `hardening/run_full.py` and `hardening/protocol.md`; its fixed evidence destinations also refuse reuse.

The final warning repair passes cross-anchor protection and the retained controls. Every earlier source, prompt, model response, failure and report remains available. Frozen questions are unchanged. Full-length test results and any limitations are reported without repairing model outputs. The source ZIP provides current files; the Git bundle preserves history and the judged-original tag. Membership eligibility and public submission remain pending.

---

The [previous package guide](hardening/history/README.md) and [previous results](hardening/history/results.md) are preserved as historical evidence. Earlier `revision/`, `repair/`, `supplemental/` and red-team directories retain their original status and failures; use the current report above for release readiness.

