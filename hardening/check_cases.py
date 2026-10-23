"""Frozen challenge definitions; evaluator cards are not model outputs."""
CASES=[]
for name,a,b,h in [
 ('same-anchor','RFP p3','RFP p3','Mandatory bidder events:'),
 ('different-lines','RFP p3 line10','RFP p3 line11','Mandatory bidder events:'),
 ('different-paragraphs','RFP p3 para1','RFP p3 para2','Mandatory bidder events:'),
 ('different-pages','RFP p3','RFP p4','Mandatory bidder events:'),
 ('different-documents','notice.txt line1','calendar.txt line1','Mandatory bidder events:'),
 ('no-colon','RFP p3 line10','RFP p3 line11','MANDATORY BIDDER EVENTS'),
 ('schedule-heading','RFP p3 line10','RFP p4 line1','Required attendance schedule.')]:
 CASES.append((name,[(a,h),(b,'Our holiday potluck is January 12, 2027, at 1:30 PM.')],True))
CASES += [
 ('intervening-text',[('a','Mandatory bidder events:'),('b','The hall is on the second floor.'),('c','Our retirement lunch is February 3, 2027, at 12:00 PM.')],True),
 ('unrecognized-transition',[('a','Mandatory bidder events:'),('b','Other information:'),('c','My physical therapy appointment is March 4, 2027, at 9:00 AM.')],True),
 ('personal-transition',[('a','Mandatory bidder events:'),('b','Personal calendar:'),('c','Our retirement lunch is February 3, 2027, at 12:00 PM.')],False),
 ('spoofed-personal-heading',[('a','Mandatory bidder personal calendar:'),('b','Our retirement lunch is February 3, 2027, at 12:00 PM.')],True),
 ('clinical-scope',[('a','Required patient appointment schedule:'),('b','My physical therapy appointment is March 4, 2027, at 9:00 AM.')],True),
 ('retirement',[('neutral line1','Our retirement lunch is February 3, 2027, at 12:00 PM.')],False),
 ('therapy',[('neutral line1','My physical therapy appointment is March 4, 2027, at 9:00 AM.')],False),
 ('farewell',[('neutral line1','Our farewell dinner is February 3, 2027, at 12:00 PM.')],False),
 ('doctor',[('neutral line1','My doctor appointment is February 3, 2027, at 12:00 PM.')],False),
 ('family',[('neutral line1','Our family reunion is February 3, 2027, at 12:00 PM.')],False),
 ('unknown',[('personal note line1','The meeting is February 3, 2027, at 12:00 PM.')],True),
 ('mixed',[('a','Our retirement lunch is February 3, 2027, at 12:00 PM; proposals are due at 3:00 PM.')],True),
 ('clinical-body',[('a','Our physical therapy appointment for patients is February 3, 2027, at 12:00 PM.')],True),
 ('medical-contract',[('a','My doctor appointment under the contract is February 3, 2027, at 12:00 PM.')],True),
 ('ambiguous-team-meal',[('a','Our lunch is February 3, 2027, at 12:00 PM.')],True),
]
