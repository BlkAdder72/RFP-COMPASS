"""Hash staged Git bytes; preserve and explicitly verify working-copy variants."""
from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parents[1];D=R/'validator-note-repair';P=D/'EVIDENCE_SHA256.json'
assert not P.exists(),'Do not overwrite an evidence manifest'
items=[]
for row in subprocess.check_output(['git','ls-files','--stage','-z','--','validator-note-repair','route-repair','documentation-sync','rebuild','README.md','results.md','SUBMISSION_COMMENT.md','packaging/COMPLIANCE.md','run-original/README.md','run-rebuild/README.md','tools/verify_submission.py'],cwd=R).split(b'\0'):
 if row:
  fields,name=row.split(b'\t',1);name=name.decode()
  if name!='validator-note-repair/EVIDENCE_SHA256.json':items.append((name,fields.decode().split()[1]))
request=''.join(h+'\n' for n,h in items).encode()
data=subprocess.run(['git','cat-file','--batch'],cwd=R,input=request,capture_output=True,check=True).stdout
pos=0;manifest={};variants=json.loads((D/'portability.json').read_text())['variants'];seen=[]
for name,h in items:
 end=data.index(b'\n',pos);head=data[pos:end].split();size=int(head[2]);pos=end+1
 blob=data[pos:pos+size];pos+=size+1
 assert head[0].decode()==h and head[1]==b'blob'
 working=(R/name).read_bytes()
 if working!=blob:
  v=variants[name]
  assert hashlib.sha256(working).hexdigest()==v['prior_working_sha256'] and hashlib.sha256(blob).hexdigest()==v['git_canonical_sha256']
  assert working.replace(b'\r\n',b'\n')==blob.replace(b'\r\n',b'\n');seen.append(name)
 manifest[name]=hashlib.sha256(blob).hexdigest()
P.write_bytes(json.dumps(manifest,indent=2).encode())
print(json.dumps({'canonical_files':len(manifest),'verified_working_variants':seen,'raw_files_changed':0}))
