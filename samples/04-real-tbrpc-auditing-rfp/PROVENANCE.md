# Sample 04: where it came from
- **Source:** Tampa Bay Regional Planning Council (TBRPC), "Request for Proposals: Auditing Services", issued June 26, 2026. It is a 16-page public RFP and is included here as `original-source.pdf`.
- **Anchor prefix:** `TBRPC Auditing RFP`, then the page and section as printed in the PDF.

## How the packet was made
The scripts in `prep/` run from any folder. They need Python 3.10+ and `pdfplumber`.
1. `prep/build_packet.py` holds the statements copied from the PDF text, with line breaks joined, bullet symbols dropped and section headings moved into the anchors. It writes `source-packet.md`.
2. `prep/exactify.py` swaps each statement for the PDF's exact characters (curly apostrophes, quotes, dashes).
3. `prep/build_card.py` builds `bid-compliance-card.md` from the packet. It uses a list, made by hand, of which statement goes in which section, following the triggers in `reference/output-schema.md`. That is only how this reference card was made. In a Claude Project, Claude applies the same triggers itself.

## Checking the packet against the PDF
```
python -X utf8 tools/make_packet.py verify samples/04-real-tbrpc-auditing-rfp/original-source.pdf samples/04-real-tbrpc-auditing-rfp/source-packet.md
```
Result: every packet statement appears word for word in the PDF. The PDF text left out of the packet:
- the page-2 table of contents, including the attachment titles listed there (the attachment titles themselves are S153 and S203);
- section headings, such as "3. Scope Of Services" and "RFP Questions and Response" (they appear in the anchors);
- the word "Contact" (a label on page 1).
