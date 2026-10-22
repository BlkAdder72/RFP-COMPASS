from pathlib import Path
import subprocess,json,sys
R=Path(__file__).resolve().parents[1];D=R/'red-team-final';C=R/'dist/redteam-final-clone';O=D/'clone-evidence';assert not O.exists();O.mkdir()
commands=[('offline-audit',[sys.executable,'tools/verify_submission.py']),
          ('original-preflight',[sys.executable,'tools/run_arm.py','original','--output-dir','.run-work/audit-original','--preflight-only']),
          ('rebuild-preflight',[sys.executable,'tools/run_arm.py','rebuild','--output-dir','.run-work/audit-rebuild','--preflight-only'])]
records=[]
for label,args in commands:
    result=subprocess.run(args,cwd=C,capture_output=True,text=True,encoding='utf-8')
    (O/(label+'-stdout.txt')).write_text(result.stdout,encoding='utf-8');(O/(label+'-stderr.txt')).write_text(result.stderr,encoding='utf-8')
    record={'case':label,'command':args,'exit_code':result.returncode};records.append(record)
    assert result.returncode==0,(label,result.stdout,result.stderr)
assert not (C/'.run-work').exists(),'Preflight unexpectedly created workspace/output'
(D/'clone-results.json').write_text(json.dumps({'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=C).decode().strip(),
                                             'checks':records,'preflight_writes':False,'model_calls':0},indent=2),encoding='utf-8')
print('PASS: independent fresh-clone audit and real CLI preflights for both arms; no model calls or preflight writes.')
