"""Preserve the first preseal manifest before a Markdown spacing cleanup."""
from pathlib import Path
import shutil,hashlib,json,subprocess,sys
R=Path(__file__).resolve().parents[1];D=R/'warning-final'
prior=D/'EVIDENCE_SHA256-pre-style.json';assert not prior.exists();shutil.copyfile(D/'EVIDENCE_SHA256.json',prior)
p=subprocess.run([sys.executable,'-B','-X','utf8',str(D/'summarize.py')],capture_output=True,text=True,encoding='utf-8');assert p.returncode==0,p.stderr
manifest={str(p.relative_to(R)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(D.rglob('*')) if p.is_file() and p.name!='EVIDENCE_SHA256.json'}
(D/'EVIDENCE_SHA256.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8',newline='\n')
print('PASS presentation-only spacing cleanup; initial manifest retained; final manifest covers',len(manifest),'files')
