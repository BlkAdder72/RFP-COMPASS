from pathlib import Path
import shutil
R=Path(__file__).resolve().parents[1];D=R/'citation-repair/history'
for arm in ('original','rebuild'):
 for name in ['CLAUDE_PROJECT_INSTRUCTIONS.txt','identity.md','rules.md','examples.md','reference/input-schema.md','reference/output-schema.md']:
  target=D/arm/name;target.parent.mkdir(parents=True,exist_ok=True)
  if target.exists():assert target.read_bytes()==(R/arm/name).read_bytes()
  else:shutil.copyfile(R/arm/name,target)
print('All six pre-repair knowledge files frozen for both arms.')
