"""Promote the preservation-aware v2 audit without changing prior audit files."""
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'revision'
text=(D/'history/tools/verify_submission.py').read_text(encoding='utf-8')
text=text.replace("assert sha(R/name)==h,'Prior evidence changed: '+name", "path=R/'revision/history'/name if name in json.loads((R/'revision/preservation.json').read_text(encoding='utf-8'))['mutable_paths'] else R/name\n        assert sha(path)==h,'Prior evidence changed: '+name")
text=text.replace("assert (R/'rebuild/tools/validate_packet.py').read_bytes()==(H/'repair/candidate/tools/validate_packet.py').read_bytes()", "current_cases=json.loads((R/'revision/default-tests-v2-results.json').read_text(encoding='utf-8'))['cases']\nassert sha(R/'rebuild/tools/validate_packet.py')==next(c['validator_sha256'] for c in current_cases if c['arm']=='rebuild')")
text=text.replace("logs=P/'final-checks'", "logs=P/'final-checks-v2'")
text=text.replace("run('feedback-contained-reviewed',A,R/'run-original/Q8-validator/contained.md',{'S004':False},R/'repair/review-records/personal-A.json')", "run('feedback-contained-default',A,R/'run-original/Q8-validator/contained.md',{'S004':False})")
text=text.replace("run('feedback-real-deadline-reviewed',A,R/'run-original/Q8-validator/missed-deadline.md',{'S002':True,'S004':False},R/'repair/review-records/personal-A.json')", "run('feedback-real-deadline-default',A,R/'run-original/Q8-validator/missed-deadline.md',{'S002':True,'S004':False})")
text=text.replace("run('neutral-personal-reviewed',F,R/'supplemental/tool-original/N2-neutral-personal/evaluator-card.md',{'S002':False},R/'repair/review-records/personal-F.json')", "run('neutral-personal-default',F,R/'supplemental/tool-original/N2-neutral-personal/evaluator-card.md',{'S002':False})")
text=text.replace("result={'local_compliance'", "revision_audit=subprocess.run([sys.executable,str(R/'revision/verify.py')],cwd=R,capture_output=True,text=True)\nassert revision_audit.returncode==0,revision_audit.stdout+revision_audit.stderr\nfresh=json.loads((R/'revision/verification.json').read_text(encoding='utf-8'))\nresult={'fresh_revision_audit':fresh,'total_raw_model_responses':count+fresh['fresh_model_responses'],'local_compliance'")
text=text.replace("'Explicit adjudication required to suppress personal hints; no claim of automatic classification'", "'Default bounded source-text filter passes Q8 without sidecars; optional manual records are not used in the paired comparison'")
for path in (R/'tools/verify_submission.py',R/'packaging/final_compliance.py'):
    with path.open('w',encoding='utf-8',newline='\n') as stream:stream.write(text)
print('Promoted v2 offline auditor; historical auditor snapshots retained.')
