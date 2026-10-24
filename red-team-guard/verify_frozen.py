from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parents[1];D=Path(__file__).resolve().parent
nchecked=0
for commit,predicate in [('40dede9',lambda n:n.startswith('red-team-guard/fixtures/') or n in ['red-team-guard/expectations.json','red-team-guard/control-definitions.json','red-team-guard/PROTOCOL.md']),('ba50915',lambda n:n.startswith('red-team-guard/run-original/'))]:
 for rec in subprocess.check_output(['git','ls-tree','-r','-z',commit],cwd=R).split(b'\0'):
  if not rec:continue
  meta,name=rec.split(b'\t',1);n=name.decode()
  if predicate(n):
   data=(R/n).read_bytes();assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==meta.decode().split()[2],n;nchecked+=1
assert subprocess.run(['git','merge-base','--is-ancestor','40dede9','ba50915'],cwd=R).returncode==0
(D/'frozen-and-baseline-verification.json').open('x').write(json.dumps({'passed':True,'files_checked_against_committed_blobs':nchecked,'freeze':'40dede9','original_baseline':'ba50915'},indent=2));print('PASS frozen cases and original baseline bytes')
