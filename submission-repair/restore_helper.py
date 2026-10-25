from pathlib import Path
import subprocess
R=Path(__file__).resolve().parents[1]
# The final phase keeps its frozen helper immutable. Causal warning-fix evidence
# comes from the preserved first comparison, where the warning code changed.
(R/'submission-repair/replay_same_card.py').write_bytes(subprocess.check_output(['git','show','b621c8883e9d10b6647bb36f76330ff00c036986:submission-repair/replay_same_card.py'],cwd=R))
print('Frozen helper restored exactly; final audit uses preserved causal replay')
