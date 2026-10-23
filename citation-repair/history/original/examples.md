# Examples

These pairs show the contract holding on a real notice, a sparse notice and an addendum that changes a deadline. Example 1 is text captured from a real public web page (see samples/01-real-public-notice/PROVENANCE.md); examples 2 and 3 are synthetic. A fourth, larger real example (a 16-page RFP, with its PDF) is in samples/04-real-tbrpc-auditing-rfp/. Examples are never evidence for a new run.

## 01-real-public-notice

A real procurement web page: title, scope, a responsibility table, schedule, procurement approach and contacts. Statements appear in every section whose trigger matches, the table rows appear in Section 9 and Section 2, and a bare link label falls to Section 12.

### Input (source-packet.md)

```text
S001 | TSCC-WEB page title | Track & Systems Construction Contract RFP
S002 | TSCC-WEB intro ¶1 | The California High-Speed Rail Authority (Authority) has released a Request for Proposals (RFP) to procure a Track & Systems Construction Contract (TSCC).
S003 | TSCC-WEB intro ¶2 | The purpose of this procurement is to select a contractor to provide construction work for track and overhead contact system (OCS) on the 119-mile First Construction Section of the California High-Speed Rail System, and design and construction for high-speed rail systems, including traction power, train control, and communication systems.
S004 | TSCC-WEB intro ¶2 | The TSCC Contractor will also be responsible for construction of track and OCS as well as design and construction of the high-speed rail systems for the Merced Extension and Bakersfield Extension.
S005 | TSCC-WEB intro ¶3 | The complete scope of work is provided in the RFP and draft agreement.
S006 | TSCC-WEB intro ¶3 | The not-to-exceed dollar value for this contract is $3.5 billion.
S007 | TSCC-WEB delivery model ¶ | The work will be delivered using a hybrid delivery model as outlined in the table below.
S008 | TSCC-WEB delivery model ¶ | This delivery method will incorporate managing cost and schedule, partnering, collaboration, in-depth communication, motivation for innovation, and progressive project development of construction packages.
S009 | TSCC-WEB delivery model ¶ | The Track & Systems Construction Contractor will work collaboratively with the Authority and the Track/OCS Design Services consultant, stakeholders, and other Interfacing Contractors to deliver the work.
S010 | TSCC-WEB delivery model ¶ | A draft table describing the delivery model for this contract is included below.
S011 | TSCC-WEB delivery model ¶ | This draft delivery model table is subject to change.
S012 | TSCC-WEB Notice of Proposed Award link line | The Notice of Proposed Award for the TSCC RFP is available to download here: Notice of Proposed Award
S013 | TSCC-WEB delivery model table header row | Initial Design | Detail Design | Construction | Integration | Material Supply
S014 | TSCC-WEB delivery model table row Track | Track | Authority | Authority | TSCC | TSCC | Authority*
S015 | TSCC-WEB delivery model table row OCS | OCS | Authority | Authority | TSCC | TSCC | Authority*
S016 | TSCC-WEB delivery model table row Traction Power | Traction Power | Authority | TSCC | TSCC | TSCC | TSCC
S017 | TSCC-WEB delivery model table row System (Signaling & Train Control) | System (Signaling & Train Control) | Authority | TSCC | TSCC | TSCC | TSCC
S018 | TSCC-WEB delivery model table row System Communication (fiber, radio systems, CCTV) | System Communication (fiber, radio systems, CCTV) | Authority | TSCC | TSCC | TSCC | TSCC
S019 | TSCC-WEB delivery model table row Power Generation | Power Generation | Authority | Authority | Authority | Authority | Authority
S020 | TSCC-WEB delivery model table row Rolling Stock | Rolling Stock | Authority | Authority | Authority | Authority | Authority
S021 | TSCC-WEB delivery model table footnote | *Material: Rail, Ballast, Ties, OCS Poles, OCS Components (including contact wire), Fiber Optic Cable ONLY.
S022 | TSCC-WEB Anticipated Schedule | Advertisement of RFP: November 26, 2025
S023 | TSCC-WEB Anticipated Schedule | Pre-bid Conference and Small Business Workshop: December 19, 2025, in Sacramento
S024 | TSCC-WEB Anticipated Schedule link label | Registration List
S025 | TSCC-WEB Anticipated Schedule | Proposals Due: April 9, 2026
S026 | TSCC-WEB Anticipated Schedule CSCR paragraph | The RFP is available to download from the California State Contracts Register (CSCR)
S027 | TSCC-WEB Anticipated Schedule CSCR paragraph | Updates, including responses to written questions and any RFP addenda, will be provided on the CSCR.
S028 | TSCC-WEB Procurement Approach ¶1 | The one-step TSCC Procurement will require each interested proposing team to submit a Notice of Intent to Propose as a precondition to participation in procurement One-on-One Meetings with the Authority.
S029 | TSCC-WEB Procurement Approach ¶1 | The RFP will require teams to identify the following:
S030 | TSCC-WEB Procurement Approach list item 1 | lead designer(s) for each systems element, including traction power, train control, and communications systems;
S031 | TSCC-WEB Procurement Approach list item 2 | lead integrator;
S032 | TSCC-WEB Procurement Approach list item 3 | lead contractor(s) for:
S033 | TSCC-WEB Procurement Approach list item 3(a) | the track and OCS construction work; and
S034 | TSCC-WEB Procurement Approach list item 3(b) | systems construction elements, including traction power, train control, and communications systems; and systems elements of the construction work; and
S035 | TSCC-WEB Procurement Approach list item 4 | lead firm(s) responsible for integration testing and commissioning.
S036 | TSCC-WEB Procurement Approach ¶2 | The RFP will not require the identification of equipment manufacturer of traction power, train control, communication systems and OEMs/vendors at this time.
S037 | TSCC-WEB Procurement Approach ¶2 | The TSCC will provide a mechanism whereby the TSCC will undertake the solicitation of these OEMs/vendors post-award, in collaboration with the Authority, on an open book basis, following further advancement of the associated design work by the TSCC.
S038 | TSCC-WEB Procurement Approach ¶2 | The RFP is anticipated to require detailed pricing for track and OCS of the construction work.
S039 | TSCC-WEB small business ¶ | Visit the Authority’s Small Business Program webpage for information including a program overview, certifications we recognize, how to get certified, access to our vendor registry, and more.
S040 | TSCC-WEB organizational conflict of interest ¶ | To avoid organizational conflicts of interest, prime firm(s) awarded the TSCC cannot also be awarded contracts that cause conflict.
S041 | TSCC-WEB organizational conflict of interest ¶ | If you have questions about potential organizational conflicts of interest, please review the Authority’s Organizational Conflict of Interest Policy at the following link and submit queries and/or a request for an Organizational Conflict of Interest determination to the Authority’s Chief Counsel at legal@hsr.ca.gov, expressly referencing the TSCC RFP.
S042 | TSCC-WEB questions ¶ | Questions regarding this procurement should be submitted to Emily Morrison at TSCC@hsr.ca.gov or (916) 324-1541.
```

### Expected output (bid-compliance-card.md)

```markdown
# RFP COMPASS — BID COMPLIANCE CARD

## 1. Opportunity identity
- “Track & Systems Construction Contract RFP” [source: source-packet.md:S001; TSCC-WEB page title]
- “The California High-Speed Rail Authority (Authority) has released a Request for Proposals (RFP) to procure a Track & Systems Construction Contract (TSCC).” [source: source-packet.md:S002; TSCC-WEB intro ¶1]
- “The RFP is available to download from the California State Contracts Register (CSCR)” [source: source-packet.md:S026; TSCC-WEB Anticipated Schedule CSCR paragraph]

## 2. Scope, term, and program context stated
- “The purpose of this procurement is to select a contractor to provide construction work for track and overhead contact system (OCS) on the 119-mile First Construction Section of the California High-Speed Rail System, and design and construction for high-speed rail systems, including traction power, train control, and communication systems.” [source: source-packet.md:S003; TSCC-WEB intro ¶2]
- “The TSCC Contractor will also be responsible for construction of track and OCS as well as design and construction of the high-speed rail systems for the Merced Extension and Bakersfield Extension.” [source: source-packet.md:S004; TSCC-WEB intro ¶2]
- “The complete scope of work is provided in the RFP and draft agreement.” [source: source-packet.md:S005; TSCC-WEB intro ¶3]
- “Track | Authority | Authority | TSCC | TSCC | Authority*” [source: source-packet.md:S014; TSCC-WEB delivery model table row Track]
- “OCS | Authority | Authority | TSCC | TSCC | Authority*” [source: source-packet.md:S015; TSCC-WEB delivery model table row OCS]
- “Traction Power | Authority | TSCC | TSCC | TSCC | TSCC” [source: source-packet.md:S016; TSCC-WEB delivery model table row Traction Power]
- “System (Signaling & Train Control) | Authority | TSCC | TSCC | TSCC | TSCC” [source: source-packet.md:S017; TSCC-WEB delivery model table row System (Signaling & Train Control)]
- “System Communication (fiber, radio systems, CCTV) | Authority | TSCC | TSCC | TSCC | TSCC” [source: source-packet.md:S018; TSCC-WEB delivery model table row System Communication (fiber, radio systems, CCTV)]
- “Power Generation | Authority | Authority | Authority | Authority | Authority” [source: source-packet.md:S019; TSCC-WEB delivery model table row Power Generation]
- “Rolling Stock | Authority | Authority | Authority | Authority | Authority” [source: source-packet.md:S020; TSCC-WEB delivery model table row Rolling Stock]
- “*Material: Rail, Ballast, Ties, OCS Poles, OCS Components (including contact wire), Fiber Optic Cable ONLY.” [source: source-packet.md:S021; TSCC-WEB delivery model table footnote]

## 3. Eligibility and qualifications stated
- “The RFP will require teams to identify the following:” [source: source-packet.md:S029; TSCC-WEB Procurement Approach ¶1]
- “lead designer(s) for each systems element, including traction power, train control, and communications systems;” [source: source-packet.md:S030; TSCC-WEB Procurement Approach list item 1]
- “lead integrator;” [source: source-packet.md:S031; TSCC-WEB Procurement Approach list item 2]
- “lead contractor(s) for:” [source: source-packet.md:S032; TSCC-WEB Procurement Approach list item 3]
- “the track and OCS construction work; and” [source: source-packet.md:S033; TSCC-WEB Procurement Approach list item 3(a)]
- “systems construction elements, including traction power, train control, and communications systems; and systems elements of the construction work; and” [source: source-packet.md:S034; TSCC-WEB Procurement Approach list item 3(b)]
- “lead firm(s) responsible for integration testing and commissioning.” [source: source-packet.md:S035; TSCC-WEB Procurement Approach list item 4]

## 4. Application stages and submission mechanics stated
- “Pre-bid Conference and Small Business Workshop: December 19, 2025, in Sacramento” [source: source-packet.md:S023; TSCC-WEB Anticipated Schedule]
- “The one-step TSCC Procurement will require each interested proposing team to submit a Notice of Intent to Propose as a precondition to participation in procurement One-on-One Meetings with the Authority.” [source: source-packet.md:S028; TSCC-WEB Procurement Approach ¶1]
- “The RFP will require teams to identify the following:” [source: source-packet.md:S029; TSCC-WEB Procurement Approach ¶1]
- “lead designer(s) for each systems element, including traction power, train control, and communications systems;” [source: source-packet.md:S030; TSCC-WEB Procurement Approach list item 1]
- “lead integrator;” [source: source-packet.md:S031; TSCC-WEB Procurement Approach list item 2]
- “lead contractor(s) for:” [source: source-packet.md:S032; TSCC-WEB Procurement Approach list item 3]
- “the track and OCS construction work; and” [source: source-packet.md:S033; TSCC-WEB Procurement Approach list item 3(a)]
- “systems construction elements, including traction power, train control, and communications systems; and systems elements of the construction work; and” [source: source-packet.md:S034; TSCC-WEB Procurement Approach list item 3(b)]
- “lead firm(s) responsible for integration testing and commissioning.” [source: source-packet.md:S035; TSCC-WEB Procurement Approach list item 4]
- “The RFP will not require the identification of equipment manufacturer of traction power, train control, communication systems and OEMs/vendors at this time.” [source: source-packet.md:S036; TSCC-WEB Procurement Approach ¶2]

## 5. Mandatory attachments and forms stated
- “The one-step TSCC Procurement will require each interested proposing team to submit a Notice of Intent to Propose as a precondition to participation in procurement One-on-One Meetings with the Authority.” [source: source-packet.md:S028; TSCC-WEB Procurement Approach ¶1]

## 6. Dates and events stated
- “The Notice of Proposed Award for the TSCC RFP is available to download here: Notice of Proposed Award” [source: source-packet.md:S012; TSCC-WEB Notice of Proposed Award link line]
- “Advertisement of RFP: November 26, 2025” [source: source-packet.md:S022; TSCC-WEB Anticipated Schedule]
- “Pre-bid Conference and Small Business Workshop: December 19, 2025, in Sacramento” [source: source-packet.md:S023; TSCC-WEB Anticipated Schedule]
- “Proposals Due: April 9, 2026” [source: source-packet.md:S025; TSCC-WEB Anticipated Schedule]
- “The one-step TSCC Procurement will require each interested proposing team to submit a Notice of Intent to Propose as a precondition to participation in procurement One-on-One Meetings with the Authority.” [source: source-packet.md:S028; TSCC-WEB Procurement Approach ¶1]

## 7. Evaluation stated
- not in source

## 8. Commercial, performance, and post-award terms stated
- “The not-to-exceed dollar value for this contract is $3.5 billion.” [source: source-packet.md:S006; TSCC-WEB intro ¶3]
- “The work will be delivered using a hybrid delivery model as outlined in the table below.” [source: source-packet.md:S007; TSCC-WEB delivery model ¶]
- “This delivery method will incorporate managing cost and schedule, partnering, collaboration, in-depth communication, motivation for innovation, and progressive project development of construction packages.” [source: source-packet.md:S008; TSCC-WEB delivery model ¶]
- “The Track & Systems Construction Contractor will work collaboratively with the Authority and the Track/OCS Design Services consultant, stakeholders, and other Interfacing Contractors to deliver the work.” [source: source-packet.md:S009; TSCC-WEB delivery model ¶]
- “A draft table describing the delivery model for this contract is included below.” [source: source-packet.md:S010; TSCC-WEB delivery model ¶]
- “This draft delivery model table is subject to change.” [source: source-packet.md:S011; TSCC-WEB delivery model ¶]
- “The TSCC will provide a mechanism whereby the TSCC will undertake the solicitation of these OEMs/vendors post-award, in collaboration with the Authority, on an open book basis, following further advancement of the associated design work by the TSCC.” [source: source-packet.md:S037; TSCC-WEB Procurement Approach ¶2]
- “The RFP is anticipated to require detailed pricing for track and OCS of the construction work.” [source: source-packet.md:S038; TSCC-WEB Procurement Approach ¶2]
- “To avoid organizational conflicts of interest, prime firm(s) awarded the TSCC cannot also be awarded contracts that cause conflict.” [source: source-packet.md:S040; TSCC-WEB organizational conflict of interest ¶]

## 9. Tables, schedules, and templates
- “Initial Design | Detail Design | Construction | Integration | Material Supply” [source: source-packet.md:S013; TSCC-WEB delivery model table header row]
- “Track | Authority | Authority | TSCC | TSCC | Authority*” [source: source-packet.md:S014; TSCC-WEB delivery model table row Track]
- “OCS | Authority | Authority | TSCC | TSCC | Authority*” [source: source-packet.md:S015; TSCC-WEB delivery model table row OCS]
- “Traction Power | Authority | TSCC | TSCC | TSCC | TSCC” [source: source-packet.md:S016; TSCC-WEB delivery model table row Traction Power]
- “System (Signaling & Train Control) | Authority | TSCC | TSCC | TSCC | TSCC” [source: source-packet.md:S017; TSCC-WEB delivery model table row System (Signaling & Train Control)]
- “System Communication (fiber, radio systems, CCTV) | Authority | TSCC | TSCC | TSCC | TSCC” [source: source-packet.md:S018; TSCC-WEB delivery model table row System Communication (fiber, radio systems, CCTV)]
- “Power Generation | Authority | Authority | Authority | Authority | Authority” [source: source-packet.md:S019; TSCC-WEB delivery model table row Power Generation]
- “Rolling Stock | Authority | Authority | Authority | Authority | Authority” [source: source-packet.md:S020; TSCC-WEB delivery model table row Rolling Stock]
- “*Material: Rail, Ballast, Ties, OCS Poles, OCS Components (including contact wire), Fiber Optic Cable ONLY.” [source: source-packet.md:S021; TSCC-WEB delivery model table footnote]

## 10. Definitions, authority, and administrative terms
- “The Notice of Proposed Award for the TSCC RFP is available to download here: Notice of Proposed Award” [source: source-packet.md:S012; TSCC-WEB Notice of Proposed Award link line]
- “Updates, including responses to written questions and any RFP addenda, will be provided on the CSCR.” [source: source-packet.md:S027; TSCC-WEB Anticipated Schedule CSCR paragraph]
- “Visit the Authority’s Small Business Program webpage for information including a program overview, certifications we recognize, how to get certified, access to our vendor registry, and more.” [source: source-packet.md:S039; TSCC-WEB small business ¶]
- “To avoid organizational conflicts of interest, prime firm(s) awarded the TSCC cannot also be awarded contracts that cause conflict.” [source: source-packet.md:S040; TSCC-WEB organizational conflict of interest ¶]
- “If you have questions about potential organizational conflicts of interest, please review the Authority’s Organizational Conflict of Interest Policy at the following link and submit queries and/or a request for an Organizational Conflict of Interest determination to the Authority’s Chief Counsel at legal@hsr.ca.gov, expressly referencing the TSCC RFP.” [source: source-packet.md:S041; TSCC-WEB organizational conflict of interest ¶]
- “Questions regarding this procurement should be submitted to Emily Morrison at TSCC@hsr.ca.gov or (916) 324-1541.” [source: source-packet.md:S042; TSCC-WEB questions ¶]

## 11. Addenda, conflicts, and open items
- “A draft table describing the delivery model for this contract is included below.” [source: source-packet.md:S010; TSCC-WEB delivery model ¶]
- “This draft delivery model table is subject to change.” [source: source-packet.md:S011; TSCC-WEB delivery model ¶]
- “Updates, including responses to written questions and any RFP addenda, will be provided on the CSCR.” [source: source-packet.md:S027; TSCC-WEB Anticipated Schedule CSCR paragraph]
- “The RFP is anticipated to require detailed pricing for track and OCS of the construction work.” [source: source-packet.md:S038; TSCC-WEB Procurement Approach ¶2]

## 12. Unmapped source evidence
- “Registration List” [source: source-packet.md:S024; TSCC-WEB Anticipated Schedule link label]
```

## 02-sparse

Two statements. Every section with no matching statement says `not in source`.

### Input (source-packet.md)

```text
S001 | NOTICE-01 official posting | Proposals must be submitted through the vendor portal.
S002 | NOTICE-01 official posting | Questions may be sent to procurement@example.invalid.
```

### Expected output (bid-compliance-card.md)

```markdown
# RFP COMPASS — BID COMPLIANCE CARD

## 1. Opportunity identity
- “Proposals must be submitted through the vendor portal.” [source: source-packet.md:S001; NOTICE-01 official posting]

## 2. Scope, term, and program context stated
- not in source

## 3. Eligibility and qualifications stated
- not in source

## 4. Application stages and submission mechanics stated
- “Proposals must be submitted through the vendor portal.” [source: source-packet.md:S001; NOTICE-01 official posting]

## 5. Mandatory attachments and forms stated
- not in source

## 6. Dates and events stated
- not in source

## 7. Evaluation stated
- not in source

## 8. Commercial, performance, and post-award terms stated
- not in source

## 9. Tables, schedules, and templates
- not in source

## 10. Definitions, authority, and administrative terms
- “Questions may be sent to procurement@example.invalid.” [source: source-packet.md:S002; NOTICE-01 official posting]

## 11. Addenda, conflicts, and open items
- not in source

## 12. Unmapped source evidence
- not in source
```

## 03-conflicting

An original deadline and an addendum extending it. Both dates are kept word for word, and the card does not choose which one controls.

### Input (source-packet.md)

```text
S001 | RFP-01 p. 4 | Proposals are due on May 1, 2027, at 2:00 p.m. Eastern Time.
S002 | ADD-01 p. 1 | The proposal deadline is extended to May 8, 2027, at 2:00 p.m. Eastern Time.
S003 | ADD-01 p. 1 | Respondents must acknowledge Addendum 1 with their proposal.
```

### Expected output (bid-compliance-card.md)

```markdown
# RFP COMPASS — BID COMPLIANCE CARD

## 1. Opportunity identity
- not in source

## 2. Scope, term, and program context stated
- not in source

## 3. Eligibility and qualifications stated
- not in source

## 4. Application stages and submission mechanics stated
- “Respondents must acknowledge Addendum 1 with their proposal.” [source: source-packet.md:S003; ADD-01 p. 1]

## 5. Mandatory attachments and forms stated
- “Respondents must acknowledge Addendum 1 with their proposal.” [source: source-packet.md:S003; ADD-01 p. 1]

## 6. Dates and events stated
- “Proposals are due on May 1, 2027, at 2:00 p.m. Eastern Time.” [source: source-packet.md:S001; RFP-01 p. 4]
- “The proposal deadline is extended to May 8, 2027, at 2:00 p.m. Eastern Time.” [source: source-packet.md:S002; ADD-01 p. 1]

## 7. Evaluation stated
- not in source

## 8. Commercial, performance, and post-award terms stated
- not in source

## 9. Tables, schedules, and templates
- not in source

## 10. Definitions, authority, and administrative terms
- not in source

## 11. Addenda, conflicts, and open items
- “The proposal deadline is extended to May 8, 2027, at 2:00 p.m. Eastern Time.” [source: source-packet.md:S002; ADD-01 p. 1]
- “Respondents must acknowledge Addendum 1 with their proposal.” [source: source-packet.md:S003; ADD-01 p. 1]

## 12. Unmapped source evidence
- not in source
```

## Input handling (not a card)

### Raw RFP text attached instead of a packet

The user attaches `harlow-rfp.txt`:

```text
CITY OF HARLOW SPRINGS
REQUEST FOR PROPOSALS #HS-25-07
JANITORIAL SERVICES FOR CITY HALL

1. INTRODUCTION
The City of Harlow Springs invites proposals from qualified firms to provide nightly janitorial services at City Hall, 200 Main Street. The initial term is two (2) years.

2. SUBMISSION
Proposals are due no later than 3:00 PM on November 3, 2026. Submit three (3) hard copies and one electronic copy on USB to the City Clerk's Office. Late proposals will not be accepted.

3. EVALUATION
Price 40%; Experience 35%; References 25%.

4. CONTACT
Questions: Dana Whitcombe, Procurement Officer, dwhitcombe@harlowsprings.example. Questions due October 20, 2026.
```

Expected response:

````markdown
INPUT NOT READY
The attached file is raw RFP text, not a line-numbered source packet. Here is a draft packet copied from it without rewording. Repeated page headers/footers kept once: none. Not copied (images): none. Check it against the original, then reply `use the draft packet` or attach a corrected source-packet.md.

```source-packet.md
S001 | harlow-rfp.txt line 1 | CITY OF HARLOW SPRINGS
S002 | harlow-rfp.txt line 2 | REQUEST FOR PROPOSALS #HS-25-07
S003 | harlow-rfp.txt line 3 | JANITORIAL SERVICES FOR CITY HALL
S004 | harlow-rfp.txt line 5 | 1. INTRODUCTION
S005 | harlow-rfp.txt line 6 | The City of Harlow Springs invites proposals from qualified firms to provide nightly janitorial services at City Hall, 200 Main Street.
S006 | harlow-rfp.txt line 6 | The initial term is two (2) years.
S007 | harlow-rfp.txt line 8 | 2. SUBMISSION
S008 | harlow-rfp.txt line 9 | Proposals are due no later than 3:00 PM on November 3, 2026.
S009 | harlow-rfp.txt line 9 | Submit three (3) hard copies and one electronic copy on USB to the City Clerk's Office.
S010 | harlow-rfp.txt line 9 | Late proposals will not be accepted.
S011 | harlow-rfp.txt line 11 | 3. EVALUATION
S012 | harlow-rfp.txt line 12 | Price 40%; Experience 35%; References 25%.
S013 | harlow-rfp.txt line 14 | 4. CONTACT
S014 | harlow-rfp.txt line 15 | Questions: Dana Whitcombe, Procurement Officer, dwhitcombe@harlowsprings.example.
S015 | harlow-rfp.txt line 15 | Questions due October 20, 2026.
```
````

After the user replies `use the draft packet`, the draft is the active input and the card cites it (for example `[source: source-packet.md:S005; harlow-rfp.txt line 6]`).

### Packet with defects

```text
S001 | RFQ-9 p. 1 | County of Ashdown seeks quotes for printing services.
S003 | RFQ-9 p. 1 | Quotes are due September 30, 2026.
S004 | | Contact the buyer with questions.
```

Expected response:

```markdown
INPUT NOT READY
- IDs are not sequential: S002 is missing between S001 and S003.
- S004 has an empty source anchor.
Correct the packet and attach it again. No card is produced from a defective packet.
```

### Long document: draft in parts, never a card from a partial draft

The user attaches `springfield-rfp.pdf` (41 pages) and asks for the card. The first reply is part 1 of the draft:

````markdown
INPUT NOT READY
The attached PDF is raw RFP text, not a line-numbered source packet. Draft packet part 1: S001–S160, pages 1–8 of 41. Not complete. Reply `continue` for the next part.

```source-packet.md
S001 | springfield-rfp.pdf p. 1 | RFP #056-2026
...
S160 | springfield-rfp.pdf p. 8 | 4.2 A proposal may only be modified by the following method prior to the official opening date and time specified:
```
````

If the user replies `use the draft packet` now, the answer is not a card:

```markdown
INPUT NOT READY
The draft packet is not complete: it covers pages 1–8 of 41 (S001–S160). A card made from part of the document would mark sections "not in source" that later pages may fill. Reply `continue` for the next part.
```

Each later part continues the numbering. The last part ends: `Draft packet part 4 of 4: S481–S612, pages 33–41 of 41. The draft is now complete (S001–S612, all 41 pages). Repeated page headers/footers kept once: "RFP #056-2026" (on 41 pages); "Page N of 41" (on 41 pages); "Revised: 02/04/2026" (on 40 pages); "Reviewed by Law: 03/06/2024" (on 41 pages). Not copied (images): p. 17 and p. 18 E-Verify form graphics and checkboxes. Check it against the original, then reply use the draft packet.`

### Copying extraction quirks exactly

A PDF's text reads `Post RFP Notification Tuesday, March 3, 2026, at 3 :00 P.M. (CST)`. The draft statement keeps the space before the colon:

```text
S224 | springfield-rfp.pdf p. 6 | Post RFP Notification | Tuesday, March 3, 2026, at 3 :00 P.M. (CST)
```

Writing `3:00` would be a correction, and corrections are not allowed. The card quotes the statement the same way.

### Long card: delivered in parts

When a complete card will not fit in one reply, the reply stops after a complete line and ends with the continuation marker:

```markdown
- “Proposals must be received electronically in the City’s e-bidding service provider Euna OpenBids (formerly DemandStar) by 3:00 P.M. (CST), on TUESDAY, MARCH 31, 2026.” [source: source-packet.md:S054; RFP-056 p. 2 line 16]
<!-- RFP COMPASS: continued in next reply -->
```

After the user replies `continue`, the next reply starts with the next bullet or heading, with no title, repeated heading or introduction. The last part has no marker.
