# Accepted Input
One UTF-8 text/Markdown file named source-packet.md, designated as the active input by the user. Each nonblank line is one statement:

`S001 | RFP-01 p. 2 section 3 | Exact procurement source statement.`

- IDs run S001, S002, S003 ... with no gaps or repeats.
- The anchor says where the statement sits in the retained original (document, page, section, table row). It must not contain ` | `.
- The text is copied from the original without rewording: one complete sentence, list item, heading or table row per line. A sentence the original wraps across lines or pages is one statement.
- Table cells are separated by ` | ` in their original column order, one row per line. A blank cell stays blank (`| |`) or keeps the placeholder the original shows, such as `_____`.
- A page header or footer that repeats on most pages (a running title, "Page 3 of 41", a revision stamp) appears once, at its first appearance.
- No narrative headers, comments or blank-line-separated sections inside the packet.

Keep the original document alongside the packet. The card traces to the packet; the packet's fidelity to the original is checked separately with `tools/make_packet.py verify ORIGINAL source-packet.md`.

## Preparing a packet
- **With Python (recommended for anything over a few pages):** `python -X utf8 tools/make_packet.py build ORIGINAL.pdf --prefix RFP-01 > source-packet.md` copies text without changing it:
  - it rejoins sentences wrapped across lines and pages, then splits at sentence ends;
  - it turns tab-separated cells into ` | `;
  - it keeps repeated page headers and footers once and reports the repeats it dropped;
  - it anchors each statement to its page and line;
  - it turns each row of a ruled PDF table into one statement, adding `(columns N–M of K)` to the anchor when the row's edge cells are blank;
  - it writes symbol-font characters (such as a Wingdings check mark) as `<U+XXXX>` so they stay visible;
  - it reports every page whose content includes images (maps, scans, checkbox marks), which text extraction cannot copy.

  Review the draft against the original, then run `make_packet.py verify`. Verify checks that every statement appears verbatim at its own position in the original, and that the cells of each table row sit together. It also lists any original text the packet leaves out.
- **By hand:** follow the format above. Scanned images and broken OCR must be corrected by a person against the original before use.

## Draft packet from raw text
When the user designates raw procurement text instead of a packet, the translator returns `INPUT NOT READY` followed by a draft packet built like this:
- **Order and splitting.** Take the attachment's text in reading order. A line break is not a sentence end: rejoin a sentence the source wraps across lines or pages, then split only where a sentence ends. Never split inside abbreviations such as "p.m.", "U.S." or "No.".
- **Copy exactly.** Copy every character exactly as it appears in the attachment, headings and list markers included:
  - curly and straight apostrophes and quotes;
  - odd spacing such as `3 :00` or `11 :00`;
  - stray symbols, broken words and misspellings.

  Never correct, normalise, reword, reorder or merge distant text.
- **Page furniture.** A header or footer that repeats on most pages (running title, "Page N of M", revision stamp) is included at its first appearance only. Nothing else is skipped. The reply that completes the draft (the only reply, for a short document) says so on one line outside the code block, listing each repeated line and roughly how often it repeats. For example: `Repeated page headers/footers kept once: "RFP #056-2026" (on 41 pages); "Page N of 41" (on 41 pages).` If none repeat, say `Repeated page headers/footers kept once: none.`
- **Anchors.** Anchor each statement as `<attachment file name> line N` (the line where it starts). For a PDF, use `<file name> p. P`; for pasted text, use `pasted text line N`.
- **Several documents.** An RFP and its addenda attached together form one draft: take the documents in the order given and continue the numbering across them. Every anchor names its own document, so an addendum's statements are always distinguishable from the RFP's.
- **Tables.** Join the cells of one table row with ` | `, in column order, but only when the text arrives with its rows intact. If a table's text arrives already scrambled, with columns interleaved or cells wrapped across lines (for example `Required at` / `High` / `(agendas, minutes, reports) Launch`), copy each line exactly as it appears. Never move words between lines to rebuild cells; that is reordering and guessing, and `make_packet.py` rebuilds ruled tables properly from the PDF. Never fill a blank cell from another row, for example the building name of a merged cell. When a row's first or last cells are blank, add the columns it fills to the anchor, such as `p. 51 (columns 2–4 of 4)`, so the row cannot be misread as starting in column 1.
- **Content in images.** Some content exists only as an image: a map, a scanned page, a signature, a logo or checkbox marks. Do not transcribe or describe it as a statement. List it on the completion line instead, for example `Not copied (images): p. 63 district map; p. 42 checkbox marks (which items are checked)`. If there is none, say `Not copied (images): none.`
- **Format.** Put the draft in one fenced code block labelled `source-packet.md`, with no other text inside the block.

### Long documents: draft in parts
A draft for a long document will not fit in one reply. Send it in consecutive parts of at most about 150 statements each, and never drop or compress text to make it fit:
- Every part starts with `INPUT NOT READY` and one line saying which part it is, which IDs it holds and how much of the document it covers. For example: `Draft packet part 1: S001–S160, pages 1–8 of 41. Not complete. Reply continue for the next part.`
- Each part ends after a complete statement. The next part continues the numbering and starts with the next statement.
- The final part says the draft is complete, with the full ID range and coverage, and lists the repeated page headers/footers kept once (see "Page furniture" above). For example: `Draft packet part 4 of 4: S481–S612, pages 33–41 of 41. The draft is now complete (S001–S612, all 41 pages). Repeated page headers/footers kept once: "RFP #056-2026" (on 41 pages); "Page N of 41" (on 41 pages). Check it against the original, then reply use the draft packet.`
- All parts together, in order, are the draft packet.

**Never make a card from a partial draft.** A card made from part of a document would mark sections `- not in source` that the rest of the document fills. If the user replies `use the draft packet` before the final part, return `INPUT NOT READY`, say how much the draft covers so far (IDs and pages), and ask them to reply `continue`.

The draft is a convenience for review, not a reviewed packet. The card made from it traces to the draft.
