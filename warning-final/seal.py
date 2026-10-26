from pathlib import Path
import subprocess,json,hashlib,sys
R=Path(__file__).resolve().parents[1];D=R/'warning-final'
p=subprocess.run([sys.executable,'-B','-X','utf8',str(D/'verify.py'),'--preseal'],capture_output=True,text=True,encoding='utf-8')
(D/'verification.json').open('x',encoding='utf-8',newline='\n').write(json.dumps({'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'note':'Preseal acceptance; final manifest is checked by default verify.py in the fresh delivery clone.'},indent=2));assert p.returncode==0,p.stderr
manifest={str(p.relative_to(R)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(D.rglob('*')) if p.is_file() and p.name!='EVIDENCE_SHA256.json'}
(D/'EVIDENCE_SHA256.json').open('x',encoding='utf-8',newline='\n').write(json.dumps(manifest,indent=2))
print('PASS preseal acceptance; manifest covers',len(manifest),'files')
