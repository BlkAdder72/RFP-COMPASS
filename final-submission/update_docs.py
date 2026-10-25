from pathlib import Path
import json,sys
R=Path(__file__).resolve().parents[1];D=R/'final-submission';prior=sys.argv[1]
t=(D/'before/README.md').read_text(encoding='utf-8').replace('submission-repair','final-submission').replace('submission-release','final-submission-release')
needle='| Material | Location |';assert needle in t;t=t.replace(needle,'A second candidate retained genuine duties but leaked negative/optional personal records and failed an exact citation. Its complete failed comparison is in `submission-repair/REPORT.md`. The current candidate makes relevance decisions in source order and retrieves literal source-row fields for every emitted citation.\n\n'+needle)
t=t.replace('`boundary-repair/`, `polarity-repair/`','`submission-repair/`, `boundary-repair/`, `polarity-repair/`');(R/'README.md').write_text(t,encoding='utf-8',newline='\n')
t=(D/'before/rebuild/README.md').read_text(encoding='utf-8').replace('submission-repair','final-submission');t+='\nThe second failed candidate, including private leakage and a rejected full-RFP anchor, remains in `../submission-repair/REPORT.md`. The current results report both failed attempts separately.\n';(R/'rebuild/README.md').write_text(t,encoding='utf-8',newline='\n')
(R/'packaging/COMPLIANCE.md').write_text('''# Current local competition compliance

Unpublished. Current report: `final-submission/REPORT.md` and root `results.md`. Frozen root Q1–Q8 are unchanged. Three original-first comparisons and both failed candidates remain visible. Before snapshots preserve nine mutable files; all other earlier tracked evidence and 47 old sealed artifacts remain unchanged.

Only rules.md and reference/output-schema.md change among the six model knowledge files in the current comparison. The entire warning and strict validator remains unchanged from the 162/162 boundary tool candidate. Structural, literal-copy, source-bound selected routing, default Q8 and warning accuracy gates remain separate. The offline launcher retains eight historical pinned integrity audits and then enforces the current hard behavioral acceptance gate in `final-submission/verify.py`.

Delivery: `dist/final-submission-release/`; read `FINAL_VERIFICATION.json` for actual fresh-clone status. Packaging compliance does not establish universal language correctness. The unposted draft has three sentences. Premium/VIP eligibility, final public URL and native-Claude acceptance remain unverified. Nothing is published.
''',encoding='utf-8',newline='\n')
plan=json.loads((D/'submission-plan.json').read_text(encoding='utf-8'));(R/'SUBMISSION_COMMENT.md').write_text('# Submission comment — DRAFT, not posted\n\n'+' '.join(plan['sentences'])+'\n',encoding='utf-8',newline='\n')
t=(D/'before/tools/verify_submission.py').read_text(encoding='utf-8');needle="('boundary-repair','118f24d3abf07b9cb736e1fd005ad40faf7fb58f','boundary-repair/verify.py')";assert needle in t;t=t.replace(needle,needle+",('submission-repair','"+prior+"','submission-repair/verify.py')").replace("R/'submission-repair/verify.py'","R/'final-submission/verify.py'");(R/'tools/verify_submission.py').write_text(t,encoding='utf-8',newline='\n')
print('Updated final evidence map, retained both failures, operating guide and draft')
