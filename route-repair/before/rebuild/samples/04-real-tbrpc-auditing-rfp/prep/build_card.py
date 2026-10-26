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
ROUTE = {1: [1, 3, 4, 20], 2: [3, 4, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 133, 134, 135], 3: [5, 21, 45, 46, 47, 48, 49], 4: [49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 93, 94, 97, 98, 99, 120, 123], 5: [47, 52, 53, 65, 72, 75, 76, 77, 78, 79, 80, 83, 89, 154], 6: [2, 8, 9, 14, 22, 23, 91, 92, 98, 111, 112, 113, 114, 115, 116, 117, 118, 119, 127, 128, 129, 132, 137], 7: [51, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 120, 121, 122, 124, 125, 126, 146, 147], 8: [18, 19, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 42, 43, 44, 81, 82, 83, 84, 85, 86, 87, 88, 123, 126, 133, 134, 135, 136, 137, 145, 148, 149, 150, 152, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214], 9: [86, 89, 110, 111, 112, 113, 114, 115, 116, 117, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214], 10: [1, 6, 7, 28, 29, 30, 31, 36, 47, 48, 79, 80, 90, 91, 92, 93, 95, 98, 109, 118, 119, 122, 125, 127, 128, 129, 130, 131, 132, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 150, 151], 11: [24, 87, 92, 113, 133, 139, 140, 141, 144, 148], 12: [96]}

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
