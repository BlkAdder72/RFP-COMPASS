from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parents[1];D=Path(__file__).resolve().parent
nchecked=0
for commit,predicate in [('efb167b',lambda n:n.startswith('red-team-polarity/fixtures/') or n in ['red-team-polarity/expectations.json','red-team-polarity/control-definitions.json','red-team-polarity/PROTOCOL.md']),('4569421',lambda n:n.startswith('red-team-polarity/run-original/'))]:
 for rec in subprocess.check_output(['git','ls-tree','-r','-z',commit],cwd=R).split(b'\0'):
  if not rec:continue
  meta,name=rec.split(b'\t',1);n=name.decode()
  if predicate(n):
   data=(R/n).read_bytes();assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==meta.decode().split()[2],n;nchecked+=1
assert subprocess.run(['git','merge-base','--is-ancestor','efb167b','4569421'],cwd=R).returncode==0
(D/'frozen-and-baseline-verification.json').open('x').write(json.dumps({'passed':True,'files_checked_against_committed_blobs':nchecked,'freeze':'efb167b','original_baseline':'4569421'},indent=2));print('PASS frozen cases and original baseline bytes')
