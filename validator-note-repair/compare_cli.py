"""Reproduce validator comparisons through the public CLI on the same files."""
from pathlib import Path
import argparse,json,subprocess,sys
R=Path(__file__).resolve().parents[1];D=R/'validator-note-repair'
p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);a=p.parse_args();assert not a.output.exists()
s=json.loads((D/'stage-2-contact/results.json').read_text());records=[];checks={}
paths={k:R/v['path'] for k,v in s['validators'].items()}
for row in s['records']:
 if not row['case'].startswith(('saved:','Q8:','sample:')):continue
 result={}
 for arm,validator in paths.items():
  cmd=[sys.executable,'-B','-X','utf8',str(validator),str(R/row['source']),*[str(R/n) for n in row['cards']]]
  run=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8')
  result[arm]={'command':cmd,'exit_code':run.returncode,'stdout':run.stdout,'stderr':run.stderr}
 checks[row['case']]=result['pre-fix']['exit_code']==result['candidate']['exit_code'] and all(not v['stderr'] for v in result.values())
 records.append({'case':row['case'],'results':result})
out={'passed':all(checks.values()),'checks':checks,'records':records,'cli_calls':3*len(records),'model_calls':0,'published':False}
a.output.write_bytes(json.dumps(out,ensure_ascii=False,indent=2).encode());print(json.dumps({k:v for k,v in out.items() if k not in ('records','checks')}));assert out['passed']
