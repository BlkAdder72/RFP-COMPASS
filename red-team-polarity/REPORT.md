# Repaired-package red team — 2026-10-25

**Recommendation: hold publication.** The sealed candidate at `21dd85b40edf835870689c9f4a0b67ddc10de81a` still has unsafe warning suppression and false personal-content warnings. Seven finding families account for ten failed new controls. Six controls regress against the immediately preceding validator `06e6a13`; four fail in both candidates. The rebuilt model routed the selected new cases correctly, so these warning defects must not be described as observed model-routing failures.

This review changes no candidate code, frozen questions, earlier report, submission draft or sealed artifact. New evidence lives only in `red-team-polarity/`. The sealed ZIP therefore does **not** contain this review; it remains the preserved pre-review delivery. Do not submit it as a package containing these latest findings.

## Findings

### F1 — High: exclusion from a different program suppresses a compulsory date

After `Companies must attend all events, including the subsection titled Private events:`, the source says `The subsection titled Private events is not part of our office-hours program and remains compulsory for all companies.` A `Private events:` heading then precedes a dated farewell dinner. The current validator suppresses the missing-Section-6 hint for that compulsory dinner. The original and preceding validator retain it. A second frozen case changes the relation to `not included in our daytime schedule` while keeping attendance compulsory; it fails the same way.

Cause: `referenced_heading()` constrains some `excluded`/`unrelated` predicates to scope objects, but its `not included|not part of` branch accepts any following object. Exclusion from an office-hours program is mistaken for exclusion from the participation requirement. This is a new regression in both controls. Evidence: `controls/exclusion-other-program/`, `controls/not-included-other-schedule/`. Fresh model fixture A correctly puts both dates in Section 6; the omission is deliberately introduced only in the evaluator cards.

### F2 — High: a genuine deadline can borrow personal evidence in one unsplit clause

`My birthday dinner is September 7, 2027 at 7 PM, with the official participation credential to reach the office by September 8, 2027 at 2 PM.`

If this whole statement appears only in Section 12, the current and preceding validators suppress the missing-date hint; the original retains it. `with ... to reach` does not match the clause splitter or the protected offer/payment/duty vocabulary. The first personal activity therefore exempts the whole mixed statement. The correct behavior is to preserve the whole quotation while retaining its genuine credential deadline in operational sections. This is an existing rebuild defect relative to the original, not a newly introduced polarity-repair regression. Evidence: `controls/mixed-credential-deadline/`. Both fresh models correctly routed the statement to Sections 4, 5 and 6, so no model omission was observed in this trial.

### F3 — Medium: explicitly optional/no-condition events seed compulsory context

Within an explicit `Private correspondence:` block, either `Attendance at these events is optional.` or `There is no attendance condition for these events.` makes a later personal date receive a false Section 6 warning. Both controls passed under the preceding validator and fail now. The unknown-event fallback creates protected scope without recognizing these negative/optional meanings. Evidence: `controls/explicit-optional-attendance/`, `controls/no-attendance-condition/`. On the exact raw rebuilt B card, S006 is newly warned by the current validator and was filtered by the preceding validator.

### F4 — Medium: ordinary private coordination creates false warnings

`My birthday dinner is September 9, 2027 at 7 PM and my share is twenty dollars.` and `My graduation ceremony and birthday dinner are September 10, 2027 at 7 PM.` each receive a false date warning. Both passed under the preceding validator. After splitting on `and`, the share helper accepts dollar figures but not this worded private share; the activity-fragment helper matches `birthday` but cannot consume the remaining `dinner`. Unknown fragments are then treated as procurement evidence. Evidence: `controls/private-worded-share/`, `controls/joint-private-activities/`. The known `$20` share guard still passes; that narrow success does not cover these variants.

### F5 — Medium: contracted negation is treated as affirmative dependency

`Participation doesn’t depend on attendance at our family reunion.` inside private correspondence contaminates the following birthday date with a false warning. The negation helper recognizes `not`, `never` and `no longer`, but not `doesn’t`. This fails in original, preceding and current validators. Evidence: `controls/contracted-negation/`. The explicit `does not depend` and affirmative `not only depends` guards pass in the current candidate. They do not close the contracted-negation gap.

### F6 — Medium: a relative-clause exclusion fails to release private scope

`All companies must attend these events; the subsection titled Private correspondence, which is excluded from these activities, is unrelated personal correspondence.` explicitly excludes that named subsection. The later private graduation date still receives a false warning. The heading-relation matcher expects the exclusion predicate immediately after the label, with a limited optional copula; `, which is` prevents recognition. This fails in all three validators. Evidence: `controls/relative-clause-exclusion/`. The direct `is excluded from these activities` guard passes under the current candidate.

### F7 — Medium: a parenthetical private heading is misread as event scope

`Private calendar (unrelated personal correspondence):` followed by a private christening date produces a false warning. The heading grammar supports dash/colon annotations but not this unambiguous parenthetical annotation, allowing the generic calendar/event fallback to establish protected scope. This fails in all three validators. Evidence: `controls/parenthetical-private-heading/`.

## Frozen tests and actual results

Cases, 24 controls and source-hash-bound selected placement expectations were committed in `efb167b` before execution. The complete original A/B/C baseline was committed in `4569421` before any rebuilt trial. Original and rebuild each ran the same three fixtures once, in the same order, using unchanged `tools/run_arm.py`, `gpt-6-astra`, medium reasoning and the same six-file selection. Every reply used a fresh ephemeral session. No tools, retries, corrections, expected answers in prompts or best-of selection. Six canonical requests and six complete tool-free raw turns passed audit. The middle validator is a tool comparator only, not a third model arm. Source hashes and selected expectations are in `expectations.json`.

These synthetic probes were informed by previous implementation and findings. They are newly frozen targeted cases, not an independent population holdout. Host system instructions remain uncontrolled; UTF-8 inline named files through Codex are not native Claude attachments. The setup-only file-move error is disclosed in `SETUP_NOTE.md`; no model or validator experiment was retried.

| New control group | Original | Preceding 06e6a13 | Current 21dd85b |
|---|---:|---:|---:|
| Warning controls | 7/17 | 11/17 | 7/17 |
| Exact/altered citation controls | 7/7 | 7/7 | 7/7 |
| Total | 14/24 | 18/24 | 14/24 |

Against the preceding validator: six regressions, two improvements and sixteen ties. The improvements are the direct exclusion and explicit uncontracted negative-dependency guards. Against the judged original: three regressions, three improvements and eighteen ties. Equal aggregate totals do not mean equal behavior. `control-results.json` preserves every verdict and raw command/stdout/stderr/exit code is under `controls/`. Warning controls use structurally valid, fully quoted all-Section-12 evaluator cards: official dates are intentionally misplaced; personal dates are correctly contained. An exit code of zero is not a warning-accuracy or semantic pass.

| Fresh model fixture | Original | Rebuild |
|---|---|---|
| A: exclusions and mixed deadlines | Exact copy and selected routing pass | Exact copy and selected routing pass |
| B: negation and private content | Exact copy passes; private content leaks operationally | Exact copy and all selected routing pass; six false date hints |
| C: opaque citation variants | Exact copy and selected routing pass | Exact copy and selected routing pass |

Combined fixture checks pass 2/3 in each arm, for different reasons. The original's lack of personal warnings on its own B card is not a success: it already leaked those dates into Section 6. The rebuilt B card correctly contains S001–S006 and S008–S013 only in Section 12. The current validator nevertheless flags S003, S006, S009, S010, S011 and S013. Replaying the **same** rebuilt card under all validators produces six false IDs in original, five in preceding and six in current. This directly establishes the new S006 warning regression without confusing it with model variability. The isolated controls reveal the additional coordination regressions that inherited scope masks in combined B. See `model-results.json`, `model-audit.json` and `same-card-warning-replay.json`.

Citation probes cover U+200A hair space, U+061C Arabic letter mark, U+2066/U+2069 directional isolates, literal `&#32;`, U+2010 hyphen and U+FF1B fullwidth semicolon in grammar-valid opaque anchors. Both models preserved all six anchors exactly. Every validator accepted the exact card and rejected all six deliberately altered cards, including deletion of one directional isolate. No new citation failure was observed. This finite result does not establish correctness for arbitrary Unicode, malformed anchors or OCR.

## Earlier evidence and competition compliance

All 120 controls from `polarity-repair/control-definitions-release.json` pass a fresh read-only current-validator replay (`prior-control-replay.json`). The new ten failures expand coverage; they do not retroactively turn those earlier recorded passes into failures. Together this is 134/144 current-validator controls, not 144/144. No old failed evidence was replaced.

The latest recorded full-length 221-statement RFP was replayed read-only, without new full-length model calls. The rebuild still passes exact validation, every selected required placement and all seven private-only-Section-12 checks. The original retains its recorded three anchor errors, six private leaks and four selected routing omissions. This is a replay of the existing trial, not a fresh estimate of model reliability. See `full-recheck.json` and preserved `polarity-repair` evidence. Root Q1–Q8 were not rerun as new model trials during this review; their frozen text and all prior results remain intact.

Preservation verification passes for all 27,050 previously tracked files and all 47 sealed artifact files; questions remain byte-identical to `bfdd812`. Twenty-eight committed frozen/baseline files were checked against their Git blobs. The candidate, judged original, complete history, old reports and submission draft remain unchanged. `preservation-verification.json` and `frozen-and-baseline-verification.json` provide the receipt.

The supplied competition spec requires the judged original, verbatim feedback, questions derived from both fixes and the tier improvement, original-first committed runs, and an honest account of ties/regressions. The historical sequence and required layout are preserved. The remaining warning defects directly threaten feedback Fix 1/Q8; polished quotation or fresh semantic wins cannot substitute for closing them. Fresh-clone archive/bundle and offline compliance checks **passed**: all 27,050 ZIP source files match the sealed target, the complete-history bundle verifies and clones at the correct commit, pristine index bytes match, both runner preflights pass, and five historical audits plus the current repair audit pass without model calls. Results are recorded in `delivery-summary.json` and `delivery-checks.json`. Offline compliance success verifies the recorded artifacts and history; it does not mean the newly discovered behavioral defects are absent.

## What could still cost the win

1. **Direct feedback closure:** false hints remain on correctly quarantined personal content, while some real missed dates become silent. F1 and F2 are the highest-priority repair boundaries; F3–F7 also remain open. All failed controls must remain in the next comparison rather than merely adding their words to a success list.
2. **Overstated readiness:** the earlier report correctly limits its claims to recorded cases, but a new submission must surface this review and updated evidence. The unchanged sealed package lacks this new report. Do not describe its 120/120 result as universal closure or submit the pre-review ZIP as the final repaired candidate.
3. **Generalization and causal attribution:** six knowledge files were unchanged by the latest warning repair. Fresh model routing/copying wins do not establish that warning-code changes caused them. Targeted tests, selected routing matrices, model variation and lack of fresh native-Claude acceptance remain material limits.
4. **Judge effort:** the sealed source has 27,050 files and a roughly 53 MB ZIP, with many historical stages. A short current evidence map and one clearly identified final candidate matter; preserving evidence must not require a judge to infer which report controls.
5. **Submission prerequisites:** Premium/VIP eligibility and the final public repository URL remain unverified. The three-sentence draft remains unposted with its URL placeholder. No publication or external message was authorized or performed.

This is a review, not a repair. Keep publication on hold until the open findings are addressed, both arms are compared fairly, and the report and final delivery explicitly include the outcomes.
