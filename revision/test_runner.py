"""Model-free runner regressions; fake CLI text is never model evidence."""
from pathlib import Path
import importlib.util,tempfile,hashlib,json,subprocess,sys
from unittest.mock import patch
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[1];D=R/'revision'
spec=importlib.util.spec_from_file_location('runner',R/'tools/run_arm.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
results=[]
def snapshot(folder):return {str(p.relative_to(folder)):hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.rglob('*') if p.is_file()}
with tempfile.TemporaryDirectory(prefix='runner-test-',dir=R/'.run-work') as temp:
    box=Path(temp);m.ROOT=box
    for name in m.FILES:
        dst=box/'original'/name;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text('TEST KNOWLEDGE ONLY',encoding='utf-8')
    (box/'fixtures').mkdir();(box/'fixtures/A.md').write_text('S001 | test | TEST FIXTURE ONLY',encoding='utf-8')
    def invoke(extra,should_fail,cli=None):
        before=snapshot(box)
        try:
            with patch.object(m.subprocess,'run',side_effect=cli) if cli else patch.object(m.shutil,'which',return_value=None):m.main(['original','--fixtures-dir',str(box/'fixtures'),*extra])
        except SystemExit as error:
            if not should_fail:raise
            assert snapshot(box)==before,'Failed preflight mutated files'
            return str(error)
        assert not should_fail,'Expected failure'
    out=box/'existing';out.mkdir();(out/'environment.json').write_text('KEEP',encoding='utf-8')
    results.append({'case':'existing-output','result':invoke(['--output-dir',str(out)],True),'unchanged':True})
    results.append({'case':'missing-executable','result':invoke(['--output-dir',str(box/'new')],True),'unchanged':True})
    old=(box/'fixtures/A.md').read_bytes();(box/'fixtures/A.md').write_text('INVALID',encoding='utf-8')
    results.append({'case':'malformed-fixture','result':invoke(['--output-dir',str(box/'bad')],True),'unchanged':True});(box/'fixtures/A.md').write_bytes(old)
    def unsupported(command,**kwargs):return subprocess.CompletedProcess(command,0,'old CLI','')
    results.append({'case':'unsupported-flags','result':invoke(['--output-dir',str(box/'unsupported'),'--codex','fake CLI with spaces'],True,unsupported),'unchanged':True})
    def fake(command,**kwargs):
        if command[-1]=='--version':return subprocess.CompletedProcess(command,0,'FAKE CLI TEST ONLY','')
        if command[-1]=='--help':return subprocess.CompletedProcess(command,0,'--ignore-user-config --ephemeral --skip-git-repo-check --sandbox --json','')
        cwd=Path(command[command.index('-C')+1]);assert cwd.is_dir()
        events=[{'type':'turn.started'},{'type':'item.completed','item':{'type':'agent_message','text':'FAKE CLI TEST ONLY; NOT MODEL OUTPUT'}},{'type':'turn.completed','usage':{}}]
        kwargs['stdout'].write(('\n'.join(json.dumps(e) for e in events)+'\n').encode());return subprocess.CompletedProcess(command,0)
    pre=box/'preflight';before=snapshot(box)
    invoke(['--output-dir',str(pre),'--codex','fake CLI with spaces','--preflight-only'],False,fake)
    assert snapshot(box)==before and not (box/'.run-work').exists()
    results.append({'case':'preflight-only-with-space-path','unchanged':True})
    actual=box/'fake-run';invoke(['--output-dir',str(actual),'--codex','fake CLI with spaces'],False,fake)
    assert (actual/'environment.json').exists() and (actual/'A/bid-compliance-card.md').read_text(encoding='utf-8').startswith('FAKE CLI TEST ONLY')
    results.append({'case':'auto-workspace-and-exclusive-metadata','passed':True,'model_called':False})
    results.append({'case':'repeat-refusal','result':invoke(['--output-dir',str(actual)],True),'unchanged':True})
target=D/'runner-tests.json';assert not target.exists();target.write_text(json.dumps({'tests':results,'count':len(results),'real_model_calls':0},indent=2),encoding='utf-8')
print('PASS: '+str(len(results))+' model-free runner tests; no real model output generated.')
