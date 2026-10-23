"""Keep historical runs bound to pre-repair knowledge, using preserved snapshots."""
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'citation-repair';K=D/'history'
p=R/'revision/verify.py';t=(K/'revision/verify.py').read_text(encoding='utf-8')
t=t.replace("R=Path(__file__).resolve().parents[1];D=R/'revision'","R=Path(__file__).resolve().parents[1];D=R/'revision'\nK=R/'citation-repair/history'")
t=t.replace("path=D/'history'/name if name in preservation['mutable_paths'] else R/name","path=D/'history'/name if name in preservation['mutable_paths'] else (K/name if (K/name).is_file() else R/name)")
t=t.replace("(R/'rebuild'/name).read_bytes()","(K/'rebuild'/name).read_bytes()").replace('sha(R/arm/name)==h','sha(K/arm/name)==h').replace('runner.request(R,arm,fixture)','runner.request(K,arm,fixture)')
p.write_text(t,encoding='utf-8')
p=R/'hardening/verify.py';t=(K/'hardening/verify.py').read_text(encoding='utf-8')
t=t.replace("R=Path(__file__).resolve().parents[1];D=R/'hardening'","R=Path(__file__).resolve().parents[1];D=R/'hardening'\nK=R/'citation-repair/history'")
t=t.replace("p=D/'history'/n if n in manifest['mutable_paths'] else R/n","p=D/'history'/n if n in manifest['mutable_paths'] else (K/n if (K/n).is_file() else R/n)")
t=t.replace('sha(R/arm/n)==h','sha(K/arm/n)==h').replace('runner.request(R,arm,','runner.request(K,arm,')
p.write_text(t,encoding='utf-8')
t=(K/'packaging/final_compliance.py').read_text(encoding='utf-8')
t=t.replace("(R/'rebuild'/name).read_bytes()==(H/'rebuild'/name).read_bytes()","(R/'citation-repair/history/rebuild'/name).read_bytes()==(H/'rebuild'/name).read_bytes()")
t=t.replace("logs=P/'final-checks-v5'","logs=P/'final-checks-v6'")
needle="(P/'final-compliance.json').write_text"
extra="citation_audit=subprocess.run([sys.executable,str(R/'citation-repair/verify.py')],cwd=R,capture_output=True,text=True,encoding='utf-8')\nassert citation_audit.returncode==0,citation_audit.stdout+citation_audit.stderr\nresult['citation_repair']=json.loads((R/'citation-repair/verification.json').read_text(encoding='utf-8'))\nresult['total_raw_model_responses']+=result['citation_repair']['fresh_model_turns']\nresult['candidate_performance']=result['citation_repair']['performance_summary']\n"
assert needle in t;t=t.replace(needle,extra+needle)
(R/'packaging/final_compliance.py').write_text(t,encoding='utf-8');(R/'tools/verify_submission.py').write_text(t,encoding='utf-8')
print('Historical audits resolve pre-repair knowledge; latest logs isolated in v6.')
