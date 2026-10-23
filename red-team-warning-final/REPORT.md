# Repaired-package red team — 2026-10-23

**Verdict: request changes; hold publication.** Exact citation validation and the sealed delivery pass the new checks, but warning relevance still fails on unseen obligation wording. The last repair also introduced false warnings on clearly private obligations and on subsequent private content. Two unfamiliar private milestones remain false-warning failures. The submission draft exceeds the competition's sentence limit.

Reviewed sealed candidate: `09684fc7129b8ff4bcbefe4b749f644f8f23f50e`, `dist/warning-release-verified/`. This review does not edit the candidate, root results, frozen questions, prior evidence or any existing delivery. This new report and its raw evidence are separate from the sealed ZIP/bundle. Do not publish the old package as if it contains these new findings.

## F1 — P1: unseen compulsory wording still suppresses genuine date warnings

`rebuild/tools/validate_packet.py:64–65,88–97` protects context only after a listed cue. These source-body obligation variants remain outside the cue set:

- `All companies are to attend the following events:`
- `Attendance at the following activities is a condition of entry:`
- `All companies will be expected to attend the following events:`

Follow each with `Our farewell dinner is January 5, 2027 at 7 PM.` on a separate page anchor. On the deliberately wrong evaluator card putting both rows only in Section 12, original warns about S002; rebuild prints PERSONAL HINT FILTER and suppresses the warning. All cards are structurally valid: these are lost safety hints, not quotation or shape failures.

The same defect occurs within one statement: `Our farewell dinner is January 6, 2027 at 7 PM; offers are to reach the office by January 7, 2027 at 2 PM.` The whole statement contains a real offer-receipt deadline. Original warns when it is misplaced only in 12; rebuild suppresses it. The delivery-action expression recognizes “deliver/send/lodge…” but not this receipt construction.

Witnesses: `controls/{are-to,condition-of-entry,will-be-expected,mixed-offers-to-reach}/`, including identical source/card and both validators' complete outputs. These are four warning regressions relative to the judged original; the earlier pre-warning-repair validator also fails them. The known have-to and clinical controls still retain warnings after the repair.

Both actual new model arms route the official dates correctly in fixture A. Do not mislabel these controls as newly observed model-routing failures: they show that if a translator misroutes equivalent real evidence, the rebuilt validator may hide the useful warning. This remains directly relevant to feedback Fix 1's requirement to distinguish unrelated personal material from procurement evidence.

## F2 — P2: the last repair treats private obligation language as procurement and contaminates later context

Correct evaluator source: `I have to attend my daughter’s birthday dinner on January 9, 2027 at 7 PM.` Correct card: only Section 12. The pre-warning-repair rebuilt validator at 06fceba suppresses the false date hint; the current validator warns. Original also warns, so this is a regression from the preceding rebuilt candidate, not a newly worse result than the judged original.

The same happens for `I do not have to attend our family dinner on January 13, 2027 at 7 PM.` The obligation expression ignores negation and the personal actor. Worse, the birthday dinner activates the global protected flag at line 92, so a following `My graduation ceremony is January 10, 2027 at 2 PM.` also produces a false warning despite containing no obligation. The previous rebuilt validator correctly suppresses that following private date.

Witnesses: `controls/{private-have-to,private-negated-have-to,private-obligation-pollutes-context}/`; each includes original, pre-warning-repair and current outputs. The reference validator is a byte-identical Git snapshot, used only for explicit-path tool checks, not a third model arm.

The new rebuilt model B correctly quarantines every private row, retains the real proposal deadline in Section 6, and copies every quote/anchor exactly. Its native validator nevertheless warns on S002–S006, five clearly private dates. This is an actual new model-plus-validator workflow failure, not only an evaluator-built control. Distinguish correct model routing from incorrect validator hints.

Cause: line 88 promotes any have/need-to phrase to procurement without establishing solicitation scope; lines 90–92 propagate that classification. Repair scope/actor/negation handling independently of the exact citation gate. Adding more obligation phrases alone risks increasing these false positives.

## F3 — P2: unfamiliar personal milestones still cause false warnings

Correct private-only cards for `My child’s christening ceremony is January 11, 2027 at 11 AM.` and `My bridal shower is January 12, 2027 at 3 PM.` still print Section 6 REVIEW. Both source bodies have explicit personal ownership; the model fixture also supplies a literal Private correspondence heading. Neither is a procurement requirement.

Witnesses: `controls/{christening,bridal-shower}/` and rebuilt fixture B. These are remaining defects tied with both original and the preceding rebuild, not new regressions introduced by the latest repair. The known baptism control passes in the current rebuild. The activity list at lines 67–70 remains a finite vocabulary, and a prior private obligation can also protect later personal rows, compounding this behavior.

## F4 — P3: submission draft has four sentences; spec asks for two or three

`packaging/competition-spec.txt` asks for a public repo link “Plus 2-3 sentences” identifying the rebuilt entry and motivating feedback line. `SUBMISSION_COMMENT.md:3` currently has four sentences: entry, feedback line, preserved evidence, latest warning repair. Consolidate before posting. This is a draft-format issue, not an already-published violation. Membership eligibility is still unverified and the public URL remains a placeholder by instruction.

## New paired model evidence

Inputs, expected matrices, controls and protocol were frozen in commit 7559772 before execution. Original A/B/C completed and was committed in 9ac5ec0 before rebuild A/B/C. Both used the unchanged tools/run_arm.py, gpt-6-astra medium, fresh sessions, same wrapper/selected knowledge and order. No tools, retries, corrections or best-of selection; exact prompts, commands, raw event/card equality and all six replies are audited. Expected answers never went to the models. These are new synthetic strings informed by previous failures, not independent real-world holdouts or a reliability estimate.

| Case | Original | Rebuild |
|---|---|---|
| A: unseen official obligation wording, exact copies and selected routing | Pass | Pass |
| B: all unrelated private rows only in 12; real deadline in 6 | Fail: private rows leak into operational sections | Pass |
| B: native warning behavior on the actual model card | No missing-date warning because private dates were misrouted; not successful containment | Fail: five false private-date warnings |
| C: opaque citation variants, exact copies and required attachment routing | Pass | Pass |

All six replies pass the identical strict quotation/anchor gate. There is no observed new model citation or semantic-routing regression on the frozen selected checks. Raw fidelity is separately checked from placement.

## Citation and validator controls

C uses six previously unused full anchors containing U+2060 word joiner, U+200E direction mark, a decomposed accent, literal `&amp;`, a nonbreaking hyphen and literal backslashes. Both models preserve every occurrence exactly. All three validator versions accept the exact anchors and reject all six corrupted-anchor variants. Current rebuild also rejects an inserted word joiner in quotation text; original wrongly accepts it under its known visible-text tolerance. No new strict citation acceptance regression appeared in these controls. Rendering may conceal invisible characters: the raw files, not their visual appearance, establish these matches.

| Validator | Control expectations met |
|---|---|
| original | 13/21 |
| pre-warning-repair | 13/21 |
| rebuild | 12/21 |

There are 63 executions, 21 evaluator cases across three validator versions. These aggregate totals mix warning and structural controls and are not a competition score. Current rebuild fails nine warning expectations: four unsafe suppressions, three private-obligation/context regressions, and two unfamiliar personal milestones. Correctly quoted but semantically misplaced cards can remain structurally valid by design; the default warnings are the behavior under test. No manual exclusion sidecars are used.

## Existing full RFP and delivery compliance

Read-only full-card replay reproduces the previous outcome, without rerunning models or rewriting old scores: rebuilt card passes strict validation, every frozen selected routing check and seven private rows only in 12. Original still fails S072 anchors, misses Section 5 for S066/S083 and Section 11 for S148, and leaks six personal rows. See full-recheck.json. This prior pass does not answer the new obligation/false-warning failures above.

The sealed bundle passes verification, its fresh clone matches its committed source bytes, all 12,591 archive entries match the untouched candidate, and offline historical/current compliance audits pass. This is integrity and automated compliance evidence, not proof that the relevance classifier or submission prose meets every judging expectation.

Preservation audit: all 12,591 pre-review tracked files and 30 existing sealed delivery files are unchanged; frozen questions remain byte-identical to bfdd812. All six new raw model replies are retained. Candidate and root results were not edited. Nothing was published.

## What can still cost the win

The strongest objection is feedback closure: the judges explicitly asked for personal content to remain only in 12 without false date hints, while genuine procurement content remains usable. New controls still demonstrate both unsafe suppression and false warnings. A long record of known-case passes cannot close that gap on unseen phrasing. Repair relevance/context decisions without relaxing the strict quote/anchor checks; retain these failures and rerun both arms fairly under a newly frozen repair protocol.

Also retain the distinctions between evaluator controls and actual model failures, previous-candidate regressions and original-relative regressions, and synthetic regression coverage and a real-world holdout. The old sealed report remains accurate for its earlier frozen cases, but publication should include this new evidence and an updated honest report. One fresh trial per arm cannot establish low failure rates; native Claude acceptance is still untested. Membership and final public URL remain external gates. The four-sentence comment is a small, avoidable spec miss.

Review only: no repair, replacement package or publication was performed. The current recommendation is to hold this candidate for warning-relevance repair.
