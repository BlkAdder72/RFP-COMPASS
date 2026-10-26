from pathlib import Path
import hashlib,json,subprocess,shutil,importlib.util,sys
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[1];D=R/'claude-native'
def put(p,t):p.parent.mkdir(parents=True,exist_ok=True);p.open('x',encoding='utf-8',newline='\n').write(t)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files=[n for n in subprocess.check_output(['git','ls-files','-z']).decode().split('\0') if n]
put(D/'preservation.json',json.dumps({'target':subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),'tracked_sha256':{n:sha(R/n) for n in files}},indent=2))
names=['CLAUDE_PROJECT_INSTRUCTIONS.txt','identity.md','rules.md','examples.md','reference/input-schema.md','reference/output-schema.md'];manifest={'knowledge':{},'fixtures':{},'prompt':{}}
for arm in ['original','rebuild']:
 text='This attachment supplies the complete translation contract as six named files. Treat the project instructions and contract files as the translation contract. Do not use tools, browse, read other files or sessions, or import outside facts. Return only the requested card.\n\n'
 manifest['knowledge'][arm]={}
 for n in names:
  text+='<file name="'+n+'">\n'+(R/arm/n).read_text(encoding='utf-8')+'\n</file>\n\n';manifest['knowledge'][arm][n]=sha(R/arm/n)
 p=D/'inputs'/arm/'translation-contract.md';put(p,text);manifest['knowledge'][arm]['bundle_sha256']=sha(p)
fixtures=[('core',p) for p in sorted((R/'fixtures').glob('*.md'))]+[('new',p) for p in sorted((R/'warning-final/fixtures').glob('*.md'))]+[('full',R/'hardening/fixtures/Z-full-length-noisy.md')]
for kind,p in fixtures:
 key=kind+'-'+p.stem;folder=D/'inputs'/key;folder.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,folder/'source-packet.md');manifest['fixtures'][key]={'source':str(p.relative_to(R)).replace('\\','/'),'sha256':sha(p)}
prompt='The attached translation-contract.md supplies the six named project files. Use the attached source-packet.md as the only active input. Apply the RFP Compass contract and return bid-compliance-card.md. Do not use tools, browse, access other files or sessions, or discuss this evaluation.\n'
put(D/'prompt.txt',prompt);manifest['prompt']['sha256']=sha(D/'prompt.txt');put(D/'inputs.json',json.dumps(manifest,indent=2))
shutil.copyfile(R/'warning-final/expectations.json',D/'expectations.json');shutil.copyfile(R/'warning-final/full-expectations.json',D/'full-expectations.json')
put(D/'PROTOCOL.md','''# Native Claude Desktop acceptance — 2026-10-26
User explicitly authorized running Competition15 in Claude App and viewing its current window. VIP eligibility is confirmed by the user. Preserve sealed source f3ff5c65, all old evidence and every old seal. No product edits or publication. Root Q1–Q8 and all sources/selected expected answers are unchanged. The canonical OpenAI comparison remains a separate experiment; this is a separately frozen native acceptance comparison, not a relabeling of old runs.
Observed native Claude Desktop Chat model: Opus5.5 Medium (display name, not an independently verified API model revision). Record exact settings before first trial; keep them fixed. Use fresh ordinary chats outside existing projects in order core A–E, supplemental A–C, full221; complete the original arm before the rebuilt arm. Attach only the corresponding six-file translation-contract.md bundle and one source-packet.md via native file upload, plus the same prompt.txt. Exclude questions, expected answers, feedback, previous responses, tools and opposite-arm files. The bundle's file bodies are byte-preserving text reads of the six frozen source files; bundle/source hashes are recorded.
No tools requested/permitted during translation; inspect visible activity, but native UI lacks the machine event audit of the CLI. Global host instructions, saved account context and native attachment parsing are uncontrolled and must be disclosed. UI settings/model label are evidence, not proof of a server revision. Use exactly continue in the same chat when the contractual marker appears. Never correct or retry a completed answer or select a best result. Retain all failures and any transport retry explanation.
Preserve the actual exported/copied response text through supported native UI where possible, its native UI observations, input hashes and chat identity. Never reconstruct a purported raw Markdown card from expected answers or silently turn rendered UI text into a claimed raw response. If only rendered text can be obtained, label it and limit grading accordingly. Validate exact quotes, opaque anchors, coverage and shape separately from selected routing and private warnings. Q7/Q8 remain file/tool checks, not model questions. Stop and report concrete app/permission/usage/export blockers honestly. Existing sealed report/package remain unchanged; native evidence and report are separate until results can be reviewed.
''')
put(D/'environment.json',json.dumps({'status':'prepared; no model trial sent yet','platform':'native Claude Desktop on Windows via Computer Use','visible_model':'Opus 5.5','visible_reasoning':'Medium','project':'fresh chats outside existing projects','delivery':'native attachments: translation-contract.md and source-packet.md','prior_source':manifest['knowledge'],'VIP_eligibility':'confirmed by user 2026-10-26','published':False},indent=2))
print('Prepared',len(fixtures),'frozen inputs for each arm; prior tracked files',len(files))
