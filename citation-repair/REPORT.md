# S072 citation-copying repair — 2026-10-23

Publication remains paused. **The fresh rebuilt full-length card passes every frozen check, including exact S072 citations in Sections 4 and 5. The earlier failed card remains unchanged and still fails validation.**

## Diagnosis and change

The previous full-length rebuild dropped `bullet` from S072's anchor in Sections 4 and 5: it emitted `TBRPC Auditing RFP p. 7 §5.II.b` instead of the packet's `TBRPC Auditing RFP p. 7 §5.II.b bullet`. All statement text was exact, but these were genuine citation failures. The old raw card, both failed validations, first-pass reports, audit corrections and earlier package remain preserved.

Four general model-knowledge files changed: `rebuild/CLAUDE_PROJECT_INSTRUCTIONS.txt`, `rebuild/rules.md`, `rebuild/reference/output-schema.md` and `rebuild/examples.md`. They treat the entire source-ID/anchor pair as opaque data, retain every anchor qualifier, construct a complete bullet from its own packet row, reuse it unchanged across sections, and compare the complete citation on every continuation. A synthetic worked example shows identical disclosure-form statements with distinct anchors, one ending in the literal word `bullet`; both anchors remain exact when the statements repeat. No S072-specific answer, TBRPC citation or shortened-anchor exception was added to model knowledge. The example was chosen after inspecting this error class, so this is a targeted known-input repair, not a holdout test.

**Both validators are byte-identical to the preceding sealed package.** No normalization, automatic citation repair, changed comparison rule, hidden postprocessing or relaxed acceptance is used. The model-free controls accept exact cards and reject shortened, swapped, punctuation/Unicode/case/spacing-altered anchors, changed quotes, missing coverage and the old S072 failure: 22/22 paired checks pass. The new worked example also passes both validators, and shortening its anchor fails both (4/4 checks). These are acceptance/rejection checks, not model trials.

## First repair attempt — failed and retained

The initial general opaque-anchor instruction change alone did **not** fix the issue. In its fresh full-length pair, original and rebuild each shortened S072's anchor twice and both failed exact validation. The rebuild still contained all seven personal statements only in Section 12; the original leaked six. Its fresh core comparison was five improvements and three ties, but that does not turn its full-length failure into a pass. Raw files remain at `run-ARM/citation-repair-core/` and `run-ARM/citation-repair-full/`, exact knowledge at `citation-repair/attempt-1-knowledge/`, and scores/scorers/hashes at `citation-repair/attempt-1/`.

After preserving and committing that failed pair, `attempt-2-protocol.md` preregistered the worked-example repair and a new pair in entirely new directories. The second original core baseline was committed before editing the example, and the second repair was committed before rebuilt calls. This report presents the latest pair below and keeps the failed first attempt in view; it is not first-try success or selection among unchanged retries.

## Prospective method and preservation

`citation-repair/protocol.md`, the preservation manifest and the unchanged 221-statement input were committed before new trials and before the instruction change. All 8,000 pre-stage tracked files are accounted for, with changed files copied under `citation-repair/history/`. All six previous knowledge files for both arms are frozen there so historical requests remain reproducible. The judged original and root `questions.md` are unchanged; the original core baseline was committed before repairing instructions, and repaired instructions were committed before rebuilt model calls.

The full fixture is the same 214-statement real TBRPC packet plus the same seven synthetic personal-calendar statements in both attempts. No source wording, anchor, order or noise changed. The noise is not part of the original PDF. Expected routing adds an explicit prospective S072 check in Sections 4 and 5; root frozen questions are unchanged. Editing examples.md in the second repair is separately recorded in `additional-mutable-paths.json`; its original bytes were already frozen before any trial, and the first preservation manifest was not altered.

Fresh original and rebuild sessions use gpt-6-astra/medium and the existing unchanged request/continuation runners. Both get the same wrapper and full input, with their own six instruction files. `continue` is sent exactly in the returned session; all commands, requests, raw events, stderr, exit codes, parts and combined unedited cards are retained. No tools, retries, corrected cards, expected answers in model context or best-of selection. Independent core/full sessions may overlap; no latency comparison is made.

## Fresh Q1–Q8 comparison

Five A–E model sessions per arm, in frozen order. Q7/Q8 are file/tool checks, not additional model conversations. Q8 uses the default invocation without review sidecars.

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

Comparisons: improved=5, tied=3, regressed=0. Any regressed subchecks remain in `citation-repair/scores-final.json`.

## Fresh full-length comparison

| Check | Original | Rebuild |
|---|---|---|
| exact_shape_quotes_coverage | True | True |
| exact_statement_text | True | True |
| exact_anchors | True | True |
| all_221_ids | True | True |
| noise_only12 | False | True |
| genuine_routing | True | True |
| no_personal_review_hints | True | True |
| max150_bullets_per_reply | True | True |
| complete | True | True |

Original: 4 replies; [96, 107, 91, 143] quoted bullets per reply; 221 distinct IDs. S072 placements: [4, 5]. Anchor mismatches: 0; quote mismatches: 0; personal REVIEW lines: 0.

Rebuild: 4 replies; [110, 72, 142, 69] quoted bullets per reply; 221 distinct IDs. S072 placements: [4, 5]. Anchor mismatches: 0; quote mismatches: 0; personal REVIEW lines: 0.

Exact-anchor fidelity ties in the latest pair: both original and rebuild preserve every anchor. The original failed this check in the first new pair but passed in the second without any original changes, demonstrating run variability. A repaired rebuilt observation is not proof of a copying advantage over original or a universal copying guarantee.

S072's successful placement alone is not sufficient: exact anchors and quotes are checked on every citation in the full card. The independent validator consumes the actual reply parts in order. Personal containment is separately scored; zero REVIEW notes alone would not prove correct routing. Original and rebuilt outputs are accepted or rejected under their unchanged validators, never corrected to make the comparison pass.

## Remaining limits and deliberately unchanged work

- This is one fresh paired run on a known full-length input after inspecting a failure. It supports an observed repair, not a general copying guarantee or statistical superiority. Earlier failed trials continue to count as failures. No fresh Claude acceptance or latency/cost advantage is claimed.
- A model can still make a different copying error on another run. The exact validator remains the acceptance gate; a raw FAIL must not be submitted as a validated card. The general instruction repair is not a deterministic renderer.
- Section routing remains a semantic task. The bounded personal-hint filter can retain warnings under uncertain context; mixed relevant/personal clauses remain indivisible under whole-statement quoting rules.
- Identity, input schema, packet/PDF builder, trace tool, validator, section-routing triggers, all previous examples and all prior repair evidence were retained. A new synthetic example was added without changing the old examples or their provenance disclosures. This stage addresses copying reliability rather than claiming a new PDF conversion improvement.
- Premium/VIP eligibility remains unverified. The public submission URL and comment remain pending explicit publication authorization. The brief's deadline remains October 28, 11:59 PM EST as written.

## Evidence map

- `run-original/citation-repair-v2-core/`, `run-rebuild/citation-repair-v2-core/`: latest fresh exact A–E prompts, model responses, validation and Q8 commands/output.
- `run-original/citation-repair-v2-full/`, `run-rebuild/citation-repair-v2-full/`: latest full-length session evidence, every continuation and unedited model part.
- `citation-repair/full-length-results.json`, `scores-final.json`, `validation-results.json`: complete results including failures, not just the summary above.
- `rebuild/run-results/citation-repair-v2-full/`: byte-for-byte copy of the latest rebuild full-length evidence in the required project layout.
- `run-rebuild/hardening-full/`, `rebuild/run-results/full-length-noisy/`, `hardening/full-first-pass/`: previous S072 failure and false-warning interaction, unchanged.
- `citation-repair/history/`: previous editable documents, knowledge and audit code; `citation-repair/preservation.json` accounts for the preceding 8,000 tracked files and delivery hashes.
- `tools/verify_submission.py`: portable offline audit, including both historical knowledge and the new trials. New validation logs use `packaging/final-checks-v6/`.

No push, publication, external message or submission comment has been sent.
