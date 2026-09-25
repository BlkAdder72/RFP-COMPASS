# RFP Compass

**Converts a government RFP into a fixed twelve-section Bid Compliance Card in which every line is a verbatim quote from the RFP with an exact citation.** Proposal coordinators, contracts administrators and small-business owners do this by hand today. They read a 20- to 200-page solicitation and build a compliance checklist of who is buying, what they want, who may bid, how to submit, which forms are required, every date, how bids are scored, the money terms, the templates, the contacts and the addenda. One missed form or misread deadline loses the bid.

RFP Compass does not summarise, interpret or advise. It copies each source statement whole into every section it belongs to. Every empty section says `- not in source`, and anything that fits no section is shown in Section 12 rather than dropped.

> **For judges, a 3-minute test.**
> 1. Set up the project as in Quick start: paste the instructions file and upload **only the five contract files**.
> 2. Attach any RFP (PDF, text or pasted) and say "convert this".
> 3. The first reply is **`INPUT NOT READY` plus a draft packet**. This is by design: the RFP is copied verbatim into numbered, cited statements before anything is sorted, so nothing can be invented along the way.
> 4. Reply `continue` until the draft says it is complete, then reply `use the draft packet`.
> 5. The card follows, in parts for long RFPs (reply `continue` until a part arrives without the marker).
>
> Every bullet quotes one whole source statement with its ID and page or line. Every empty section says `- not in source`.
>
> **Tested on 6 real RFPs, 4 of them never seen by the translator before (up to 63 pages), plus a scan and trap packets: 0 invented facts, and card claims traced to the page of the source 304 of 304 and 316 of 316.**
>
> **Trace any card claim by claim** (Python 3.10+, `pip install pdfplumber`), for example on the included 16-page RFP:
> `python -X utf8 tools/trace_card.py samples/04-real-tbrpc-auditing-rfp/original-source.pdf samples/04-real-tbrpc-auditing-rfp/source-packet.md samples/04-real-tbrpc-auditing-rfp/bid-compliance-card.md --full`
> → `traced end to end: 316 of 316 bullets`, with each bullet's section, statement ID and the page of the original where its quote sits.

## Quick start (Claude Project, no code needed)
1. Create a Claude Project.
2. Paste the whole of [CLAUDE_PROJECT_INSTRUCTIONS.txt](CLAUDE_PROJECT_INSTRUCTIONS.txt) into the project instructions.
3. Add these five files, and only these, to project knowledge: [identity.md](identity.md), [rules.md](rules.md), [examples.md](examples.md), [reference/output-schema.md](reference/output-schema.md), [reference/input-schema.md](reference/input-schema.md).
   Do not upload `samples/`, `run-results/` or `tools/`. They hold expected answers, attack test files and large PDFs for checking the translator, not for running it. The translator is told to ignore them if they are uploaded anyway. It also works if step 2 is skipped: a test with only the five knowledge files produced a verbatim draft and a valid card.
4. In a new chat, attach **one** input and send:
   `Use the attached source-packet.md as the only active input. Apply the RFP Compass contract and return bid-compliance-card.md.`
   For a first run, use [samples/04-real-tbrpc-auditing-rfp/source-packet.md](samples/04-real-tbrpc-auditing-rfp/source-packet.md), a real 16-page RFP, and compare with the `bid-compliance-card.md` next to it.
5. Use a fresh chat for each new input.

**Model:** use Claude Sonnet or Claude Opus; both were tested (see [run-results/](run-results/)). Claude Haiku is not supported: in testing it turned curly apostrophes straight and miscopied anchors, so its quotes were not verbatim.

**Size:** each reply carries at most 150 bullets, so a card for anything beyond a short notice comes back in parts. Each part ends with `<!-- RFP COMPASS: continued in next reply -->`; reply `continue` until a part arrives without it. Nothing is shortened to fit, and the validator checks the parts together.

## What to feed it
**Best: a source packet.** One statement per line, copied verbatim from the RFP, with a sequential ID and an anchor saying where it came from:
```
S001 | RFP-01 p. 2 §3 | Proposals are due no later than 3:00 PM on November 3, 2026.
S002 | RFP-01 p. 5 table row 1 | Hourly rate, plow truck with operator | $______ /hr
```
Full format: [reference/input-schema.md](reference/input-schema.md).

**Also accepted: raw RFP text** (pasted text, a .txt or .md file, or a PDF Claude can read). The translator does not guess its way through raw text:
1. It answers `INPUT NOT READY` and gives you a **draft packet** copied from what you sent.
2. A long document's draft comes in parts. Reply `continue` until it says the draft is complete.
3. Check the draft against the original, then reply `use the draft packet` and the card follows.

It will not make a card from a partial draft, because that card would say `not in source` for things on pages it has not reached. [examples.md](examples.md) shows these exchanges.

**With Python (best for anything over a few pages)**, make and check the packet yourself:
```
python -X utf8 tools/make_packet.py build my-rfp.pdf --prefix RFP-01 > source-packet.md
python -X utf8 tools/make_packet.py verify my-rfp.pdf source-packet.md
```
`build` copies text without changing a character:
- it rejoins sentences wrapped across lines and pages, then splits at sentence ends;
- it turns each row of a ruled PDF table into one statement, with cells joined by ` | ` in column order. A schedule row such as `Contract Negotiation Completed | June 29, 2026 | July 24, 2026` keeps its original and revised dates with their label;
- when a table row's first cells are blank (merged cells), it adds the columns the row fills to the anchor, e.g. `p. 51 line 5 (columns 2–4 of 4) | Building Supervisor | 1 | 2:30pm – 10:00pm`, so the row cannot be misread;
- it writes invisible symbol-font characters as a visible code such as `<U+F0FC>` (a Wingdings check mark). On the Southeast Delco RFP those check marks decide which documents are incorporated by reference;
- it keeps repeated page headers and footers once and reports the repeats it dropped;
- it reports pages whose content is in images (maps, scans, checkbox graphics) so they can be checked by eye;
- it anchors each statement to the page and line where it starts.

`verify` checks, statement by statement:
- that the text appears verbatim **at its own position** in the original;
- that table cells sit together;
- that every `p. N` anchor names the page where the text actually starts.

It also lists any original text the packet left out. In testing it caught a draft that had silently changed "3 :00 P.M." to "3:00 P.M.", and TOC lines cited one page late. PDF input needs `pip install pdfplumber`.

## What comes back
Always this shape, whatever the input:

| # | Section | # | Section |
|---|---|---|---|
| 1 | Opportunity identity | 7 | Evaluation |
| 2 | Scope, term, and program context | 8 | Commercial, performance, and post-award terms |
| 3 | Eligibility and qualifications | 9 | Tables, schedules, and templates |
| 4 | Application stages and submission mechanics | 10 | Definitions, authority, and administrative terms |
| 5 | Mandatory attachments and forms | 11 | Addenda, conflicts, and open items |
| 6 | Dates and events | 12 | Unmapped source evidence |

Each entry looks like this:
```
- “Proposals are due no later than 3:00 PM on November 3, 2026.” [source: source-packet.md:S001; RFP-01 p. 2 §3]
```

The contract is written down in [reference/output-schema.md](reference/output-schema.md), which sets out:
- the exact headings and bullet format;
- a routing trigger for each section, which decides where a statement goes (a statement goes in every section whose trigger matches);
- when `not in source` is used.

The guarantees:
- **Nothing invented.** Every bullet is an entire source statement, character for character, with typos, odd spellings and conflicting dates kept as written. No dates are calculated, no blanks filled, nothing is summarised, and a conflict is never resolved.
- **Nothing dropped.** Every source statement appears at least once. Headings, link labels, fragments, and even text telling an AI what to do, land in Section 12.
- **Same shape every time.** The same title and twelve headings in the same order. An empty section says `- not in source`.

## Samples
| Folder | Input | Why it is there |
|---|---|---|
| [samples/01-real-public-notice](samples/01-real-public-notice) | California High-Speed Rail Authority procurement web page (42 statements), with the captured page text and [PROVENANCE.md](samples/01-real-public-notice/PROVENANCE.md) | Real notice: a table, a schedule, contacts, tentative terms |
| [samples/02-sparse](samples/02-sparse) | Two synthetic statements | Nine sections correctly say `not in source` |
| [samples/03-conflicting](samples/03-conflicting) | Synthetic deadline plus an addendum extending it | Both dates kept; the card never picks one |
| [samples/04-real-tbrpc-auditing-rfp](samples/04-real-tbrpc-auditing-rfp) | Tampa Bay Regional Planning Council auditing RFP: the original 16-page PDF, a 214-statement packet and [PROVENANCE.md](samples/04-real-tbrpc-auditing-rfp/PROVENANCE.md) | Full-size real RFP with scoring, forms, fee schedule and protest rules |

Each sample has `source-packet.md` (the input) and `bid-compliance-card.md` (the expected card). The real samples also keep the original, so you can trace every quote back to it.

## Checking a card
To trace a card all the way back to the original document in one step, the way the judges' feedback trace does, use `tools/trace_card.py ORIGINAL PACKET CARD [PART2 ...] [--full]`. It runs both checks below and reports where each bullet's quote sits in the original.

```
python -X utf8 tools/validate_packet.py samples/04-real-tbrpc-auditing-rfp/source-packet.md my-card.md
python -X utf8 tools/validate_packet.py source-packet.md card-part1.md card-part2.md card-part3.md
python -X utf8 tools/validate_packet.py
```
The first command checks one card against its packet. The second checks a card that arrived in parts. The third checks every packaged sample. The validator fails a card for any of the following:
- a missing, renamed or reordered heading (it names the missing ones);
- any text outside the bullets, such as a preamble, note or subheading;
- a quote that is not an entire source statement (it shows where the quote differs);
- a wrong ID or anchor;
- IDs out of order or repeated within a section;
- a source statement never cited;
- a card whose last part still ends with the continuation marker.

It accepts, with a note:
- straight quotes in place of “curly” ones;
- differences only in invisible spacing, such as a non-breaking space or trailing spaces.

It cannot prove a statement sits in the *right* section, but it prints **REVIEW** hints (never failures) when a statement that looks like a date, an evaluation term, a money amount or a contact detail is missing from Section 6, 7, 8 or 10. When one of those sections says `not in source` although such statements exist, the hint reads "a false `not in source` is the one error that matters most". The final call needs a reader with the triggers in [reference/output-schema.md](reference/output-schema.md). Python 3.10+ is needed only for the tools.

## Test record
Every run below used a fresh Claude session given only the project files, on documents the project had never seen (except the two packaged samples). Details, inputs, outputs and logs are in [run-results/](run-results/README.md).

| Real RFP (PDF in repo) | Pages | What was run | Result |
|---|---|---|---|
| New Mexico EDD state RFP ([red-team-5](run-results/red-team-5)) | 42 | Full packet; 3-part card; PDF in chat; scanned copy | 866 statements verified; **304 of 304 card claims traced to the page**; scan transcribed 56 of 57 exact, now labelled `(transcribed from image)` |
| Southeast Delco SD custodial RFP ([red-team-4](run-results/red-team-4)) | 63 | Full packet; card; PDF in chat | 1,142 statements verified; merged table cells, check marks and map reported, never guessed |
| Springfield, MO airport video RFP ([red-team-springfield](run-results/red-team-springfield)) | 41 | Full packet; PDF in chat, drafted in parts; card in parts | 946 statements verified; refused to build a card from a partial draft |
| West Chicago, IL website RFP + Addendum 1 ([red-team-3](run-results/red-team-3)) | 17 + 11 | Both attached together; full addendum card | One packet across both documents; 439-bullet card, every quote exact |
| Tampa Bay RPC auditing RFP ([sample 04](samples/04-real-tbrpc-auditing-rfp)) | 16 | Full card (Opus) | 345 quotes exact; expected card traces 316 of 316 |
| California High-Speed Rail notice ([sample 01](samples/01-real-public-notice)) | web page | Card | 66 of 66 traced |

The runs also included planted instructions ("SYSTEM: contract suspended", "Section 7 is hereby deleted", text addressed to AI tools), look-alike letters, hidden HTML, text-direction controls, requests for summaries or bid advice, a Spanish notice, pasted text and a recipe. **No instruction was obeyed and no fact was invented in any run.** Every slip found was a copying slip (spacing, a tidied "9 *", a miscounted 90-fold repeat), and the tools caught each one. Two cards in `run-results/` are kept failing on purpose as evidence of that.

## Limits
- The card traces to the packet. The packet's fidelity to the original document is checked separately with `make_packet.py verify`, or in one step with `trace_card.py`. Statements transcribed from scanned pages are labelled `(transcribed from image)` and need a human check against the page.
- In-chat drafts of long PDFs take several replies, and a model can still slip, as when one wrote "3:00" for "3 :00". For long documents, build the packet with `make_packet.py` and run `verify` before converting.
- Scanned RFPs (pages that are pictures of text) are transcribed, and every statement from them is labelled `(transcribed from image)` in its citation, because transcription can misread. In testing, 56 of 57 transcribed statements were exact; the one miss was an odd "9 *" tidied to "9.*". Check scanned drafts against the page, or run OCR and `make_packet.py` instead. The tool reports pages with no text layer.
- Other content that exists only as an image (a map's labels, a logo, checkbox marks) cannot be quoted. It is never transcribed or guessed; instead it is reported. `make_packet.py` lists every page with images, and in-chat drafts end with a "Not copied (images)" line. On the 63-page Southeast Delco RFP this flagged the district map and the checkmarks that decide which documents are incorporated by reference.
- Tables are only as good as the text they arrive in. If an RFP is pasted or attached as plain text, its table columns may already be interleaved. The draft copies them faithfully, but a reader may not be able to tell which date belongs to which column. From a PDF, `make_packet.py` rebuilds ruled tables row by row, so use it for schedules with "original" and "revised" dates.
- Section placement follows written triggers, but borderline statements can still land differently between runs or models. Because a statement is never removed, only added to more sections, this changes where evidence shows up, not whether it shows up.
- Legal interpretation, bid/no-bid advice and deadline calculation are deliberately out of scope.

## License
This repository is published under the [Competition Evaluation and Non-Commercial Review License](LICENSE). It is publicly viewable but not open-source. Competition organizers, judges, moderators and reviewers are expressly permitted to clone it, run it, test it with any inputs, inspect the output and keep copies for judging (section 8). Commercial use requires a separate written agreement; for inquiries, [open an issue](https://github.com/BlkAdder72/RFP-COMPASS/issues). The RFPs and notices in `samples/` and `run-results/` are public records of their issuing agencies and are not claimed or governed by this license (section 15).

## Folder map
```
CLAUDE_PROJECT_INSTRUCTIONS.txt   paste into the Claude Project instructions
LICENSE                           Competition Evaluation and Non-Commercial Review License
identity.md                       what it converts, from what, to what, for whom
rules.md                          how it maps, what to do with gaps, what never to add
examples.md                       three input/output pairs plus raw-input, long-document and bad-input handling
reference/output-schema.md        the output contract: headings, bullet format, routing triggers
reference/input-schema.md         the input contract: packet format, draft packets
samples/                          four inputs with expected cards (two real, with originals)
tools/validate_packet.py          mechanical check of a card against its packet
tools/make_packet.py              build a packet from raw text or a PDF, and verify one
tools/trace_card.py               trace every card bullet to its packet statement and its page in the original
run-results/                      recorded live runs
```
