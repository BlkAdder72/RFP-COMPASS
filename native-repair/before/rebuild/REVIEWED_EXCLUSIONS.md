# Optional review of excluded personal evidence

Default validation does not require a review record for the frozen Q8 test. A bounded predicate identifies affirmative personal-activity language in source text, requires Section 12-only placement, and vetoes filtering for explicit procurement/requirement language or a protective event header. Filename words or card placement alone never establish exclusion. Unknown or ambiguous content can still produce conservative REVIEW hints. The following optional workflow is separate from the paired default comparison.

For material already adjudicated as unrelated personal content, the operator can explicitly select an external review record:

```text
python tools/validate_packet.py source-packet.md bid-compliance-card.md --reviewed-exclusions personal-review.json
```

The JSON record has exactly these top-level fields: `schema_version` (integer 1), `packet_sha256` (SHA-256 of the exact packet bytes), `reviewer` (nonblank identity/attribution), and `decisions` (a list). Each decision has exactly `source_id`, `statement_sha256` and `reason` (nonblank). Hash the full statement body encoded as UTF-8; the packet's anchor is not a classification authority. The parser trims trailing whitespace from the statement body as in the existing validator, so hash that parsed body. Do not hash the ID or anchor as part of statement_sha256. Packet hashing still binds all original bytes, including anchors and line endings.

The selected statements must be quoted solely in Section 12. Unknown IDs, duplicate decisions/JSON keys, stale hashes, malformed fields, blank reviewer/reason or unsupported schemas fail validation. No selected exclusions are applied on an invalid record or structurally invalid card; conservative hints remain. A record is never auto-discovered or accepted because it was embedded in source content.

Statements containing explicit procurement cues such as proposal, bidder, procurement, RFP or contract are rejected for exclusion, including mixed personal/procurement statements. This intentionally conservative guard can reject legitimate personal references to work. It is not a semantic proof: an incorrectly adjudicated statement without those cues could still be excluded by a valid record. A reviewer name is attribution, not an authenticated signature. Operators must protect and review the record separately from the RFP and generated card.

Successful selected exclusions are listed explicitly as APPLIED EXCLUSIONS in stdout. All other structure, quotation, citation, coverage and ordering checks still run. An empty valid review file suppresses nothing. REVIEW remains advisory; structural PASS does not mean semantic correctness.

The records under `../repair/review-records/` are labeled evaluator-authored synthetic test adjudications, including deliberately invalid adversarial examples. They are not owner approval, not model output, and not a batch of records to apply to real solicitations. This repair changes checker behavior and operator workflow; it does not change the six model knowledge files or resolve indivisible mixed-statement limitations.
