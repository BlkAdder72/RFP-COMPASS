# Sample 04 provenance
- **Source:** Tampa Bay Regional Planning Council (TBRPC), "Request for Proposals: Auditing Services", issued June 26, 2026. It is a 16-page public solicitation and is included here as `original-source.pdf`.
- **Anchor prefix:** `TBRPC Auditing RFP`, followed by the page and section as printed in the PDF.

## How the packet was made
The scripts in `prep/` run from any folder and need Python 3.10+ and `pdfplumber`.
1. `prep/build_packet.py` holds the statements transcribed from the PDF text: line wraps joined, bullet glyphs dropped, section headings moved into anchors. It writes `source-packet.md`.
2. `prep/exactify.py` replaces each statement with the PDF's exact characters (curly apostrophes, quotes, dashes).
3. `prep/build_card.py` renders `bid-compliance-card.md` from the packet using a section map applied by hand under the routing triggers in `reference/output-schema.md`. That map is how this reference card was made; it is not how the Claude project works. In a Claude project, Claude applies the same triggers itself.

## Checking the packet against the PDF
```
python -X utf8 tools/make_packet.py verify samples/04-real-tbrpc-auditing-rfp/original-source.pdf samples/04-real-tbrpc-auditing-rfp/source-packet.md
```
Result: every packet statement appears verbatim in the PDF. The PDF text left out of the packet is:
- the page-2 table of contents, including the attachment titles listed there (the attachment titles themselves are S153 and S203);
- the section headings, such as "3. Scope Of Services" and "RFP Questions and Response" (they appear in the anchors);
- the word "Contact" (a page-1 label).
