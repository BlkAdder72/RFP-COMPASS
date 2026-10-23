from pathlib import Path
import subprocess,sys
R=Path(__file__).resolve().parents[1];arm=sys.argv[1]
assert arm in ['original','rebuild']
for kind,script,extra in [('core','tools/run_arm.py',[]),('new','tools/run_arm.py',['--fixtures-dir',str(R/'final-repair/fixtures')]),('full','hardening/run_full.py',[])]:
 cmd=[sys.executable,'-B','-X','utf8',str(R/script),arm,'--output-dir',str(R/('run-'+arm)/('final-repair-v2-'+kind)),*extra]
 folder=R/'final-repair';out=folder/(arm+'-v2-'+kind+'-runner-stdout.txt');err=folder/(arm+'-v2-'+kind+'-runner-stderr.txt')
 with out.open('xb') as o,err.open('xb') as e:r=subprocess.run(cmd,stdout=o,stderr=e)
 (folder/(arm+'-v2-'+kind+'-runner-exit.txt')).open('x').write(str(r.returncode))
 print(arm,kind,r.returncode,flush=True)
 if r.returncode:raise SystemExit('Failed raw run retained; no retry')
