from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'submission-repair'
t=(R/'boundary-repair/verify.py').read_text(encoding='utf-8').replace('boundary-repair','submission-repair')
t=t.replace("assert a[a.index(b'def difference('):]==b[b.index(b'def difference('):]",'assert a==b')
t=t.replace("for n,h in env['knowledge_sha256'].items():assert sha(R/arm/n)==h==m['tracked'][arm+'/'+n]","""for n,h in env['knowledge_sha256'].items():
   assert sha(R/arm/n)==h
   if arm=='rebuild' and n in ['rules.md','reference/output-schema.md']:
    assert h!=m['tracked'][arm+'/'+n] and subprocess.check_output(['git','show',ch['candidate']+':'+arm+'/'+n],cwd=R)==(R/arm/n).read_bytes()
   else:assert h==m['tracked'][arm+'/'+n]""")
t=t.replace("'six_model_knowledge_files':'unchanged'","'model_knowledge':'rules and output schema changed; other four unchanged'")
t=t.replace("same=read(D/'same-card-warning-replay.json')","same=read(R/'boundary-repair/same-card-warning-replay.json')")
t=t.replace("assert (D/'REPORT.md').read_bytes()==(R/'results.md').read_bytes()","""assert (D/'REPORT.md').read_bytes()==(R/'results.md').read_bytes()
assert all(x['passed_all_checks'] for x in read(D/'model-results.json')['rebuild'].values())
assert read(D/'full-length-results.json')['rebuild']['passed']
assert all(x['verdict']=='pass' for x in read(D/'scores-final.json')['scores']['1']['rebuild'].values())""")
(D/'verify.py').open('x',encoding='utf-8',newline='\n').write(t)
print('Prepared current acceptance audit and initial-to-final same-card replay')
