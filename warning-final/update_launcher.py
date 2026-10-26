from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'warning-final';p=R/'tools/verify_submission.py'
t=(D/'before/tools/verify_submission.py').read_text(encoding='utf-8')
t=t.replace("('submission-repair','339365bab38dcbf7850b85af4ed7242dd4b7e52a','submission-repair/verify.py')]:","('submission-repair','339365bab38dcbf7850b85af4ed7242dd4b7e52a','submission-repair/verify.py'),('final-submission','8e2afd4e9963cf29fbcf32a874fd196a03a78a02','final-submission/verify.py')]:")
t=t.replace("pythonpath(R/'final-submission/verify.py')","pythonpath(R/'warning-final/verify.py')")
assert "('final-submission','8e2afd4" in t and "R/'warning-final/verify.py'" in t
p.write_text(t,encoding='utf-8',newline='\n')
print('Nine unchanged pinned historical gates, then current warning repair acceptance')
