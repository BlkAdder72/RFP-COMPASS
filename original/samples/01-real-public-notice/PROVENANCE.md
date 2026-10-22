# Sample 01: where it came from
- **Source:** California High-Speed Rail Authority, "Track & Systems Construction Contract RFP" web page: https://hsr.ca.gov/work-with-us/procurements/architectural-engineering-and-capital-contracts/archived-ae-and-capital-procurements/track-systems-construction-contract-rfp/
- **Captured:** 2026-09-25, from the text the page shows.
- **Anchor prefix:** `TSCC-WEB` means this page. The rest of each anchor names the part of the page, such as `intro ¶2` (paragraph 2), `Anticipated Schedule` or `delivery model table row Track`.

## Files
- `original-source.txt` is the page text as captured, from the page title to the contact for questions, with nothing edited. Table cells are separated by tabs.
- `source-packet.md` is the packet. The text is split where sentences end and is otherwise unchanged. Table cells are joined with ` | `.
- `bid-compliance-card.md` is the expected card.

## Checking the packet against the capture
```
python -X utf8 tools/make_packet.py verify samples/01-real-public-notice/original-source.txt samples/01-real-public-notice/source-packet.md
```
Result: every packet statement appears word for word in the capture. The only captured text not made into statements:
- **Section headings** "Anticipated Schedule" and "Procurement Approach". They appear in the anchors instead.
- **Web-page buttons and icon labels:** the table widget's text ("10 25 50 100 entries per page", "Search:", "Showing 1 to 7 of 7 entries", "‹1›"), "PDF Document", and "External Link" with the lone "." after it.

"External Link" is an icon label that sits between "(CSCR)" and ". Updates". So S026 ends at "(CSCR)" and S027 starts at "Updates". No text was added to join them.

## Not captured
The site's menu (a list of other Authority procurements), the RESOURCES and CONTACT sidebar, and the site footer. None of these is part of this notice.

The page is now in the Authority's archive of past procurements and shows a Notice of Proposed Award (S012). The page may change after the capture date. The capture in `original-source.txt` is the record this sample traces to.
