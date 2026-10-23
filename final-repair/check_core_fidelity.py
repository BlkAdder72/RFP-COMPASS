"""Apply the identical stricter fidelity gate to both arms; no semantic scoring here."""
from pathlib import Path
import json,subprocess,sys
R=Path(__file__).resolve().parents[1];D=R/'final-repair';out=[]
for arm in ['original','rebuild']:
 for kind,fixtures in [('core',R/'fixtures'),('new',D/'fixtures')]:
  for source in sorted(fixtures.glob('*.md')):
   card=R/('run-'+arm)/('final-repair-'+kind)/source.stem/'bid-compliance-card.md'
   cmd=[sys.executable,'-B','-X','utf8',str(R/'rebuild/tools/validate_packet.py'),str(source),str(card)]
   r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8');out.append({'arm':arm,'kind':kind,'fixture':source.name,'same_strict_validator':True,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
(D/'identical-strict-fidelity.json').open('x',encoding='utf-8').write(json.dumps(out,indent=2));print(json.dumps({'cases':len(out),'passed':sum(x['exit_code']==0 for x in out)}));assert all(x['exit_code']==0 for x in out)
