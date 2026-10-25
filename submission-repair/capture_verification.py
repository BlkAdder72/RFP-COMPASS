from pathlib import Path
import subprocess,sys,json
R=Path(__file__).resolve().parents[1];D=R/'submission-repair';cmd=[sys.executable,'-B','-X','utf8',str(D/'verify.py')];r=subprocess.run(cmd,cwd=R,capture_output=True,text=True,encoding='utf-8')
for n,t in [('verification-command.json',json.dumps(cmd)),('verification-stdout.txt',r.stdout),('verification-stderr.txt',r.stderr),('verification-exit.txt',str(r.returncode))]:(D/n).open('x',encoding='utf-8',newline='\n').write(t)
if r.returncode:print(r.stdout,r.stderr);raise SystemExit(r.returncode)
(D/'verification.json').open('x',encoding='utf-8',newline='\n').write(json.dumps(json.loads(r.stdout),indent=2));print(r.stdout)
