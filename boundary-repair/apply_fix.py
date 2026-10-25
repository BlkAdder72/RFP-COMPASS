"""Apply the reviewed warning-only candidate after the original baseline commit."""
from pathlib import Path
R=Path(__file__).resolve().parents[1];p=R/'rebuild/tools/validate_packet.py';before=(R/'boundary-repair/before/rebuild/tools/validate_packet.py').read_bytes();assert p.read_bytes()==before
t=before.decode('utf-8').replace('\r\n','\n')
def replace(a,b):
 global t
 assert a in t,a
 t=t.replace(a,b,1)
replace('mandatory|shall|must|','mandatory|compulsory|shall|must|')
replace('r"\\b(potluck|birthday|dentist|','r"\\b(potluck|birthday(?:\\s+(?:dinner|party|celebration))?|dentist|')
a=t.index('PERSONAL_HEADER = re.compile(');b=t.index('# An official participation payment',a)
t=t[:a]+'''# Parentheses are accepted only around an explicitly private annotation.
PRIVATE_ANNOTATION = r"(?:unrelated\\s+)?(?:personal|private|family)\\s+(?:correspondence|notes|calendar|schedule|email|thread)"
PERSONAL_HEADER = re.compile(
    r"\\s*(?P<label>(?:(?:my|our|your|his|her|their)\\s+)?(?:(?:personal|private|family)\\s+)+"
    r"(?:calendar|correspondence|notes|schedule|email|thread|events|activities))"
    r"(?:\\s*(?:[—–-]|:)\\s*" + PRIVATE_ANNOTATION + r"|\\s*\\(\\s*" + PRIVATE_ANNOTATION + r"\\s*\\))?\\s*[:.—-]?\\s*", re.IGNORECASE)
'''+t[b:]
a=t.index('PERSONAL_SHARE = re.compile(');b=t.index('\n\n\ndef personal_hint_exclusions',a)
t=t[:a]+'''# A complete bounded private cost-share phrase, never an arbitrary action.
SMALL_NUMBER = r"(?:one|two|three|four|five|six|seven|eight|nine)"
WORD_NUMBER = r"(?:zero|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|" + SMALL_NUMBER + r"|(?:twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety)(?:[ -]" + SMALL_NUMBER + r")?)"
PERSONAL_SHARE = re.compile(r"(?:my|our|your|his|her|their)\\s+share\\s+(?:is|was)\\s+(?:\\$\\s*\\d+(?:\\.\\d{1,2})?|" + WORD_NUMBER + r"\\s+dollars?)", re.IGNORECASE)
# Explicit optionality prevents a new unknown-event scope. It never clears an
# inherited duty, and independent procurement/clinical cues still take priority.
OPTIONAL_EVENT = re.compile(
    r"\\b(?:attendance|events?|activities)\\b[^.;!?]*\\b(?:is|are)\\s+optional\\b|"
    r"\\bno\\s+attendance\\s+condition\\b", re.IGNORECASE)
'''+t[b:]
a=t.index('    def negative_dependency(text):');b=t.index('    def private_activity_fragment',a)
t=t[:a]+'''    def negative_dependency(text):
        # Analyze an expanded copy only; source and citation bytes never change.
        text = re.sub(r"\\b(\\w+)n['’]t\\b", r"\\1 not", text, flags=re.IGNORECASE)
        text = re.sub(r"\\bnot\\s+only\\b", "only", text, flags=re.IGNORECASE)
        # Negation must modify the dependency predicate, not a subject qualifier
        # such as "Participation, not payment, depends on ...".
        return bool(re.search(
            r"\\b(?:not|never|no\\s+longer)\\s+(?:\\w+\\s+){0,2}"
            r"(?:depends?|contingent|conditional|conditioned|determined)\\s+(?:on|by)\\s*$",
            text, re.IGNORECASE))

'''+t[b:]
replace('(?:these|the|this|those|all|required|mandatory)', '(?:these|the|this|those|all|our|your|their|required|mandatory)')
replace('r"^[\\s\\\"“”\'‘’)]*(?:(?:is|are|was|were|remains?)\\s+)?(?:"', 'r"^[\\s\\\"“”\'‘’)]*(?:,\\s*(?:which|that)\\s+)?(?:(?:is|are|was|were|remains?)\\s+)?(?:"')
replace('r"not\\s+(?:included|part\\s+of)\\b|outside\\s+(?:the\\s+)?(?:scope|requirements)\\b)", suffix)', 'r"not\\s+(?:included\\s+in|part\\s+of)\\s+" + scope_object + r"|outside\\s+(?:the\\s+)?(?:scope|requirements)\\b)", suffix)')
replace('''        # Coordinating conjunctions delimit clauses even without a comma.
        clauses = [c.strip() for c in re.split(
            r"[;.!?](?:\\s+|$)|(?:,\\s*)?\\b(?:and|but|while|also|then|or)\\b\\s+",
''','''        # A "with ... to <action>" adjunct cannot borrow a preceding private
        # activity. Pure private calendar adjuncts remain intact and are checked
        # against the same independent procurement/clinical vetoes.
        clauses = [c.strip() for c in re.split(
            r"[;.!?](?:\\s+|$)|(?:,\\s*)?\\b(?:and|but|while|also|then|or)\\b\\s+|"
            r"(?:,\\s*)?\\bwith\\s+(?=[^.;!?]*\\bto\\s+\\w+)",
''')
replace('and not private_heading and not only_negative_dependency','and not private_heading and not only_negative_dependency and not OPTIONAL_EVENT.search(body)')
replace('''    Unknown event statements keep scope without a modality/colon requirement.
    Negated dependencies do not create or clear genuine inherited scope.
''','''    Unknown event statements keep scope; explicit optionality cannot create it.
    Negated dependencies do not create or clear genuine inherited scope.
''')
# Preserve exact strict implementation bytes, including original line endings.
strict=before[before.index(b'def difference('):];prefix=t[:t.index('def difference(')].encode('utf-8')
p.write_bytes(prefix+strict)
assert p.read_bytes()[p.read_bytes().index(b'def difference('):]==strict
print('Applied warning-only boundary candidate; strict block unchanged')
