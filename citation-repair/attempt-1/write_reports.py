from pathlib import Path
import json,shutil
R=Path(__file__).resolve().parents[1];D=R/'citation-repair';dest=R/'rebuild/run-results/citation-repair-full'
if dest.exists():raise SystemExit('Refusing existing packaged trial before writes')
core=json.loads((D/'scores-final.json').read_text(encoding='utf-8'));full=json.loads((D/'full-length-results.json').read_text(encoding='utf-8'));r=full['rebuild']
headline=('The fresh rebuilt full-length card passes every frozen check, including exact S072 citations in Sections 4 and 5. The earlier failed card remains unchanged and still fails validation.' if r['passed'] else 'The fresh rebuilt full-length card still has failed checks. The repair is not a clean full-length pass; every failure is reported below and retained.')
report='''# S072 citation-copying repair — 2026-10-23

Publication remains paused. **'''+headline+'''**

## Diagnosis and change

The previous full-length rebuild dropped `bullet` from S072's anchor in Sections 4 and 5: it emitted `TBRPC Auditing RFP p. 7 §5.II.b` instead of the packet's `TBRPC Auditing RFP p. 7 §5.II.b bullet`. All statement text was exact, but these were genuine citation failures. The old raw card, both failed validations, first-pass reports, audit corrections and earlier package remain preserved.

Three general model-knowledge files changed: `rebuild/CLAUDE_PROJECT_INSTRUCTIONS.txt`, `rebuild/rules.md` and `rebuild/reference/output-schema.md`. They now treat the entire source-ID/anchor pair as opaque data, retain every anchor qualifier, construct a complete bullet from its own packet row, reuse it unchanged across sections, and compare the complete citation on every continuation. No S072-specific answer, fixture ID or shortened-anchor exception was added to these instructions.

**Both validators are byte-identical to the preceding sealed package.** No normalization, automatic citation repair, changed comparison rule, hidden postprocessing or relaxed acceptance is used. The model-free controls accept exact cards and reject shortened, swapped, punctuation/Unicode/case/spacing-altered anchors, changed quotes, missing coverage and the old S072 failure: 22/22 paired checks pass. This demonstrates that invalid output remains invalid; those controls are not model trials.

## Prospective method and preservation

`citation-repair/protocol.md`, the preservation manifest and the unchanged 221-statement input were committed before new trials and before the instruction change. All 8,000 pre-stage tracked files are accounted for, with changed files copied under `citation-repair/history/`. All six previous knowledge files for both arms are frozen there so historical requests remain reproducible. The judged original and root `questions.md` are unchanged; the original core baseline was committed before repairing instructions, and repaired instructions were committed before rebuilt model calls.

The full fixture is the same 214-statement real TBRPC packet plus the same seven synthetic personal-calendar statements. No source wording, anchor, order or noise changed. The noise is not part of the original PDF. Expected routing adds an explicit prospective S072 check in Sections 4 and 5; root frozen questions are unchanged.

Fresh original and rebuild sessions use gpt-6-astra/medium and the existing unchanged request/continuation runners. Both get the same wrapper and full input, with their own six instruction files. `continue` is sent exactly in the returned session; all commands, requests, raw events, stderr, exit codes, parts and combined unedited cards are retained. No tools, retries, corrected cards, expected answers in model context or best-of selection. Independent core/full sessions may overlap; no latency comparison is made.

## Fresh Q1–Q8 comparison

Five A–E model sessions per arm, in frozen order. Q7/Q8 are file/tool checks, not additional model conversations. Q8 uses the default invocation without review sidecars.

| Question | Original | Rebuild | Comparison |
|---|---|---|---|
'''
for q,c in core['comparisons']['1'].items():report+=f"| {q} | {c['original']} | {c['rebuild']} | {c['comparison']} |\n"
report+='\nComparisons: '+', '.join(f'{k}={v}' for k,v in core['totals'].items())+'. Any regressed subchecks remain in `citation-repair/scores-final.json`.\n\n## Fresh full-length comparison\n\n| Check | Original | Rebuild |\n|---|---|---|\n'
for key in r['checks']:report+=f"| {key} | {full['original']['checks'][key]} | {r['checks'][key]} |\n"
for arm,result in full.items():
 report+=f"\n{arm.capitalize()}: {result['parts']} replies; {result['bullets_per_part']} quoted bullets per reply; {result['cited_distinct_ids']} distinct IDs. S072 placements: {result['positions'].get('S072',[])}. Anchor mismatches: {len(result['anchor_mismatches'])}; quote mismatches: {len(result['quote_mismatches'])}; personal REVIEW lines: {len(result['personal_review_hints'])}.\n"
 for error in result['anchor_mismatches']:report+='\nAnchor failure: `'+json.dumps(error,ensure_ascii=False)+'`.\n'
 for error in result['quote_mismatches']:report+='\nQuote failure: `'+json.dumps(error,ensure_ascii=False)+'`.\n'
report+='''
S072's successful placement alone is not sufficient: exact anchors and quotes are checked on every citation in the full card. The independent validator consumes the actual reply parts in order. Personal containment is separately scored; zero REVIEW notes alone would not prove correct routing. Original and rebuilt outputs are accepted or rejected under their unchanged validators, never corrected to make the comparison pass.

## Remaining limits and deliberately unchanged work

- This is one fresh paired run on a known full-length input after inspecting a failure. It supports an observed repair, not a general copying guarantee or statistical superiority. Earlier failed trials continue to count as failures. No fresh Claude acceptance or latency/cost advantage is claimed.
- A model can still make a different copying error on another run. The exact validator remains the acceptance gate; a raw FAIL must not be submitted as a validated card. The general instruction repair is not a deterministic renderer.
- Section routing remains a semantic task. The bounded personal-hint filter can retain warnings under uncertain context; mixed relevant/personal clauses remain indivisible under whole-statement quoting rules.
- Identity, examples, input schema, packet/PDF builder, trace tool, validator, section-routing triggers and all prior repair evidence were retained. This stage addresses copying reliability rather than claiming a new PDF conversion improvement.
- Premium/VIP eligibility remains unverified. The public submission URL and comment remain pending explicit publication authorization. The brief's deadline remains October 28, 11:59 PM EST as written.

## Evidence map

- `run-original/citation-repair-core/`, `run-rebuild/citation-repair-core/`: fresh exact A–E prompts, model responses, validation and Q8 commands/output.
- `run-original/citation-repair-full/`, `run-rebuild/citation-repair-full/`: new full-length session evidence, every continuation and unedited model part.
- `citation-repair/full-length-results.json`, `scores-final.json`, `validation-results.json`: complete results including failures, not just the summary above.
- `rebuild/run-results/citation-repair-full/`: byte-for-byte copy of the fresh rebuild full-length evidence in the required project layout.
- `run-rebuild/hardening-full/`, `rebuild/run-results/full-length-noisy/`, `hardening/full-first-pass/`: previous S072 failure and false-warning interaction, unchanged.
- `citation-repair/history/`: previous editable documents, knowledge and audit code; `citation-repair/preservation.json` accounts for the preceding 8,000 tracked files and delivery hashes.
- `tools/verify_submission.py`: portable offline audit, including both historical knowledge and the new trials. New validation logs use `packaging/final-checks-v6/`.

No push, publication, external message or submission comment has been sent.
'''
(D/'REPORT.md').write_text(report,encoding='utf-8');(R/'results.md').write_text(report,encoding='utf-8')
intro='''# RFP-COMPASS — Competition #15 candidate

Not published. '''+headline+'''

Start with [current results](results.md), [frozen questions](questions.md), [verbatim feedback](feedback.md) and [citation repair evidence](citation-repair/REPORT.md). Previous reports and all failed raw trials remain under `citation-repair/history/`, `hardening/`, `revision/`, `repair/` and `supplemental/`.

The judged original is pinned at `92847d2a17250fa18914d932826db63d99dcb75c` with tag `judged-original-comp13`, from [RFP-COMPASS](https://github.com/BlkAdder72/RFP-COMPASS). Its 134 files remain unchanged under `original/`. The usable project is `rebuild/`. The portable audit verifies the original Git tree, feedback, frozen questions, original-before-rebuild sequence, old and new raw sessions and the unchanged validators.

Run `python -X utf8 tools/verify_submission.py` for the offline audit (Git history required; ignored delivery binaries optional). For a fresh full-length comparison run `python hardening/run_full.py original --output-dir NEW_ORIGINAL_DIRECTORY`, then rebuild with a different new directory. For A–E use `python tools/run_arm.py original --output-dir NEW_CORE_DIRECTORY` and the corresponding rebuilt invocation. Existing destinations refuse before writes; `--preflight-only` calls no model; `--codex` supports an executable override. See `citation-repair/protocol.md` for comparison rules and limits.

The source ZIP contains current files; the Git bundle contains the complete preserved history and judged-original tag. Premium/VIP eligibility and the public submission link remain pending. A passing fresh trial is not a universal model reliability claim.
'''
(R/'README.md').write_text(intro,encoding='utf-8')
compliance='''# Current local competition compliance

Publication: NOT PERFORMED. '''+headline+'''

The required layout, original Git pin, verbatim feedback, frozen eight questions and sequence remain verified. Both validators are byte-identical to the preceding seal and continue rejecting the previous shortened S072 anchors. Current performance is reported separately from evidence integrity in `citation-repair/REPORT.md` and `citation-repair/verification.json`.

Historical audits read their pre-repair model knowledge from `citation-repair/history/`; their raw prompts and pass/fail outcomes are not replaced. Current validation logs use `packaging/final-checks-v6/`. All 8,000 pre-stage tracked files and five previous delivery files are retained; previous local deliveries are archived under `dist/prior-citation-repair/`.

Public URL/comment and Premium/VIP eligibility remain pending. No publish action is authorized.
'''
(R/'packaging/COMPLIANCE.md').write_text(compliance,encoding='utf-8')
project='> Current Competition #15 evidence: `../citation-repair/REPORT.md`. '+headline+' Exact-anchor validation is unchanged; all previous failed evidence remains preserved.\n\n'+(D/'history/rebuild/README.md').read_text(encoding='utf-8')
(R/'rebuild/README.md').write_bytes(project.encode('utf-8'))
(R/'SUBMISSION_COMMENT.md').write_text('''DRAFT — do not post; replace the public URL only after publication is authorized.

I rebuilt my Comp #13 Translator entry, RFP-COMPASS: [PUBLIC_REPOSITORY_URL]. The feedback line that drove it was: “A noisy-input test in `run-results/` showing a stapled thread held in Section 12 only.” The repo preserves the judged original and raw comparisons, including a failed full-length citation-copying run and the repair's fresh paired rerun, with ties, regressions and remaining limits disclosed.
''',encoding='utf-8')
dest.mkdir();(dest/'.gitattributes').write_text('* -text\n',encoding='utf-8')
for p in (R/'run-rebuild/citation-repair-full').rglob('*'):
 target=dest/p.relative_to(R/'run-rebuild/citation-repair-full')
 if p.is_dir():target.mkdir()
 else:shutil.copyfile(p,target)
shutil.copyfile(D/'fixtures/Z-full-length-noisy.md',dest/'source-packet.md');shutil.copyfile(D/'calendar.txt',dest/'calendar.txt')
(dest/'README.md').write_text('Unedited fresh full-length rebuild run after the general citation-copying instruction repair. Every continuation request, raw model response and validator result is retained. All source statement text/anchors remain unchanged from the preceding 221-statement noisy trial. See ../../../citation-repair/REPORT.md and ../../../citation-repair/full-length-results.json for the fair original comparison, failures and limits. Historical failed S072 output remains in ../full-length-noisy/.\n',encoding='utf-8')
print('Current report and required raw-evidence layout updated; no publication.')
