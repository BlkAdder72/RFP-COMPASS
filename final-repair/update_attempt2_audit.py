from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'final-repair';p=D/'verify.py';s=p.read_text(encoding='utf-8')
s=s.replace("for n,h in m['files'].items():assert sha(D/'history'/n if n in m['mutable_paths'] else R/n)==h,'Prior evidence changed: '+n","extra=json.loads((D/'additional-mutable-paths.json').read_text())['paths']\nfor n,h in m['files'].items():assert sha(D/'history'/n if n in m['mutable_paths']+extra else R/n)==h,'Prior evidence changed: '+n\nfor n,h in json.loads((D/'attempt-1/manifest.json').read_text()).items():assert sha(R/n)==h,'Failed first-attempt evidence changed: '+n")
start=s.index("for arm in ['original','rebuild']:");end=s.index('controls=json.loads',start);block=s[start:end]
block=block.replace("('final-repair-'+kind)","(prefix+'-'+kind)").replace('sha(R/arm/name)','sha(knowledge/arm/name)').replace('core.request(R,arm,','core.request(knowledge,arm,')
s=s[:start]+"for prefix,knowledge in [('final-repair',D/'attempt-1-knowledge'),('final-repair-v2',R)]:\n"+''.join(' '+line+'\n' for line in block.splitlines())+s[end:]
start=s.index("copied=R/'rebuild/run-results/final-repair-full'")
tail=s[start:].replace('final-repair-full','final-repair-v2-full').replace('final-repair-new','final-repair-v2-new')
tail=tail.replace("scores=json.loads((D/'scores-final.json')","E=D/'attempt-2'\nscores=json.loads((E/'scores-final.json')").replace("full=json.loads((D/'full-length-results.json')","full=json.loads((E/'full-length-results.json')").replace("new=json.loads((D/'new-results.json')","new=json.loads((E/'new-results.json')")
s=s[:start]+tail
s=s.replace("print(json.dumps({'status'", "old_parts=sorted((R/'run-rebuild/final-repair-full').glob('part-*/bid-compliance-card.md'),key=lambda p:int(p.parent.name.split('-')[1]))\nold=subprocess.run([sys.executable,'-B','-X','utf8',str(R/'rebuild/tools/validate_packet.py'),str(R/'hardening/fixtures/Z-full-length-noisy.md'),*[str(p) for p in old_parts]],capture_output=True,text=True,encoding='utf-8')\nassert old.returncode==1 and 'S100' in old.stdout\nprint(json.dumps({'preserved_S100_failure_still_rejected':True,'status'")
p.write_text(s,encoding='utf-8',newline='\n')
source=(D/'check_core_fidelity.py').read_text().replace('final-repair-'+"'+kind",'final-repair-v2-'+"'+kind").replace('identical-strict-fidelity.json','identical-strict-fidelity-v2.json')
(D/'check_core_fidelity_v2.py').open('x',encoding='utf-8').write(source)
p=D/'write_reports.py';s=p.read_text(encoding='utf-8').replace('`identical-strict-fidelity.json`','`identical-strict-fidelity-v2.json`');p.write_text(s,encoding='utf-8',newline='\n')
print('Audit now verifies both attempts and preserves first failure')
