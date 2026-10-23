# Final sealed-package red team — 2026-10-23

**Verdict: hold for warning-suppression repair.** No new citation or model-routing regression appeared in these paired trials. Two deliberately misrouted controls expose genuine warning regressions: original warns about mandatory activity/deadline evidence, while rebuild suppresses the warning. Clearly personal unfamiliar milestones also still produce false warnings. These directly affect the feedback's requested distinction between unrelated personal material and real procurement obligations.

Reviewed candidate: `06fcebace08c19410b63f1cd8c2523f66822d18b`, sealed under `dist/release/`. This is a review only. Candidate files, root scores, frozen questions, earlier raw evidence and every sealed delivery remain unchanged. This new report/evidence is committed separately; it is not inside the existing ZIP/bundle. No publication or replacement package was performed.

## Confirmed findings

### P1 — mandatory-event context phrased as “have to” loses its warning

Frozen evaluator source:

```text
S001 | RFP participation p. 2 | All companies have to attend the following events:
S002 | RFP participation p. 3 | Our farewell dinner is December 6, 2026 at 7 PM.
```

The evaluator-built card deliberately puts both statements only in Section 12. The event is compulsory in this official participation context; its date should be in Section 6. Original prints a Section 6 REVIEW for S002. Rebuild prints `PERSONAL HINT FILTER: S002` and suppresses that REVIEW. Replacing only “have to” with “must” restores the rebuilt warning. The clinical-context control also keeps its warning.

Witnesses: `controls/compulsory-have-to/{source-packet.md,card.md,original/stdout.txt,rebuild/stdout.txt}` and `controls/mandatory-must-control/`.

Cause: `rebuild/tools/validate_packet.py:58–66` recognizes a keyword set, while `:84–94` protects context only after a procurement/clinical keyword match. “Companies have to attend” is an express obligation but contains none of the procurement keywords. The subsequent recognized personal activity is therefore excluded even across an official event list. This reopens the protected-context problem under a new wording, despite the earlier literal-must cross-anchor controls still passing.

This is a **warning regression relative to original**, not an assertion that the validator should mechanically fail every semantic misplacement. Both tools structurally accept the evaluator card, as designed. The safety hint is the behavior under test. In the new model trial Z, rebuild actually routes the official event correctly; this control shows what its validator misses if an output is wrong.

### P1 — a real offer deadline inside a personal-looking statement is suppressed

Frozen evaluator source:

```text
S001 | RFP participation instructions | Our farewell dinner is December 6, 2026 at 7 PM; companies have to deliver their offers by December 7, 2026 at 2 PM.
```

The whole statement must be preserved, including its genuine offer-delivery deadline. A card placing it only in Section 12 is deliberately wrong. Original prints the Section 6 warning. Rebuild suppresses it as personal activity. “Offers” and “have to deliver” are not recognized procurement cues; the personal phrase wins the heuristic despite a real response obligation.

Witness: `controls/mixed-offer-deadline/`. This is a second, same-statement instance of the warning regression; it does not require a heading or a cross-page transition. It is evaluator-built, not a newly observed model failure. Fixing only header context would leave this case unresolved.

Before release, the suppression rule should retain warnings for equivalent obligation wording and mixed requirements, with both controls frozen and genuine/clinical protections retained. Adding broad role words alone could create more personal false warnings; a repair needs negative controls as well as the failing examples. No fix was applied during this review.

### P2 — personal-content warning generalization still fails

Correct Section 12-only cards for `My child’s baptism ceremony is December 3, 2026 at 11 AM.` and `My baby shower is December 4, 2026 at 3 PM.` produce false Section 6 warnings in both versions. The source anchors explicitly identify unrelated private family correspondence, and the bodies are plainly personal. Rebuild's activity whitelist does not cover them.

Witnesses: `controls/baptism/` and `controls/baby-shower/`. This is a remaining defect tied with original, **not** a new regression relative to original. The graduation control is improved: rebuild suppresses its false warning while original still warns.

The new model Z confirms the practical mismatch: rebuild correctly quarantines all three personal milestones and preserves the real compulsory event in Section 6, then its native validator warns on the baptism and baby shower anyway. Original misroutes the three personal milestones into Section 6, so its model card has no corresponding missing-date warnings. Zero warnings on that original card is not successful containment.

## New paired model results

Sources and expected matrices were frozen in commit `47ad81f` before execution. Original ran X/Y/Z first, then rebuild used the identical sources/order through the unchanged `tools/run_arm.py`: gpt-6-astra, medium reasoning, fresh ephemeral sessions, same wrapper, six designated knowledge files only, no tools, no retry, best-of selection or output correction. Exact prompt equality, knowledge hashes, commands and raw event/card equality are verified for all six replies. Expected matrices and scorers were never supplied to models.

| Dimension | Original | Rebuild |
|---|---|---|
| X: unseen citation microvariants, exact text/anchors | Pass | Pass |
| X: required attachment routing | Pass | Pass |
| Y: required/optional and eligibility/post-award boundaries | Fail: required maximum price omitted from Section 5 | Pass |
| Z: private milestones only in 12, compulsory official event retained in 6 | Fail: private milestones in 6 | Pass |
| Z: no false warnings on the correctly quarantined private milestones | Original model card is misrouted; correct-card controls fail | Fail: two false warnings |

X adds new complete anchor strings containing Roman-letter lookalikes, narrow NBSP, zero padding, superscript versus ordinary digits, nested brackets, literal backticks and zero-width characters. All quotation and anchor occurrences are exact in both arms. The same rebuilt strict validator was also applied to original outputs, so permissive original quotation tolerances do not make this fidelity tie. The strict controls accept the exact new anchors and reject all six altered-anchor variants in both tools. Rebuild additionally rejects altered zero-width quotation text and straight delimiters; original's known permissive behavior remains visible.

There are 32 evaluator-built validator executions. Rebuild meets 12/16 control expectations: its four failures are the two unsafe suppressions and two personal false warnings above. Original meets 11/16, failing the three personal-warning controls and its two known quotation-tolerance controls. These mixed control totals are not a statistical score or evidence that warning safety is acceptable. The two paired warning regressions remain failures regardless of improvements elsewhere.

No citation regression or new model-routing regression was observed on the frozen selected checks. These are short synthetic sources whose test classes were informed by earlier failures. The complete strings are new; this is not an independent real-world holdout, fresh Claude acceptance or a long-input copying guarantee. No new full-length model call was made in this review.

## Expanded retrospective full-RFP routing review

`full-semantic-review-plan.json` binds the unchanged 221-statement packet by SHA-256 and selects 17 real RFP statements covering qualifications, mandatory response information and price, statutory forms, contract expectations, costs, insurance and post-award licenses. Required and forbidden placements are reviewed separately. This is explicitly retrospective; it does not replace the prior frozen score or become a prospective model result.

Rebuild meets every selected required/forbidden placement. Original misses S066 in Section 5 and S133/S148 in Section 11. There are no paired routing regressions in this expanded sample. S076 remains in Sections 4 and 5. Witnesses, source rows, raw-card hashes and line numbers are retained in `full-semantic-results.json`.

This improves the evidence for required-information routing but does not adjudicate every section of every statement. Soft modality, bare headings and other unselected assignments remain outside this matrix. Exact ID coverage alone cannot establish complete semantic correctness.

## Competition and delivery compliance

Fresh clone from the sealed bundle: **PASS**. Archive file set and all 10,335 source files checked byte-for-byte, bundle verification, pristine clone/index bytes, both runner preflights and the full offline historical/current audit all pass. This delivery audit calls no model. The long-path-safe auditor runs successfully with authorized local Windows Git execution; the prior environment failures remain preserved.

The required original/feedback/rebuild/results/questions/raw-run layout and original pin remain verified. The original matches its judged commit, feedback is verbatim, eight questions remain frozen before the first rebuild, and the required original-before-rebuild Git sequence survives. Existing results disclose ties, failed attempts and deliberately unchanged areas. The model-free Q7/Q8 checks and bounded nature of warning hints are disclosed. The three new probes are supplemental and do not change the eight root questions.

The integrity check preserves every one of the 10,335 pre-review tracked files and all 20 sealed delivery files. No raw failure or earlier report was rewritten. See `preservation.json`, `verification.json`, `delivery-summary.json` and the complete `delivery-checks.json` commands/stdout/stderr.

## What can still cost the win

1. The two new warning regressions can hide genuine date evidence from an evaluator; this is the strongest reason to hold publication.
2. Fresh personal milestones recreate the exact false-warning class named in feedback, even when the model's containment is correct. Known-case closure has not solved that general problem.
3. Short unseen-anchor success and selected semantic checks do not establish long-input robustness. Earlier failed S072/S100 attempts remain evidence of variability. The latest repair still has one final pair on a known full-length input after inspecting failures; there is no statistical copying advantage claim.
4. Thousands of evidence files make reviewer navigation important. Root results are truthful about their frozen checks, but this new audit is separate and not yet in the sealed release. Any future repair/repackage should surface these findings in the release report and navigation.
5. Premium/VIP eligibility remains unverified. Public repository submission URL and draft comment remain unposted as requested. The brief's deadline remains Wednesday October 28, 11:59 PM EST as written. Those gates are pending; no eligibility or submission completion is claimed.

The warning regressions should be repaired and both arms rerun fairly before another release decision. Nothing has been published.
