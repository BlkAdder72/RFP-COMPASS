from pathlib import Path
import subprocess,sys
R=Path(__file__).resolve().parents[1];arm=sys.argv[1]
assert arm in ['original','rebuild']
for kind,script,extra in [('core','tools/run_arm.py',[]),('new','tools/run_arm.py',['--fixtures-dir',str(R/'submission-repair/fixtures')]),('full','hardening/run_full.py',[])]:
 cmd=[sys.executable,'-B','-X','utf8',str(R/script),arm,'--output-dir',str(R/('run-'+arm)/('submission-repair-'+kind)),*extra]
 folder=R/'submission-repair';out=folder/(arm+'-'+kind+'-runner-stdout.txt');err=folder/(arm+'-'+kind+'-runner-stderr.txt')
 with out.open('xb') as o,err.open('xb') as e:r=subprocess.run(cmd,stdout=o,stderr=e)
 (folder/(arm+'-'+kind+'-runner-exit.txt')).open('x').write(str(r.returncode))
 print(arm,kind,r.returncode,flush=True)
 if r.returncode:raise SystemExit('Failed raw run retained; no retry')
