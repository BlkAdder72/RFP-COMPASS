from pathlib import Path
import shutil,json
R=Path(__file__).resolve().parents[1];D=R/'submission-repair';p=D/'REPORT.md';shutil.copyfile(p,D/'REPORT-before-citation-summary.md');t=p.read_text(encoding='utf-8')
t=t.replace('**HOLD: four private statements still leak in B.','**HOLD: four private statements still leak in B, and the full run has a rejected S100 citation.')
needle='## Recorded results';t=t.replace(needle,'The fresh full rebuilt run also substitutes a neighboring `pp. 9-10` anchor for S100’s literal `p. 9` in Section 6. The unchanged strict validator rejects this occurrence. This is a new exact-anchor regression relative to the first comparison’s rebuilt full run and the current original full run. The failed raw parts, first report draft and full score are preserved; no output is corrected. The third comparison’s pre-candidate citation addendum addresses source-row retrieval without relaxing the universal exact-anchor gate.\n\n'+needle)
p.write_text(t,encoding='utf-8',newline='\n');(R/'results.md').write_text(t,encoding='utf-8',newline='\n')
p=D/'SUMMARY.json';m=json.loads(p.read_text());m['acceptance']='HOLD — B private leakage and rejected full-RFP S100 citation';m['citation_regression']={'sid':'S100','section':6,'actual':'TBRPC Auditing RFP pp. 9-10 §7 Selection Process','expected':'TBRPC Auditing RFP p. 9 §7 Selection Process'};p.write_text(json.dumps(m,indent=2),encoding='utf-8',newline='\n')
print('Surfaced preserved S100 regression alongside B at report entry')
