from pathlib import Path
import hashlib,json,subprocess,shutil
R=Path(__file__).resolve().parents[1];D=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,t):p.parent.mkdir(parents=True,exist_ok=True);p.open('x',encoding='utf-8',newline='\n').write(t)
mutable=['README.md','results.md','SUBMISSION_COMMENT.md','packaging/COMPLIANCE.md','tools/verify_submission.py','rebuild/README.md','rebuild/rules.md','rebuild/reference/output-schema.md','rebuild/tools/validate_packet.py']
files=[p for p in subprocess.check_output(['git','ls-files','-z'],cwd=R).decode().split('\0') if p]
for n in mutable:
 p=D/'history'/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(R/n,p)
for arm in ['original','rebuild']:
 for n in ['CLAUDE_PROJECT_INSTRUCTIONS.txt','identity.md','rules.md','examples.md','reference/input-schema.md','reference/output-schema.md']:
  p=D/'baseline-knowledge'/arm/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(R/arm/n,p)
new(D/'preservation.json',json.dumps({'target':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),'files':{n:sha(R/n) for n in files},'mutable_paths':mutable,'artifacts':{p.name:sha(p) for p in (R/'dist').iterdir() if p.is_file()}},indent=2))
new(D/'fixtures/U-unseen-citations.md',(R/'red-team-citations/fixtures/U-unseen-citations.md').read_text(encoding='utf-8'))
new(D/'fixtures/V-required-response-info.md','S001 | RFP p. 5 §Response Contents | Required response contents:\nS002 | RFP p. 5 §Response Contents paragraph 2 | The applicant shall also provide information on the findings of external compliance inspections during the last two years.\nS003 | RFP p. 5 §Response Contents paragraph 3 | Provide a narrative describing prior quality assurance findings with the proposal.\n')
new(D/'fixtures/W-personal-graduation.md','S001 | Unrelated personal correspondence, attached in error | My niece’s graduation celebration is November 19, 2026 at 7 PM.\n')
expect={'U-unseen-citations':{'required':{**{f'S{i:03}':[4,5] for i in range(1,9)},'S009':[6]},'exclusive':{'S010':[12]}},'V-required-response-info':{'required':{'S002':[4,5],'S003':[4,5]},'exclusive':{}},'W-personal-graduation':{'required':{},'exclusive':{'S001':[12]}}}
for name,v in expect.items():v['source_sha256']=sha(D/'fixtures'/(name+'.md'))
new(D/'expectations.json',json.dumps(expect,indent=2))
full=json.loads((R/'citation-repair/full-length-expectations.json').read_text());full['routing']['S076']=[4,5];full['packet_sha256']=sha(R/'hardening/fixtures/Z-full-length-noisy.md');new(D/'full-expectations.json',json.dumps(full,indent=2))
new(D/'protocol.md','''# Final repair frozen protocol
Preserve every pre-stage tracked file. Mutable files are snapshotted in history; all six baseline knowledge files in baseline-knowledge. Frozen questions.md is unchanged. Preserve all existing audit failures and sealed delivery files.
Run original baseline before candidate edits: original root A–E core fixtures, new U/V/W fixtures in lexical order, then unchanged 221-statement full-length RFP. Commit baseline raw evidence before editing candidate. Then run rebuilt core, U/V/W and full in the same order, same unchanged runners, model gpt-6-astra medium, wrappers, inputs and continuation policy. One run per version, no best-of, retry or raw correction. Failure is retained. No answer keys, feedback, questions or scorers supplied to models.
Full-length prospective matrix retains all prior checks and adds S076 in sections 4 and 5. New required-information and graduation sources generalize the observed defects. U is the previously frozen unseen-anchor fixture, now a known regression fixture; do not call this a new holdout. W is a known failure case. V is synthetic. Q7/Q8 are deterministic file/default-tool tests, not model questions. Same Q8 cards, no sidecars.
Tighten rebuilt validator quotation comparisons and curly delimiters; original remains untouched. Test both validators on identical exact and mutated evaluator-built cards, record expected original failures. Require genuine-deadline and cross-anchor protections, known false-warning closure, unchanged anchors and coverage, no new acceptance of invalid cards. Replay historical cards honestly: stricter validation may reject historical outputs accepted under prior tolerances; preserve them and disclose differences.
All results remain local. Package new committed source and complete Git history into a new release directory without replacing any prior sealed artifact. Verify from a fresh clone and extracted ZIP. No publish action.
''')
print('Preservation and prospective expectations frozen')
