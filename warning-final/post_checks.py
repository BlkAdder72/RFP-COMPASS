from pathlib import Path
import subprocess,sys,json,hashlib,shutil
R=Path(__file__).resolve().parents[1];D=R/'warning-final'
def save(p,t):p.parent.mkdir(parents=True,exist_ok=True);p.open('x',encoding='utf-8',newline='\n').write(t)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def copy_full():
 copy=R/'rebuild/run-results/warning-final-full';shutil.copytree(R/'run-rebuild/warning-final-full',copy);save(copy/'.gitattributes','* -text\n')
if '--copy-only' in sys.argv:
 copy_full();print('PASS exact full-run copy created');raise SystemExit(0)
source=R/'red-team-oct26/fixtures/B-personal-boundaries.md';card=R/'red-team-oct26/run-rebuild/B-personal-boundaries/bid-compliance-card.md';out={}
for label,v in [('before',D/'before/rebuild/tools/validate_packet.py'),('after',R/'rebuild/tools/validate_packet.py')]:
 p=subprocess.run([sys.executable,'-B','-X','utf8',str(v),str(source),str(card)],capture_output=True,text=True,encoding='utf-8');out[label]={'source_sha256':sha(source),'card_sha256':sha(card),'validator_sha256':sha(v),'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
assert 'S002, S004' in out['before']['stdout'] and 'REVIEW' not in out['after']['stdout'] and out['after']['exit_code']==0
save(D/'same-card-warning-replay.json',json.dumps(out,indent=2))
parts=sorted((R/'run-rebuild/submission-repair-full').glob('part-*/bid-compliance-card.md'),key=lambda p:int(p.parent.name.split('-')[1]))
cmd=[sys.executable,'-B','-X','utf8',str(R/'rebuild/tools/validate_packet.py'),str(R/'hardening/fixtures/Z-full-length-noisy.md'),*[str(p) for p in parts]];p=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8');assert p.returncode!=0 and 'S100' in p.stdout
save(D/'retained-S100-rejection.json',json.dumps({'passed':True,'command':cmd,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'part_sha256':{str(f.relative_to(R)).replace('\\','/'):sha(f) for f in parts}},indent=2))
if '--defer-copy' not in sys.argv:copy_full()
print('PASS same-card warnings removed, bad S100 still rejected; full copy '+('deferred' if '--defer-copy' in sys.argv else 'created'))
