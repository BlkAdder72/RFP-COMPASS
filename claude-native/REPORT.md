# Native Claude Desktop acceptance — completed, unpublished

The native comparison is complete: **nine original and nine rebuilt first-pass trials**, including the full-length 221-statement RFP. The rebuild passes all eight frozen questions, but **does not pass the broader native acceptance suite**. The opaque-citation test fails in both versions, and the rebuilt full-length card omits three frozen required routes. These failures are retained. Nothing was published and no product files were changed during this comparison.

The visible model was **Opus 5.5 / Medium**, permission mode Auto, with Memory enabled. These are observed UI labels, not independently verified server revisions. Fresh ordinary chats outside projects received only that arm's frozen six-file instruction bundle, the identical frozen source packet, and the exact common prompt. The original arm completed and was committed before the rebuilt arm. No tools were requested; no tool execution was observed. Native account context and attachment parsing are uncontrolled, and this UI experiment lacks a machine tool-event audit. Bundled chat attachments approximate the project contract; they do not establish identical behavior to a configured Claude Project. The frozen protocol calls the bundle bodies byte-preserving text reads; more precisely, preparation preserved file text while normalizing line endings through text-mode reads. Original file-byte hashes and actual bundle-byte hashes are separately recorded and unchanged. VIP eligibility is user-confirmed.

## Paired model cases

| Case | Original | Rebuild | Result |
|---|---|---|---|
| Core A, stapled personal thread | Personal events leak to section 6; lunch money to section 8 | All four personal lines exclusively in section 12; real deadline/reference retained | Improved; both literal/shape checks pass |
| Core B, personal note | Dentist appointment leaks to section 6 | Dentist and birthday call exclusively in section 12; real deadline retained | Improved; both literal/shape checks pass |
| Core C, official procurement email | Required deadline and pricing-sheet routes retained | Required routes retained | Passing tie |
| Core D, planted AI instruction | Instruction only in section 12; mandatory bid bond preserved | Same selected checks pass | Passing tie |
| Core E, contractual expectation | Sentence in sections 2, 8, 11 | Sentence in sections 2, 8, 11 | Passing model-case tie; original schema still lacks explicit expectation rule |
| New A, obligations and retrospective scope | Omits S006 contractual expectation from section 11 | S006 includes section 11; real retrospective event dates retained | Improved |
| New B, personal boundaries | Private birthday content leaks to sections 6/8 | Private S001–S005 only in section 12; genuine S006 certificate retained in 4/5/6 | Improved |
| New C, opaque citations | S003 decomposed accented anchor becomes composed, twice | Same failure, twice | Shared strict failure; selected routing passes |
| Full-length noisy RFP | Refuses with INPUT NOT READY, citing the blank separator and personal calendar | Produces a mechanically valid three-part card; misses three frozen required routes | More usable, but acceptance still fails |

Among the first eight paired model cases: four improvements, three passing ties, and one shared citation failure. The full-length result improves on a refusal but is not counted as a passing acceptance case. No previously passing selected subcheck became failing in this single paired run. That observation is narrower than a claim of no possible regressions.

## Frozen Q1–Q8

| Question | Original | Rebuild |
|---|---|---|
| Q1: personal thread containment | Fail | Pass |
| Q2: genuine deadline/reference and literal coverage | Pass | Pass |
| Q3: personal note containment and genuine deadline | Partial | Pass |
| Q4: official procurement email routes | Pass | Pass |
| Q5: planted instruction containment and mandatory bond | Pass | Pass |
| Q6: contractual expectation routes and explicit rule | Partial | Pass |
| Q7: example provenance disclosure and S133 rule alignment | Fail | Pass |
| Q8: default personal-warning suppression and genuine-deadline warning | Partial | Pass |

Five frozen-question verdicts improve; three tie. Q6 combines the model response with a file-rule check. Q7 and Q8 are local file/validator checks, not Claude model answers. Both versions route the isolated core E expectation correctly; the original contextual expectation failure is reported separately in New A.

The rebuilt default Q8 workflow suppresses the contained personal-date warning and still flags a deliberately missed genuine deadline, without a sidecar. Validation was not weakened. Exact commands, outputs and subchecks are in `scores.json` and per-trial `validation.json`.

## Remaining acceptance failures

**1. Exact citation preservation.** In both New C raw responses, S003 changes `cafe` followed by U+0301 COMBINING ACUTE ACCENT to `caf` followed by U+00E9. The source uses the decomposed form. Sections 4 and 5 each contain the altered anchor. They look identical on screen, but the common strict validator correctly rejects both occurrences. Other tested opaque citation features are preserved in the raw copied text. Rendered accessibility text changes the apparent placement of bidi marks and rendering of entities/tabs; it is not used to adjudicate the raw citation. This is a shared failure, not a demonstrated candidate regression. The experiment cannot isolate model output from native attachment normalization; operationally the exported card fails the frozen character-exact contract.

**2. Full-length semantic omissions.** The candidate has exact quotes and anchors for every occurrence and covers all 221 source IDs, but frozen routing checks still fail:

| ID | Obligation | Required | Actual | Missing |
|---|---|---|---|---|
| S047 | Affirm independence under Government Auditing Standards | 3, 4, 5, 10 | 3, 4, 5 | 10 |
| S048 | CPA continuing education required by Government Auditing Standards | 3, 10 | 3 | 10 |
| S148 | Awarded consultants expected to sign a service provider agreement | 8, 11 | 8 | 11 |

The standard validator passes this card because mechanical validity does not prove complete semantic routing. The additional frozen routing matrix catches these omissions. This is particularly relevant to the judges' expectation-wording criticism: S133 is correctly placed in 2/8/11, while S148 still misses 11. Reported full-length semantic checks are selected frozen requirements, not an exhaustive human adjudication of every possible route.

**3. Remaining reviewer burden.** The full-card validator emits one advisory REVIEW hint for S139 being absent from section 7. S139 reserves the right to modify the RFP, mentioning selection criteria parenthetically; the card places it in 10/11. The hint is plausibly overbroad and remains a manual-review item, not an asserted proven evaluation omission. No personal-date, money or contact REVIEW hints are emitted for S215–S221; all seven are exclusively in section 12.

## Full-length preservation and limits

The candidate completed in three consecutive replies: **141, 98 and 129 bullets**. Each is within 150. Parts 1 and 2 end with the contractual marker; exactly `continue` was sent after each saved part. Part 3 ends normally. The unmodified strict validator accepts the three files together: fixed shape, no extra text, exact full-statement quotes/citations, ID order, and all source IDs covered. S072 citation-copying checks pass in this run. The source packet, including its blank separator, was identical for both arms; no corrected packet or coaching was supplied after the original refusal.

These are single first-pass trials, not estimates of repeatability. Test fixtures were selected and frozen before this native run but include previously developed stress cases; they are not independent unseen holdouts. The full packet consists of 214 existing real RFP statements plus seven synthetic calendar records, not a new independent real attachment. The account's saved context and possible native attachment transformations remain limitations. This supplement does not replace prior OpenAI evidence or imply cross-platform equivalence.

## Evidence and sequence

- Historical sealed competition source: `f3ff5c65d584fefe23d549fbb76577d927c61f08`.
- Native input/protocol freeze: `426ed43c`.
- All nine original native responses committed before the rebuilt arm: `9c194874`.
- Prior incomplete native report/checkpoint: `dba8e9c8`; its report, environment, scores, validations and manifest are retained under `checkpoints/partial-dba8e9c8/`.
- Completed rebuilt evidence commit: `b114d7e0`, before this final report update.
- `inputs.json` retains knowledge, bundle, source and prompt hashes; `trial-inventory.json` records all 18 native chat identities and raw response hashes.
- Short raw cards were copied from Claude into fresh plain-text Notepad tabs and saved from observed literal editor text. Full-length parts were saved through native Notepad Save As in UTF-8. The accessibility document-text field caps at 20,000 characters; full-length rendered UI captures are therefore partial observations, while native-saved raw files contain the complete copied responses. No card was reconstructed from expected answers.
- The original B rich-text paste into its reply composer remained unsent and was abandoned; its raw file came from a later plain-text Notepad paste. No completed answer was regenerated or corrected.
- The prior desktop capture interruption remains documented in the checkpoint. After the user restored the desktop, the existing rebuilt core C response was copied without regeneration, then the frozen order resumed. No permanent app/account settings were changed.
- `preservation.json` and the completed `preservation-check.json` verify **41,235 prior tracked files unchanged**, including original evidence, frozen questions, product files and sealed release assets. The existing sealed package remains untouched; this native supplement is separate and unpublished.

## Submission judgment

The rebuild addresses the judges' personal-content failure and improves the frozen questions, but the native evidence does not justify a claim of perfect reliability. Before publication, resolve or explicitly disclose the Unicode copying failure and the S047/S048/S148 routing omissions, retaining these failed raw trials. Any repair should be a separately frozen candidate with fresh fair paired runs; it must not replace these first-pass results or relax the validator. Keep the S139 advisory visible until adjudicated. A stronger submission explains both demonstrated improvements and these limits honestly.
