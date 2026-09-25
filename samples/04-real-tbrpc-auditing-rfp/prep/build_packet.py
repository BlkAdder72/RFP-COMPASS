# Builds source-packet.md from the TBRPC Auditing Services RFP (16 pp.), transcribed by hand from
# the pdftotext output and checked against page positions. Line-wraps joined; bullet glyphs dropped.
# Omitted as non-evidence: page-2 table of contents, section heading lines (moved into anchors).
from pathlib import Path

D = "TBRPC Auditing RFP"
L = []
def add(anchor, text): L.append((f"{D} {anchor}", text))

add("p. 1 memo header", "FROM: Maria Robles, Manager of Administration/Public Information, TBRPC")
add("p. 1 memo header", "DATE: June 26, 2026")
add("p. 1 memo header", "RE: Request for Proposals: Auditing Services for Tampa Bay Regional Planning Council (TBRPC)")
add("p. 1 memo body", "The Tampa Bay Regional Planning Council (TBRPC) is seeking proposals from qualified independent auditors to provide auditing services.")
add("p. 1 memo body", "The Consultant must have sufficient governmental accounting and auditing experience in performing an audit in accordance with the specifications outlined in this Request for Proposal (RFP).")
add("p. 1 Contact", "For questions and clarifications, please contact Maria Robles, Manager of Administration in writing via email maria@tbrpc.org.")
add("p. 1 Contact", "All responses to questions and clarifications will be posted publicly on www.tbrpc.org/rfp in accordance with the RFP Timeline provided.")
add("p. 1 footer", "Issue Date: June 26, 2026")
add("p. 1 footer", "Submittal Deadline: July 17, 2026")

s = "p. 3 §1 About the TBRPC"
add(s, "The Tampa Bay Regional Planning Council (TBRPC) brings together governments to coordinate planning for the community's future and provides an opportunity for sharing solutions among the local government jurisdictions in the six-county Tampa Bay region.")
add(s, "The TBRPC was established as Florida's first regional planning council in 1962, when representatives from St. Petersburg, Clearwater, and Tampa recognized the need for regional coordination.")
add(s, "They believed growth and community issues extend beyond county and municipal boundaries, a concept that still defines the Council's purpose today.")
add(s, "The TBRPC is one of ten regional planning councils in Florida.")
add(s, "The Council's fiscal year is October 1st through September 30th.")
add(s, "The Council currently uses QBO accounting software and will be converting to AccuFund for fiscal year 2027.")
add(s, "The Council maintains one main operating checking account.")
add(s, "Total accounts payable and payroll transactions issued throughout the year total approximately 1,000.")
add(s, "The current operating budget is $3.7 million.")
add(s, "The Council may require a single audit to be performed depending on the federal funding levels.")

s = "p. 3 §2 Introduction"
add(s, "The Tampa Bay Regional Planning Council (TBRPC) is seeking proposals from qualified independent auditors to provide auditing services.")
add(s, "The auditor must have sufficient governmental accounting and auditing experience in performing an audit in accordance with the specifications outlined in this Request for Proposal (RFP).")
add(s, "The RFP will be for the fiscal years ending September 30, 2026, 2027, and 2028.")
add(s, "The contract for the fiscal years ending in 2027 and 2028 may be terminated by either party in writing no later than September 30, 2027, and September 30, 2028, respectively.")
add(s, "Each year's contract price is to be determined at the award of the proposal.")

add("p. 3 §3 Scope of Services", "Audits shall be performed in accordance with the following:")
for pg, t in [
    ("p. 3", "Generally accepted auditing standards in the United States of America;"),
    ("p. 4", "Government Auditing Standards, as issued by the Comptroller General of the United States;"),
    ("p. 4", "The requirements of the State of Florida and the rules and regulations of the Auditor General;"),
    ("p. 4", "Uniform Guidance (2 CFR 200) and Section 215.97 Florida Statutes, Single Audit Act;"),
    ("p. 4", "Title 2 U.S. Code of Federal Regulations Part 200, Uniform Administrative Requirements Cost Principles, and Audit Requirements for Federal Awards (Uniform Guidance); and"),
    ("p. 4", "Any other applicable Federal, State, and local laws or regulations."),
]:
    add(f"{pg} §3 auditing standards bullet", t)
add("p. 4 §3 Scope of Services", "The respondent will be required to complete the following deliverables:")
for pg, t in [
    ("p. 4", "Conduct a financial audit and a compliance audit in accordance with auditing standards detailed in Section II. C. Required Auditing Standards To Be Followed above."),
    ("p. 4", "Complete a report on the fair presentation of the financial statements in conformity with generally accepted accounting principles (GAAP)."),
    ("p. 4", "Complete a report on internal control over financial reporting and on compliance and other matters based on an audit of the financial statement performed in accordance with Governmental Auditing Standards and a communication of internal control matters identified in the audit to those charged with governance and management."),
    ("p. 4", "Complete a report on compliance for each major federal program and on internal control over compliance required by the Uniform Guidance and Chapter 10.550, Rules of the Auditor General and the Florida Single Audit Act, Section 215.97, Florida Statutes, as applicable."),
    ("p. 4", "Present the audit to the Council's Personnel, Executive Budget Committee, and Council Board."),
    ("p. 5", "Prepare the Data Collection Form for Reporting on Audits of States, Local Governments, and Non-Profit Organizations as required by Uniform Guidance."),
    ("p. 5", "Serve as audit and accounting consultant to the Council throughout the agreement period and as such provide necessary information and assistance on an as needed basis."),
    ("p. 5", "Prepare all required tax returns for the Council."),
    ("p. 5", "The Council is required to file one 990 Return of Organization Exempt from Income Tax."),
    ("p. 5", "If the Auditing Firm, due to one or more accounting and/or reporting deficiencies, is required to give advice, testimony, or other such activity not within the scope of rendering, confirming, or justifying a report of audit services rendered, such service will be made without an additional charge to the Council."),
    ("p. 5", "The Auditing Firm will obtain corrective action and submit audit reports to appropriate agencies."),
    ("p. 5", "Any preliminary findings of possible fraud, misapplication or misappropriation of funds shall be immediately reported to the Executive Director of the Council."),
]:
    add(f"{pg} §3 deliverables bullet", t)

add("p. 5 §4 Minimum Qualifications", "Auditor must meet the following minimum qualifications to be considered responsive to this RFP:")
add("p. 5 §4.I", "I. The firm must have been established as a legal entity in the State of Florida and have performed continuous CPA services for a minimum of (5) years.")
add("p. 5 §4.II", "II. The firm must submit an affirmation that proposer meets Government Auditing Standards independence requirements, as published by the U.S. General Accounting Office.")
add("p. 5 §4.III", "III. Government Auditing Standards require the Certified Public Accountant in charge of the audit to have completed, within the preceding 2 years, at least 24 hours of continuing professional education that directly relates to government auditing and will enhance the professional proficiency of the auditor to perform audits or attestation agreements.")
add("p. 6 §4.IV", "IV. The firm must clearly state the government expertise of its staff at the local office level that will be assigned to this project in its proposal.")

s = "p. 6 §5 Submittal Content, Format, and Instructions"
add(s, "All submittals must follow the format guidelines and content requirements listed below.")
add(s, "Nonconforming submittals may be rejected as nonresponsive.")
add("p. 6 §5.I", "I. Letter of Interest (5 pages maximum).")
add("p. 6 §5.I", "Please include in the submittal a letter introducing the auditor and expressing the auditor's interest in being considered for auditing services.")
add("p. 6 §5.I", "The letter of interest should also include all the following:")
add("p. 6 §5.I.a", "a. Describe the organization and provide the name of the entity, its mailing address, and telephone number.")
add("p. 6 §5.I.b", "b. Indicate that the auditor has the availability and time to dedicate the personnel and resources necessary to provide auditing services and an affirmative statement that it is independent of TBRPC as defined by generally accepted auditing standards and the U.S. General Accounting Office's Government Auditing Standards (2003).")
add("p. 6 §5.I.c", "c. License to Practice in Florida – An affirmative statement should be included that the firm and/or its partners are properly licensed to practice in Florida, and all supervisory staff are licensed or qualified to be licensed to practice in Florida.")
add("p. 6 §5.I.d", "d. Indicate that the auditor has the minimum qualifications listed in Section 4 above.")
add("p. 6 §5.I.e", "e. Indicate the intention of the auditor to adhere to the provisions described in the RFP.")
add("p. 6 §5.I.e", "Include a statement of the Auditing Firm's understanding of the work to be performed.")
add("p. 6 §5.I.e", "Include time estimates for completion of the audit.")
add("p. 6 §5.I.f", "f. Identify the contact person responsible for the submittal, specifying the name, title, and contact information.")
add("p. 6 §5.I.f", "Note that the person signing the letter of interest must be a legal representative authorized to bind the auditor to an agreement in the event of an award.")
add("p. 7 §5.II", "II. Relevant Experience of Key Personnel and the Firm (10 pages maximum).")
add("p. 7 §5.II.a", "a. Key Personnel Experience. The submittal must include resumes of the key personnel that are to be assigned if awarded a contract, detailing their qualifications, certifications, and areas of expertise.")
add("p. 7 §5.II.a", "Indicate whether each person is registered or licensed to practice as a Certified Public Accountant in Florida.")
add("p. 7 §5.II.a", "Provide information on the government auditing experience of each person, including information on relevant continuing professional education for the past three (3) years and membership in professional organizations relevant to the performance of this audit.")
add("p. 7 §5.II.b", "b. Firm Experience. The Auditing Firm should describe its prior auditing experience.")
add("p. 7 §5.II.b", "It should include the following categories:")
add("p. 7 §5.II.b bullet", "Prior experience with performing audits in accordance with the auditing standards.")
add("p. 7 §5.II.b bullet", "Prior experience auditing similar multi-funded programs funded by the State of Florida and the Federal Government.")
add("p. 7 §5.II.b bullet", "The Auditing Firm must include a copy of the most recent peer review report, the related letters of comments, and the firm's response to the letter of comments.")
add("p. 7 §5.II.c", "c. General Firm Information. General firm information including the number of employees, location of firm headquarters, branch offices, and number of years in business may also be provided.")
add("p. 7 §5.II.c", "Please note that general firm information is not a substitute for the specific information requested above.")
add("p. 7 §5.II.c.i", "i. The firm is also required to submit a copy of the report on its most recent external quality control review, with a statement of whether that quality control review included a review of specific government engagements.")
add("p. 7 §5.II.c.ii", "ii. The firm shall also provide information on the results of any federal or state desk reviews or field reviews of its audits during the past three (3) years.")
add("pp. 7-8 §5.II.c.ii", "In addition, the firm shall provide information on the circumstances and status of any disciplinary action taken or pending against the firm during the past three (3) years with state regulatory bodies or professional organizations.")
add("p. 8 §5.III", "III. Required Certifications. The firm must be able to provide the following certifications.")
add("p. 8 §5.III.a", "a. Public Entity Crimes Certification. In accordance with Florida Statutes section 287.133(3) (a), the Consultant will complete and return as part of the RFP the Public Entity Crimes Certification form.")
add("p. 8 §5.III.b", "b. Drug-Free Workplace Certification. In accordance with Florida Statutes section 287.087, the Consultant will complete and return as part of the RFP the Drug-Free Workplace Certification form.")
add("p. 8 §5.IV", "IV. Insurance Requirement. The Auditing Firm awarded the contract shall secure, maintain, and present insurance coverage reflecting the minimum insurance requirements by the State of Florida for general liability, professional liability, and worker's compensation to include employer's liability limits as required by the State of Florida.")
add("p. 8 §5.IV", "The firm must also name the Council as an additional insured on general liability and professional liability.")
add("p. 8 §5.V", "V. Fee Structure. Please include a Total All-Inclusive Maximum Price.")
add("p. 8 §5.V", "The bid should contain all pricing information related to performing the audit engagement as described in this request for proposal.")
add("p. 8 §5.V", "The total all-inclusive maximum price bid is to contain all direct and indirect costs including all out-of-pocket expenses.")
add("p. 8 §5.V", "All out-of-pocket expenses should be included in Attachment B.")
add("p. 8 §5.V.a", "a. Rates for Additional Professional Services. If it should become necessary for TBRPC to request the auditor to render any additional services to either supplement the services requested in this RFP or to perform additional work as a result of the specific recommendations included in any report issued on this engagement, then such additional work shall be performed only if set forth in an addendum to the contract between TBRPC and the firm.")
add("p. 8 §5.V.a", "Any additional work agreed to between TBRPC and the firm shall be performed at the same rates set forth in the Attachment B Schedule of Fees and Expenses included in the bid.")
add("p. 8 §5.VI", "VI. Client References. The consultant must provide a minimum of three (3) client references by completing Attachment A.")
add("pp. 8-9 §5.VI", "The consultant's submission of an RFP application constitutes the consultant's express consent for TBRPC staff to contact the listed references to inquire regarding the qualifications of the consultant.")

add("p. 9 §6.I Questions", "I. Questions. All questions concerning the RFP must be submitted to Maria Robles, Manager of Administration in writing via email maria@tbrpc.org by Friday, July 3, 2026, by 5:00 PM.")
add("p. 9 §6.I Questions", "All questions will be answered and posted on TBRPC's website as an addendum to this RFP on Wednesday, July 8, 2026.")
add("p. 9 §6.II", "II. Exceptions. Any proprietary information revealed in the submission should be clearly identified as such.")
add("p. 9 §6.II.a", "a. Proprietary Information. Proposers should note any exceptions to the RFP specifications or Terms and Conditions (including insurance requirements) on a separate sheet marked by exceptions attached to the price submission.")
add("p. 9 §6.II.a", "Exceptions made do not oblige TBRPC to change the specifications.")
add("p. 9 §6.III", "III. Submission Instructions")
add("p. 9 §6.III.a", "a. Please use your auditor firm's name in the file name of your electronic submissions.")
add("p. 9 §6.III.b", "b. Consultants shall submit one electronic (.PDF) file or file share link of the information in Section 5 above to Maria Robles, Manager of Administration in writing via email maria@tbrpc.org by Friday, July 17, 2026, by 5:00 PM.")
add("p. 9 §6.III.c", 'c. Submittals shall be clearly identified in the email subject line: "Statement of Qualifications for TBRPC Auditing Services"')

add("p. 9 §7 Selection Process", "Submittals received by the deadline will be reviewed by a selection panel comprised of TBRPC staff who have relevant knowledge and experience.")
add("pp. 9-10 §7 Selection Process", "The panel will score the proposals based on the qualification materials submitted according to the following criteria:")
add("p. 10 §7.I", "I. Letter of Interest. Availability, demonstrated capabilities, and qualifications necessary to provide the auditing services specified in the RFP. Ability to meet standard TBRPC contract and insurance requirements. (20 Points Maximum)")
add("p. 10 §7.II", "II. Relevant Experience. Demonstrated ability, based on consultant experience and specific experience of key personnel, to provide the services listed in the RFP. (40 Points Maximum)")
add("p. 10 §7.III", "III. Responsiveness to the RFP. Presentation, completeness, and clarity of information provided. (15 Points Maximum)")
add("p. 10 §7.IV", "IV. Fee Structure. The consultant's cost competitiveness and reasonableness. (25 Points Maximum)")
add("p. 10 §7.V", "V. Client References. (Pass/Fail)")
add("p. 10 §7 Selection Process", "The submittals will be scored on a 0-to-100-point scale, excluding bonus points.")
add("p. 10 §7 Selection Process", "Consultants who receive a minimum of 90 points will be placed on a short-list.")
add("p. 10 §7 Selection Process", "Placement on the short-list is not a guarantee of work and does not constitute a commitment by TBRPC to enter into a contract with the consultant.")

# Timeline table: row pairing verified from word y-positions and a rendered page image
# (pdftotext -layout had shifted every date down one row).
t = "p. 10 §8 RFP Timeline table"
add(f"{t} header row", "Milestone | Date")
for i, (m, d) in enumerate([
    ("Proposal Opens", "Friday, June 26, 2026"),
    ("Questions Due", "Friday, July 3, 2026, by 5:00 PM"),
    ("Addendum Posted", "Wednesday, July 8, 2026"),
    ("Proposal Deadline", "Friday, July 17, 2026, by 5:00 PM"),
    ("Notification via Email", "Friday, July 31, 2026"),
    ("Council Approval", "Monday, August 10, 2026"),
    ("Contract Negotiations Begin", "Monday, August 17, 2026"),
], 1):
    add(f"{t} row {i}", f"{m} | {d}")

s = "p. 11 RFP Questions and Response"
add(s, "To ensure consistent responses and provide correct information to all interested parties, questions regarding this Request for Proposals should be directed to Maria Robles, Manager of Administration at maria@tbrpc.org no later than Friday, July 3, 2026 @ 5:00 p.m.")
add(s, "The Council will post the responses to the RFP questions to the Council website tbrpc.org/rfp no later than Wednesday July 8, 2026.")

s = "p. 11 §9 Review and Notification Process"
for t_ in [
    "The Council may, at its discretion, request presentations from the top three scorers to clarify or negotiate modifications to the Firm's proposals.",
    "The Council considers the contract award to the responsible Auditing Firm with the highest total points.",
    "However, the Council reserves the right to award without further discussing the proposals submitted.",
    "Therefore, proposals should be submitted initially on the most favorable terms, from both technical and price standpoints, which the Auditing Firm can propose.",
    "The Council considers the contract award to the responsible Auditing Firm with the highest total points.",
    "The Council reserves the right to segment proposals or accept portions of proposals as is in the best interest of the program and the Council.",
    "Final price negotiation will result from the selection of all or part of the most successful proposal.",
    "In accordance with Florida Statutes Section 120.57, any person adversely affected by the agency decision or intended decision shall file a notice of protest in writing within 72 hours after the posting of the notice of decision or intended decision.",
    "With respect to a protest of the terms, conditions, and specifications contained in a solicitation, including any provisions governing the methods for ranking bids, proposals, or replies, awarding contracts, reserving rights of further negotiation, or modifying or amending any contract, the notice of protest shall be filed in writing within 72 hours after the posting of the solicitation.",
    "The formal written protest shall be filed within ten days after the notice of protest.",
    "Failure to file a notice of protest or a formal written protest shall constitute a waiver of proceedings under this chapter.",
    "The formal written protest shall state with particularity the facts and law upon which the protest is based.",
    "Saturdays, Sundays, and state holidays shall be excluded from the computation of the 72-hour periods provided by this paragraph.",
]:
    add(s, t_)

add("p. 12 §10.I", "I. Terms of Agreement. It is expected that the contract shall be a three-year fixed-price contract.")
add("p. 12 §10.I", "The contract is for audits of fiscal years 2026, 2027, and 2028.")
add("p. 12 §10.I", "At the discretion of the Council, this audit contract can be renewed for up to three additional years.")
add("p. 12 §10.I", "The cost for the optional periods will be negotiated at renewal.")
add("p. 12 §10.I", "The audit should be completed in February of the year following the end of the fiscal year.")
add("p. 12 §10.II", "II. Nondiscrimination. The TBRPC will not discriminate against any interested consultant on the grounds of race, religious creed, color, national origin, ancestry, handicap, disability, marital status, pregnancy, sex, age, or sexual orientation.")
add("p. 12 §10.III", "III. TBRPC's Right to Modify RFP. The TBRPC reserves the right at its sole discretion to modify this RFP (including but not limited to the selection criteria) should the TBRPC deem that it is in its best interests to do so.")
add("p. 12 §10.III", "Any changes to the proposal requirements will be made by written addendum.")
add("p. 12 §10.III", "The failure of a consultant to read the latest addendums shall have no effect on the validity of such modification.")
add("p. 12 §10.IV", "IV. TBRPC's Right to Cancel RFP. The TBRPC reserves the right at its sole discretion to cancel this RFP in part or in its entirety should the TBRPC deem that it is in the TBRPC's best interests to do so.")
add("p. 12 §10.V", "V. TBRPC's Right to Reject All Submittals. The TBRPC reserves the right, in its sole discretion, to reject all submittals should the TBRPC deem that it is in its best interests to do so.")
add("p. 12 §10.VI", "VI. TBRPC's Right to Extend RFP Deadlines. The TBRPC reserves the right to extend the deadline for submittals by written addendum should the TBRPC deem that it is in its best interests to do so.")
add("p. 12 §10.VII", "VII. TBRPC Right to Negotiate with Consultants. The TBRPC reserves the right to negotiate with the consultants on the list of qualified on-call consultants regarding their exceptions to the standard service provider agreement, if any, or regarding other prices and terms in their submittals and to require the selected consultant to submit such technical, price, or other revisions of their submittals as may result from negotiations.")
add("p. 13 §10.VIII", "VIII. Standard Service Provider Agreement and Requirements. Consultants acknowledge that placement on the list of qualified on-call consultants does not commit the TBRPC to award a contract.")
add("p. 13 §10.VIII", "For any project, the TBRPC reserves the right to award a contract to consultants (1) that are on the list of qualified on-call consultants; (2) that have an existing contract with the TBRPC, or (3) that are selected through a separate competitive process.")
add("p. 13 §10.VIII", "Consultants on the list of qualified on-call consultants who are awarded a contract will be expected to sign a service provider agreement with the TBRPC.")
add("p. 13 §10.VIII", "If there are any concerns or proposed exceptions requested to the standard service provider agreement, these issues will be discussed at the time the TBRPC awards a contract, if any.")
add("p. 13 §10.IX", "IX. Cost of Submittals. All costs incurred during submittal preparation or in any way associated with the consultant's preparations or submission shall be the sole responsibility of the consultant.")
add("p. 13 §10.X", "X. Liability for Submittal Errors. Consultants are liable for all errors and omissions contained in their submittals.")
add("p. 13 §10.XI", "XI. Permits and Licenses. Consultants, at their sole expense, shall obtain and maintain during the term of any agreement, all appropriate permits, certificates, and licenses including, but not limited to, a State of Florida Business License which will be required in connection with the performance of on-call consulting services.")

a = "p. 14 Attachment A"
add(f"{a} title", "ATTACHMENT A: OFFEROR REFERENCES FORM")
add(f"{a} instructions", "CONTRACTOR: PROVIDE A MINIMUM OF THREE (3) REFERENCES FROM CUSTOMERS THAT ARE CAPABLE OF DISCUSSING YOUR COMPANY'S ABILITY TO PERFORM THE TECHNICAL TASKS DESCRIBED.")
add(f"{a} instructions", "It is imperative that accurate contact names and phone numbers be given for the projects listed.")
add(f"{a} instructions", "All references should include a contact person who can comment on the company's ability to perform the services required under this RFP.")
add(f"{a} instructions", "The company should ensure that telephone numbers and contact names given are up-to-date and accurate.")
FIELDS = ["1. Name of Client Organization:", "2. Name and Title of Point of Contact (POC) for Client Organization:",
          "3. Phone Number of POC:", "4. Email Address of POC:", "5. Approximate Value of Contract:",
          "6. Duration of Contract:", "7. Description of Services Provided:", "8. Were Deliverable Deadlines Met:"]
for n in range(1, 6):
    pg = "p. 14" if n <= 2 else "p. 15"
    add(f"{pg} Attachment A Reference {n} block", f"Reference Number {n}")
    for f in FIELDS:
        add(f"{pg} Attachment A Reference {n} field", f)

b = "p. 16 Attachment B"
add(f"{b} title", "ATTACHMENT B: SCHEDULE OF PROFESSIONAL FEES AND EXPENSES")
add(f"{b} column header row", "Quoted Hourly Rates | Total")
for r in ["Partners", "Managers", "Staff"]:
    add(f"{b} row {r}", f"{r} | _________ | _________")
for fy in ["FY26", "FY27", "FY28"]:
    add(f"{b} {fy} block row 1", f"{fy} | Annual Audit Fee | _________")
    add(f"{b} {fy} block row 2", "Major Program Fee (cost per) | _________")
add(f"{b} note", "Note: Quote should include all out-of-pocket expenses and copies of prior year working papers.")

out = Path(__file__).resolve().parent.parent / "source-packet.md"
out.write_text("".join(f"S{i:03d} | {anc} | {txt}\n" for i, (anc, txt) in enumerate(L, 1)), encoding="utf-8")
print(f"{len(L)} statements -> {out}")
