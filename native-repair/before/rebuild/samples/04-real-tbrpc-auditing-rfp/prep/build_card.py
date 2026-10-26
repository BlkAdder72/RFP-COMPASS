# Renders bid-compliance-card.md from source-packet.md using the section routing below.
# Routing is the RFP Compass classification (per rules.md); quotes are copied from the packet, never retyped.
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
HEADINGS = [
    "1. Opportunity identity",
    "2. Scope, term, and program context stated",
    "3. Eligibility and qualifications stated",
    "4. Application stages and submission mechanics stated",
    "5. Mandatory attachments and forms stated",
    "6. Dates and events stated",
    "7. Evaluation stated",
    "8. Commercial, performance, and post-award terms stated",
    "9. Tables, schedules, and templates",
    "10. Definitions, authority, and administrative terms",
    "11. Addenda, conflicts, and open items",
    "12. Unmapped source evidence",
]

def r(a, b): return list(range(a, b + 1))

# Each statement is listed under every section whose trigger in reference/output-schema.md matches.
ROUTE = {
    1: [1, 3, 4, 20],
    2: [3, 4] + r(10, 20) + [22] + r(25, 43) + [133, 134, 135],
    3: [5, 21] + r(45, 49),
    4: r(49, 77) + [93, 94, 97, 98, 99, 120, 123],
    5: [47, 52, 53, 65, 72, 75, 76, 77, 78, 79, 80, 83, 89, 154],
    6: [2, 8, 9, 14, 22, 23, 91, 92, 98] + r(111, 119) + [127, 128, 129, 132, 137],
    7: [51] + r(100, 109) + r(120, 122) + r(124, 126) + [139, 146, 147],
    8: [18, 19, 23, 24] + r(25, 40) + [42, 43, 44] + r(81, 88) + [123, 126] + r(133, 137)
       + [145, 148, 149, 150, 152] + r(203, 214),
    9: [86, 89] + r(110, 117) + r(153, 214),
    10: [1, 6, 7, 28, 29, 30, 31, 36, 79, 80, 90, 91, 92, 93, 95, 98, 109, 118, 119, 122, 125]
        + r(127, 132) + r(138, 147) + [150, 151],
    11: [24, 87, 92, 113, 133, 139, 140, 141, 144],
    12: [96],
}

stmts = {}
for line in (HERE / "source-packet.md").read_text(encoding="utf-8").splitlines():
    sid, anchor, text = line.split(" | ", 2)
    stmts[int(sid[1:])] = (sid, anchor, text)

covered = {i for ids in ROUTE.values() for i in ids}
assert covered == set(stmts), f"uncovered: {sorted(set(stmts) - covered)}"

out = ["# RFP COMPASS — BID COMPLIANCE CARD"]
for n, h in enumerate(HEADINGS, 1):
    out.append(f"## {h}")
    ids = sorted(set(ROUTE[n]))
    if not ids:
        out.append("- not in source")
    for i in ids:
        sid, anchor, text = stmts[i]
        out.append(f"- “{text}” [source: source-packet.md:{sid}; {anchor}]")
(HERE / "bid-compliance-card.md").write_text("\n".join(out) + "\n", encoding="utf-8")
print({n: len(set(v)) for n, v in ROUTE.items()})
