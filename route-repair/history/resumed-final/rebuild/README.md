# RFP Compass — Competition 15 candidate

RFP Compass converts one designated source packet into a fixed twelve-section Bid Compliance Card. Every populated bullet quotes a whole source statement with its exact ID and complete anchor. Clearly unrelated personal material belongs only in section 12; mixed statements retain their genuine procurement placements without changing their quotations.

**Unpublished; the latest native comparison is incomplete.** Start with the parent [current results](../results.md), [frozen feedback questions](../questions.md) and [current documentation index](../documentation-sync/REPORT.md). Earlier full-RFP and twenty-trial results describe earlier candidates, not acceptance of this one.

## ICM architecture

Each part keeps one job:

| Part | Responsibility |
|---|---|
| [identity.md](identity.md) | Defines the conversion, intended user and evidence boundary. |
| [rules.md](rules.md) | Governs source handling, quotation fidelity and routing behavior. |
| [examples.md](examples.md) | Demonstrates the contract and discloses script-built sample provenance. |
| [reference/](reference/) | Defines the input packet and exact twelve-section output schemas. |
| README | Explains operation, evidence and limits. |

[CLAUDE_PROJECT_INSTRUCTIONS.txt](CLAUDE_PROJECT_INSTRUCTIONS.txt) supplies the deployment instructions. The six named instruction/schema files remain byte-frozen for the current native comparison. Validator and export tools operate outside the model's context; they do not replace the folder's behavioral contract.

## Current evidence

All 11 original first-pass native responses are saved in [route-repair/evidence/original/](../route-repair/evidence/original/). Three repaired responses are completely exported in [route-repair/evidence/rebuild/](../route-repair/evidence/rebuild/): personal-thread containment improves, personal-note containment improves, and official clarification ties. Each passes raw strict validation and selected routing checks. The fourth repaired response finished but has no verified raw export; seven subsequent cases remain unrun. Do not regenerate that fourth response or count it as passing.

In the latest saved comparison, Q1–Q4, Q7 and Q8 pass; Q5 and Q6 remain pending. Q7/Q8 include local artifact/default-validator checks. Earlier Q1–Q8 passes and earlier full-RFP cards remain preserved under [native-repair/](../native-repair/), with their failures and limitations; they cannot establish completion of the current comparison.

The two false personal-note advisory warnings were fixed offline using bounded whole-text patterns. The [repair report](../validator-note-repair/REPORT.md) preserves both pre-fix warnings, sequential tests, comparisons with the judged-original and pre-fix validators, and unchanged strict-validation proof. No Claude run was repeated for that fix. Unknown or mixed-purpose wording can still need human review.

## Use the folder

Supply only CLAUDE_PROJECT_INSTRUCTIONS.txt, identity.md, rules.md, examples.md, reference/input-schema.md and reference/output-schema.md, plus the active packet named source-packet.md. Keep evaluator questions, expected answers, past responses, tools and the opposite arm out of the model session. Preserve each first-pass response. If the contract explicitly requests continuation, send exactly `continue` and retain every part. Current user direction excludes further Claude runs.

## Preserve and finalize an existing export

Keep the exact raw parts. From this folder, with Python 3.10 or later:

```text
python -B -X utf8 tools/finalize_card.py source-packet.md raw-part-1.md raw-part-2.md --output-dir new-export
```

Pass only parts actually returned; the output directory must be new. This explicit transport stage restores only canonically equivalent Unicode anchor drift for the same source ID and an already exact quotation. It changes no routing, IDs, body text, whitespace or non-equivalent anchor. Raw hashes and changes are recorded in export-audit.json; rejected attempts retain REJECTED.json. A derived-export PASS is not a raw-copying success. The same export tool is available externally to both arms.

## Validate saved output

```text
python -B -X utf8 tools/validate_packet.py source-packet.md bid-compliance-card.md
python -B -X utf8 tools/validate_packet.py source-packet.md part-1.md part-2.md
```

With no arguments, the validator checks the four packaged samples. It rejects changed quotations/anchors, missing IDs, wrong headings/order, extra prose and malformed continuation boundaries. REVIEW hints are advisory. A strict PASS does not prove semantic placement, the truth of `not in source`, or fidelity to the original PDF. PDF tracing is separate and requires pdfplumber; see [tools/trace_card.py](tools/trace_card.py).

The latest offline warning repair passed 263 differential cases per stage, 60 CLI comparisons, 216 retained warning/corruption controls and 17 citation-export controls. Earlier full-length saved cards were replayed offline without changing strict outcomes or existing full-RFP hints. These checks verify saved outputs and tooling; they do not fill the missing native trials.

## Evidence and package status

The [restart guide](../route-repair/RESUME.md) records the interrupted fourth response. The [current results](../results.md) distinguish raw strict checks, selected routing and derived exports. Historical reports, raw evidence, frozen questions and judged original remain unchanged. The current source ZIP, full-history bundle and package-verification receipts are in `../dist/documentation-sync-review-v2/`, explicitly labelled an incomplete offline review snapshot. Older archives, including the verified validator-repair v2 package and the first failed package, remain preserved. Final submission stays on HOLD; nothing is published.
