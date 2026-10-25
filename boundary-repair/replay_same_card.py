from pathlib import Path
import hashlib,json,subprocess,sys
R=Path(__file__).resolve().parents[1];D=Path(__file__).resolve().parent
source=R/'red-team-polarity/fixtures/B-negation-and-private-content.md';card=R/'red-team-polarity/run-rebuild/B-negation-and-private-content/bid-compliance-card.md';out={}
for name,v in [('before',D/'before/rebuild/tools/validate_packet.py'),('after',R/'rebuild/tools/validate_packet.py')]:
 cmd=[sys.executable,'-B','-X','utf8',str(v),str(source),str(card)];p=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8');out[name]={'command':cmd,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'validator_sha256':hashlib.sha256(v.read_bytes()).hexdigest(),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'card_sha256':hashlib.sha256(card.read_bytes()).hexdigest()}
(D/'same-card-warning-replay.json').open('x',encoding='utf-8').write(json.dumps(out,indent=2));print({n:x['stdout'] for n,x in out.items()})
