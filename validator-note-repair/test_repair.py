"""Offline differential checks; never call a model or rewrite a saved response."""
from pathlib import Path, PureWindowsPath
import argparse,hashlib,importlib.util,json,re,subprocess,sys
R=Path(__file__).resolve().parents[1];D=R/'validator-note-repair'
p=argparse.ArgumentParser();p.add_argument('--output-dir',required=True,type=Path)
p.add_argument('--stage',choices=['baseline','dentist','final'],required=True);a=p.parse_args()
O=a.output_dir.resolve();O.mkdir(parents=True,exist_ok=False)
def load(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
paths={'judged-original':R/'original/tools/validate_packet.py','pre-fix':D/'before/rebuild/tools/validate_packet.py','candidate':R/'rebuild/tools/validate_packet.py'}
mods={k:load(v,k.replace('-','_')) for k,v in paths.items()}
m=mods['candidate'];records=[];checks={}
def evaluate(label,source,cards,expected_excluded=None):
 result={}
 for name,mod in mods.items():
  errors,notes=mod.validate(source,cards)
  result[name]={'errors':errors,'notes':notes,'strict_pass':not errors}
 records.append({'case':label,'source':str(source.relative_to(R)),'cards':[str(v.relative_to(R)) for v in cards],'results':result})
 checks[label+':strict_same']=result['candidate']['errors']==result['pre-fix']['errors']
 if expected_excluded is not None:
  notes='\n'.join(result['candidate']['notes'])
  # A date/contact on S002 must retain the appropriate warning unless the
  # complete private statement is trusted, only12 and outside required scope.
  hinted=any('REVIEW' in n and 'S002' in n for n in result['candidate']['notes'])
  checks[label+':hint']=hinted is not expected_excluded
 return result
date='November 24, 2026, at 9:00 AM'
dentist='Dentist appointment: '+date+'.'
contact='Call Morgan at personal@example.invalid about the birthday dinner.'
cases=[
 ('dentist-private',dentist,[],True),
 ('birthday-contact-private',contact,[],a.stage=='final'),
 ('unknown-date','Meeting: '+date+'.',[],False),
 ('unknown-contact','Call Morgan at personal@example.invalid about the meeting.',[],False),
 ('dentist-must','You must attend the dentist appointment on '+date+'.',[],False),
 ('dentist-mixed',dentist+' Return offers by '+date+'.',[],False),
 ('dentist-unknown-action',dentist+' Check attendance at '+date+'.',[],False),
 ('dentist-tail','Dentist appointment: '+date+' and submit the registration.',[],False),
 ('clinical-dentist',dentist,['Clinical services appointments:'],False),
 ('required-dentist',dentist,['Mandatory events:'],False),
 ('required-private-heading',dentist,['Attendance is mandatory at the events in the section headed Private calendar.','Private calendar'],False),
 ('contact-must','You must '+contact.lower(),[],False),
 ('contact-mixed',contact+' Proposals are due '+date+'.',[],False),
 ('contact-offers',contact+' Lodge offers by '+date+'.',[],False),
 ('contact-unknown-action',contact+' Confirm attendance at '+date+'.',[],False),
 ('clinical-contact',contact,['Patient services appointments:'],False),
 ('contact-required-context',contact,['Attendance is mandatory at these events:'],False),
 ('private-anchor-only','Meeting: '+date+'.',[],False),
 ('unknown-contact-private-address','Call Morgan at personal@example.invalid about the proposal.',[],False),
]
for name,body,prefix,excluded in cases:
 if a.stage=='baseline':excluded=False
 t=O/'fixtures'/name;t.mkdir(parents=True)
 # Prefix IDs sort before S002; all keep an unrelated-looking anchor to test
 # that neither it nor private email local parts authorize suppression.
 rows=[(f'S000{i}','unrelated private notes',v) for i,v in enumerate(prefix)]
 rows+=[('S001','unrelated private notes','City requests proposals.'),('S002','unrelated private notes',body)]
 source=t/'source-packet.md';source.write_bytes(('\n'.join(' | '.join(v) for v in rows)+'\n').encode())
 card=t/'card.md';card.write_bytes((m.TITLE+'\n\n'+'\n\n'.join(h+'\n'+('\n'.join('- “'+v+'” [source: source-packet.md:'+s+'; '+anchor+']' for s,anchor,v in rows) if i==12 else '- not in source') for i,h in enumerate(m.HEADINGS,1))+'\n').encode())
 evaluate(name,source,[card],excluded)
 # Exact-copy trust is independent of the new private grammar.
 if name in ('dentist-private','birthday-contact-private'):
  raw=card.read_text(encoding='utf-8')
  for kind,mut in [('quote',raw.replace(body,body+' altered',1)),('anchor',raw.replace('S002; unrelated private notes','S002; other anchor',1)),('id',raw.replace('md:S002;','md:S999;',1))]:
   bad=t/(kind+'.md');bad.write_bytes(mut.encode());r=evaluate(name+'-bad-'+kind,source,[bad]);checks[name+'-bad-'+kind+':reject']=not r['candidate']['strict_pass']
 # Putting personal content into operational sections must not hide hints.
 if name in ('dentist-private','birthday-contact-private'):
  raw=card.read_text(encoding='utf-8');bullet='- “'+body+'” [source: source-packet.md:S002; unrelated private notes]'
  bad=t/'wrong-placement.md';bad.write_bytes(raw.replace(m.HEADINGS[0]+'\n- not in source',m.HEADINGS[0]+'\n'+bullet).encode());evaluate(name+'-wrong-placement',source,[bad],False)
# Every exported saved native response, including known failures/refusals.
inputs=json.loads((R/'route-repair/final-inputs.json').read_text())
for arm in ('original','rebuild'):
 for key in inputs['fixtures']:
  t=R/'route-repair/evidence'/arm/key;parts=sorted(t.glob('raw-response-part-*.md')) or ([t/'raw-response.md'] if (t/'raw-response.md').exists() else [])
  if parts:
   r=evaluate('saved:'+arm+':'+key,R/'route-repair/inputs'/key/'source-packet.md',parts)
   if arm=='rebuild' and key=='core-B-personal-note':
    ns=r['candidate']['notes'];checks['saved_dentist_fixed']=not any('REVIEW' in n and 'S003' in n for n in ns) if a.stage!='baseline' else any('REVIEW' in n and 'S003' in n for n in ns)
    checks['saved_contact_fixed']=not any('REVIEW' in n and 'S004' in n for n in ns) if a.stage=='final' else any('REVIEW' in n and 'S004' in n for n in ns)
# Frozen Q8 and shipped full-length card use the same bytes for all arms.
for kind in ('contained','missed-deadline'):
 r=evaluate('Q8:'+kind,R/'fixtures/A-stapled-thread.md',[R/'run-original/Q8-validator'/(kind+'.md')])
 if kind=='missed-deadline':checks['real_deadline_hint']=all(any('REVIEW' in n and 'S002' in n for n in v['notes']) for v in r.values())
for name in m.SAMPLES:
 r=evaluate('sample:'+name,R/'rebuild/samples'/name/'source-packet.md',[R/'rebuild/samples'/name/'bid-compliance-card.md']);checks['sample:'+name]=r['candidate']['strict_pass']
# Retained controls are evaluated fairly by all three implementations, without
# changing their old expected outputs. Candidate must preserve pre-fix errors
# and every old review hint on these obligation/scope/corruption adversaries.
retained=json.loads((R/'native-repair/stages/C3-warning/results.json').read_text())
for i,row in enumerate(retained):
 args=[]
 for arg in row['command'][5:]:
  wp=PureWindowsPath(arg)
  if 'Competition 15' in wp.parts:arg=str(R.joinpath(*wp.parts[wp.parts.index('Competition 15')+1:]))
  args.append(Path(arg))
 r=evaluate('retained:'+str(i)+':'+row['name'],args[0],args[1:])
 checks['retained:'+str(i)+':notes_unchanged']=r['candidate']['notes']==r['pre-fix']['notes']
 # Reconstruct previous CLI records to check fixture replay fidelity.
 expected_errors=r['pre-fix']['errors'];checks['retained:'+str(i)+':expected_exit']=bool(expected_errors)==bool(row['exit_code'])
res={'stage':a.stage,'passed':all(checks.values()),'checks':checks,'records':records,'validators':{k:{'path':str(v.relative_to(R)),'sha256':hashlib.sha256(v.read_bytes()).hexdigest()} for k,v in paths.items()},'model_calls':0,'published':False}
(O/'results.json').write_bytes(json.dumps(res,ensure_ascii=False,indent=2).encode())
print(json.dumps({'stage':a.stage,'cases':len(records),'checks':len(checks),'passed':res['passed'],'failed':[k for k,v in checks.items() if not v]}))
raise SystemExit(0 if res['passed'] else 1)
