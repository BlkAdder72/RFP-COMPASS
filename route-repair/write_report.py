"""Render the current results from saved scores; no model calls or score edits."""
from pathlib import Path
import json,sys
D=Path(__file__).resolve().parent;R=D.parent
A=(D/(sys.argv[1] if len(sys.argv)>1 else 'analysis-final')).resolve()
s=json.loads((A/'scores.json').read_text(encoding='utf8'))
assert s['comparison_complete'],'Current release report requires complete saved evidence'
base='https://github.com/BlkAdder72/RFP-COMPASS/'
def link(label,path,folder=False):return '['+label+']('+base+('tree/' if folder else 'blob/')+'codex/competition-15-rebuild/'+path+')'
def state(v):return 'Pass' if v else 'Fail'
def total(arm,field):
 return sum(bool(v['derived_export']['strict_pass'] if field=='export' else v[field]) for v in s['model_trials'][arm].values())
rank={'fail':0,'partial':1,'pass':2}; improved=[];tied=[];regressed=[]
labels={'Q1':'Keep the stapled personal thread only in Section 12','Q2':'Retain the real deadline and required references','Q3':'Keep a different personal note only in Section 12','Q4':'Retain genuine procurement clarification sent by email','Q5':'Quote the planted AI instruction without obeying it','Q6':'Align contractual expectations with an explicit written rule','Q7':'Disclose the script-built sample and align its placement','Q8':'Remove false personal-date hints; retain real deadline hints'}
qrows=[]
for q,label in labels.items():
 a=s['frozen_questions']['original'][q]['verdict'];b=s['frozen_questions']['rebuild'][q]['verdict'];assert a in rank and b in rank
 outcome='Improved' if rank[b]>rank[a] else 'Tied' if rank[b]==rank[a] else 'Regressed'
 (improved if outcome=='Improved' else tied if outcome=='Tied' else regressed).append(q)
 qrows.append(f'| {q}: {label} | {a.title()} | {b.title()} | {outcome} |')
case_labels={'core-A-stapled-thread':'Stapled personal thread','core-B-personal-note':'Separate personal note','core-C-official-email':'Official procurement email','core-D-ai-instruction':'Planted AI instruction','core-E-contract-expectation':'Expected contract term','new-A-obligation-and-retrospective-scope':'Obligations and later scope clarification','new-B-personal-boundaries':'Personal-content boundaries','new-C-opaque-citations':'Unusual citation characters','new-D-native-regressions':'Combined routing and citation regressions','new-E-routing-families':'Related routing wording','full-Z-full-length-noisy':'Full 221-statement noisy RFP'}
case_rows=[]
for key,label in case_labels.items():
 a=s['model_trials']['original'][key]['expanded_semantic_pass'];b=s['model_trials']['rebuild'][key]['expanded_semantic_pass']
 case_rows.append(f'| {label} | {state(a)} | {state(b)} |')
counts={a:{'raw':total(a,'strict_pass'),'routing':total(a,'expanded_semantic_pass'),'export':total(a,'export')} for a in ['original','rebuild']}
feedback=link('judges’ feedback','feedback.md');questions=link('frozen questions','questions.md');scores=link('saved score details','route-repair/analysis-final/scores.json')
text=f'''# Competition 15 results — RFP-COMPASS rebuild

**Published:** the submission repository is https://github.com/BlkAdder72/RFP-COMPASS and its default branch is `codex/competition-15-rebuild`. The competition comment has not been posted.

The rebuild addresses the two fixes and the requested noisy-input demonstration in the {feedback}. Across the eight frozen feedback questions, **{len(improved)} improve, {len(tied)} tie, and {len(regressed)} regress**; all eight rebuilt outcomes pass. Across the separate eleven-case native Claude comparison, **{counts['rebuild']['routing']}/11 rebuilt cases pass the selected routing checks, versus {counts['original']['routing']}/11 for the original**. This does not mean every response copied every citation exactly: raw validation passes {counts['rebuild']['raw']}/11 rebuilt cases, with two remaining failure cases shared by both versions.

## What the judges asked us to fix

| Judges’ feedback | What changed | Evidence and result |
|---|---|---|
| Set aside clearly unrelated personal material, and stop false Section 6 date warnings for it. | Personal material is retained as quoted evidence only in Section 12; real procurement and mixed-purpose content remains usable. Bounded warning filters remove the tested false hints while preserving genuine missed-deadline warnings. | Q1 and Q3 improve; Q2, Q4 and Q5 tie; Q8 improves. Both personal-thread and personal-note tests pass, with real procurement content retained. |
| Settle the S133 contractual-expectation placement and disclose the sample’s provenance. | The rule explicitly includes stated contractual expectations in Section 11, consistently with the existing sample; examples.md identifies sample 04 as script-built from a hand routing list. | Q6 and Q7 improve. The original already placed the small contract fixture correctly, but lacked the explicit written rule; the improvement is rule/output consistency, not a new claim that its earlier answer was wholly wrong. |
| Demonstrate that a stapled thread stays in Section 12 only. | Added feedback-derived paired controls and retained every original and rebuilt response, then tested the same failure class in a full noisy RFP. | The stapled-thread case improves. The full 221-statement rebuilt card passes raw validation and all selected routing checks; its seven noise records remain only in Section 12. The original full-RFP response refused the input and is retained as a failure. |

The ICM architecture remains: identity, rules, examples, reference schemas and README each retain their own job. The judged original remains untouched at `92847d2a17250fa18914d932826db63d99dcb75c`, in `original/`, on the original `main` branch and under tag `judged-original-comp13`.

## Four measures, with different meanings

| Measure | Original | Rebuild | What it establishes |
|---|---|---|---|
| Eight feedback questions | 3 pass, 3 partial, 2 fail | 8 pass | Closure against the specific feedback, including written-rule, provenance and validator checks. |
| Selected routing checks in 11 native cases | {counts['original']['routing']}/11 pass | {counts['rebuild']['routing']}/11 pass | Whether the source statements satisfy the frozen selected placement and containment checks. |
| Raw output validation in those 11 cases | {counts['original']['raw']}/11 pass | {counts['rebuild']['raw']}/11 pass | Structure, exact quotations/citations, ID order and source coverage before export correction. |
| Validation after the same audited citation-export step | {counts['original']['export']}/11 pass | {counts['rebuild']['export']}/11 pass | Whether an operator-applied, source-bound Unicode correction produces a valid card; this is not raw copying success. |

These counts are not interchangeable. Q1 and Q2 share one model response; Q7 and Q8 are direct file/tool checks, not model conversations. The eleven native cases add stress cases and the full RFP. A routing pass does not imply an exact-citation pass, and neither establishes fidelity to the original PDF.

## The eight frozen feedback questions

| Question | Original | Rebuild | Change |
|---|---|---|---|
'''+ '\n'.join(qrows)+f'''

The question text and expected answers remain unchanged in {questions}. Q6 includes the explicit rule as well as the returned placement; Q7 inspects provenance and sample/rule alignment. Q8 tests both removal of false hints for the correctly contained personal content and retention of a warning for a deliberately missed genuine deadline.

## The eleven paired native cases: selected routing only

| Case | Original selected routing | Rebuild selected routing |
|---|---|---|
'''+ '\n'.join(case_rows)+f'''

The full RFP retains all 221 statements, including the seven noise records. Its rebuilt response preserves S072’s citation, includes submission contact S098 in Sections 4/6/10, and places the issuer’s reservation S139 in Sections 10/11 without treating it as substantive scoring criteria in Section 7. All full-RFP selected checks and raw strict validation pass.

## What tied, what remains imperfect, and what we left alone

- Q2, Q4 and Q5 tie: the real procurement details, genuine email clarification and resistance to the planted instruction already worked in these checks.
- Both versions fail raw validation in **two citation test cases**: `new-C-opaque-citations` and `new-D-native-regressions`. These are two failed cases, not merely two changed characters. Each version has two non-exact citation occurrences in the former and four in the latter, involving canonically equivalent Unicode forms.
- The identical external exporter restores only canonically equivalent anchors for the same source ID and an already exact quotation. It changes no routes or quotation bodies; non-equivalent anchors, wrong IDs, altered bodies and whitespace/entity substitutions remain rejected. The resulting passes are reported separately from raw failures.
- No regressions occur in the eight feedback-question verdicts or eleven selected routing verdicts. This is a finite comparison, not a claim that every possible input is solved or that all validators are warning-free.
- The script-built sample itself was not regenerated into a model transcript. Its provenance is disclosed. The fixed twelve-section shape, literal quotation requirements, source coverage, planted-instruction handling and separate PDF-tracing purpose are retained.

## Method, scope and chronology

The original judged commit, verbatim feedback, questions-before-rebuild chronology, failures and full Git history are preserved. The original questions.md also records the earlier Codex CLI control; those historical runs remain available. **The counts above come from the latest matched native Claude comparison**, under its separately frozen {link('routing protocol','route-repair/PROTOCOL.md')}, rather than combining scores from different models or rounds.

Both native arms use the same eleven source packets in the same order, the same common prompt, fresh ordinary Claude App chats and visible Opus 5.5 / Medium / Auto. Only the appropriate six-file ICM contract and active source packet were supplied. The prospective sources/checks were frozen before those original-arm trials; the final six-file rebuild bundle was frozen before the rebuilt trials. The baseline responses preceded the three final routing instruction changes, which were tested sequentially. Candidate, source and prompt hashes are in {link('final-inputs.json','route-repair/final-inputs.json')}.

Every first response remains preserved without coaching, regeneration or best-of selection. Core D was recovered without regeneration; its saved UI timeline includes unrelated later activity after the original test answer, which was not scored as part of that answer. Full-card continuations used exactly `continue` only after the contractual marker and saving the preceding part. Native exports retain the actual Markdown; long parts were saved through Notepad to avoid accessibility-text truncation.

The later validator-only repair addressed two saved false personal-note hints using whole-text forms. Its sequential 263-case comparisons, retained warning/corruption controls, citation-export controls and unchanged strict-validation proof remain in {link('validator-note-repair','validator-note-repair',True)}. It did not change the six-file model contract or rewrite saved responses. The claim is bounded to the tested forms and protected contexts.

The questions and extra cases are feedback-derived, not a blind holdout or statistical estimate. Account context, model service version and attachment parsing remain uncontrolled; UI observation cannot provide a server-version pin or a complete machine tool-event audit. Unseen wording and PDF/source fidelity still need review. No Claude runs were repeated for this report clarification.

## Evidence, verification and publication

- {scores}: individual verdicts, subchecks, positions, warnings, raw failures and export outcomes.
- {link('Original raw responses','route-repair/evidence/original',True)} and {link('rebuilt raw responses','route-repair/evidence/rebuild',True)}; exact {link('common prompt','route-repair/prompt.txt')} and {link('source/order hashes','route-repair/final-inputs.json')}.
- {link('Historical audit','route-repair/HISTORICAL_AUDIT.json')}: ten unchanged pinned snapshots plus current integrity, 31 successful steps; the Windows path-handoff failure and corrected-step retry remain preserved.
- {link('FINAL_CHECK.json','route-repair/FINAL_CHECK.json')}: completed comparison, evidence integrity and selected acceptance pass; raw citation perfection is false. Its `published: false` records the pre-publication verification snapshot, not current GitHub status.
- {link('Publication notes','publication/README.md')}: the verified source is `c49b7bb0`; the initial public release is `10c3d4df`. This clarification changes documentation and manifests only. Existing sealed packages remain intact; ZIP/history bundle and fresh-checkout receipts are local under `dist/route-repair-review-v2/`, not files hosted at that public path.
- {link('Report clarification verification','publication/report-repair/VERIFICATION.json')}: immutable-input hashes, exact before snapshots, regenerated report and unchanged score checks.
- {link('Previous exact results report','publication/report-repair/before/results.md')}: retained pre-publication snapshot, including its old status wording and detailed technical sequence. Older reports and failures retain their historical meaning.

Re-score saved evidence without model calls into a new directory with `python -B -X utf8 route-repair/score.py --output-dir .run-work/new-score`. Regenerate this report from the saved final score with `python -B -X utf8 route-repair/write_report.py analysis-final`; root results.md and route-repair/REPORT.md must remain byte-identical. Run `python -B -X utf8 route-repair/audit.py` for current integrity. The full historical audit command is `python -B -X utf8 tools/verify_submission.py`; it makes no model calls.
'''
for p in [R/'results.md',D/'REPORT.md']:p.write_bytes(text.encode('utf8'))
print(json.dumps({'report':'published current results','feedback_improved':improved,'feedback_tied':tied,'feedback_regressed':regressed,'counts':counts,'scores_changed':False}))
