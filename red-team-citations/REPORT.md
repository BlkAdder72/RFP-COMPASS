# Competition-spec red team — 2026-10-23

**Verdict: hold for another repair.** The feedback-driven rebuild remains stronger on personal-thread containment, and the new citation variants did not reproduce S072. However, a genuine routing regression and a remaining false warning weaken the submission. Mechanical PASS is broader than the written exact-output contract. No publication, candidate edit, root-score rewrite or delivery replacement was performed.

Reviewed sealed candidate: `157d8fe22339ce5385b8291728c48f7141840206`. This audit is separate from that sealed package. Its new files are not inside the existing ZIP/bundle. See `preservation.json` and `delivery-review.json` for preservation and fresh-clone checks.

## Findings that could cost the win

### 1. High: the current full-length rebuild loses a required-response placement that original gets right

S076 says: “ii. The firm shall also provide information on the results of any federal or state desk reviews or field reviews of its audits during the past three (3) years.” Its source context is Submittal Content, Format, and Instructions, §5.II.c.ii. This is required information with the response, covered by the written Section 5 trigger (“provided with the response”), as well as submission mechanics in Section 4.

Original includes S076 in Sections 4 and 5; rebuild includes it only in Section 4. The rebuilt card still covers the ID and copies it exactly, so mechanical validation and the six selected genuine-routing checks miss this defect. This is an observed semantic regression in the latest existing paired full-length run, not a new model trial or a copying regression. `semantic-review.json` binds the source and raw cards by SHA-256 and records the actual lines: original 137/173, rebuild 99. The expectation was selected retrospectively and is explicitly separate from the old frozen scores.

This matters to judges who try a required-document lookup rather than merely checking that every sentence occurs somewhere. Before release, repair the behavior generally and fairly rerun both arms; retain the current failed observation. Expand prospective routing checks without putting an answer key into model knowledge. The old “5 improved / 3 tied / 0 regressed” table describes its frozen eight questions; it does not describe this wider semantic review.

### 2. Medium: clearly unrelated personal material can still produce the exact false Section 6 warning named in feedback

New evaluator-built source: `My niece’s graduation celebration is November 19, 2026 at 7 PM.`, explicitly anchored as unrelated personal correspondence attached in error. A correct card quotes it only in Section 12. Both validators accept the card but print a Section 6 REVIEW warning. Witness: `controls/unrelated-graduation/` and `control-results.json`.

The rebuilt filter recognizes a finite set of activities; graduation falls outside it. This is a remaining generalization failure, not evidence that the original frozen Q8 cases regressed. The original feedback cards, cross-anchor protections and real-deadline warning still pass the fresh offline audit. Any repair must retain those protections; blindly suppressing everything labeled personal would recreate the earlier genuine-deadline problem.

### 3. Medium: validator acceptance does not enforce all of the advertised exact-output contract

Both unchanged validators return exit 0 and PASS when a quotation gains a zero-width character, or a source NBSP becomes an ordinary space. They disclose a NOTE but still describe entire-statement quotations as passing. Both also accept straight delimiters with a NOTE, although the output contract explicitly requires curly quotation delimiters. See `controls/zero-width-inserted/`, `controls/nbsp-normalized/` and `controls/straight-delimiters/`; implementation in `rebuild/tools/validate_packet.py` at the visible-text fallback and straight-quote notes.

These are pre-existing acceptance tolerances in both versions, not newly introduced S072 regressions. Anchors remain strictly compared: the exact bracketed-anchor control passes, the changed-anchor control fails both. The new real model outputs had zero character mismatches under an independent strict comparison, so these controls do not invalidate those observed successes. They do limit what a validator PASS alone proves. Strict mode or an explicit contract/acceptance reconciliation is needed before making a general character-exact validation claim.

Additional low-priority coverage limit: a 151-bullet single-file card is accepted. The separate full-run scorer enforces the 150-bullet reply budget; this validator does not. Combined-file validation cannot generally reconstruct reply boundaries, and the long-card prose also permits stopping near a section boundary. Treat this as a boundary/enforcement ambiguity, not a newly demonstrated model regression or competition disqualification.

## Frozen unseen citation experiment

Protocol/source/expectations were committed at `8dd4781` before either model call. Validator-control definitions were committed at `2dc7cf5` before execution. Original ran first, then rebuild, with the same unchanged `tools/run_arm.py`: gpt-6-astra, medium reasoning, fresh ephemeral session, identical wrapper and fixture, no tools, retries, best-of selection or output correction. Only the six designated contract files and source packet were supplied; expectations were not supplied. All requests, commands, model events, stderr, exit codes, unedited cards and audits remain under `run-original/` and `run-rebuild/` here.

The ten-statement synthetic fixture contains eight repeated mandatory-form statements with unseen near-collision anchors: page ranges, nested clauses, table qualifiers, embedded square brackets, composed/decomposed accents, NBSP, Greek characters, distinct bullet symbols and footnotes. It also has a genuine procurement deadline and an explicitly unrelated personal dinner.

| Check | Original | Rebuild |
|---|---|---|
| Every quotation and complete anchor character-exact | Pass | Pass |
| All eight mandatory statements in Sections 4 and 5 | Pass | Pass |
| Genuine deadline in Section 6 | Pass | Pass |
| Personal dinner only in Section 12 | Fail: Sections 6 and 8 | Pass |
| Mechanical validator | Pass | Pass |
| All prospectively frozen checks | Fail | Pass |

Citation fidelity ties; personal containment improves. No new citation regression was observed. This is one short synthetic pair, not a long-input unseen-RFP replication, fresh Claude acceptance, statistical result or general copying guarantee. Anchors were unseen; the repeated-statement pattern is deliberately related to the repair's worked example. Do not call the whole task distribution independent.

## Competition compliance and remaining judging risks

The fresh sealed-bundle clone passed the offline repository audit: original pin/134 original files, verbatim feedback hash, frozen eight questions, required Git sequence, required root layout, historical failures and raw transcripts remain verifiable. The audit checks 116 preserved model replies from earlier stages. The new pair contributes two additional raw replies in this audit directory. Current Q8 defaults and the prior warning/cross-anchor controls remain covered by that audit. A separate pristine clone verifies sealed working-tree/index bytes and runner preflights before any audit rewrites derived metadata. An initially misordered post-audit byte check failed on regenerated verification metadata; that sequencing error is retained, not hidden, in `post-audit-index-failure.txt`.

What could still cost the win, beyond the confirmed findings:

- **Judges can find semantic omissions beyond the selected matrix.** Exact quotes, all-ID coverage and S072 success do not prove every section assignment. This review found one such regression without changing the input.
- **Known-input tuning and model variability.** Multiple failed attempts were honestly preserved; the final long-input success is one pair after inspecting failures. Original also recovered citation accuracy without an original change. The new short pair does not establish a copying advantage or long-input robustness.
- **Platform transfer remains untested.** The authorized automated connection is Codex/OpenAI. No fresh Sonnet/Opus/Claude Project acceptance run is claimed.
- **Evidence volume can obscure the feedback story.** Thousands of retained files support integrity but make navigation expensive. A reviewer should be able to reach each feedback line, question and raw witness immediately. The concise root map helps; it does not replace a complete routing check.
- **Entry gates remain pending.** Premium/VIP eligibility is unverified. A public repository URL and submission comment are intentionally not posted. The brief says Wednesday October 28, 11:59 PM EST; this review preserves that wording. These are completion gates, not permission to publish.

The three earlier repair areas remain supported on their recorded tests: Q8 runs without a sidecar; warning suppression retains genuine required-event warnings across anchors; S072 is exact in the latest full-length pair and the new anchor forms copy correctly. Their broader problem classes are not universally solved, as findings 1–3 show. The competition rewards closing the feedback gap with defensible evidence, not a claim that every output is now correct.

All existing source, evidence, questions, Git history and sealed deliveries remain unchanged. The report recommends another local repair before any release; it authorizes no publication.
