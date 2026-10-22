"""Independent workspace-creation check using a labeled fake CLI, never a model."""
from pathlib import Path
import importlib.util,json,subprocess,sys
from unittest.mock import patch
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[1];D=R/'red-team-final';box=D/'workspace-sandbox';assert not box.exists();box.mkdir()
spec=importlib.util.spec_from_file_location('runner',R/'tools/run_arm.py');runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner);runner.ROOT=box
for name in runner.FILES:
    p=box/'original'/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('FAKE TEST CONTRACT ONLY',encoding='utf-8')
(box/'fixtures').mkdir();(box/'fixtures/case.md').write_text('S001 | test | FAKE TEST INPUT ONLY',encoding='utf-8')
observations=[]
def fake(command,**kwargs):
    if command[-1]=='--version':return subprocess.CompletedProcess(command,0,'FAKE CLI TEST ONLY','')
    if command[-1]=='--help':return subprocess.CompletedProcess(command,0,'--ignore-user-config --ephemeral --skip-git-repo-check --sandbox --json','')
    cwd=Path(command[command.index('-C')+1]);assert cwd.is_dir();observations.append({'working_directory_created':True,'cwd':str(cwd),'executable':command[0]})
    text='FAKE CLI TEST ONLY; NOT A MODEL RESPONSE'
    events=[{'type':'item.completed','item':{'type':'agent_message','text':text}},{'type':'turn.completed'}]
    kwargs['stdout'].write(('\n'.join(json.dumps(e) for e in events)+'\n').encode());return subprocess.CompletedProcess(command,0)
assert not (box/'.run-work').exists()
with patch.object(runner.subprocess,'run',side_effect=fake):
    assert runner.main(['original','--fixtures-dir',str(box/'fixtures'),'--output-dir',str(box/'new-output'),'--codex','fake executable path with spaces'])==0
assert observations and (box/'new-output/environment.json').exists()
(D/'workspace-results.json').write_text(json.dumps({'passed':True,'real_model_calls':0,'observations':observations,'temporary_cwd_removed':not Path(observations[0]['cwd']).exists()},indent=2),encoding='utf-8')
print('PASS: isolated workspace auto-created; path with spaces preserved as one argument; fake CLI only.')
