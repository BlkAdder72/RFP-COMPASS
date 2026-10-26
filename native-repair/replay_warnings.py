"""Compare unchanged full-RFP cards with pre-repair and current advisory logic."""
from pathlib import Path
import hashlib,json,subprocess,sys
D=Path(__file__).resolve().parent; R=D.parent; records=[]
for label,base in [('retained-native',R/'claude-native'),('fresh-native',D)]:
    source=base/'inputs/full-Z-full-length-noisy/source-packet.md'
    parts=sorted((base/'evidence/rebuild/full-Z-full-length-noisy').glob('raw-response-part-*.md'))
    for version,validator in [('before',D/'before/rebuild/tools/validate_packet.py'),('after',R/'rebuild/tools/validate_packet.py')]:
        cmd=[sys.executable,'-B','-X','utf8',str(validator),str(source),*[str(p) for p in parts]]
        r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8')
        records.append({'case':label,'version':version,'command':cmd,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'raw_sha256':[hashlib.sha256(p.read_bytes()).hexdigest() for p in parts],'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
for case in ('retained-native','fresh-native'):
    before,after=[r for r in records if r['case']==case]
    assert before['source_sha256']==after['source_sha256'] and before['raw_sha256']==after['raw_sha256']
    assert before['exit_code']==after['exit_code']==0
    assert 'S139' in before['stdout'] and 'S139' not in after['stdout']
assert 'S098' in records[-1]['stdout'], 'A real contact-route warning must remain visible'
(D/'same-card-warning-replay.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS: same-card false evaluation warning removed on old and fresh full RFP; genuine contact hint retained')
