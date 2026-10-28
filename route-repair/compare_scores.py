from pathlib import Path
import json
R=Path.cwd(); A=R/'route-repair/analysis-final'; B=R/'.run-work/route-reproduction'
a=json.loads((A/'scores.json').read_text(encoding='utf-8')); b=json.loads((B/'scores.json').read_text(encoding='utf-8'))
def norm(v):
 if isinstance(v,dict):return {k:norm(x) for k,x in v.items()}
 if isinstance(v,list):return [norm(x) for x in v]
 if isinstance(v,str):
  for p in (A,B):
   v=v.replace(str(p),'OUTPUT').replace(p.as_posix(),'OUTPUT')
  return v
 return v
ok=norm(a)==norm(b)
(R/'route-repair/reproducibility-check.json').write_text(json.dumps({'passed':ok,'method':'independent fresh score; exact JSON comparison with only analysis-output directory prefixes normalized','first':'route-repair/analysis-final','second':'.run-work/route-reproduction'},indent=2),encoding='utf-8')
assert ok
print('Independent complete scoring reproduced')
