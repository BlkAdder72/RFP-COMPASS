from pathlib import Path
import json,subprocess,sys
R=Path(__file__).resolve().parents[1];D=R/'warning-final';cmd=[sys.executable,'-B','-X','utf8',str(R/'rebuild/tools/validate_packet.py')];r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8');(D/'packaged-samples-validation.json').open('x',encoding='utf-8',newline='\n').write(json.dumps({'command':cmd,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr},indent=2));assert r.returncode==0;print('PASS default packaged samples')
