"""Replay prior cards under both validators without altering their evidence."""
from pathlib import Path
import subprocess,sys,json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'hardening';O=D/'final-replays-v2';assert not O.exists();O.mkdir();results=[]
for validator in ('original','rebuild'):
    pairs=[]
    for arm in ('original','rebuild'):
        for fixture in sorted((R/'fixtures').glob('*.md')):pairs.append((f'first-{arm}-{fixture.stem}',fixture,R/('run-'+arm)/fixture.stem/'bid-compliance-card.md'))
        for fixture in sorted((R/'supplemental/fixtures').glob('*.md')):
            for repeat in (1,2):pairs.append((f'stress-{arm}-{fixture.stem}-{repeat}',fixture,R/'supplemental'/('run-'+arm)/fixture.stem/('repeat-'+str(repeat))/'bid-compliance-card.md'))
    for sample in sorted((R/validator/'samples').iterdir()):pairs.append(('sample-'+sample.name,sample/'source-packet.md',sample/'bid-compliance-card.md'))
    for label,source,card in pairs:
        folder=O/validator/label;folder.mkdir(parents=True)
        args=[sys.executable,'-X','utf8',str(R/validator/'tools/validate_packet.py'),str(source),str(card)]
        result=subprocess.run(args,capture_output=True,text=True,encoding='utf-8')
        (folder/'command.json').write_text(json.dumps(args,indent=2),encoding='utf-8');(folder/'stdout.txt').write_text(result.stdout,encoding='utf-8');(folder/'stderr.txt').write_text(result.stderr,encoding='utf-8')
        record={'validator':validator,'label':label,'exit_code':result.returncode,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'card_sha256':hashlib.sha256(card.read_bytes()).hexdigest()}
        results.append(record)
(D/'final-replay-results-v2.json').write_text(json.dumps({'count':len(results),'passed':sum(r['exit_code']==0 for r in results),'cases':results},indent=2),encoding='utf-8')
print(f"{sum(r['exit_code']==0 for r in results)}/{len(results)} archived/reference structural replays passed; no model calls.")
