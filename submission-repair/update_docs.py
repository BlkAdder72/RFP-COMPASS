from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];D=R/'submission-repair'
t=(D/'before/README.md').read_text(encoding='utf-8').replace('boundary-repair','submission-repair').replace('boundary-release','submission-release').replace(' (not sealed: semantic D failed)','')
needle='| Material | Location |';assert needle in t
t=t.replace(needle,'The warning-only attempt passed its controls but failed a new model context case. That complete failed comparison remains in `boundary-repair/REPORT.md`; this candidate also repairs statement-level routing boundaries in rules and the output schema. Do not mistake the earlier structural PASS for semantic acceptance.\n\n'+needle)
t=t.replace('`polarity-repair/`, `red-team-polarity/`','`boundary-repair/`, `polarity-repair/`, `red-team-polarity/`');(R/'README.md').write_text(t,encoding='utf-8',newline='\n')
t=(D/'before/rebuild/README.md').read_text(encoding='utf-8').replace('boundary-repair','submission-repair');t=t.replace('This candidate is unpublished.','The failed warning-only model comparison remains in `../boundary-repair/REPORT.md`. This candidate is unpublished.');(R/'rebuild/README.md').write_text(t,encoding='utf-8',newline='\n')
(R/'packaging/COMPLIANCE.md').write_text('''# Current local competition compliance

Unpublished. Current report: `submission-repair/REPORT.md` and root `results.md`. Root Q1–Q8 are unchanged. The original-first protocol is repeated fairly after the retained warning-only semantic failure in `boundary-repair/REPORT.md`. Nine mutable files have before snapshots; all other earlier evidence stays byte-identical.

The warning validator and strict implementation remain unchanged from the passing boundary tool candidate. Only rules.md and reference/output-schema.md change among the six model knowledge files. Native and common-strict gates, selected routing checks, default Q8, frozen controls and raw model audits remain separate. The offline launcher retains seven historical pinned audits and then checks `submission-repair/verify.py`. Delivery: `dist/submission-release/`; `FINAL_VERIFICATION.json` records actual fresh-clone status. Mechanical compliance does not establish universal semantic correctness.

The submission draft has three sentences. Premium/VIP eligibility, final public URL and native-Claude acceptance remain unverified. Nothing has been published.
''',encoding='utf-8',newline='\n')
plan=json.loads((D/'submission-plan.json').read_text(encoding='utf-8'));(R/'SUBMISSION_COMMENT.md').write_text('# Submission comment — DRAFT, not posted\n\n'+' '.join(plan['sentences'])+'\n',encoding='utf-8',newline='\n')
t=(D/'before/tools/verify_submission.py').read_text(encoding='utf-8');needle="('polarity-repair','21dd85b40edf835870689c9f4a0b67ddc10de81a','polarity-repair/verify.py')";assert needle in t;t=t.replace(needle,needle+",('boundary-repair','118f24d3abf07b9cb736e1fd005ad40faf7fb58f','boundary-repair/verify.py')").replace("R/'boundary-repair/verify.py'","R/'submission-repair/verify.py'");(R/'tools/verify_submission.py').write_text(t,encoding='utf-8',newline='\n')
print('Updated one current evidence map, retained failed comparison, operating guide and draft')
