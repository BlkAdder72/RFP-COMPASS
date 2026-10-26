"""Apply each bounded repair only after baseline completion and its predecessor's gate."""
from pathlib import Path
import subprocess,sys,json,time
R=Path(__file__).resolve().parents[1];D=R/'warning-final';P=R/'rebuild/tools/validate_packet.py'
def write(p,t):p.write_text(t,encoding='utf-8',newline='\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=R).decode().strip()
def commit(message,paths):
 subprocess.run(['git','add','--',*paths],cwd=R,check=True);subprocess.run(['git','commit','--quiet','-m',message],cwd=R,check=True);return git('rev-parse','HEAD')
deadline=time.monotonic()+2400
while True:
 markers=[D/('original-'+k+'-runner-exit.txt') for k in ['core','new','full']]
 for p in markers:
  if p.exists() and p.read_text()!='0':raise SystemExit('Original baseline failed; retained, no repairs made')
 if all(p.exists() for p in markers):break
 if time.monotonic()>deadline:raise SystemExit('Baseline not completed; no repairs made')
 time.sleep(5)
if (D/'chronology.json').exists():
 ch=json.loads((D/'chronology.json').read_text())
else:
 assert P.read_bytes()==(D/'before/rebuild/tools/validate_packet.py').read_bytes()
 ch={'freeze':'79257825','original_baseline':commit('Preserve complete original baseline before sequential warning repairs',['run-original/warning-final-core','run-original/warning-final-new','run-original/warning-final-full','warning-final'])}
 write(D/'chronology.json',json.dumps(ch,indent=2));print('BASELINE COMMITTED '+ch['original_baseline'],flush=True)
for number in range(1,5):
 if 'F'+str(number) in ch:
  assert json.loads((D/'stages'/('F'+str(number))/'results.json').read_text())['passed_required']
  continue
 text=P.read_text(encoding='utf-8');before=text
 if number==1:
  text=text.replace(r'depends?\s+on|contingent\s+on',r'depends?\s+on|hinges?\s+on|dependent\s+on|contingent\s+on')
  text=text.replace(r'(?:depends?|contingent|conditional|conditioned|determined)',r'(?:depends?|hinges?|dependent|contingent|conditional|conditioned|determined)')
 elif number==2:
  old=r'''                if excluded_before and re.match(r"\s+from\b", suffix):
                    excluded_before = re.match(r"\s+from\s+" + scope_object, suffix)
'''
  new=r'''                if excluded_before:
                    if re.match(r"\s+from\b", suffix):
                        excluded_before = re.match(r"\s+from\s+" + scope_object, suffix)
                    else:
                        # A program/schedule subject is not the requirement
                        # scope. Bind the entire exclusion relation locally.
                        subject = prefix[:excluded_before.start()].strip(" ,:")
                        scoped_subject = re.fullmatch(
                            scope_object + r"\s*(?:(?:do|does|did)\s*)?", subject)
                        scoped_attendance = re.search(
                            r"\b(?:attend|attending|attendance\s+at)\s+" + scope_object + r"\s*$", subject)
                        excluded_before = scoped_subject or scoped_attendance
'''
  assert old in text;text=text.replace(old,new,1)
 elif number==3:
  lines=text.splitlines(keepends=True)
  for i,line in enumerate(lines):
   if line.startswith('WORD_NUMBER = '):
    lines[i]=line.replace('WORD_NUMBER','UNDER_HUNDRED',1)+r'''UNDER_THOUSAND = r"(?:" + SMALL_NUMBER + r"\s+hundred(?:\s+(?:and\s+)?" + UNDER_HUNDRED + r")?|" + UNDER_HUNDRED + r")"
WORD_NUMBER = r"(?:" + UNDER_THOUSAND + r"\s+thousand(?:\s+(?:and\s+)?" + UNDER_THOUSAND + r")?|" + UNDER_THOUSAND + r")"
''';break
  else:raise AssertionError('Number grammar not found')
  text=''.join(lines)
  text=text.replace('        clauses = [c.strip() for c in re.split(','''        # Collapse only a complete recognized private share in an analysis
        # copy. Its internal number conjunction is not a separate obligation.
        clause_body = PERSONAL_SHARE.sub(lambda m: m.group().split()[0] + " share is $0", body)
        clauses = [c.strip() for c in re.split(''',1)
  old='            body, flags=re.IGNORECASE) if c.strip()]';assert old in text;text=text.replace(old,'            clause_body, flags=re.IGNORECASE) if c.strip()]',1)
 elif number==4:
  marker='PERSONAL_HEADER = re.compile('
  text=text.replace(marker,r'''OUTSIDE_PRIVATE_ANNOTATION = r"(?:outside|unrelated\s+to|not\s+part\s+of)\s+(?:the\s+)?(?:procurement|solicitation)"
PRIVATE_ANNOTATION = r"(?:" + PRIVATE_ANNOTATION + "|" + OUTSIDE_PRIVATE_ANNOTATION + ")"
'''+marker,1)
  old='        hard_procurement = PROCUREMENT_CUE.search(body) or OFFER_DELIVERY_CUE.search(body) or PAYMENT_CUE.search(body) or positive_dependency'
  new='''        private_heading = PERSONAL_HEADER.fullmatch(body)
        # Only a complete private heading can neutralize the procurement noun
        # in its own negative annotation. Other cues and inherited scope stay.
        outside_private_heading = bool(private_heading and re.search(OUTSIDE_PRIVATE_ANNOTATION, body, re.IGNORECASE))
        hard_procurement = ((not outside_private_heading and PROCUREMENT_CUE.search(body))
                            or OFFER_DELIVERY_CUE.search(body) or PAYMENT_CUE.search(body) or positive_dependency)'''
  assert old in text;text=text.replace(old,new,1)
 assert text!=before
 write(P,text)
 cmd=[sys.executable,'-B','-X','utf8',str(D/'test_stage.py'),'F'+str(number),str(number)]
 with (D/('F'+str(number)+'-test-stdout.txt')).open('xb') as o,(D/('F'+str(number)+'-test-stderr.txt')).open('xb') as e:p=subprocess.run(cmd,stdout=o,stderr=e,cwd=R)
 (D/('F'+str(number)+'-test-exit.txt')).open('x').write(str(p.returncode))
 if p.returncode:raise SystemExit('F'+str(number)+' failed; all evidence retained; next issue NOT started')
 result=json.loads((D/'stages'/('F'+str(number))/'results.json').read_text());assert result['passed_required']
 ch['F'+str(number)]=commit('Repair warning issue F'+str(number)+' after passing sequential regression gate',['rebuild/tools/validate_packet.py','warning-final'])
 write(D/'chronology.json',json.dumps(ch,indent=2));print('F'+str(number)+' PASS; remaining failures '+str(len(result['all_remaining_failures']))+'; commit '+ch['F'+str(number)],flush=True)
ch['candidate']=ch['F4'];write(D/'chronology.json',json.dumps(ch,indent=2));print('ALL FOUR GATES PASS; candidate '+ch['candidate'],flush=True)
