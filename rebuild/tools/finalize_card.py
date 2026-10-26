#!/usr/bin/env python3
"""Preserve raw exports; restore canonical-Unicode-only anchor drift, then validate.

This is an explicit export stage, not a relaxed validator or model transcript.
Never changes quotations, IDs, routing, whitespace, entities or non-equivalent
anchors. Raw files remain untouched; every anchor change is recorded by code point.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import unicodedata
from validate_packet import validate

BULLET=re.compile(r'^- “(.*)” \[source: source-packet\.md:(S\d+); (.*)\]$')
def sha(data): return hashlib.sha256(data).hexdigest()
def restore(source, raw):
    rows={}
    for line in source.read_text(encoding='utf-8-sig').splitlines():
        if not line.strip(): continue
        fields=line.split(' | ',2)
        if len(fields)!=3 or fields[0] in rows: raise ValueError('Malformed or repeated packet row')
        rows[fields[0]]=(fields[1],fields[2])
    text=raw.decode('utf-8'); result=[]; changes=[]
    for number,line in enumerate(text.splitlines(keepends=True),1):
        content=line.rstrip('\r\n'); ending=line[len(content):]
        m=BULLET.fullmatch(content)
        if m and m[2] in rows:
            body,sid,anchor=m.groups(); expected,quote=rows[sid]
            if anchor!=expected and body==quote and unicodedata.normalize('NFC',anchor)==unicodedata.normalize('NFC',expected):
                changes.append({'line':number,'id':sid,'field':'anchor','before':anchor,'after':expected,'before_codepoints':[f'U+{ord(c):04X}' for c in anchor],'after_codepoints':[f'U+{ord(c):04X}' for c in expected]})
                content=content[:m.start(3)]+expected+content[m.end(3):]
        result.append(content+ending)
    return ''.join(result).encode('utf-8'),changes

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('source',type=Path);p.add_argument('parts',nargs='+',type=Path)
    p.add_argument('--output-dir',type=Path,required=True)
    a=p.parse_args()
    if a.output_dir.exists(): p.error('output directory already exists; no evidence may be overwritten')
    if len({x.resolve() for x in a.parts})!=len(a.parts):p.error('duplicate input part')
    before=[x.read_bytes() for x in a.parts]
    source_before=a.source.read_bytes()
    try: restored=[restore(a.source,b) for b in before]
    except (ValueError,UnicodeError) as e: print(json.dumps({'status':'rejected','error':str(e)}));return 1
    a.output_dir.mkdir(parents=True,exist_ok=False)
    staging=a.output_dir/'validation-inputs';staging.mkdir()
    paths=[]
    for n,(data,_) in enumerate(restored,1):
        f=staging/f'part-{n:02}.md';f.write_bytes(data);paths.append(f)
    errors,notes=validate(a.source,paths)
    if errors:
        rejection={'status':'rejected','errors':errors,'notes':notes}
        (a.output_dir/'REJECTED.json').write_text(json.dumps(rejection,ensure_ascii=False,indent=2),encoding='utf-8')
        print(json.dumps(rejection,ensure_ascii=False));return 1
    # Refuse concurrent raw/source replacement before creating a new derived folder.
    assert all(f.read_bytes()==b for f,b in zip(a.parts,before)),'raw changed during export'
    assert a.source.read_bytes()==source_before,'source changed during export'
    audit={'status':'validated derived export','source':str(a.source.resolve()),'source_sha256':sha(a.source.read_bytes()),'raw_model_success_claimed':False,'parts':[],'strict_errors':errors,'strict_notes':notes}
    for n,(f,b,(data,changes)) in enumerate(zip(a.parts,before,restored),1):
        name=f'part-{n:02}.md';(a.output_dir/name).write_bytes(data)
        audit['parts'].append({'raw_path':str(f.resolve()),'raw_sha256':sha(b),'output':name,'output_sha256':sha(data),'changes':changes})
    (a.output_dir/'export-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'status':audit['status'],'changes':sum(len(x['changes']) for x in audit['parts']),'parts':len(before)}));return 0
if __name__=='__main__':raise SystemExit(main())
