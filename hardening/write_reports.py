from pathlib import Path
import json,shutil
R=Path(__file__).resolve().parents[1];D=R/'hardening'
if (R/'rebuild/run-results/full-length-noisy').exists():raise SystemExit('Refusing existing packaged full-length evidence before any writes')
full=json.loads((D/'full-length-results.json').read_text(encoding='utf-8'));scores=json.loads((D/'scores.json').read_text(encoding='utf-8'))
rows=[]
for q,c in scores['comparisons']['1'].items():rows.append(f"| {q} | {c['original']} | {c['rebuild']} | {c['comparison']} |")
fullrows=[]
for key in full['rebuild']['checks']:
 fullrows.append(f"| {key} | {full['original']['checks'][key]} | {full['rebuild']['checks'][key]} |")
report='''# Final warning repair and full-length comparison — 2026-10-23

Publication remains paused. The cross-anchor warning regression is repaired: requirement context follows source order across lines, paragraphs, pages and documents. Unknown transitions stay protected; an explicit personal-calendar/correspondence heading can end the scope. Anchors never authorize exclusion. Requirements and clinical-service wording veto filtering. Retirement/farewell meals, private medical appointments and explicit meal contributions now clear their false hints when contained only in Section 12.

## Fresh frozen-question comparison

Same A–E, same order, same six arm-specific files, same exact wrapper, gpt-6-astra/medium. One fresh session per fixture per arm: ten sessions, no retries or tools. Original baseline committed before the validator edit. The translation knowledge itself did not change in this stage. Q7 and Q8 are deterministic checks, not extra model conversations. Q8 uses the default invocation without a sidecar. No frozen questions or expected answers changed.

| Question | Original | Rebuild | Comparison |
|---|---|---|---|
'''+ '\n'.join(rows)+'''

Five improved question results, three ties, no scored regressions in this fresh comparison. These are correlated, known fixtures; no statistical generalization or Claude acceptance claim.

## Warning regression and control evidence

The 26 new evaluator-card controls compare identical source/card inputs under both validators. Before repair: original 18/26, prior rebuild 14/26. First repair: rebuild 25/26, with a missed `Mandatory bidder personal calendar:` heading. That failed run and its exact candidate code remain under `hardening/after/` and `hardening/candidates/initial.py`. Final repair: rebuild 26/26; original remains 18/26. The observed eight improvements over original have no final control regressions. The cross-anchor failures remain preserved in `red-team-final/` and `hardening/before/`; they were checker failures on evaluator-built cards, not invented model misroutes.

All 51 prior default/structural/duplicate controls meet current declared expectations; all 92 archived-card/reference structural replays pass. One prior expectation deliberately changes: “Please bring $30 for lunch” contained only in Section 12 now clears its money hint. Its old warning expectation remains untouched in the revision evidence. Genuine fees, contacts, mixed requirements and operational duplicates retain warnings. A plain “our lunch,” an unknown meeting, and an uncertain transition remain conservative warnings.

## Full-length noisy RFP

The fixture preserves every byte of the existing 214-statement TBRPC packet before appending seven synthetic calendar statements, for 221 statements. Original PDF and its historical trace evidence remain unchanged. The seven new statements trace to retained `hardening/calendar.txt`; they are not part of that PDF. This run tests a complete known RFP with synthetic noise, not a new real-world holdout or a new end-to-end PDF conversion.

Fresh persistent session per arm; original first, then rebuild. Same wrapper/model/settings; exact `continue` in the returned session ID whenever the model emits the required marker. Every request, raw event, stderr, command, model part and combined unedited card is retained. The final validator receives the actual parts in order. No transcript repairs, output compression, best-of selection or tool use.

| Full-length check | Original | Rebuild |
|---|---|---|
'''+ '\n'.join(fullrows)+'\n\n'
for arm in ('original','rebuild'):
 r=full[arm];report+=f"{arm.capitalize()}: {r['parts']} replies, {r['bullets_per_part']} quoted bullets per reply, {r['cited_distinct_ids']} distinct cited IDs. Personal REVIEW lines: {len(r['personal_review_hints'])}. Detailed routing and every failed check appear in `hardening/full-length-results.json`.\n\n"
report+='A zero REVIEW count alone does not prove containment: the original can avoid a missing-section warning by putting the personal statement into that operational section. The separate noise-only-Section-12 check is the decisive routing check.\n\n'
report+='''## What can still cost the win

- This is a bounded English hint filter. It does not prove semantic routing. A requirement scope can conservatively extend farther than necessary; unrecognized personal activities or headings can still warn. A misleading explicit personal heading can also misrepresent source context. Contextual inference remains reviewable rather than certified.
- Mixed relevant/personal content within one source statement is indivisible under exact-quote rules. Relevant placements can carry personal text in that whole quote; no claim that all mixed clauses disappear.
- The complete RFP and deterministic cases are known, synthetic-noise tests. One new paired run does not establish broad reliability, statistical superiority, latency or cost advantage. Earlier Claude results are historical, not fresh acceptance of this repair.
- Evidence is extensive. Start with this report and the portable verifier; older stages deliberately retain failures and superseded reports. Historical pass counts are not a claim the superseded candidate had no bugs.
- Premium/VIP eligibility remains unverified. A public submission link and the platform comment are pending explicit publication authorization. The brief's deadline remains Wednesday October 28, 11:59 PM EST as written.

## Evidence and provenance

- `hardening/protocol.md`, `preservation.json`, frozen test definitions and full-length expectations precede the repair/trials in Git.
- `run-original/hardening/`, `run-rebuild/hardening/`: fresh A–E exact requests and raw model evidence; default Q8 command/output evidence.
- `run-original/hardening-full/`, `run-rebuild/hardening-full/`: complete session continuation evidence.
- `hardening/before/`, `after/`, `after-v2/`, `prior-controls/`, `replays/`: model-free tool checks; never counted as model translations.
- `hardening/verification.json`, `packaging/final-compliance.json`: offline preservation, raw-event, sequence and current validation audits.

Original judged files, feedback, questions, all previous failures and Git history are retained. No push, public release, submission comment or external message has been sent.
'''
(D/'REPORT.md').write_text(report,encoding='utf-8')
(R/'results.md').write_text(report+'\n\n---\n\n# Preserved preceding stage report\n\n'+(D/'history/results.md').read_text(encoding='utf-8'),encoding='utf-8')
intro='''# RFP-COMPASS — Competition #15 rebuild

Local candidate; not published. Start with [current results](results.md), [frozen questions](questions.md), and [final hardening evidence](hardening/REPORT.md). The judged original is unchanged under `original/`; verbatim feedback is `feedback.md`; the usable project is under `rebuild/`.

Run `python -X utf8 tools/verify_submission.py` for the portable offline audit (Git history required; delivery binaries are optional). For a fresh core comparison use `python tools/run_arm.py original --output-dir NEW_DIRECTORY`, then the same command for rebuild with a different new directory. Existing destinations refuse before writes. For the full-length continuation protocol see `hardening/run_full.py` and `hardening/protocol.md`; its fixed evidence destinations also refuse reuse.

The final warning repair passes cross-anchor protection and the retained controls. Every earlier source, prompt, model response, failure and report remains available. Frozen questions are unchanged. Full-length test results and any limitations are reported without repairing model outputs. The source ZIP provides current files; the Git bundle preserves history and the judged-original tag. Membership eligibility and public submission remain pending.

---

## Previous package guide (historical)

'''
(R/'README.md').write_text(intro+(D/'history/README.md').read_text(encoding='utf-8'),encoding='utf-8')
compliance='''# Current local competition compliance

Publication: NOT PERFORMED. Required layout, judged original, verbatim feedback, frozen eight questions, original-before-rebuild chronology and all evidence are retained. Current candidate adds source-order scope protection and bounded personal-calendar hint fixes. See `hardening/REPORT.md` for fresh comparison results, full-length checks, failed first repair control and residual risks. `tools/verify_submission.py` audits old stages against their preserved code, then current evidence; no old run is silently regenerated. Current validator replay logs use `packaging/final-checks-v3/`.

The prior package and all prior tracked bytes are accounted for by `hardening/preservation.json`. Prior local delivery files are retained under `dist/prior-scope-hardening/`. The new source ZIP and history bundle are sealed only after committing current evidence. Ignored local delivery binaries are not required in a Git clone.

Public repository link/comment and Premium/VIP eligibility remain pending. No publish action is authorized.
'''
(R/'packaging/COMPLIANCE.md').write_text(compliance,encoding='utf-8')
(R/'rebuild/README.md').write_text('''> Competition #15 current verification: see `../hardening/REPORT.md`. The default validator now protects requirement context across changing citation anchors and clears bounded personal-calendar false hints. Unknown context retains REVIEW hints; structural PASS never proves correct section routing. All historical runs and their limitations remain preserved.

'''+(D/'history/rebuild/README.md').read_text(encoding='utf-8'),encoding='utf-8')
(R/'SUBMISSION_COMMENT.md').write_text('''DRAFT — do not post; replace the placeholder only after publication is authorized.

I rebuilt my Comp #13 Translator entry, RFP-COMPASS: [PUBLIC_REPOSITORY_URL]. The feedback drove clearer personal-thread containment, aligned contract-expectation routing, and default validator repairs, tested on the frozen questions and a complete 221-statement noisy RFP. The repo preserves the judged original, raw paired runs, discovered regressions and failed repair controls, with the fixes and remaining heuristic and mixed-statement limits disclosed.
''',encoding='utf-8')
dest=R/'rebuild/run-results/full-length-noisy';assert not dest.exists();dest.mkdir()
(dest/'.gitattributes').write_text('* -text\n',encoding='utf-8')
for p in (R/'run-rebuild/hardening-full').iterdir():
 if p.is_dir():shutil.copytree(p,dest/p.name)
 else:shutil.copyfile(p,dest/p.name)
shutil.copyfile(D/'fixtures/Z-full-length-noisy.md',dest/'source-packet.md');shutil.copyfile(D/'calendar.txt',dest/'calendar.txt')
(dest/'README.md').write_text('Complete unedited rebuild noisy-RFP run, copied byte-for-byte from run-rebuild/hardening-full. All continuation requests and raw responses retained. Base RFP: 214 unchanged original packet statements; seven synthetic calendar statements appended. See ../../../hardening/REPORT.md and ../../../hardening/full-length-results.json for original comparison, exact checks and limitations. Calendar source is separate from the original PDF. Not a hand-routed expected card.\n',encoding='utf-8')
print('Reports updated; full-length rebuild raw evidence packaged.')
