# Final warning repair and full-length comparison — 2026-10-23

Publication remains paused. **The warning defects are repaired, but the fresh full-length rebuild has an open structural regression: two S072 citations omit a word from the source anchor. Its raw card correctly fails validation.** All 221 statement texts are exact and all personal noise stays only in Section 12; this is not a clean full-length pass. No raw output has been repaired or retried.

The cross-anchor warning regression is repaired: requirement context follows source order across lines, paragraphs, pages and documents. Unknown transitions stay protected; an explicit personal-calendar/correspondence heading can end the scope. Anchors never authorize exclusion. Requirements and clinical-service wording veto filtering. Retirement/farewell meals, private medical appointments and explicit meal contributions now clear their false hints when contained only in Section 12.

## Fresh frozen-question comparison

Same A–E, same order, same six arm-specific files, same exact wrapper, gpt-6-astra/medium. One fresh session per fixture per arm: ten sessions, no retries or tools. Original baseline committed before the validator edit. The translation knowledge itself did not change in this stage. Q7 and Q8 are deterministic checks, not extra model conversations. Q8 uses the default invocation without a sidecar. No frozen questions or expected answers changed.

| Question | Original | Rebuild | Comparison |
|---|---|---|---|
| Q1 | fail | pass | improved |
| Q2 | pass | pass | tied |
| Q3 | partial | pass | improved |
| Q4 | pass | pass | tied |
| Q5 | pass | pass | tied |
| Q6 | partial | pass | improved |
| Q7 | fail | pass | improved |
| Q8 | partial | pass | improved |

Five improved question results, three ties, no scored regressions in this fresh comparison. These are correlated, known fixtures; no statistical generalization or Claude acceptance claim.

## Warning regression and control evidence

The 26 new evaluator-card controls compare identical source/card inputs under both validators. Before repair: original 18/26, prior rebuild 14/26. First repair: rebuild 25/26, with a missed `Mandatory bidder personal calendar:` heading. That failed run and its exact candidate code remain under `hardening/after/` and `hardening/candidates/initial.py`. Final repair: rebuild 26/26; original remains 18/26. The observed eight improvements over original have no final control regressions. The cross-anchor failures remain preserved in `red-team-final/` and `hardening/before/`; they were checker failures on evaluator-built cards, not invented model misroutes.

Six additional adversarial probes were then frozen and run. The intermediate repair passed only 1/6: required-charge, meal, requirements and clinical headings could still lose their warnings. These five regressions are preserved under `hardening/guards-before/` with the exact candidate in `candidates/second.py`. The final repair protects explicit requirement headings and clinical appointment context as well as event headers: 6/6 additional probes and all 26 earlier controls pass (32/32 total), versus original 23/32, with no final control regressions. This additional checker-only repair occurred during the full-length model trial; the model knowledge and prompts remained unchanged. Raw model responses were not rerun or selected in response to these tool checks.

The first full-length validation revealed another warning interaction: the two unrelated S072 anchor failures disabled all personal filtering. First-pass validation, reports and hashes remain under `hardening/full-first-pass/`. Final filtering trusts each exact, singly cited personal row separately; malformed shape, bad personal anchors/quotes, duplicate personal citations and missing headings cannot authorize filtering. Eight additional paired trust controls pass 8/8 for rebuild, versus 5/8 original. The full raw card still fails on both S072 anchors; those genuine errors are not suppressed or repaired.

All 51 prior default/structural/duplicate controls meet current declared expectations under the final checker; all 92 archived-card/reference structural replays pass. Two prior expectations deliberately change: “Please bring $30 for lunch” contained only in Section 12 clears its money hint, and an unrelated bad deadline quote no longer creates a hint on valid personal S004 (the bad card still fails). Old expectations remain untouched in revision evidence. Genuine fees, contacts, mixed requirements and operational duplicates retain warnings. A plain “our lunch,” an unknown meeting, and an uncertain transition remain conservative warnings. Intermediate and final replays occupy separate directories; Q8-final and validation-final logs preserve the earlier Q8-default and validation logs.

## Full-length noisy RFP

The fixture preserves every byte of the existing 214-statement TBRPC packet before appending seven synthetic calendar statements, for 221 statements. Original PDF and its historical trace evidence remain unchanged. The seven new statements trace to retained `hardening/calendar.txt`; they are not part of that PDF. This run tests a complete known RFP with synthetic noise, not a new real-world holdout or a new end-to-end PDF conversion.

Fresh persistent session per arm; original first, then rebuild. Same wrapper/model/settings; exact `continue` in the returned session ID whenever the model emits the required marker. Every request, raw event, stderr, command, model part and combined unedited card is retained. The final validator receives the actual parts in order. No transcript repairs, output compression, best-of selection or tool use.

| Full-length check | Original | Rebuild |
|---|---|---|
| exact_shape_quotes_coverage | True | False |
| exact_statement_text | True | True |
| exact_anchors | True | False |
| all_221_ids | True | True |
| noise_only12 | False | True |
| genuine_routing | True | True |
| no_personal_review_hints | True | True |
| max150_bullets_per_reply | True | True |
| complete | True | True |

**Observed structural regression:** original passes exact anchors; rebuild cites S072 in Sections 4 and 5 as `TBRPC Auditing RFP p. 7 §5.II.b`, while the packet anchor is `TBRPC Auditing RFP p. 7 §5.II.b bullet`. Every statement text remains exact. Original leaks six personal statements into operational sections; rebuild contains all seven only in Section 12. Final checker emits no personal false hints and still rejects both bad anchors. Full comparison is mixed: a routing improvement and a structural regression, with no overall-win claim.

Original: 4 replies, [93, 109, 95, 148] quoted bullets per reply, 221 distinct cited IDs. Personal REVIEW lines: 0. Detailed routing and every failed check appear in `hardening/full-length-results-final.json`; first-pass results remain in `hardening/full-length-results.json`.

Rebuild: 4 replies, [96, 69, 130, 141] quoted bullets per reply, 221 distinct cited IDs. Personal REVIEW lines: 0. Detailed routing and every failed check appear in `hardening/full-length-results-final.json`; first-pass results remain in `hardening/full-length-results.json`.

A zero REVIEW count alone does not prove containment: the original can avoid a missing-section warning by putting the personal statement into that operational section. The separate noise-only-Section-12 check is the decisive routing check.

## Deliberately unchanged

The six translation knowledge files remain byte-identical to the preceding repaired package. The PDF packet builder, trace tool, exact whole-statement quoting contract, twelve-section layout, source-coverage checks and injection resistance were retained. This stage changes the default warning fallback and adds evidence; it does not claim to improve the already-praised PDF conversion or silently rewrite the judged original.

## What can still cost the win

- This is a bounded English hint filter. It does not prove semantic routing. A requirement scope can conservatively extend farther than necessary; unrecognized personal activities or headings can still warn. A misleading explicit personal heading can also misrepresent source context. Contextual inference remains reviewable rather than certified.
- Mixed relevant/personal content within one source statement is indivisible under exact-quote rules. Relevant placements can carry personal text in that whole quote; no claim that all mixed clauses disappear.
- The complete RFP and deterministic cases are known, synthetic-noise tests. One new paired run does not establish broad reliability, statistical superiority, latency or cost advantage. Earlier Claude results are historical, not fresh acceptance of this repair.
- Evidence is extensive. Start with this report and the portable verifier; older stages deliberately retain failures and superseded reports. Historical pass counts are not a claim the superseded candidate had no bugs.
- Premium/VIP eligibility remains unverified. A public submission link and the platform comment are pending explicit publication authorization. The brief's deadline remains Wednesday October 28, 11:59 PM EST as written.

## Evidence and provenance

- `hardening/protocol.md`, `preservation.json`, frozen test definitions and full-length expectations precede the repair/trials in Git.
- `run-original/hardening/`, `run-rebuild/hardening/`: fresh A–E exact requests and raw model evidence; default Q8 command/output evidence.
- `run-original/hardening-full/`, `run-rebuild/hardening-full/`: complete session continuation evidence.
- `hardening/before/`, `after/`, `after-v2/`, `prior-controls/`, `replays/`: model-free tool checks; never counted as model translations.
- `hardening/verification.json`, `packaging/final-compliance.json`: offline preservation, raw-event, sequence and current validation audits.

Original judged files, feedback, questions, all previous failures and Git history are retained. No push, public release, submission comment or external message has been sent.

[Preserved preceding stage report](hardening/history/results.md). All earlier reports remain in their stage directories and Git history.
