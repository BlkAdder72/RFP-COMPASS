from pathlib import Path
import hashlib,json,re,subprocess,sys
R=Path(__file__).resolve().parents[1];D=R/'citation-repair';O=D/'worked-example-validation';O.mkdir(exist_ok=False)
text=(R/'rebuild/examples.md').read_text(encoding='utf-8').split('## Exact anchors with similar source rows')[1].split('## 01-real-public-notice')[0]
source=re.search(r'```text\n(.*?)\n```',text,re.S)[1];card=re.search(r'```markdown\n(.*?)\n```',text,re.S)[1]
(O/'source-packet.md').write_text(source+'\n',encoding='utf-8');(O/'exact.md').write_text(card+'\n',encoding='utf-8');(O/'shortened.md').write_text(card.replace('§3 bullet]','§3]')+'\n',encoding='utf-8')
records=[]
for arm in ('original','rebuild'):
 for kind in ('exact','shortened'):
  box=O/(arm+'-'+kind);box.mkdir();cmd=[sys.executable,'-B','-X','utf8',str(R/arm/'tools/validate_packet.py'),str(O/'source-packet.md'),str(O/(kind+'.md'))]
  r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8')
  for n,t in [('command.json',json.dumps(cmd)),('stdout.txt',r.stdout),('stderr.txt',r.stderr),('exit-code.txt',str(r.returncode))]:(box/n).write_text(t,encoding='utf-8')
  records.append({'arm':arm,'kind':kind,'passed':(r.returncode==0)==(kind=='exact'),'validator_sha256':hashlib.sha256((R/arm/'tools/validate_packet.py').read_bytes()).hexdigest()})
(O/'results.json').write_text(json.dumps(records,indent=2),encoding='utf-8');assert all(c['passed'] for c in records);print('4/4 worked-example acceptance/rejection checks passed; no model calls.')
