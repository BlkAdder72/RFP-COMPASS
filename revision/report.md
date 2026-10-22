# Resolution of all three red-team findings

October 22, 2026. Unpublished. Frozen questions and all earlier evidence remain preserved.

## Fresh fair comparison

Twenty fresh sessions reran A–E twice per version with identical knowledge-file selection, request wrapper, user prompt, fixtures, gpt-6-astra/medium settings and no-tools requirement. Repeat 1's original baseline was committed before the default-validator change; repeat 2 reversed arm order. No model retries or best-of selection occurred. Q8 used the identical two evaluator cards with ordinary validator commands and no review records.

| Question | Original repeats 1 / 2 | Rebuild repeats 1 / 2 |
|---|---|---|
| Q1 Thread containment | Fail / fail | Pass / pass |
| Q2 Preserve requirements | Pass / pass | Pass / pass |
| Q3 Different personal note | Partial / partial | Pass / pass |
| Q4 Official clarification | Pass / pass | Pass / pass |
| Q5 Planted instruction | Pass / pass | Pass / pass |
| Q6 S133 rule and placement | Partial / partial | Pass / pass |
| Q7 Script-built sample provenance | Fail / fail | Pass / pass |
| Q8 Default validator hints | Partial / partial | Pass / pass |

Ten improved paired question comparisons, six ties, no regressed scored subcheck. The questions are not independent samples: A serves two questions and Q7/Q8 are inspection/tool checks. Raw runs are under ../run-original/revision-v2/ and ../run-rebuild/revision-v2/; subchecks are in scores.json. Host-system variation remains uncontrolled. These are descriptive results, not statistical reliability estimates or a Claude replication.

## Default Q8 is now closed in the submitted workflow

The default filter requires affirmative personal-activity language in source text and Section 12-only placement. Filename wording or card placement alone cannot grant exclusion. Explicit requirement/procurement language vetoes filtering, including indirect response/application deadlines and mixed personal/requirement statements. A requirement-bearing event header on the same anchor protects following entries. Unknown meetings and ambiguous language retain hints; invalid cards do not receive automatic exclusions.

On the original Q8 cards, S004 no longer generates a Section 6 REVIEW, while misplaced real S002 still does. Both arms receive identical inputs and no sidecar. This supersedes the prior assisted-only closure; the earlier failure and repair remain visible.

This is a bounded, primarily English heuristic, not a complete semantic classifier. Procurement content expressed only in personal-looking language without detected requirements/context could be misclassified. Personal statements mentioning work obligations can retain false hints. Generic lunch-money S007 still generates a conservative Section 8 hint: the specific Section 6 obligation is closed, not every possible noise hint. Mixed indivisible statements remain whole and can carry personal clauses into operational sections. Optional reviewed exclusions remain for compatibility but are not used in the paired test and do not authenticate a reviewer.

## Runner preservation and portability

The supported runner checks an entire destination before any writes. Each experiment claims a new directory exclusively; metadata and trial files use exclusive creation. Existing destinations, even empty ones, are refused without alteration. The executable is discovered on PATH or supplied with --codex, and a unique working directory is created automatically.

--preflight-only checks paths, fixture structure, executable and required flags without writes or a model call. Authentication/model availability is tested by the first real trial; a failure is retained. Seven model-free tests cover refusal, repeat refusal, absent executable, malformed fixture, unsupported flags, paths with spaces, read-only preflight and workspace creation. Fake CLI text is explicitly labeled and never counted as model evidence. Historical scripts and the destructive-refusal reproduction remain preserved.

## Testing and evaluator correction

The corrected default suite passed 51/51 recorded checks, including Q8/N1/N2 under both versions, personal activities, ambiguous meetings, genuine deadlines, mixed text, misleading anchors, protected headers, operational duplicates and structural/quotation corruption. Both validators replayed all 42 prior model cards and four reference samples: 92/92 structural checks passed. No source output was edited.

The initial suite recorded 50/51 because one assertion wrongly expected a downstream date hint after a missing heading caused early structural failure. The validator correctly rejected that card. Initial failure/outputs remain in default-tests/ and default-results.json; TEST_CORRECTION.md explains the correction. No validator code or frozen question was changed to satisfy it. The corrected suite is separate in default-tests-v2/.

## Preservation and package

The manifest covers 2,756 pre-revision tracked files. Changed current entry points and reports were copied byte for byte to revision/history/ before edits; every other prior file remains in place. Questions, original, feedback, old reports/scores, all raw runs, red-team findings and Git history are retained. Earlier sealed files are preserved under dist/prior-default-q8/ when replacements are built.

Run python tools/verify_submission.py for the package audit or python revision/verify.py for this stage. There are now 62 actual model responses: 42 historical plus 20 fresh. Tool checks, evaluator cards and fake CLI tests are not model responses. New artifacts must pass exact-byte and clean-clone checks before delivery. No public push, posting or submission has occurred. Membership eligibility remains unverified.

Earlier delivery binaries are retained locally in the ignored dist archive and verified when available. A Git clone contains their recorded hashes and complete prior source history, not the ignored ZIP/bundle files themselves; the verifier reports that absence separately instead of requiring local delivery binaries to audit source evidence.
