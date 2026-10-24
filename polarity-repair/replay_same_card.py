from pathlib import Path
import hashlib,json,subprocess,sys
R=Path(__file__).resolve().parents[1];D=Path(__file__).resolve().parent
src=R/'red-team-guard/fixtures/B-negated-scope-and-private-headings.md';card=R/'red-team-guard/run-rebuild/B-negated-scope-and-private-headings/bid-compliance-card.md';out={}
for label,v in [('before',D/'before/rebuild/tools/validate_packet.py'),('after',R/'rebuild/tools/validate_packet.py')]:
 cmd=[sys.executable,'-B','-X','utf8',str(v),str(src),str(card)];p=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8');out[label]={'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'card_sha256':hashlib.sha256(card.read_bytes()).hexdigest(),'validator_sha256':hashlib.sha256(v.read_bytes()).hexdigest(),'command':cmd,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
assert out['before']['exit_code']==out['after']['exit_code']==0
assert 'S003, S006, S008' in out['before']['stdout'] and 'REVIEW' not in out['after']['stdout']
(D/'same-card-warning-replay.json').open('x',encoding='utf-8').write(json.dumps(out,indent=2));print('PASS exact old card: three false warning IDs -> zero')
