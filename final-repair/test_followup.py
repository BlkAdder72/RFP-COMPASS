from pathlib import Path
import json,subprocess,sys
R=Path(__file__).resolve().parents[1];D=R/'final-repair';O=D/'followup-controls';O.mkdir(exist_ok=False)
example=(R/'rebuild/examples.md').read_text(encoding='utf-8').split('## Exact anchors with similar source rows',1)[1].split('## 01-real-public-notice',1)[0]
source=O/'source-packet.md';source.write_text(example.split('```text\n',1)[1].split('```',1)[0],encoding='utf-8')
card=example.split('```markdown\n',1)[1].split('```',1)[0];exact=O/'exact.md';exact.write_text(card,encoding='utf-8');bad=O/'swapped-page-range.md';bad.write_text(card.replace('S003; Harbor notice p. 4 §6','S003; Harbor notice pp. 4–5 §6'),encoding='utf-8')
out=[]
for arm in ['original','rebuild']:
 for label,src,parts,want in [('exact',source,[exact],True),('swapped-page-range',source,[bad],False),('preserved-S100-failure',R/'hardening/fixtures/Z-full-length-noisy.md',sorted((R/'run-rebuild/final-repair-full').glob('part-*/bid-compliance-card.md')),False)]:
  folder=O/label/arm;folder.mkdir(parents=True);cmd=[sys.executable,'-B','-X','utf8',str(R/arm/'tools/validate_packet.py'),str(src),*[str(p) for p in parts]];r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8')
  for n,t in [('command.json',json.dumps(cmd)),('stdout.txt',r.stdout),('stderr.txt',r.stderr),('exit-code.txt',str(r.returncode))]:(folder/n).open('x',encoding='utf-8').write(t)
  out.append({'arm':arm,'label':label,'expected_valid':want,'exit_code':r.returncode,'passed':(r.returncode==0)==want})
(D/'followup-control-results.json').open('x').write(json.dumps(out,indent=2));print(json.dumps(out,indent=2));assert all(c['passed'] for c in out)
