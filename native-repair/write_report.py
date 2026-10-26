from pathlib import Path
import json
D=Path(__file__).resolve().parent; R=D.parent
def read(n):return json.loads((D/n).read_text(encoding='utf-8'))
s=read('scores.json'); inventory=read('trial-inventory.json')
def yn(v):return 'Pass' if v else 'Fail'
rows=[]
for key in s['model_trials']['original']:
    a,b=[s['model_trials'][arm][key] for arm in ('original','rebuild')]
    rows.append('| '+key+' | '+ ' | '.join(yn(x['strict_pass'])+' / '+yn(x['semantic_pass'])+' / '+yn(x['derived_export']['strict_pass']) for x in (a,b))+' |')
qrows=['| '+q+' | '+s['frozen_questions']['original'][q]['verdict']+' | '+v['verdict']+' |' for q,v in s['frozen_questions']['rebuild'].items()]
report='''# Native Claude repair comparison — completed, held for review

Twenty first-pass native Claude App trials are preserved: ten original, ten repaired. The rebuild passes frozen Q1–Q8 and the full-length RFP's strict and selected semantic checks. Broader acceptance remains **FAIL**: the combined regression card omits one frozen required route, and raw Unicode citation copying still fails in both versions. Nothing is published. This report supersedes readiness claims in older reports without altering those reports or their evidence.

## Repairs and sequential evidence

1. **Citation transport, C1.** Added `rebuild/tools/finalize_card.py` and made it the documented default export step. It restores only canonically equivalent Unicode anchors from the same source ID when the entire quotation is already exact. It never changes routes, IDs, body text, whitespace, entities or non-equivalent citations. It preserves raw files, records codepoint changes and hashes, and runs the unchanged strict checks before emitting a derived card. Rejections retain validation inputs and REJECTED.json. This is an explicit operator tool, not improved raw model copying. The identical external tool was applied to both arms.

   The first test attempt had eight infrastructure failures from denied temporary-directory access; all stdout/stderr and failed outputs remain in stages/C1-citation. Replacing temporary staging with a new retained validation-inputs directory produced 15/15 passing checks in C1-citation-retest. Final C4 testing passed 17/17, including both versions' retained/fresh Unicode failures. Controls reject changed bodies, wrong IDs, page ranges, removed invisible characters, changed tab/NBSP, entity decoding and compatibility-only Unicode substitutions. No validation tolerance was added.

2. **Semantic routing, C2.** Clarified that binding named government/professional standards also route to section 10, and expected signing/execution of a service agreement also routes to section 11. Added independent sweeps so sections 3/8 do not substitute for those routes. Coherence checks passed 5/5; these were instruction checks, not model acceptance. Sample 04 and its hand routing list were aligned for S047/S048, S148 and S139, with explicit provenance. The before card is retained and the script roundtrip plus four packaged sample checks passed.

3. **False evaluation warning, C3.** Restricted only the evaluation advisory for a reservation to modify an RFP where selection criteria are merely an incidental object. Actual evaluation, ranking, weights, scores and combined reservation-plus-scoring remain protected. All 216 warning/corruption controls passed (207 prior controls plus nine new guards). Strict validation code is unchanged apart from the call to the advisory predicate. Same-card replay on both the retained and fresh native full-RFP cards removes the false S139 warning while retaining a genuine S098 contact-route warning in the fresh card. Personal-content warning controls and the original Q8 defective-deadline guard still pass.

Each repair was tested before moving to the next. Protocol freeze 473b87dd preceded the ten fresh original trials committed at d3318dff. Citation repair 3fe49304, routing clarification b7cff67d and advisory repair 745159d9 precede candidate freeze b8f37d6a. Repaired native evidence is committed at da25a37f. The frozen questions and all prior failed evidence remain unchanged.

## Native method and limits

Same ten-case order, identical source bytes and prompt, fresh ordinary chats outside projects, visible Opus 5.5 / Medium / Auto in both arms. Memory was observed enabled and left unchanged. Only the appropriate six-file translation-contract attachment and active source-packet attachment were supplied. Expected answers, scorer, tools, prior responses and opposite arm were excluded. File bundles preserve text but normalize file line endings; original-file and actual-bundle byte hashes are recorded separately. This approximates the folder contract in ordinary chats, not a configured Claude Project or independently verified server revision. No tools were requested or observed, but UI evidence cannot provide a machine tool-event audit or isolate account context and attachment parsing.

No response regeneration, coaching, corrected answer or best-of selection. Full-RFP continuations were exactly `continue`, twice, after preserving each preceding part. Copy to fresh Notepad tabs preserved short raw Markdown; native UTF-8 Save As preserved all full-length parts because accessibility text caps at 20,000 characters. Rendered UI/text trees are supporting observations, not substitutes for complete raw files. Window capture/activation failures and one geometry mismatch were recovered by fresh window selection. When desktop recovery failed before the repaired arm, input stopped until the user restored it; no prompt or completed answer was retried.

## Paired cases

Columns show **raw strict / selected semantic / derived strict**. Derived strict checks shape, literal quotations, exact restored citations and coverage; it does not certify routing.

| Case | Original | Rebuild |
|---|---|---|
'''+ '\n'.join(rows)+'''

Across all ten cases: original raw strict 7/10, selected semantic 5/10, derived strict 9/10; rebuilt raw strict 8/10, selected semantic 9/10, derived strict 10/10. Requiring both derived strict and selected semantics gives 5/10 versus 9/10. These are finite, feedback-derived checks, not blinded statistical estimates or proof of general superiority. The original full-RFP refusal remains counted as failure, never silently excluded.

## Frozen feedback questions

| Question | Original | Rebuild |
|---|---|---|
'''+ '\n'.join(qrows)+'''

Five question verdicts improve and three tie. Q6's model card alone ties; the original written trigger still lacks the explicit contractual-expectation rule. Q7 and Q8 are direct artifact/default-validator checks, not additional Claude conversations. The genuine missed-deadline REVIEW in Q8 is required to remain visible.

## Full-length result

The source has 221 statements, including seven calendar/noise statements. The repaired card has three parts of 137, 150 and 83 bullets; all IDs are covered, literal quotations and complete anchors pass strict comparison, and every frozen required/forbidden route passes. S047/S048 now include section 10 and S148 includes section 11. Personal S215–S221 remain exclusively in section 12, with no personal REVIEW hint. S081/S152 remain outside the forbidden mandatory-form routes. No Unicode restoration was needed for this full card. S098 is absent from section 10 even though it names the submission contact; the default validator correctly flags this genuine remaining route issue. Frozen full expectations do not require S098, so the selected semantic pass does not imply a complete route audit.

The original refuses the same valid packet, citing a blank separator and the calendar's unrelatedness. That refusal is retained without corrective follow-up. The older native full-card failures remain in claude-native/ and are separately identified from this fresh success.

## Ties, regressions and publication hold

- Both arms still compose decomposed accents in new C (two anchors) and new D (four anchors). Raw strict validation rejects all six occurrences per arm. Derived exports restore them with unchanged routes and full audit trails. This is a shared raw-model failure; applying the export tool fairly benefits both arms.
- New D improves the authority, expected-execution and personal-content checks, but loses S003's section-11 modification-reservation placement that the original retained. Original missing subchecks were S001 authority, S002 expectation and S008 privacy; repaired missing subcheck is S003 section 11. This is a real selected-check regression despite aggregate improvement. The source quote remains in sections 1/10, so coverage alone cannot detect it. Keep acceptance false.
- Core C omits the pricing-sheet statement from section 8 in the rebuild while retaining frozen required sections 5/11. Original and the prior candidate included section 8. The source says the revised pricing sheet replaces an earlier one; under the broad money trigger this is a plausible additional commercial-route regression outside Q4's selected checks. It needs source-based review, not a claim of no regressions.
- The fresh full card omits S098's contact route; the visible warning is genuine. Do not suppress it to make the report clean.
- New A now ties: the fresh original meets its selected obligations/expectation checks, although an older original trial failed one. Keep both results; do not attribute sampling variation to the repair.

The competition rewards the gap closed against feedback. All eight frozen feedback questions pass, but remaining routing variability and reliance on an explicit export tool could still cost the win. This is an unpublished **review package**, not release approval. Universal semantic routing and original-PDF fidelity remain outside a packet validator's guarantee. A fresh source-based route review and fair rerun would be required before claiming those remaining omissions resolved.

## Preservation, reproducibility and deliberate nonchanges

The judged original stays pinned at 92847d2a17250fa18914d932826db63d99dcb75c, feedback remains verbatim, questions precede rebuild in Git, and VIP eligibility is user-confirmed. The 41,358-file prior inventory is checked in preservation-check.json: unedited prior evidence remains byte-identical; changed product/docs have matching before snapshots or historical Git blobs. The initial complete workspace hash check is retained; final verification checks every baseline Git blob against that inventory and uses Git to detect current index/worktree differences. Every changed prior file has its original snapshot or Git blob checked. Old sealed packages are untouched. Source packets, identity, examples and input schema were deliberately left unchanged; examples already discloses the script-built card. The old evidence is not regenerated.

A fresh score reproduction matched all twenty trial results and Q1–Q8 (22 checks), and an attempted reuse of its output directory was refused. Reproduction now requires a new output directory, preserving the recorded validation evidence.

Reproduce scores: `python -B -X utf8 native-repair/score.py --output-dir .run-work/new-score`. Check integrity separately from acceptance: `python -B -X utf8 native-repair/audit.py`. Reproduce the isolated advisory comparison: `python -B -X utf8 native-repair/replay_warnings.py`. Local evidence is in native-repair/stages/; raw native transcripts, exact common prompt, hashes and chat identities are in native-repair/evidence/, prompt.txt, final-inputs.json and trial-inventory.json. The competition run directories link to this supplement. Current source ZIP and full-history Git bundle are in dist/native-repair-review/ with checksums and package verification. The submission comment remains a three-sentence, unposted draft with a public-URL placeholder.
'''
(D/'REPORT.md').write_text(report,encoding='utf-8'); (R/'results.md').write_text(report,encoding='utf-8')
env={'platform':'native Claude App, Windows, Computer Use','visible_model':'Opus 5.5','visible_reasoning':'Medium','permission_mode':'Auto','memory_enabled_observed':True,'VIP_eligibility':'user confirmed','comparison_complete':True,'trials_per_arm':10,'prompt':'prompt.txt','frozen_inputs':'final-inputs.json','protocol_commit':'473b87dd','original_evidence_commit':'d3318dff','candidate_commit':'b8f37d6a','repaired_evidence_commit':'da25a37f','continuations':['continue','continue'],'behavioral_acceptance':False,'raw_citation_perfection':False,'published':False,'limitation':'ordinary-chat attachment bundles; account context and attachment parsing uncontrolled; no machine tool-event audit'}
(D/'environment.json').write_text(json.dumps(env,indent=2),encoding='utf-8')
for arm in ('original','rebuild'):
    p=R/('run-'+arm)/'native-repair';p.mkdir(exist_ok=False)
    (p/'README.md').write_text('# Fresh native Claude comparison\n\nRaw '+arm+' evidence: [native-repair/evidence/'+arm+'](../../native-repair/evidence/'+arm+'/). Exact common prompt: [prompt.txt](../../native-repair/prompt.txt). Case order and input hashes: [final-inputs.json](../../native-repair/final-inputs.json). Q1/Q2 use core A, Q3 B, Q4 C, Q5 D, Q6 E; Q7/Q8 are local artifact/default-validator checks. Then new A/B/C/D and full Z, same order in both arms. See [report](../../native-repair/REPORT.md) for all passes and failures. No response corrections or regeneration.\n',encoding='utf-8')
