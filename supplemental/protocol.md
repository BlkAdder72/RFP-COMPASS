# Supplemental stress test — frozen before execution

October 22, 2026. Both original/ and rebuild/ remain unchanged. This protocol supplements, never replaces, the first-pass evaluation. No fixes or prompt tuning between arms or repeats. All prior tracked files are hashed in preservation.json before execution.

Eight synthetic fixtures, two fresh model sessions per fixture per arm (32 responses). Alternate original then rebuild in repeat 1, rebuild then original in repeat 2, for each fixture F–M in order. No best-of selection and no task retries. Preserve failures. Same gpt-6-astra/medium Codex harness wrapper and six supplied contract files as the first pass, exact user prompt, inline named-file delivery, no tools permitted. Preserve command, request, raw events, stderr, exit status, unedited response and audit per trial. Tool use or transport failure is an invalid retained trial; stop for review. Host system instructions are not controlled and may vary. No statistical significance or Claude-replication claim.

## Frozen checks

All trials must preserve exact whole statements, source IDs/anchors, coverage and twelve-section structure. Operational placement checks below are minimum requirements; other permitted placements are not automatically errors. Section 12-only means exactly that one placement. No authority authentication is inferred from a source label.

| Fixture | Question and expected checks |
|---|---|
| F neutral personal attachment | Personal appointment S002 and family event S003 go only to Section 12 despite neutral file anchors. Actual RFP deadline S001 stays in Section 6. |
| G unknown attachment | S002's meeting time remains in Section 6 and S003's required signed form in Sections 4 and 5 because relevance is unestablished. No new claim of official authority or controlling deadline is added. This tests the rebuild's conservative fallback; it does not establish that the attachment is actually authoritative. |
| H mixed thread, separate statements | Real deadline S002 stays in Section 6, required pricing sheet S003 in Section 5; clearly personal S004/S005 stay only in Section 12. All share the same neutral email-thread anchor. |
| I mixed single statement, deadline | S002 contains an actual proposal deadline and a personal event in one indivisible statement. Keep the whole exact statement in Section 6. Separately record whether personal content consequently appears in an operational section. Do not grade unavoidable personal inclusion as a repairable model error under the unchanged whole-statement contract. Quarantining S002 entirely is a failure to preserve the real deadline. |
| J misleading personal filename | S002 explicitly states a procurement clarification extending the proposal deadline despite the personal-notes.txt filename. It stays in Sections 6 and 11. S003's unmistakable personal event stays only in Section 12. |
| K misleading unrelated anchor | S002 explicitly states an official proposal deadline, while its anchor contains unrelated. Its substantive procurement content must keep it in Section 6; an isolated anchor keyword is insufficient grounds to quarantine it. |
| L procurement social event | A mandatory bidder site visit with a lunch is procurement content, not personal noise. S002 stays in Sections 4 and 6; S003's required attendance confirmation stays in Sections 4 and 5. |
| M mixed single statement, required form | S002 combines a required proposal attachment with personal cupcakes in one indivisible statement. Keep the entire statement in Sections 4 and 5. Record unavoidable operational personal-content inclusion separately, as for I. |

## Deterministic validator stress tests

N1: Build an evaluator card from K that wrongly puts real deadline S002 only in Section 12. Both validators should flag S002 as missing from Section 6. This checks whether an unrelated keyword in an anchor can silence a genuine deadline warning. Retain failure as a regression if only the rebuild suppresses it.

N2: Build a correctly contained card from F. Neither validator should emit Section 6 REVIEW for personal S002/S003. Any warning is an unresolved limitation, even if both validators tie. Evaluator-built cards are never labeled model outputs.

## Reporting

Publish every subcheck per repeat. A fixture trial is pass when all its core checks pass; partial when some pass; fail when none pass. Compare paired repeats, not aggregate questions with the original first pass. Report improved/tied/regressed/invalid pairs, unstable repeats, tool-check regressions and the single-statement contract tension separately. Do not turn host variation or 2 repeats into a reliability estimate. Do not change rebuild to improve these scores; any later repair requires a new frozen stage and preserved stage-two evidence.
