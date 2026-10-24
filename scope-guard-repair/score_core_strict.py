from pathlib import Path
import json,subprocess,sys
R=Path(__file__).resolve().parents[1];D=R/'scope-guard-repair';out=[]
for arm in ['original','rebuild']:
 for fixture in sorted((R/'fixtures').glob('*.md')):
  card=R/('run-'+arm)/'scope-guard-repair-core'/fixture.stem/'bid-compliance-card.md';cmd=[sys.executable,'-B','-X','utf8',str(R/'rebuild/tools/validate_packet.py'),str(fixture),str(card)];r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8');out.append({'arm':arm,'fixture':fixture.name,'exit_code':r.returncode,'command':cmd,'stdout':r.stdout,'stderr':r.stderr})
(D/'core-common-strict.json').open('x').write(json.dumps(out,indent=2));print(json.dumps([x for x in out if x['exit_code']],indent=2))
