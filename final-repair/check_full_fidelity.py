"""Same strict quotation/shape gate on both arms' actual second-attempt reply parts."""
from pathlib import Path
import json,subprocess,sys
R=Path(__file__).resolve().parents[1];D=R/'final-repair';out=[]
for arm in ['original','rebuild']:
 parts=sorted((R/('run-'+arm)/'final-repair-v2-full').glob('part-*/bid-compliance-card.md'),key=lambda p:int(p.parent.name.split('-')[1]))
 cmd=[sys.executable,'-B','-X','utf8',str(R/'rebuild/tools/validate_packet.py'),str(R/'hardening/fixtures/Z-full-length-noisy.md'),*[str(p) for p in parts]]
 r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8');out.append({'arm':arm,'same_strict_validator':True,'command':cmd,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
(D/'identical-full-fidelity-v2.json').open('x',encoding='utf-8').write(json.dumps(out,indent=2));print(json.dumps({c['arm']:c['exit_code'] for c in out}));assert out[1]['exit_code']==0,'Rebuilt strict full-length failure retained'
