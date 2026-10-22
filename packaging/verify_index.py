"""Ensure staged Git blobs preserve the exact working bytes before packaging."""
from pathlib import Path
import hashlib,subprocess
R=Path(__file__).resolve().parents[1];count=0
for record in subprocess.check_output(['git','ls-files','--stage','-z'],cwd=R).split(b'\0'):
    if not record:continue
    metadata,path=record.split(b'\t',1);_,oid,stage=metadata.decode().split();assert stage=='0'
    name=path.decode();data=(R/name).read_bytes()
    actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert actual==oid,'Staged bytes differ (possible line-ending conversion): '+name
    count+=1
print(f'PASS: {count} staged files match exact working bytes.')
