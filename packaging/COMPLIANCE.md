# Final local competition compliance — default-Q8 revision

October 22, 2026. Unpublished. Local checks pass for the revised workflow; this does not predict the judges' broader rerun results.

| Requirement / red-team finding | Current result |
|---|---|
| Root original, feedback, rebuild, questions, results and both raw arms | Present; latest fair runs nested in both arms under revision-v2/. |
| Original pinned and untouched | All 134 files match actual judged Git objects at 92847d2a17250fa18914d932826db63d99dcb75c; tag and ancestry retained. |
| Feedback and frozen questions | Byte-identical; eight questions committed before first rebuild. |
| Sequence and fair fresh rerun | Original baseline committed before the default-validator change; two repeats, same model/settings/prompts/inputs, second-repeat arm order reversed. Twenty raw model responses plus Q7/Q8 inspections retained. |
| Q8 default workflow | Rebuild passes both components in both repeats, with no selected review records. Original remains partial in both. |
| Final Q1–Q8 scorecard | Five questions improve per repeat; three tie; no regressed scored subcheck. Ten improved paired comparisons, six ties. |
| Runner refuses before mutation | Seven model-free tests passed, including existing-destination and repeat refusal. Metadata/files are created exclusively in new destinations. |
| Runner portability/workspace | Executable discovery or --codex; read-only preflight; auto-created unique working directory; no personal versioned path in supported runner. Model access/authentication still required. |
| Default checker boundaries | Corrected 51/51 suite passes. Source-text personal cue plus placement guard; requirement/context veto. Ambiguity keeps hints. |
| Prior corpus compatibility | Both validators structurally replayed 42 prior model cards and four samples: 92/92. |
| Original failures/ties preserved | All 2,756 pre-revision tracked files preserved in place or byte-identical revision/history/ copies; earlier 1,287-file snapshot, all stage reports, old scores and raw logs retained. |
| Test assertion correction | Initial 50/51 result retained; one missing-heading expectation corrected separately, without validator/frozen-question changes. |
| Publication and public URL | NOT PERFORMED, as instructed. Submission comment remains a draft. |
| Premium/VIP membership | NOT VERIFIED; external gate before entry. |

Run `python tools/verify_submission.py` from a full-history checkout with Python 3.10+. No third-party Python packages are needed. It audits 62 actual model responses (42 historical plus 20 fresh), historical and current checker evidence, and preservation; it writes current audit output only under the new final-checks-v2/ and revision audit paths. It never rewrites earlier scores. Historical verifiers remain evidence of their own stages.

The bound is explicit: English personal-activity heuristics are not universal semantic proof, generic lunch-money hints can remain, mixed indivisible statements stay whole, source authority is not authenticated, host-system messages are not byte-controlled, and synthetic repetitions are not a statistical or blind-corpus reliability estimate. Optional review records are outside the paired default workflow.

Delivery is a source ZIP plus a complete-history Git bundle and SHA-256 checksums. The ZIP lacks .git; use the bundle for the supported history audit. Prior sealed files are retained under dist/prior-default-q8/. Fresh-clone and exact-byte checks are required before the replacement artifacts are delivered. The root -text checkout policy preserves evidence bytes across platforms. No push, hosting change or submission is performed by packaging.

The supplied brief's deadline reads Wednesday, October 28th, 11:59 PM EST; no timezone reinterpretation or eligibility confirmation is claimed. The original brief remains competition-spec.txt.
