from pathlib import Path,PureWindowsPath
import argparse,json,subprocess,sys
D=Path(__file__).resolve().parent;R=D.parent
parser=argparse.ArgumentParser(description='Replay retained offline controls into a new directory without changing evidence.')
parser.add_argument('--output-dir',type=Path,default=D/'stages/R4-retained-validation')
O=parser.parse_args().output_dir.resolve();O.mkdir(parents=True,exist_ok=False);results=[]
for kind,path in [('export','native-repair/stages/C4-final-export/results.json'),('warning','native-repair/stages/C3-warning/results.json')]:
 rows=json.loads((R/path).read_text(encoding='utf-8'))
 for i,row in enumerate(rows):
  old=row['command'];args=[]
  for arg in old[4:]:
   wp=PureWindowsPath(arg)
   if 'Competition 15' in wp.parts:
    j=wp.parts.index('Competition 15');arg=str(R.joinpath(*wp.parts[j+1:]))
   args.append(arg)
  if kind=='export':args[-1]=str(O/'exports'/row['name'])
  cmd=[sys.executable,'-B','-X','utf8',*args];p=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8');passed=p.returncode==row['exit_code']
  if kind=='warning':passed=passed and p.stdout==row['stdout'] and p.stderr==row['stderr']
  results.append({'kind':kind,'name':row['name'],'command':cmd,'expected_exit_code':row['exit_code'],'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'passed':passed})
 (O/(kind+'-results.json')).write_text(json.dumps([r for r in results if r['kind']==kind],indent=2,ensure_ascii=False),encoding='utf-8')
 print(kind,len(rows),all(r['passed'] for r in results if r['kind']==kind),flush=True)
assert all(r['passed'] for r in results)
