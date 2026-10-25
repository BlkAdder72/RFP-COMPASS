from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];D=R/'boundary-repair'
t=(D/'before/README.md').read_text(encoding='utf-8').replace('polarity-repair','boundary-repair').replace('polarity-release','boundary-release').replace('five findings in `red-team-guard/REPORT.md`','seven finding families in `red-team-polarity/REPORT.md`').replace('`red-team-guard/REPORT.md`','`red-team-polarity/REPORT.md`').replace('`scope-guard-repair/`, `scope-repair/`','`polarity-repair/`, `red-team-polarity/`, `scope-guard-repair/`, `scope-repair/`')
(R/'README.md').write_text(t,encoding='utf-8',newline='\n')
(R/'rebuild/README.md').write_text('''# RFP Compass — current Competition 15 candidate

RFP Compass turns one source packet into a twelve-section Bid Compliance Card. Every bullet quotes a whole source statement with its exact ID and complete anchor. Non-source personal material stays only in Section 12; a mixed statement retains its genuine procurement requirements without editing its quotation.

Current measured results, failed evidence, ties and limits: [results.md](../results.md) and [boundary-repair/REPORT.md](../boundary-repair/REPORT.md). The findings that drove this repair remain in [red-team-polarity/REPORT.md](../red-team-polarity/REPORT.md). The prior operating guide is preserved in `../boundary-repair/before/rebuild/README.md` and Git history. This candidate is unpublished.

## Use the folder

Supply `CLAUDE_PROJECT_INSTRUCTIONS.txt`, `identity.md`, `rules.md`, `examples.md`, `reference/input-schema.md` and `reference/output-schema.md`, plus one active packet named `source-packet.md`. Keep evaluator questions, expected answers, past runs and the opposite arm out of the translation session. Follow the source and output schemas; carry over complete statements and opaque anchors exactly. If a response continues, preserve each reply and send exactly `continue`.

## Validate the output

From this folder, with Python 3.10 or later:

```text
python -B -X utf8 tools/validate_packet.py source-packet.md bid-compliance-card.md
python -B -X utf8 tools/validate_packet.py source-packet.md part-1.md part-2.md
```

With no arguments the validator checks the four packaged samples. The packet/card validator uses the Python standard library. PDF tracing is a separate check with its own `pdfplumber` dependency; see `tools/trace_card.py` and the preserved setup guide.

Validation rejects altered quotations or anchors, missing source IDs, wrong headings/order, extra prose and malformed continuation boundaries. REVIEW hints are advisory. A structural PASS cannot establish semantic placement or prove that `not in source` is true. The personal-content warning filter is a bounded heuristic; source-bound routing checks in the competition evidence assess selected meanings separately. Explicit procurement and clinical cues retain warning protection. Negation alone cannot erase an inherited duty, and exclusion from another schedule is not exclusion from a requirement.

## Evidence and provenance

`run-results/boundary-repair-full/` contains the exact latest full-RFP model evidence. `examples.md` identifies the script-built sample and its hand routing list; it is not a raw model transcript. All earlier runs, including failures, remain preserved. The parent repository contains the judged original, verbatim feedback, frozen questions, paired raw runs and offline compliance command. See the parent results for the actual acceptance state rather than treating any individual validator PASS as submission approval.
''',encoding='utf-8',newline='\n')
(R/'packaging/COMPLIANCE.md').write_text('''# Current local competition compliance

Unpublished. Current report: `boundary-repair/REPORT.md` and root `results.md`. The judged original and all earlier evidence remain preserved. Root Q1–Q8 are unchanged. New raw core, supplemental and full-RFP runs follow the frozen original-first protocol; outcomes and failures are reported rather than inferred from structural validation.

Required root layout, feedback, pinned original and historical sequence remain intact. Seven mutable documents have exact before snapshots. Strict validation from def difference onward and the six model knowledge files are unchanged. Historical audits execute unchanged at their pinned commits; current evidence is checked by `boundary-repair/verify.py`. Delivery is under `dist/boundary-release/`; `FINAL_VERIFICATION.json` records actual fresh-clone packaging status. Mechanical compliance is separate from semantic performance.

The submission draft has three sentences. Premium/VIP eligibility and the final public repository URL remain unverified. No publication is authorized or performed.
''',encoding='utf-8',newline='\n')
plan=json.loads((D/'submission-plan.json').read_text(encoding='utf-8'));plan['sentences'][2]='The paired runs and frozen regression controls document what improved, what tied or regressed, and the remaining limits, with all failed evidence preserved.'
(D/'submission-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
(R/'SUBMISSION_COMMENT.md').write_text('# Submission comment — DRAFT, not posted\n\n'+' '.join(plan['sentences'])+'\n',encoding='utf-8',newline='\n')
t=(D/'before/tools/verify_submission.py').read_text(encoding='utf-8');needle="('scope-guard-repair','06e6a1384c94bd0c1298f0d50cfbe09ce3fc1bcf','scope-guard-repair/verify.py')";assert needle in t;t=t.replace(needle,needle+",('polarity-repair','21dd85b40edf835870689c9f4a0b67ddc10de81a','polarity-repair/verify.py')").replace("R/'polarity-repair/verify.py'","R/'boundary-repair/verify.py'")
# Duplicate historical checkouts need no cloud synchronization. Their assertions
# and pinned commits are unchanged; all audit stdout remains in release receipts.
t=t.replace("work=R/'.run-work';work.mkdir(exist_ok=True)","work=Path(tempfile.mkdtemp(prefix='rfp-comp15-historical-'))")
(R/'tools/verify_submission.py').write_text(t,encoding='utf-8',newline='\n')
print('Updated current evidence map, operating guide, offline audit and unposted draft')
