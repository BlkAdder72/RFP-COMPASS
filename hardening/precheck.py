"""Run the historical/current-validator audit while full sessions are still in progress."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
code=(R/'packaging/final_compliance.py').read_text(encoding='utf-8').split('hardening_audit=subprocess.run')[0]
scope={'__file__':str(R/'packaging/final_compliance.py'),'__name__':'__main__'}
exec(compile(code,str(R/'packaging/final_compliance.py'),'exec'),scope)
summary={k:v for k,v in scope['result'].items() if k!='checks'}
(R/'hardening/precheck-summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2))
