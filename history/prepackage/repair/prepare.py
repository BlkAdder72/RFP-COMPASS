from pathlib import Path
import hashlib,json,subprocess,shutil
R=Path(__file__).resolve().parents[1]; D=R/'repair'
target=D/'preservation.json';assert not target.exists()
names=subprocess.check_output(['git','ls-files','-z'],cwd=R).decode().split('\0')
records={n:hashlib.sha256((R/n).read_bytes()).hexdigest() for n in names if n and n!='README.md'}
target.write_text(json.dumps({'baseline_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),
                             'protected_files':records},indent=2),encoding='utf-8')
print('Recorded '+str(len(records))+' protected files')
