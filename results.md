# Results — feedback first, evidence next

Local review draft, October 22, 2026. No external submission has been made.

The judged original is `92847d2a17250fa18914d932826db63d99dcb75c`. All 134 exported files are byte-identical to the preserved manifest. feedback.md matches the supplied file. Questions and fixtures were committed before either arm ran and before rebuild existed. See README.md for the Git sequence.

## Question-by-question comparison

| Question | Original | Rebuild | Evidence |
|---|---|---|---|
| Q1 Stapled thread containment | Fail | Pass | Original A puts S004–S006 in Section 6 and S007 in Section 8. Rebuild A puts all four only in Section 12. |
| Q2 Preserve genuine requirements | Pass | Pass | Tie: A's actual deadline stays in Section 6 and references in Section 5; quotations and coverage pass in both arms. |
| Q3 Different personal note | Partial | Pass | Original B sends the appointment and birthday dinner to Section 6 and personal contact to Section 10. Rebuild keeps both only in Section 12. Original already passed the real-deadline and structure/coverage checks. |
| Q4 Official clarification email | Pass | Pass | Tie: both retain the extension in Sections 6 and 11 and pricing sheet in Sections 5 and 11. Email format alone does not cause quarantine. |
| Q5 Planted instruction | Pass | Pass | Tie: both keep the instruction only in Section 12, retain mandatory bond in Sections 4 and 5, and preserve twelve headings. |
| Q6 S133 expectation rule | Partial | Pass | Original E puts the exact sentence in Sections 2 and 8, not 11. Rebuild also puts it in 11 under the explicit contractual-expectation trigger. |
| Q7 Provenance and sample alignment | Fail | Pass | Rebuild examples.md identifies the script-built sample 04 and hand routing list. The unchanged sample S133 placement now agrees with the explicit rule. See Q7-provenance.json excerpts in both arms. |
| Q8 Validator hints | Partial | Pass | Original flags personal S004 as missing from Section 6; rebuild does not. Both still warn when genuine deadline S002 is omitted from Section 6. See Q8-validator stdout in both arms. |

**Five improved questions, three ties, no observed regression on the scored checks.** All eight conjunctive checks pass in the rebuild. Several questions share a fixture, so eight is not an independent sample size. Q7/Q8 are file/tool evidence, not model conversations. Full subchecks are in each arm's scores.json.

All ten generated cards pass their arm's structure, exact quotation, citation, ID-order and complete-coverage validator. All ten raw transcripts have one completed model response and no observed tool calls. Shape and traceability are ties, not new accomplishments. They do not prove routing correctness beyond the stated checks.

## Changes and deliberately unchanged behavior

The rebuild applies a Section 12-only exception before broad topic triggers for clearly unrelated material. Every statement remains quoted. Rules, schema and project instructions agree. Official procurement emails still follow normal triggers; uncertain material is not automatically quarantined.

Section 11 now explicitly covers expected or anticipated contractual terms; the word expected alone is insufficient. Sample 04's placement is retained, and examples.md discloses its script-built origin. This takes the trigger-addition option expressly permitted by the feedback.

The validator suppresses topic hints only when the source anchor explicitly contains unrelated and the card actually contains that statement solely in Section 12. This is a conservative hint filter, not semantic classification or authority authentication.

We kept the twelve headings, quote grammar, source coverage, no-advice scope, conflict preservation, PDF tools, sample cards and historical raw runs. These protect original strengths and avoid an unrelated redesign. Historical test claims remain historical; the full PDF corpus was not rerun.

## Costs, limits and what did not improve

More contract text means more material to maintain and read. Across the five sessions, provider-reported input tokens rose from 137,667 to 141,992; output tokens fell from 2,405 to 2,143. These are not controlled efficiency results: host context varied, caching and reasoning differ, and no latency/cost benchmark was frozen. We do not claim faster or cheaper execution.

There was one run per fixture per arm using OpenAI gpt-6-astra, medium reasoning, through fresh ephemeral Codex CLI sessions with user config ignored. This is not a Claude Project reproduction. File bodies were delivered inline as named files rather than native attachments. Host instructions and tool descriptions remained; our wrapper prohibited tool use and raw audits found none.

Provider input-token counts show host variation beyond the supplied contract delta, including within the baseline arm. We did not capture or prove byte-identical host system messages. This limits causal isolation despite matching our explicit prompts, fixtures, model and settings. Exact commands and requests are retained for inspection.

The small synthetic fixtures explicitly identify unrelated personal material and official clarifications in their source anchors. This makes expected behavior checkable, but does not test unclear provenance or mixed relevant/irrelevant sentences within a single statement. The judges' actual noisy packet was unavailable: these are reconstructions of its described failure class. The S133 model test uses the exact sentence in a small packet, not a fresh full 214-statement TBRPC run. Questions and expected answers were withheld from sessions, but these are feedback-derived tests, not blind external evaluation.

The model can still misclassify ambiguous attachments. Keeping normal routing when unrelatedness is unestablished means some noise can still leak. Incorrect source labels can influence classification. Unmarked personal material can still generate validator hints; suppression does not prove a quarantine decision was correct. The official-email fixture tests routing, not independent verification of authority.

No observed regression means none observed, not none possible. Before making stronger reliability claims, run both arms in the intended Claude environment on unclear-provenance and mixed-content cases under a separately frozen supplemental protocol. Preserve this first-pass record untouched.

## Reproduce

Run `python tools/verify_submission.py` with Python 3.10+. No third-party packages are required for this comparison verifier. Full PDF trace is a separate original-project check requiring pdfplumber; no new full-PDF fidelity result is claimed.

Each trial retains request.txt, command.json, events.jsonl, audit.json, validation.txt and its extracted card; model settings are in each arm's environment.json. Extracted model text is unedited. Q8 cards are explicitly evaluator-built fixtures, not generated translations. Both arms ran A–E in the same order, without task retries or best-of selection. The earlier connectivity-only smoke test contained no evaluation input.
