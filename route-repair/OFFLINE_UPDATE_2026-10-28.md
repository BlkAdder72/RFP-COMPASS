# October 28 offline update — unpublished

No Claude calls, new responses, regenerations or candidate changes were made.

## Resolved locally

- Replaced obsolete README claims and commands with current route-repair evidence and clear pending status.
- Fixed partial scoring so Q1–Q4, Q7 and Q8 are independently reportable; Q5 and Q6 remain pending. Expected answers and frozen inputs were not edited.
- Regenerated matching root and detailed reports from the saved raw evidence. Completed containment improves in A/B, C ties; unknown cases remain unknown.
- Preserved prior versions before editing, and retained the three existing raw exports and the fourth-response recovery checkpoint.
- Added a reproducible offline audit with exclusive output directories. All 42,270 baseline Git blobs and original working files passed preservation checks. All frozen candidate/source/protocol hashes passed.
- Replayed four shipped samples, 17 citation-export controls and 216 warning/corruption controls. All expected outcomes passed. Repeated scoring in an independent directory reproduced every verdict, route, literal mismatch and warning after normalizing only diagnostic output-directory prefixes.
- Verified the existing-output guard refuses overwrite. Final submission audit now gates on the current route-repair evidence instead of invoking an obsolete candidate audit; it returns HOLD (exit 2) while final evidence is missing. Historical audit code and assertions remain intact.
- Updated the unposted submission draft to supported, limited claims.

## Remaining limitations

Core B is correctly contained but still produces two false advisory warnings, for its dentist date and birthday contact. Q8's pass is limited to its frozen fixture A. The unchanged conservative filter requires body-supported private context and retains unknown cases; this update does not broaden suppression based on an anchor, a date or the output's own placement. It therefore makes no claim that all false warnings are fixed.

Three of eleven repaired responses are fully exported. The fourth was submitted and finished but must be recovered, never regenerated. Seven subsequent cases remain unrun, including full-RFP and remaining routing/citation checks. Current user direction excludes further Claude runs. No complete native acceptance, final competition archive or fresh-clone release verification is claimed. Old dist archives remain historical; final packaging guards are unchanged.

Evidence: offline-review-2026-10-28/review.json, verification.json, analysis/, controls/. Historical archive was preserved outside source under .run-work; archive-location.json records its SHA256. No file was published or pushed.
