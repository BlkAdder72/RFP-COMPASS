from pathlib import Path
import hashlib,json,shutil,subprocess,sys
R=Path(__file__).resolve().parents[1];D=R/'warning-repair'
def run(label,args):
 r=subprocess.run([sys.executable,'-B','-X','utf8',*args],cwd=R,capture_output=True,text=True,encoding='utf-8')
 (D/(label+'-execution.json')).open('x',encoding='utf-8').write(json.dumps({'command':args,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr},indent=2))
 if r.returncode:raise SystemExit(label+' failed; evidence retained')
 return r.stdout
run('score-full-rebuild',['warning-repair/score_full.py','rebuild'])
full={}
for arm in ['original','rebuild']:full.update(json.loads((D/('full-length-results-'+arm+'.json')).read_text()))
(D/'full-length-results.json').open('x').write(json.dumps(full,indent=2))
source=R/'run-rebuild/warning-repair-full';target=R/'rebuild/run-results/warning-repair-full';shutil.copytree(source,target);(target/'.gitattributes').write_text('* -text\n',encoding='utf-8')
for p in source.rglob('*'):
 if p.is_file():assert p.read_bytes()==(target/p.relative_to(source)).read_bytes()
verification=json.loads(run('current-verification',['warning-repair/verify.py']));(D/'verification.json').open('x').write(json.dumps(verification,indent=2))
run('report-update',['warning-repair/report.py'])
print(json.dumps({'full_rebuild_passed':full['rebuild']['passed'],'integrity':verification},indent=2))
