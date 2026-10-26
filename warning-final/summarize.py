from pathlib import Path
import json,hashlib,subprocess
R=Path(__file__).resolve().parents[1];D=R/'warning-final'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def put(p,t):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8',newline='\n')
m=read(D/'preservation.json');q=read(D/'scores-final.json');models=read(D/'model-results.json');full=read(D/'full-length-results.json');stages={f'F{i}':read(D/'stages'/f'F{i}'/'results.json') for i in range(1,5)}
historical=read(D/'historical-control-replays-release.json');strict=read(D/'core-common-strict.json')
accept=all(s['passed_required'] for s in stages.values()) and not stages['F4']['all_remaining_failures'] and all(x['passed_all_checks'] for x in models['rebuild'].values()) and full['rebuild']['passed'] and all(x['verdict']=='pass' for x in q['scores']['1']['rebuild'].values()) and all(x['passed'] for x in historical if x['arm']=='rebuild') and all(x['exit_code']==0 for x in strict)
transport=[]
for arm in ['original','rebuild']:
 for kind in ['core','new','full']:
  for p in (R/('run-'+arm)/('warning-final-'+kind)).rglob('stderr.txt'):
   retry=[l for l in p.read_text(encoding='utf-8').splitlines() if 'retrying sampling request' in l]
   if retry:transport.append({'path':str(p.relative_to(R)).replace('\\','/'),'lines':retry})
final=stages['F4']['results'];controls={a:sum(c['passed'] for c in final if c['arm']==a) for a in ['original','before','rebuild']};comp={'improved':0,'tied':0,'regressed':0}
before={c['case']:c['passed'] for c in final if c['arm']=='before'}
for c in final:
 if c['arm']=='rebuild':comp['tied' if c['passed']==before[c['case']] else 'improved' if c['passed'] else 'regressed']+=1
ch=read(D/'chronology.json');status='PASS all recorded gates' if accept else 'HOLD: one or more recorded gates failed'
summary={'acceptance':status,'controls_of_207':controls,'controls_vs_before':comp,'question_comparison':q['totals'],'model_combined_of_3':{a:sum(x['passed_all_checks'] for x in d.values()) for a,d in models.items()},'full_RFP':{a:x['passed'] for a,x in full.items()},'automatic_transport_retries':transport,'chronology':ch,'prior_files_preserved':len(m['tracked']),'sealed_artifacts_preserved':len(m['artifacts']),'published':False}
put(D/'SUMMARY.json',json.dumps(summary,indent=2))
text=f'''# RFP Compass — sequential warning repairs, 2026-10-26

**{status}; unpublished.** The four remaining finding families in red-team-oct26/REPORT.md were repaired separately, with each issue's tests and all previously solved boundaries passing before the next edit. The original questions, all earlier evidence and all old sealed packages remain preserved. This is finite measured acceptance, not a claim of perfect language understanding.

## What changed and why

1. **F1, dependency wording.** Attendance conditions expressed as “hinges on” or “is dependent on” now retain warning protection. Their corresponding negative/contraction forms are analyzed with negation tied to the dependency predicate. “Not payment” and “not only” are positive guards. This repairs missed date warnings without treating the word participation alone as an obligation.
2. **F2, relation binding.** An exclusion before a private heading must bind to the requirement scope: an explicit `from` object or a supported scope subject. Being excluded from an office-hours program or daytime schedule cannot cancel a separate compulsory event requirement. Real exclusions and local subsection boundaries remain supported.
3. **F3, worded shares.** A bounded compositional English amount grammar covers hundreds and thousands. Complete private-share phrases are treated as a single unit during clause analysis so the `and` inside an amount is not mistaken for an independent action. Only that matched phrase is replaced in an analysis copy; original quotations/citations are untouched. Genuine mixed return, payment and credential deadlines retain hints.
4. **F4, annotated private headings.** Explicit outside-procurement annotations are recognized only within the complete private-heading grammar. Their own negative annotation no longer supplies an affirmative procurement cue. This cannot erase explicit inherited inclusion, clinical requirements or a later genuine duty.

Only rebuild/tools/validate_packet.py changes product behavior. The entire implementation from `def difference` onward is byte-identical, including strict quotations, opaque anchors, IDs, coverage, headings, prose and continuation checks. All six model knowledge files are unchanged. Source data, frozen questions, source-hash-bound matrices and raw model outputs were not corrected or relaxed.

## Ordered tests before moving on

207 controls were frozen: the prior162, all18 October26 review controls and27 new safety controls. Each stage runs all207 across original, before and current validators, preserving every stdout/stderr/command and the actual stage validator. Stage gates require the prior162, common guards and every issue solved so far; later issue failures remain visible until their own repair. Baseline reproduces18 failures. Stage results:

| Stage | Required gate | Remaining failing controls across all207 |
|---|---|---|
'''
for n,s in stages.items():text+=f"| {n} | {'PASS' if s['passed_required'] else 'FAIL'} | {len(s['all_remaining_failures'])} |\n"
text+=f'''
Final controls: original {controls['original']}/207; before {controls['before']}/207; repaired {controls['rebuild']}/207. Against before: {comp}. These controls include correct private cards, deliberately missed genuine dates and altered citations; all-12 deliberate omissions can pass structure while still requiring advisory hints. Structural PASS never proves semantic placement.

## Frozen questions and fresh fair model comparison

Freeze {ch['freeze']}; completed fresh original baseline {ch['original_baseline']}; final validator candidate {ch['candidate']}. Each fix is separately committed after passing its own gate. Q1–Q8 remain identical to bfdd812 and the initial competition chronology remains in Git history.

Same canonical runners, gpt-6-astra medium, six unchanged knowledge files, same core/new/full order and source packets, fresh sessions, expected answers excluded, exact `continue` turns for full RFP. No agent retry, raw correction or best-of selection. Automatic client transport retries are separately retained in SUMMARY.json; a transport retry is not claimed as a pristine identical request environment. Because this repair changes only a validator, different generated cards are sampling variation rather than a demonstrated causal improvement in the translator. Before/after replay of the exact same card isolates the actual warning repair.

| Question | Original | Rebuild | Comparison |
|---|---|---|---|
'''
for name,c in q['comparisons']['1'].items():text+=f"| {name} | {c['original']} | {c['rebuild']} | {c['comparison']} |\n"
text+=f"\nTotals: {q['totals']}. Q8 uses default handling without an exclusion sidecar. Regressed subchecks, if any, remain in scores-final.json.\n\n| Supplemental fixture | Original combined | Rebuild combined |\n|---|---|---|\n"
for name in models['original']:text+=f"| {name} | {'PASS' if models['original'][name]['passed_all_checks'] else 'FAIL'} | {'PASS' if models['rebuild'][name]['passed_all_checks'] else 'FAIL'} |\n"
for arm in ['original','rebuild']:
 for name,x in models[arm].items():text+=f"\n{arm} {name}: failed selected checks {[k for k,v in x['semantic_checks'].items() if not v]}; exact-copy mismatches {x['mismatches']}; private review hints {x['personal_review_hints']}.\n"
text+='\n## Fresh full-length noisy RFP\n\n214 real TBRPC statements plus seven synthetic personal records. Fresh original and rebuilt sessions, full raw continuations retained.\n\n| Gate | Original | Rebuild |\n|---|---|---|\n'
for k in full['original']['checks']:text+=f"| {k} | {full['original']['checks'][k]} | {full['rebuild']['checks'][k]} |\n"
for arm,x in full.items():text+=f"\n{arm}: {x['parts']} parts, bullets {x['bullets_per_part']}; quote mismatches {x['quote_mismatches']}; anchor mismatches {x['anchor_mismatches']}; missing selected routes {[s for s,v in x['genuine_routing'].items() if not v]}; private-only failures {[s for s,v in x['noise_only12'].items() if not v]}.\n"
text+=f'''
## Preserved failures, unchanged strengths and limitations

The exact failed October26 B card formerly warned on private S002/S004; the repaired default validator now gives no REVIEW on that identical source/card. The full failed S100 citation from submission-repair is still rejected. Earlier failed boundary/submission comparisons and all later red-team reports remain untouched. Old seals remain byte-identical; a new release path is used. Original judged source remains untouched. Four packaged samples pass; historical controls pass rebuilt {sum(x['passed'] for x in historical if x['arm']=='rebuild')}/{sum(x['arm']=='rebuild' for x in historical)}. Original historical failures are retained.

No changes to translator rules, S133 handling, script-built provenance, sparse Section12, prompt-injection behavior, input drafting or PDF trace behavior were necessary for these warning fixes. Those established strengths remain in the frozen core checks and historical audits. Validator source matching is not independent PDF-source authentication; PDF tracing remains a separate check and dependency.

The warning filter is a bounded heuristic; selected semantic matrices are not exhaustive grading. These are targeted synthetic cases and one fresh sample per model case, not an independent population holdout or a reliability estimate. Native Claude/attachment acceptance and Premium/VIP eligibility remain unverified. The public submission URL remains a placeholder until an authorized publication step. Repeated language expansion cannot establish “perfect”; the defensible claim is closure of these measured findings without observed regression within the recorded gates.

## Submission layout and delivery

Read feedback.md → questions.md → results.md. Original, verbatim feedback, rebuild, frozen questions and both raw arms remain at the required root locations. Latest evidence is warning-final/ and run-original/warning-final-* / run-rebuild/warning-final-*. Exact latest rebuilt full-RFP raw copy is rebuild/run-results/warning-final-full/. Older files remain evidence, not the current readiness report. The three-sentence SUBMISSION_COMMENT.md is unposted.

Offline audit: python -B -X utf8 tools/verify_submission.py. Nine historical assertions run unchanged at pinned commits before the current gate; no model calls. Source ZIP and full-history bundle use dist/warning-final-release/. Read its FINAL_VERIFICATION.json for actual fresh-clone compliance status; do not infer delivery completion from this report. No publication.
'''
put(D/'REPORT.md',text);put(R/'results.md',text)
readme='''# RFP-COMPASS — Competition 15: The Rebuild

Local candidate, unpublished. Start with [feedback.md](feedback.md), [questions.md](questions.md), then [results.md](results.md).

The judged Comp13 original is preserved byte-for-byte in original/, pinned at 92847d2a17250fa18914d932826db63d99dcb75c (tag judged-original-comp13). Source: https://github.com/BlkAdder72/RFP-COMPASS.

The judges asked for unrelated personal material only in Section12 without false date warnings, consistent S133 contractual-expectation handling, explicit script-built sample provenance and raw noisy-input evidence. Frozen Q1–Q8 address those requests and precede the first rebuild. Current results report wins, ties, failures and intentionally unchanged behavior.

The October26 review found four remaining warning issues. They were fixed and tested sequentially; all previous failed evidence is retained. Current report: results.md. Detailed stages and preservation: warning-final/. New paired raw runs: run-original/warning-final-* and run-rebuild/warning-final-*. Candidate folder: rebuild/. Exact packaged full-RFP raw evidence: rebuild/run-results/warning-final-full/.

Earlier acceptance reports describe their own recorded gates. red-team-oct26/REPORT.md and the failed boundary-repair/ and submission-repair/ comparisons remain preserved; they are not the current readiness status. Git history and before snapshots retain all earlier documents. Previously sealed packages remain unchanged.

Offline verification: python -B -X utf8 tools/verify_submission.py. It executes historical assertions unchanged at pinned commits, then evaluates current acceptance without model calls. Fresh runs use tools/run_arm.py and hardening/run_full.py with new output paths. Delivery: dist/warning-final-release/; read FINAL_VERIFICATION.json for actual fresh-clone status. Submission draft: SUBMISSION_COMMENT.md, unposted.

Finite test passes do not prove universal semantic routing or native-Claude acceptance. Premium/VIP eligibility and final public URL remain unverified. Nothing is published.
'''
put(R/'README.md',readme)
rebuild=(D/'before/rebuild/README.md').read_text(encoding='utf-8').replace('final-submission','warning-final').replace('red-team-polarity/REPORT.md','red-team-oct26/REPORT.md').replace('The prior operating guide is preserved in `../warning-final/before/rebuild/README.md`','The prior operating guide is preserved in `../warning-final/before/rebuild/README.md`')
put(R/'rebuild/README.md',rebuild)
sentences=['I rebuilt my Comp #13 Translator entry, RFP-COMPASS: [PUBLIC_REPOSITORY_URL].','The feedback line that drove it was: “A noisy-input test in `run-results/` showing a stapled thread held in Section 12 only.”','The frozen paired tests and sequential warning repairs show the measured improvements, ties, retained failures and limits, with all original evidence and Git history preserved.']
put(D/'submission-plan.json',json.dumps({'sentences':sentences,'published':False},indent=2));put(R/'SUBMISSION_COMMENT.md','# Submission comment — DRAFT, not posted\n\n'+' '.join(sentences)+'\n')
put(R/'packaging/COMPLIANCE.md',f'''# Current local competition compliance

{status}. Unpublished. Current report: warning-final/REPORT.md and root results.md. Root Q1–Q8 unchanged; original, verbatim feedback and every earlier evidence file remain preserved, with before snapshots of seven mutable files and53 old sealed artifacts. Only the warning analysis changes product behavior; all six model knowledge files and strict validation from def difference onward are unchanged. Four sequential gates,207 controls, fresh core/new/full paired runs, default Q8 and source-bound routing/opaque citation checks are separate.

The offline launcher preserves nine pinned historical audits and runs warning-final/verify.py as the current hard gate. Delivery: dist/warning-final-release/; FINAL_VERIFICATION.json determines fresh-clone completion. The submission draft is three unposted sentences. Native-Claude acceptance, Premium/VIP eligibility and public URL remain unverified. Nothing published.
''')
print(json.dumps(summary,indent=2))
