# Final repair and paired evaluation — 2026-10-23

Publication: **NOT PERFORMED**. This candidate closes all three reviewed findings on their frozen cases. The new rebuilt full-length run passes every prospective check, including S076 in Sections 4 and 5 and character-exact citations throughout. This is observed test closure, not a claim of universal semantic or copying correctness.

## What changed and why

1. Required response information is explicitly a Section 5 item even without a named form or report. The rules require a section-by-section scan of every ID, retain enclosing required-submittal context, and prohibit dropping an item merely because it already appears in Section 4. The distinction from suggestions and post-award deliverables remains. No S076 identifier, TBRPC answer or source-specific routing matrix was added to model knowledge for this repair.
2. The bounded personal-activity filter now recognizes graduation celebrations, parties and ceremonies with a personal owner. It still requires exact trusted text and Section 12-only placement, and retains procurement, clinical and cross-anchor required-event vetoes. Labels alone do not authorize suppression. Unknown celebrations retain their warning.
3. The rebuilt validator rejects straight quotation delimiters and every altered quotation character, including invisible characters and Unicode normalization changes. Source trailing spaces are preserved in comparison. The old visible-text fallback and tolerant-success notes are removed. Exact anchor checks, coverage, ordering, continuation and shape checks remain. Original is untouched. This is stricter validation, not an exception to make new model outputs pass.

## Preservation and sequence

`final-repair/preservation.json` binds all pre-stage tracked files and previous delivery hashes. Mutable files were copied byte-for-byte to `final-repair/history/` before edits; all six baseline knowledge files were separately frozen. Frozen root questions remain byte-identical to their pre-rebuild commit. All previous failures, raw transcripts, red-team findings, scores and Git history remain unchanged. The original was run first on A–E, then U/V/W, then the full 221-statement input; its raw baseline was committed before candidate edits. Rebuild used the same inputs and order after its candidate commit.

The prospective protocol and expected matrices were committed before trials. The initial asynchronous baseline-commit wait correction is disclosed in `final-repair/AUDIT_NOTES.md`; it involved no model retry or output replacement. Runners, model (gpt-6-astra), medium reasoning, wrappers, no-tool rule and continuation policy are unchanged. No retries, best-of selection or output corrections were used. Knowledge differs only by the intended repair. Q7/Q8 remain deterministic file/default-tool checks, with no sidecar required. All requests, raw model events, stderr and continuation prompts are under `run-ARM/final-repair-v2-{core,new,full}/`.

## First attempt: failed and preserved

The initial final-repair candidate passed Q1–Q8, all three new cases, the S076 placement check and personal containment, but changed one S100 Section 6 anchor from its own single-page citation to the next statement’s page range. The unchanged strict validator rejected it. Original copied all anchors exactly. This was a real copying regression; it is not counted as a pass or replaced by the later run.

Exact first-attempt knowledge, scores, scorers and hashes remain in `final-repair/attempt-1/` and `final-repair/attempt-1-knowledge/`; all raw runs remain at `run-ARM/final-repair-*`. Before the second knowledge change, a new protocol was frozen and a new original baseline was committed. The second version adds a general p.-versus-pp. safeguard and four-row synthetic near-collision example; it adds no S100 or actual RFP answer. Both arms then rerun all cases and the full input in the same order. The validator and expectations are unchanged between attempts.

The first attempt also placed V's bare response-content heading in Sections 4 and 5. That extra placement was outside the frozen matrix and remains disclosed as an unscored semantic risk. The latest positions appear below; their change is an observation, not a prospectively scored heading repair.

## Frozen questions

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

Totals: {"improved": 5, "tied": 3, "regressed": 0}. Regressed core subchecks: {}. These totals apply only to frozen Q1–Q8, not every possible routing assignment.

## New known regression cases

| Fixture | Original passes all checks | Rebuild passes all checks |
|---|---|---|
| U-unseen-citations | False | True |
| V-required-response-info | False | True |
| W-personal-graduation | False | True |

U retains the previously unseen anchor forms unchanged; it is now a known regression fixture. V tests mandatory response information without a named attachment. W tests the known graduation false-warning case. Exact quotations/anchors, required routing and personal-only placement are scored separately. See `final-repair/attempt-2/new-results.json`; no new independent holdout claim is made.

The matrix for V adjudicates the substantive response items, not its bare heading. Rebuild places `Required response contents:` in [12], versus original [4]. Heading placement remains an unscored semantic risk; the fixture-level pass does not certify every extra placement. A missing W warning alone is not personal containment: its actual positions are rebuild [12] versus original [6]. The independent correct-card control is the evidence that the graduation false warning itself is repaired.

## Full-length noisy RFP

The source remains the same 214 real TBRPC statements plus seven explicitly synthetic personal-calendar statements. No source word, anchor or order was changed. The prospective matrix keeps all previous selected checks and adds S076 in Sections 4 and 5. Every quote and anchor is compared independently, not only S072/S076.

| Check | Original | Rebuild |
|---|---|---|
| exact_shape_quotes_coverage | False | True |
| exact_statement_text | True | True |
| exact_anchors | False | True |
| all_221_ids | True | True |
| noise_only12 | False | True |
| genuine_routing | False | True |
| no_personal_review_hints | True | True |
| max150_bullets_per_reply | True | True |
| complete | True | True |

Original S076 placements: [4, 5]; rebuild: [4, 5]. Original bullets per reply: [126, 127, 139]; rebuild: [113, 88, 142, 74]. Copy mismatches: original 1 anchors/0 quotations, rebuild 0 anchors/0 quotations. All other selected placements and every negative result remain in `final-repair/attempt-2/full-length-results.json`.

The prior S076 regression is still visible in the unchanged `red-team-citations/semantic-review.json` and previous raw full-length cards. The new success does not rewrite that failure. The original's varying results across attempts remain evidence of run variability, rather than something to discard.

Exact citation copying differs in this pair; the recorded mismatches above remain failures. A single pair does not establish a copying advantage. S076's actual placements are shown above; improvement, tie or failure follows those observations, not the previous version's result. A separate identical strict-fidelity gate passes all 16 core/new cards across both arms (`identical-strict-fidelity-v2.json`), so original is not receiving a scoring advantage from its more permissive native quotation validator.

The same strict validator also evaluates both arms' actual full-length reply parts in `identical-full-fidelity-v2.json`; an original failure remains a failure. The six follow-up controls accept the exact extended example, reject a swapped page range, and continue rejecting the preserved S100 failure in both versions. Validator code is byte-identical across the two final-repair attempts.

## Validation and regression controls

137 evaluator-built validator checks spanning both arms were executed, with zero rebuilt expectation failures. They include exact Unicode acceptance, altered invisible/NBSP/normalization/trailing-space rejection, straight-delimiter rejection, anchor corruption, missing coverage, the preserved S072 failure, graduation false-warning closure, mixed real requirements, clinical scope, unknown events and cross-anchor context. Original contract gaps are recorded explicitly in `control-results.json`, not scored away.

Historical/reference replay: 92/92 cards pass current structural validation under their recorded validator arms. Any rejected historical card remains unchanged; its raw stdout, stderr, hashes and exit code are retained in `final-repair/historical-replays/`. Controls are evaluator-built, not model responses.

Historical audits run against the sealed historical commit in a disposable local clone, preserving their original assertions. The current audit independently checks preservation, exact new prompts and knowledge hashes, unedited raw responses, no tools, same-session continuations, and the new strict validator. No historical test expectation is weakened to accommodate this repair.

## Deliberately unchanged and remaining limits

- The judged original, frozen eight questions, raw failed outputs, source packet, prior routing scores, model/provider and evaluation runners remain unchanged. Identity and input schema were not altered. The second attempt extends the general synthetic anchor example with single-page/page-range near-collisions; that example was chosen after inspecting the new failure.
- The full-input semantic matrix is still selected coverage, not a complete expert adjudication of all 221 statements in every section. Mechanical PASS cannot prove section placement. Unknown personal activities may retain conservative warnings.
- This repair had two versioned attempts. The first failed full-length citation validation; the second has one fresh pair per fixture and one fresh full-length pair after that failure. There is no statistical or universal copying guarantee, independent holdout claim, fresh Claude/Sonnet/Opus acceptance or cost/latency advantage claim.
- Reply-budget compliance is checked by the full-run scorer; a combined card does not preserve all reply boundaries for the standalone validator. No blanket claim that the validator enforces every output-contract rule is made.
- Premium/VIP eligibility is unverified. Public URL and submission comment remain unposted. The competition deadline remains Wednesday October 28, 11:59 PM EST as written.

## Local delivery

The updated source archive and complete-history Git bundle are sealed under `dist/final-repair/`, with SHA256SUMS, release commit and fresh-clone verification alongside them. Earlier delivery files remain untouched. The source ZIP excludes `.git` as usual; use the bundle for the complete sequence/history. The report and new evidence are included in the new release. No publication is authorized or performed.
