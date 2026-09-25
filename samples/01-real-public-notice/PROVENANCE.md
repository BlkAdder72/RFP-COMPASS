# Sample 01 provenance
- **Source:** California High-Speed Rail Authority, "Track & Systems Construction Contract RFP" procurement page. https://hsr.ca.gov/work-with-us/procurements/architectural-engineering-and-capital-contracts/archived-ae-and-capital-procurements/track-systems-construction-contract-rfp/
- **Captured:** 2026-09-25, from the page's rendered text.
- **Anchor prefix:** `TSCC-WEB` means this page. The rest of each anchor names the page part, such as `intro ¶2`, `Anticipated Schedule` or `delivery model table row Track`.

## Files
- `original-source.txt` is the captured page text, from the page title through the questions contact, with nothing edited. Table rows keep their tab-separated cells.
- `source-packet.md` is the packet, split at sentence ends with the text unchanged. Table cells are joined with ` | `.
- `bid-compliance-card.md` is the expected card.

## Checking the packet against the capture
```
python -X utf8 tools/make_packet.py verify samples/01-real-public-notice/original-source.txt samples/01-real-public-notice/source-packet.md
```
Result: every packet statement appears verbatim in the capture. The only capture text not carried into statements:
- **Section headings** "Anticipated Schedule" and "Procurement Approach". They are kept in the anchors.
- **Web-page controls and icon labels:** the data-table widget text ("10 25 50 100 entries per page", "Search:", "Showing 1 to 7 of 7 entries", "‹1›"), "PDF Document" and "External Link".

Because "External Link" is an icon label between "(CSCR)" and ". Updates", S026 ends at "(CSCR)" and S027 begins at "Updates". No text was added to join them.

## Not captured
The page's site-wide navigation (a list of other Authority procurements), the RESOURCES and CONTACT sidebar, and the site footer. None of these is part of this notice.

The page is now in the Authority's archived procurements and shows a Notice of Proposed Award (S012). The page may change after the capture date; the capture in `original-source.txt` is the record this sample traces to.
