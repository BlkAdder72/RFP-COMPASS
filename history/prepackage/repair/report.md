# Validator warning repair

October 22, 2026. Local review draft. Not published.

**The filename-based warning suppression is removed from the repaired candidate.** The missed-deadline regression is repaired. False warnings for confirmed personal material are suppressed only when the operator explicitly selects a valid, packet-bound review record. This is an additional review workflow, not an automatic semantic classifier.

The complete candidate is in [candidate/](candidate/README.md); its validator is [candidate/tools/validate_packet.py](candidate/tools/validate_packet.py). The root rebuild/ remains the historical version that produced the first-pass and supplemental results. Both prior reports and all existing evidence remain unchanged. Final submission packaging has not been performed, and the historical root rebuild must not be mistaken for the repaired candidate.

## Evidence and sequence

The repair protocol and preservation manifest were committed as `e86e16f` before implementation. Candidate code and the regression test runner were committed as `5c30121` before execution. Raw check outputs and audits were committed as `1cc70ee` before this report.

All **752 protected prior files** were verified byte-identical, including both previously tested versions, first-pass and supplemental raw runs, fixtures, questions, reports and scoring code. Only the root navigation README is updated to point to the latest stage. No historic transcript, score, fixture or report was corrected or replaced.

## What changed

Previously, a source anchor containing unrelated plus the card's own Section 12-only placement was enough to suppress a warning. That combined two untrusted signals and could hide a genuinely misplaced deadline.

The repaired validator ignores filenames and anchors when deciding whether to suppress hints. With no selected review record, normal conservative hints remain. An optional `--reviewed-exclusions` record must name a reviewer, give reasons, match the exact packet SHA-256 and selected statement hashes, and select only statements actually quoted solely in Section 12. Records are selected explicitly; they are never auto-discovered from source files or card content.

Invalid/stale records cause validation failure and apply no exclusions. Blank attribution/reasons, duplicate IDs or JSON keys, unknown IDs, unsupported schemas, wrong hashes and malformed fields are rejected. Statements with explicit procurement cues are also rejected for exclusion, including the tested mixed deadline/personal statement. Structurally invalid cards cannot receive applied exclusions. Applied decisions are printed in stdout for inspection rather than silently hidden.

The six model knowledge files are byte-identical to the historical rebuild. This repair changes only validator behavior and documentation/operator workflow. No new model runs were made, and the archived model results are not presented as new trials of the repaired validator.

## Regression and original-feedback outcomes

| Check | Historical result | Repaired result |
|---|---|---|
| N1: real deadline wrongly quarantined; anchor says unrelated | Original warned; historical rebuild missed it | Warns for S002 without any review file. A valid empty review file still warns. |
| Q8 A: correctly contained personal thread | Original emitted personal-date warning; historical rebuild suppressed automatically | Default warning remains. With valid selected personal decisions, personal hints are suppressed and applied decisions are listed. |
| Q8 A: genuine deadline missing while personal material is excluded | Both old versions warned about real S002 | Still warns about S002, including when valid personal decisions are applied. |
| N2 F: neutral filenames, personal appointment correctly contained | Both old versions emitted a false date warning | Default warning remains. With valid selected decisions, the false personal-date hint is suppressed. |
| Invalid/stale review records | Feature did not exist | Ten malformed/stale/invalid record cases fail closed; no exclusions applied and the personal-date warning remains. |
| Operational, real-procurement or mixed-statement exclusion attempt | Feature did not exist | All three attempts are rejected; real deadline warnings remain where relevant. |
| Archived cards | Existing structural checks passed | All 42 archived model cards and four shipped reference cards still pass structure, exact quotation, citations, ordering and coverage without review records. |

**75 recorded expectations were satisfied:** 12 historical/default comparison checks, four valid-review/empty-review checks, ten invalid-record cases, three incompatible exclusion attempts, and 46 archived/reference-card replays. This count includes correctly detected failures and historical controls; it is not 75 new model translations or an independent reliability sample.

Inspect [results.json](results.json) for every expectation, input/code hash and outcome. Each directory under run/ preserves the exact command, stdout, stderr, exit code and audit. In particular:

- [Repaired N1 warning](run/N1-default/repaired/stdout.txt).
- [Q8 contained thread with selected review decisions](run/A-contained-reviewed/repaired/stdout.txt).
- [Q8 missed real deadline with those same personal decisions](run/A-missed-deadline-reviewed/repaired/stdout.txt).
- [Neutral personal material with selected decisions](run/N2-reviewed/repaired/stdout.txt).
- [Rejected attempt to exclude a real procurement deadline](run/procurement-exclusion/repaired/stdout.txt).

## Honest limits and changed tradeoffs

The earlier first-pass 8/8 claim does not transfer unchanged to the repaired candidate's default workflow. The original personal-date false hints return if the operator supplies no review decisions. Removing filename trust repairs the regression but gives up automatic suppression. The feedback's hint requirement is now met conditionally through explicit adjudication, tested alongside the requirement to keep real-deadline warnings. Do not describe that as zero-effort or out-of-the-box noise classification.

Review decisions add work. The test records identify their author as Codex evaluation adjudication, not owner or independent human approval. A reviewer name is attribution, not authentication or a signature. Hashes bind a record to the selected input; they do not prove that the relevance judgment is correct. A mistaken or malicious review record for a genuine requirement lacking the guarded procurement words could still suppress a hint. Operators must control and review these explicit trust inputs separately from the solicitation and generated card.

The procurement-word guard is deliberately conservative and incomplete. It can reject a genuinely personal statement mentioning work or a contract, while missing indirect procurement language. Unknown/ambiguous cases should keep their warnings. This repair does not establish universal semantic classification, independent authority verification or safety against an operator approving the wrong statement.

The mixed-statement limitation is unchanged: a whole quotation containing both a real requirement and a personal invitation still carries both into operational sections. The repair rejects excluding the tested mixed requirement; it does not split it or change the model contract.

All checker PASS outputs concern mechanical validity, not legal correctness or complete routing correctness. REVIEW remains advisory. No new full-PDF corpus verification, cost benchmark, fresh Claude replication or blind evaluation is claimed. The candidate is ready for review of this narrower validator fix; final public packaging and any owner judgment about the added review workflow remain separate.

## Verify without changing evidence

Run `python repair/verify.py` with Python 3.10+. It audits all 75 recorded expectations, the logged input/code hashes, the 752 protected files and the unchanged six knowledge files. It does not rerun or overwrite historical evidence. `repair/test_repair.py` intentionally refuses to overwrite its recorded run directory; a fresh execution belongs in a separate checkout or separately versioned stage.

See [candidate/REVIEWED_EXCLUSIONS.md](candidate/REVIEWED_EXCLUSIONS.md) for the command, record schema, hashing rules and limitations. No external submission has been made.
