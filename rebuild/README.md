# RFP Compass — current Competition 15 candidate

RFP Compass turns one source packet into a twelve-section Bid Compliance Card. Every bullet quotes a whole source statement with its exact ID and complete anchor. Non-source personal material stays only in Section 12; a mixed statement retains its genuine procurement requirements without editing its quotation.

Current measured results, failed evidence, ties and limits: [results.md](../results.md) and [warning-final/REPORT.md](../warning-final/REPORT.md). The findings that drove this repair remain in [red-team-oct26/REPORT.md](../red-team-oct26/REPORT.md). The prior operating guide is preserved in `../warning-final/before/rebuild/README.md` and Git history. The failed warning-only model comparison remains in `../boundary-repair/REPORT.md`. This candidate is unpublished.

## Use the folder

Supply `CLAUDE_PROJECT_INSTRUCTIONS.txt`, `identity.md`, `rules.md`, `examples.md`, `reference/input-schema.md` and `reference/output-schema.md`, plus one active packet named `source-packet.md`. Keep evaluator questions, expected answers, past runs and the opposite arm out of the translation session. Follow the source and output schemas; carry over complete statements and opaque anchors exactly. If a response continues, preserve each reply and send exactly `continue`.

## Preserve and finalize the export

Keep the exact raw Claude response parts. The default export step is:

```text
python -B -X utf8 tools/finalize_card.py source-packet.md raw-part-1.md raw-part-2.md --output-dir new-export
```

Use only the parts actually returned. The output folder must be new. This explicit transport step restores only canonically equivalent Unicode anchor drift from the matching source ID, with an unchanged exact quotation. It never changes routing, IDs, body text, whitespace or non-equivalent anchors. Every change and raw hash is recorded in `export-audit.json`; the raw files stay untouched. The ordinary strict validator runs before final part files are emitted. Rejected attempts retain `REJECTED.json` and validation inputs. A successful derived export is not a claim that the raw model response copied Unicode exactly. The same stage can be applied to the original arm for a fair operational comparison.

## Validate the output

From this folder, with Python 3.10 or later:

```text
python -B -X utf8 tools/validate_packet.py source-packet.md bid-compliance-card.md
python -B -X utf8 tools/validate_packet.py source-packet.md part-1.md part-2.md
```

With no arguments the validator checks the four packaged samples. The packet/card validator uses the Python standard library. PDF tracing is a separate check with its own `pdfplumber` dependency; see `tools/trace_card.py` and the preserved setup guide.

Validation rejects altered quotations or anchors, missing source IDs, wrong headings/order, extra prose and malformed continuation boundaries. REVIEW hints are advisory. A structural PASS cannot establish semantic placement or prove that `not in source` is true. The personal-content warning filter is a bounded heuristic; source-bound routing checks in the competition evidence assess selected meanings separately. Explicit procurement and clinical cues retain warning protection. Negation alone cannot erase an inherited duty, and exclusion from another schedule is not exclusion from a requirement.

## Evidence and provenance

`run-results/warning-final-full/` contains the exact latest full-RFP model evidence. `examples.md` identifies the script-built sample and its hand routing list; it is not a raw model transcript. All earlier runs, including failures, remain preserved. The parent repository contains the judged original, verbatim feedback, frozen questions, paired raw runs and offline compliance command. See the parent results for the actual acceptance state rather than treating any individual validator PASS as submission approval.

The second failed candidate, including private leakage and a rejected full-RFP anchor, remains in `../submission-repair/REPORT.md`. The current results report both failed attempts separately.
