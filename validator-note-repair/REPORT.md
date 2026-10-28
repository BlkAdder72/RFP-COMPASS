# Offline repair of two personal-note warnings

**The two saved false warnings are fixed. No Claude run, response, source, frozen question or six-file model contract changed. Nothing is published.**

The saved core-B response already puts its dentist date S003 and birthday contact S004 only in section 12. The pre-fix rebuild validator nevertheless advised checking sections 6 and 10, because its private-body test required an owner pronoun. It recognized “my dentist appointment” but not the complete calendar entry; it did not recognize the complete birthday contact instruction.

The repair adds two whole-statement forms: a dentist appointment with its bounded calendar/time format, and a named contact at an email address about a birthday dinner, party or celebration. It does not suppress based on an anchor, a source ID, the date alone, the email's local part or the output's placement alone. Existing independent procurement/clinical cues, mixed-clause checks, inherited scope and exact-citation trust still apply. Unknown meetings and contacts retain hints.

## Preserved sequence and evidence

The protocol, pre-fix validator, baseline results and new cases were frozen in commit `34be3ce0` before the implementation. Stage 1 fixes only the dentist warning and retains the contact warning; its candidate bytes and results are saved. Stage 2 fixes the birthday contact warning. Each stage passed 263 identical differential cases and 729 checks. Original, pre-fix rebuild and repaired validators are evaluated on the same packet/card bytes. The judged original is untouched.

- [Baseline](baseline/results.json), [dentist stage](stage-1-dentist/results.json), [final stage](stage-2-contact/results.json).
- [CLI comparison](cli-comparison.json): 60 public CLI invocations on the 14 saved current responses, two frozen Q8 cards and four samples. Strict exit outcomes are unchanged between pre-fix and repaired validators.
- [Retained controls](retained-controls/): 17/17 citation-export controls and 216/216 warning/corruption controls pass. Every retained strict error and advisory hint is unchanged in the differential test.
- [Earlier native replay](historical-native-replay.json): 21 raw/derived cases across the earlier 20 native cards, including the three-part full noisy RFP. Strict results and full-RFP hints are unchanged. The full packet has 221 nonblank statements plus a blank separator; the initial replay metadata counted lines rather than statements and is preserved in historical-native-replay-initial.json, with corrected counts in the current replay. This is an offline validator replay, not a new model run.
- [Integrity proof](FINAL_INTEGRITY.json): every pre-update tracked file is checked; changed files require exact before snapshots. AST comparison permits only the two added patterns and private-support predicate. All strict checks, citation/export logic, procurement vetoes and inherited-scope logic remain unchanged.

Raw Unicode citation failures and the latest original full-RFP refusal remain failures; no response was corrected, regenerated or replaced. Separate derived exports remain labelled. All completed semantic routes and frozen question verdicts are unchanged by this warning-only repair.

## Reproduce without Claude

Use new output paths:

```text
python -B -X utf8 validator-note-repair/test_repair.py --stage final --output-dir .run-work/new-warning-check
python -B -X utf8 validator-note-repair/verify_integrity.py --output .run-work/new-warning-integrity.json
python -B -X utf8 route-repair/score.py --output-dir .run-work/new-saved-score
```

Baseline records describe the pre-fix checkout; do not overwrite or rerun them against the repaired implementation as though it were the old version. The before validator is always included in the differential test.

## Package and remaining limits

A nested Git attribute normalized the shipped sample-04 card from Windows CRLF to Git LF. The original working bytes are preserved in portability/working-snapshots/, and portability.json verifies the pinned Git equivalent differs only in line endings. No raw response has a portability exception. The archive manifest hashes canonical Git bytes, and fresh-clone verification checks those exact bytes.

`dist/validator-note-repair-review-v2/` preserves the verified validator-repair snapshot at commit 43108f35. The current documentation-aligned source ZIP, full Git-history bundle, SHA256 checksums and fresh-clone verification are in `dist/documentation-sync-review/`; see [the current documentation index](../documentation-sync/REPORT.md). Both are explicitly incomplete offline review snapshots. Older archives are preserved. This does not replace the final competition package gate or establish pending native acceptance.

Three current repaired responses are completely exported. The fourth finished but still needs recovery/export, and seven later native cases remain unrun. The final submission audit must continue returning HOLD. The finite warning grammar can still produce review hints on unfamiliar private wording; the repair establishes the two specific false-warning closures plus preserved adversarial controls, not universal semantic certainty.

The first review archive is retained at dist/validator-note-repair-review/ with FAILED.json: Python initially omitted the Windows extended-length path prefix while reading deep evidence paths. The version-2 verifier uses extended Python paths and ordinary Git paths; validation logic and all prior evidence are unchanged.
