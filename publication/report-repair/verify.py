from pathlib import Path
import json,hashlib,re,subprocess,sys
R=Path.cwd();D=R/'publication/report-repair';saved=json.loads((D/'PRESERVED_INPUT_SHA256.json').read_text(encoding='utf8'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checks={}
checks['all_frozen_inputs_scores_tools_and_native_evidence_unchanged']=all(sha(R/n)==h for n,h in saved.items())
checks['previous_documents_preserved_exactly']=all(p.read_bytes()==subprocess.check_output(['git','show','10c3d4df:'+p.relative_to(D/'before').as_posix()],cwd=R) for p in (D/'before').rglob('*') if p.is_file())
checks['root_and_route_reports_identical']=(R/'results.md').read_bytes()==(R/'route-repair/REPORT.md').read_bytes()
before=sha(R/'results.md');run=subprocess.run([sys.executable,'-B','-X','utf8',str(R/'route-repair/write_report.py'),'analysis-final'],capture_output=True,text=True,encoding='utf8');checks['report_regeneration_deterministic']=run.returncode==0 and before==sha(R/'results.md')
s=json.loads((R/'route-repair/analysis-final/scores.json').read_text(encoding='utf8'));counts={a:{'raw':sum(v['strict_pass'] for v in ts.values()),'selected':sum(v['expanded_semantic_pass'] for v in ts.values()),'export':sum(v['derived_export']['strict_pass'] for v in ts.values())} for a,ts in s['model_trials'].items()};checks['counts_match_saved_scores']=counts=={'original':{'raw':8,'selected':5,'export':10},'rebuild':{'raw':9,'selected':11,'export':11}}
verdicts=s['frozen_questions'];rank={'fail':0,'partial':1,'pass':2};improved=[q for q in verdicts['rebuild'] if rank[verdicts['rebuild'][q]['verdict']]>rank[verdicts['original'][q]['verdict']]];ties=[q for q in verdicts['rebuild'] if verdicts['rebuild'][q]['verdict']==verdicts['original'][q]['verdict']];checks['feedback_five_improvements_three_ties']=improved==['Q1','Q3','Q6','Q7','Q8'] and ties==['Q2','Q4','Q5']
text=(R/'results.md').read_text(encoding='utf8');checks['current_publication_status_clear']=text.startswith('# Competition 15 results') and 'Nothing has been published' not in text and 'Nothing is published' not in text and '**Published:**' in text
bad=[];prefix='https://github.com/BlkAdder72/RFP-COMPASS/'
for href in re.findall(r'\]\(([^)]+)\)',text):
 for mode in ['blob/','tree/']:
  start=prefix+mode+'codex/competition-15-rebuild/'
  if href.startswith(start):
   n=href[len(start):]
   if n!='publication/report-repair/VERIFICATION.json' and not (R/n).exists():bad.append(n)
checks['current_report_evidence_links_resolve_in_source']=not bad
result={'passed':all(checks.values()),'kind':'documentation-only current-results repair','checks':checks,'unchanged_immutable_files':len(saved),'scores_sha256':sha(R/'route-repair/analysis-final/scores.json'),'report_sha256':sha(R/'results.md'),'counts':counts,'feedback_improved':improved,'feedback_tied':ties,'broken_links':bad,'model_calls':0,'competition_comment_posted':False,'prior_public_commit':'10c3d4dfd437d76a683f270ab66ee130346b1ba6'}
(D/'VERIFICATION.json').write_text(json.dumps(result,indent=2),encoding='utf8');assert result['passed'];print(json.dumps(result))
