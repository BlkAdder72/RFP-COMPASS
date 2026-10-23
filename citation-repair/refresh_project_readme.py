"""Refresh editable project navigation without rewriting any trial evidence."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];D=R/'citation-repair'
assert json.loads((D/'full-length-results.json').read_text(encoding='utf-8'))['rebuild']['passed']
legacy='**RFP Compass turns'+(D/'history/rebuild/README.md').read_text(encoding='utf-8').split('**RFP Compass turns',1)[1]
text='''# RFP Compass

## Current Competition #15 rebuild

The fresh rebuilt full-length card passes every frozen check, including exact S072 citations in Sections 4 and 5. The earlier failed cards remain unchanged and still fail validation.

See `../citation-repair/REPORT.md` for both repair attempts, the fresh comparison and limits. Four model knowledge files changed to preserve complete anchors; both validators remain byte-identical to the preceding seal. Every old failed card is retained and still rejected. Current full-length raw evidence is in `run-results/citation-repair-v2-full/`. The earlier README, including its superseded failure status, is preserved at `../citation-repair/history/rebuild/README.md`.

Q8 still passes with the ordinary default invocation and no review sidecar. Unknown context retains conservative hints; a structural pass does not prove section placement. The original packet/PDF tools and setup workflow remain available below.

## Setup and tool guide

The guide below retains earlier operating instructions and historical model results. Its older Claude/sample claims are historical, not new acceptance of this repair. Use the current report above for present test results.

'''+legacy
(R/'rebuild/README.md').write_bytes(text.encode('utf-8'))
