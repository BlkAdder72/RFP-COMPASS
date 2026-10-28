"""Fair offline replay of the earlier 20 native cards, including full RFP parts."""
from pathlib import Path
import importlib.util,json,sys
R=Path(__file__).resolve().parents[1];D=R/'validator-note-repair';O=D/'historical-native-replay.json'
assert not O.exists()
paths={'judged-original':R/'original/tools/validate_packet.py','pre-fix':D/'before/rebuild/tools/validate_packet.py','candidate':R/'rebuild/tools/validate_packet.py'}
mods={}
for name,path in paths.items():
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);mods[name]=m
records=[];checks={}
for arm in ['original','rebuild']:
 for t in sorted((R/'native-repair/evidence'/arm).iterdir()):
  if not t.is_dir():continue
  parts=sorted(t.glob('raw-response-part-*.md')) or ([t/'raw-response.md'] if (t/'raw-response.md').exists() else [])
  if not parts:continue
  source=R/'native-repair/inputs'/t.name/'source-packet.md'
  variants={'raw':parts}
  if t.name.startswith('full-'):
   derived=sorted((t/'derived-export').glob('part-*.md'))
   if derived:variants['preserved-derived']=derived
  for kind,files in variants.items():
   result={name:dict(zip(['errors','notes'],m.validate(source,files))) for name,m in mods.items()}
   key=arm+'/'+t.name+'/'+kind;checks[key]=result['pre-fix']['errors']==result['candidate']['errors']
   # Full-length saved outputs must preserve every existing procurement hint.
   if t.name.startswith('full-'):checks[key+':warnings']=result['pre-fix']['notes']==result['candidate']['notes']
   records.append({'case':key,'source':source.relative_to(R).as_posix(),'parts':[p.relative_to(R).as_posix() for p in files],'source_statements':sum(bool(line.strip()) for line in source.read_text(encoding='utf-8').splitlines()),'results':result})
out={'passed':all(checks.values()),'cases':len(records),'checks':checks,'records':records,'model_calls':0,'published':False}
O.write_bytes(json.dumps(out,ensure_ascii=False,indent=2).encode());print(json.dumps({k:v for k,v in out.items() if k not in ('records','checks')}));assert out['passed']
