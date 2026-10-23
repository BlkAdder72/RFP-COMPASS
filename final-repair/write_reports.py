from pathlib import Path
import json,shutil
R=Path(__file__).resolve().parents[1];D=R/'final-repair'
E=D/'attempt-2'
core=json.loads((E/'scores-final.json').read_text());full=json.loads((E/'full-length-results.json').read_text());new=json.loads((E/'new-results.json').read_text());controls=json.loads((D/'control-results.json').read_text());replay=json.loads((D/'replay-results.json').read_text())
assert not controls['rebuild_failures']
assert full['rebuild']['passed'] and all(v['passed'] for v in new['rebuild'].values()),'Record failed attempt before another repair; do not write a success report'
rows=[]
for q,c in core['comparisons']['1'].items():rows.append(f"| {q} | {c['original']} | {c['rebuild']} | {c['comparison']} |")
fullrows=[f"| {k} | {full['original']['checks'][k]} | {v} |" for k,v in full['rebuild']['checks'].items()]
newrows=[f"| {name} | {new['original'][name]['passed']} | {value['passed']} |" for name,value in new['rebuild'].items()]
regressed={q:c['regressed_subchecks'] for q,c in core['comparisons']['1'].items() if c['regressed_subchecks']}
copy_comparison=('Exact citation copying ties in this pair.' if full['original']['checks']['exact_anchors']==full['rebuild']['checks']['exact_anchors'] else 'Exact citation copying differs in this pair; the recorded mismatches above remain failures. A single pair does not establish a copying advantage.')
report=f'''# Final repair and paired evaluation — 2026-10-23

Publication: **NOT PERFORMED**. This candidate closes all three reviewed findings on their frozen cases. The new rebuilt full-length run passes every prospective check, including S076 in Sections 4 and 5 and character-exact citations throughout. This is observed test closure, not a claim of universal semantic or copying correctness.

## What changed and why

1. Required response information is explicitly a Section 5 item even without a named form or report. The rules require a section-by-section scan of every ID, retain enclosing required-submittal context, and prohibit dropping an item merely because it already appears in Section 4. The distinction from suggestions and post-award deliverables remains. No S076 identifier, TBRPC answer or source-specific routing matrix was added to model knowledge for this repair.
2. The bounded personal-activity filter now recognizes graduation celebrations, parties and ceremonies with a personal owner. It still requires exact trusted text and Section 12-only placement, and retains procurement, clinical and cross-anchor required-event vetoes. Labels alone do not authorize suppression. Unknown celebrations retain their warning.
3. The rebuilt validator rejects straight quotation delimiters and every altered quotation character, including invisible characters and Unicode normalization changes. Source trailing spaces are preserved in comparison. The old visible-text fallback and tolerant-success notes are removed. Exact anchor checks, coverage, ordering, continuation and shape checks remain. Original is untouched. This is stricter validation, not an exception to make new model outputs pass.

## Preservation and sequence

`final-repair/preservation.json` binds all pre-stage tracked files and previous delivery hashes. Mutable files were copied byte-for-byte to `final-repair/history/` before edits; all six baseline knowledge files were separately frozen. Frozen root questions remain byte-identical to their pre-rebuild commit. All previous failures, raw transcripts, red-team findings, scores and Git history remain unchanged. The original was run first on A–E, then U/V/W, then the full 221-statement input; its raw baseline was committed before candidate edits. Rebuild used the same inputs and order after its candidate commit.

The prospective protocol and expected matrices were committed before trials. The initial asynchronous baseline-commit wait correction is disclosed in `final-repair/AUDIT_NOTES.md`; it involved no model retry or output replacement. Runners, model (gpt-6-astra), medium reasoning, wrappers, no-tool rule and continuation policy are unchanged. No retries, best-of selection or output corrections were used. Knowledge differs only by the intended repair. Q7/Q8 remain deterministic file/default-tool checks, with no sidecar required. All requests, raw model events, stderr and continuation prompts are under `run-ARM/final-repair-v2-{{core,new,full}}/`.

## First attempt: failed and preserved

The initial final-repair candidate passed Q1–Q8, all three new cases, the S076 placement check and personal containment, but changed one S100 Section 6 anchor from its own single-page citation to the next statement’s page range. The unchanged strict validator rejected it. Original copied all anchors exactly. This was a real copying regression; it is not counted as a pass or replaced by the later run.

Exact first-attempt knowledge, scores, scorers and hashes remain in `final-repair/attempt-1/` and `final-repair/attempt-1-knowledge/`; all raw runs remain at `run-ARM/final-repair-*`. Before the second knowledge change, a new protocol was frozen and a new original baseline was committed. The second version adds a general p.-versus-pp. safeguard and four-row synthetic near-collision example; it adds no S100 or actual RFP answer. Both arms then rerun all cases and the full input in the same order. The validator and expectations are unchanged between attempts.

The first attempt also placed V's bare response-content heading in Sections 4 and 5. That extra placement was outside the frozen matrix and remains disclosed as an unscored semantic risk. The latest positions appear below; their change is an observation, not a prospectively scored heading repair.

## Frozen questions

| Question | Original | Rebuild | Comparison |
|---|---|---|---|
{chr(10).join(rows)}

Totals: {json.dumps(core['totals'])}. Regressed core subchecks: {json.dumps(regressed)}. These totals apply only to frozen Q1–Q8, not every possible routing assignment.

## New known regression cases

| Fixture | Original passes all checks | Rebuild passes all checks |
|---|---|---|
{chr(10).join(newrows)}

U retains the previously unseen anchor forms unchanged; it is now a known regression fixture. V tests mandatory response information without a named attachment. W tests the known graduation false-warning case. Exact quotations/anchors, required routing and personal-only placement are scored separately. See `final-repair/attempt-2/new-results.json`; no new independent holdout claim is made.

The matrix for V adjudicates the substantive response items, not its bare heading. Rebuild places `Required response contents:` in {new['rebuild']['V-required-response-info']['positions'].get('S001')}, versus original {new['original']['V-required-response-info']['positions'].get('S001')}. Heading placement remains an unscored semantic risk; the fixture-level pass does not certify every extra placement. A missing W warning alone is not personal containment: its actual positions are rebuild {new['rebuild']['W-personal-graduation']['positions'].get('S001')} versus original {new['original']['W-personal-graduation']['positions'].get('S001')}. The independent correct-card control is the evidence that the graduation false warning itself is repaired.

## Full-length noisy RFP

The source remains the same 214 real TBRPC statements plus seven explicitly synthetic personal-calendar statements. No source word, anchor or order was changed. The prospective matrix keeps all previous selected checks and adds S076 in Sections 4 and 5. Every quote and anchor is compared independently, not only S072/S076.

| Check | Original | Rebuild |
|---|---|---|
{chr(10).join(fullrows)}

Original S076 placements: {full['original']['positions'].get('S076')}; rebuild: {full['rebuild']['positions'].get('S076')}. Original bullets per reply: {full['original']['bullets_per_part']}; rebuild: {full['rebuild']['bullets_per_part']}. Copy mismatches: original {len(full['original']['anchor_mismatches'])} anchors/{len(full['original']['quote_mismatches'])} quotations, rebuild {len(full['rebuild']['anchor_mismatches'])} anchors/{len(full['rebuild']['quote_mismatches'])} quotations. All other selected placements and every negative result remain in `final-repair/attempt-2/full-length-results.json`.

The prior S076 regression is still visible in the unchanged `red-team-citations/semantic-review.json` and previous raw full-length cards. The new success does not rewrite that failure. The original's varying results across attempts remain evidence of run variability, rather than something to discard.

{copy_comparison} S076's actual placements are shown above; improvement, tie or failure follows those observations, not the previous version's result. A separate identical strict-fidelity gate passes all 16 core/new cards across both arms (`identical-strict-fidelity-v2.json`), so original is not receiving a scoring advantage from its more permissive native quotation validator.

The same strict validator also evaluates both arms' actual full-length reply parts in `identical-full-fidelity-v2.json`; an original failure remains a failure. The six follow-up controls accept the exact extended example, reject a swapped page range, and continue rejecting the preserved S100 failure in both versions. Validator code is byte-identical across the two final-repair attempts.

## Validation and regression controls

{controls['count']} evaluator-built validator checks spanning both arms were executed, with zero rebuilt expectation failures. They include exact Unicode acceptance, altered invisible/NBSP/normalization/trailing-space rejection, straight-delimiter rejection, anchor corruption, missing coverage, the preserved S072 failure, graduation false-warning closure, mixed real requirements, clinical scope, unknown events and cross-anchor context. Original contract gaps are recorded explicitly in `control-results.json`, not scored away.

Historical/reference replay: {replay['passed']}/{replay['count']} cards pass current structural validation under their recorded validator arms. Any rejected historical card remains unchanged; its raw stdout, stderr, hashes and exit code are retained in `final-repair/historical-replays/`. Controls are evaluator-built, not model responses.

Historical audits run against the sealed historical commit in a disposable local clone, preserving their original assertions. The current audit independently checks preservation, exact new prompts and knowledge hashes, unedited raw responses, no tools, same-session continuations, and the new strict validator. No historical test expectation is weakened to accommodate this repair.

## Deliberately unchanged and remaining limits

- The judged original, frozen eight questions, raw failed outputs, source packet, prior routing scores, model/provider and evaluation runners remain unchanged. Identity and input schema were not altered. The second attempt extends the general synthetic anchor example with single-page/page-range near-collisions; that example was chosen after inspecting the new failure.
- The full-input semantic matrix is still selected coverage, not a complete expert adjudication of all 221 statements in every section. Mechanical PASS cannot prove section placement. Unknown personal activities may retain conservative warnings.
- This repair had two versioned attempts. The first failed full-length citation validation; the second has one fresh pair per fixture and one fresh full-length pair after that failure. There is no statistical or universal copying guarantee, independent holdout claim, fresh Claude/Sonnet/Opus acceptance or cost/latency advantage claim.
- Reply-budget compliance is checked by the full-run scorer; a combined card does not preserve all reply boundaries for the standalone validator. No blanket claim that the validator enforces every output-contract rule is made.
- Premium/VIP eligibility is unverified. Public URL and submission comment remain unposted. The competition deadline remains Wednesday October 28, 11:59 PM EST as written.

## Local delivery

The updated source archive and complete-history Git bundle are sealed under `dist/final-repair-verified/`, with SHA256SUMS, release commit and fresh-clone verification alongside them. Earlier delivery files remain untouched. The source ZIP excludes `.git` as usual; use the bundle for the complete sequence/history. The report and new evidence are included in the new release. No publication is authorized or performed.
'''
for p in [D/'REPORT.md',R/'results.md']:p.write_text(report,encoding='utf-8',newline='\n')
(R/'README.md').write_text('''# RFP-COMPASS — Competition 15: The Rebuild

Local candidate; not published. Start with [feedback.md](feedback.md), [questions.md](questions.md), then [results.md](results.md).

The Comp #13 Translator entry is preserved at judged commit `92847d2a17250fa18914d932826db63d99dcb75c` (tag `judged-original-comp13`) and byte-identical under `original/`. Source: https://github.com/BlkAdder72/RFP-COMPASS. Its Git history and every rebuild stage remain in this repository.

The feedback asked for unrelated personal material only in Section 12 without false Section 6 warnings; explicit contractual-expectation routing; honest script-built-example provenance; and a noisy-input run in `run-results/`. Frozen Q1–Q8 trace those requests and precede the first rebuild in Git.

Current repair: required response information is checked for Section 5, graduation notes no longer create the known false warning, and quotation validation is strictly character-exact. Read the actual outcomes and limits in [results.md](results.md).

| Material | Location |
|---|---|
| Judged original and verbatim feedback | `original/`, `feedback.md` |
| Frozen questions/expected answers | `questions.md` |
| Candidate knowledge, tools and operating guide | `rebuild/` |
| New exact prompts and unedited replies | `run-original/final-repair-v2-*`, `run-rebuild/final-repair-v2-*` |
| Current protocol, scores, controls, preservation and report | `final-repair/` |
| Previous red-team findings, including S076 regression | `red-team-citations/REPORT.md` |
| Previous citation failures and repairs | `citation-repair/`, `hardening/`, earlier `run-ARM/` folders |
| Earlier complete audit trail | `revision/`, `repair/`, `supplemental/`, `history/`, `packaging/` |
| Updated local ZIP and complete-history bundle | `dist/final-repair-verified/` (local delivery; not source-tracked) |

Offline audit from a Git clone: `python -B -X utf8 tools/verify_submission.py`. It runs historical assertions in a disposable clone of their sealed commit, then checks current repair evidence. It calls no model. Fresh controlled runs: `tools/run_arm.py` for core/new sources and `hardening/run_full.py` for the full fixture; always choose new output directories. Authentication/model access is required for real reruns. The stored trials prohibit tools and record any violations.

`SUBMISSION_COMMENT.md` remains a draft. Eligibility is unverified; public link and comment are pending. Do not publish without authorization.
''',encoding='utf-8',newline='\n')
p=R/'rebuild/README.md';old=p.read_text(encoding='utf-8');p.write_text('''# Current final-repair status

See root `results.md` and `final-repair/REPORT.md` for current results. The latest paired full-length run preserves all citations and includes required response information S076 in Sections 4 and 5. Strict validation now rejects altered invisible characters and straight delimiters. Every previous failed run remains unchanged.

The current raw full-length rebuilt run is copied byte-for-byte to `run-results/final-repair-v2-full/`. The operating guide below is retained from the preceding stage; statements about earlier runs or unchanged validators describe that historical stage, not this stricter validator.

---

'''+old,encoding='utf-8',newline='\n')
(R/'packaging/COMPLIANCE.md').write_text('''# Current local competition compliance

No publication performed. Current performance and limitations: `final-repair/REPORT.md` and root `results.md`. The new full-length pair checks S076 prospectively as well as every citation. Strict validation replaces the earlier visible-character tolerance; original remains untouched.

Required root layout, original pin, verbatim feedback, frozen questions, original-before-rebuild sequence and all historical raw failures remain preserved. Historical audits execute against their sealed commit; current evidence is independently audited by `final-repair/verify.py`. The local updated release is `dist/final-repair-verified/`; earlier delivery hashes remain unchanged.

Premium/VIP eligibility remains unverified. Public URL/comment remain pending. Use the release's FINAL_VERIFICATION.json for actual delivery-check status, not this narrative alone.
''',encoding='utf-8',newline='\n')
(R/'SUBMISSION_COMMENT.md').write_text('''DRAFT — do not post; replace the public URL only after publication is authorized.

I rebuilt my Comp #13 Translator entry, RFP-COMPASS: [PUBLIC_REPOSITORY_URL]. The feedback line that drove it was: “A noisy-input test in `run-results/` showing a stapled thread held in Section 12 only.” The repo preserves the judged original, frozen questions, raw paired runs, ties and failed attempts, including the later citation and required-response routing repairs and their limitations.
''',encoding='utf-8',newline='\n')
dest=R/'rebuild/run-results/final-repair-v2-full';assert not dest.exists();shutil.copytree(R/'run-rebuild/final-repair-v2-full',dest);shutil.copyfile(R/'hardening/fixtures/Z-full-length-noisy.md',dest/'source-packet.md')
(dest/'README.md').write_text('Unedited rebuilt final-repair full-length trial, copied byte-for-byte from run-rebuild/final-repair-v2-full. Source has 214 real statements plus seven synthetic personal-calendar statements. This is one targeted paired observation, not an independent holdout or universal guarantee. See final-repair/REPORT.md at repository root.\n',encoding='utf-8')
(dest/'.gitattributes').write_text('* -text\n',encoding='utf-8',newline='\n')
print('Current reports, navigation and byte-identical packaged trial updated')
