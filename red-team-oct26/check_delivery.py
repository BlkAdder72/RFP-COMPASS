from pathlib import Path
import hashlib,json,subprocess,zipfile,sys
R=Path(__file__).resolve().parents[1];D=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((D/'preservation.json').read_text());bad=[]
for n,h in {**m['files'],**m['artifacts']}.items():
 if sha(R/n)!=h:bad.append(n)
assert not bad,bad
assert (R/'questions.md').read_bytes()==subprocess.check_output(['git','show','bfdd812:questions.md'],cwd=R)
feedback=Path('C:/Users/mmazu/Downloads/feedback/feedback/matthew-mazur.md')
spec=Path('C:/Users/mmazu/.codex/attachments/9a768b27-c7c9-4cd0-a934-4f4735e05b4e/Pasted text.txt')
source_checks={}
for label,external,internal in [('feedback',feedback,R/'feedback.md'),('spec',spec,R/'packaging/competition-spec.txt')]:
 source_checks[label]={'external_available':external.exists()}
 if external.exists():
  source_checks[label]['exact_bytes']=external.read_bytes()==internal.read_bytes()
  source_checks[label]['same_text_normalized_newlines']=external.read_text(encoding='utf-8-sig')==internal.read_text(encoding='utf-8-sig')
  source_checks[label]['external_sha256']=sha(external)
release=R/'dist/final-submission-release';z=release/'RFP-COMPASS-Comp15-source.zip'
with zipfile.ZipFile(z) as archive:
 names=[n for n in archive.namelist() if not n.endswith('/')]
 # The sealed release's own manifest defines its paths; permit a single enclosing folder.
 entries={n:archive.read(n) for n in names}
 missing=[]
 for n,h in m['files'].items():
  hits=[k for k in [n,'RFP-COMPASS-Comp15/'+n] if k in entries]
  if not hits or hashlib.sha256(entries[hits[0]]).hexdigest()!=h:missing.append(n)
 assert not missing,missing[:20]
out={'target':m['target'],'all_prior_tracked_preserved':len(m['files']),'all_sealed_files_preserved':len(m['artifacts']),'questions_unchanged':True,'sealed_zip_exact_source_files':len(m['files']),'sealed_zip_sha256':sha(z),'user_source_checks':source_checks,'method':'Read-only preservation and archive-byte check. Fresh-clone compliance from sealed FINAL_VERIFICATION.json is historical, not rerun here.','published':False}
(D/'delivery-checks.json').open('x',encoding='utf-8').write(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
