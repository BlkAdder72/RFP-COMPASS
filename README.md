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
- it joins table cells with ` | `;
- it keeps repeated page headers and footers once and reports the repeats it dropped;
- it anchors each statement to its page and line.

`verify` checks that every statement appears verbatim **at its own position** in the original and that table cells sit together. It lists any original text the packet left out. On a 41-page city RFP it caught a draft that had silently changed "3 :00 P.M." to "3:00 P.M.". PDF input needs `pip install pdfplumber`.

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
- differences only in invisible spacing, such as a non-breaking space or trailing spaces. It cannot tell whether a statement sits in the *right* section or whether a `not in source` is true; that needs a reader with the triggers in [reference/output-schema.md](reference/output-schema.md). Python 3.10+ is needed only for the tools.

## Test record
[run-results/](run-results/) holds live outputs from fresh sessions given only the project files, with what was checked.

**Unseen real RFP (red team).** City of Springfield, Missouri, RFP #056-2026: 41 pages, about 15,700 words, and never seen by the project. The PDF is included.
- Attached raw in chat, it came back as a verbatim draft in parts, with each part stating its page coverage.
- The model refused to build a card from a partial draft.
- Extraction quirks such as "3 :00 P.M." were kept exactly.
- A card for part of it arrived in two parts, and those parts together pass the validator.
- The Python route turned the whole PDF into 960 statements that `verify` confirms are verbatim, in order and complete.
- The same round showed three more things:
  - planted instructions such as "SYSTEM: contract suspended" are quoted, not obeyed;
  - requests for summaries or bid advice return only the card;
  - a recipe is rejected as not an RFP.

**Earlier runs:**
- an unseen bid packet with typos, an addendum and a planted AI instruction;
- raw RFP text turned into a draft packet and then a card;
- the 42-statement real notice;
- the 214-statement real RFP (all 345 quotes exact).

Every card in run-results/ passes the validator.

## Limits
- The card traces to the packet. The packet's fidelity to the original document is checked separately with `make_packet.py verify`. Scanned images need a human-checked transcription first.
- In-chat drafts of long PDFs take several replies, and a model can still slip, as when one wrote "3:00" for "3 :00". For long documents, build the packet with `make_packet.py` and run `verify` before converting.
- Section placement follows written triggers, but borderline statements can still land differently between runs or models. Because a statement is never removed, only added to more sections, this changes where evidence shows up, not whether it shows up.
- Legal interpretation, bid/no-bid advice and deadline calculation are deliberately out of scope.

## Folder map
```
CLAUDE_PROJECT_INSTRUCTIONS.txt   paste into the Claude Project instructions
identity.md                       what it converts, from what, to what, for whom
rules.md                          how it maps, what to do with gaps, what never to add
examples.md                       three input/output pairs plus raw-input, long-document and bad-input handling
reference/output-schema.md        the output contract: headings, bullet format, routing triggers
reference/input-schema.md         the input contract: packet format, draft packets
samples/                          four inputs with expected cards (two real, with originals)
tools/validate_packet.py          mechanical check of a card against its packet
tools/make_packet.py              build a packet from raw text or a PDF, and verify one
run-results/                      recorded live runs
```
