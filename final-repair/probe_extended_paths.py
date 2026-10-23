from pathlib import Path
import os,subprocess,sys,json
R=Path(__file__).resolve().parents[1]
if len(sys.argv)>1:
 print(json.dumps({'file':__file__,'resolved':str(Path(__file__).resolve()),'root':str(R),'questions_readable':(R/'questions.md').is_file()}));raise SystemExit(0)
if os.name=='nt':
 script='\\\\?\\'+str(Path(__file__).resolve())
 r=subprocess.run([sys.executable,script,'child'],capture_output=True,text=True,encoding='utf-8');print(r.stdout);print(r.stderr);assert r.returncode==0 and json.loads(r.stdout)['root'].startswith('\\\\?\\')
