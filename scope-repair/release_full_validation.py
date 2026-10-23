from pathlib import Path
import hashlib,json,subprocess,sys
R=Path(__file__).resolve().parents[1];D=R/'scope-repair';out=[]
for arm in ['original','rebuild']:
 parts=sorted((R/('run-'+arm)/'scope-repair-full').glob('part-*/bid-compliance-card.md'),key=lambda p:int(p.parent.name.split('-')[1]))
 for label,validator in [('native',arm),('common-strict','rebuild')]:
  tool=R/validator/'tools/validate_packet.py';cmd=[sys.executable,'-B','-X','utf8',str(tool),str(R/'hardening/fixtures/Z-full-length-noisy.md'),*[str(p) for p in parts]];r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8');out.append({'arm':arm,'gate':label,'validator_sha256':hashlib.sha256(tool.read_bytes()).hexdigest(),'command':cmd,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
(D/'release-full-validation.json').open('x').write(json.dumps(out,indent=2));print({x['arm']+'-'+x['gate']:x['exit_code'] for x in out})
