# Validator repair protocol — before implementation

October 22, 2026. Preserve every currently tracked file except the root navigation README, including both tested versions and all first-pass and supplemental evidence. Record SHA-256 hashes before implementation. Implement the repair as a complete candidate copy under repair/candidate/. The existing rebuild/ remains the tested historical version; it must not be silently replaced.

## Design

Remove filename/anchor-keyword suppression entirely. With no explicit review file selected, keep conservative warnings. To suppress false hints for adjudicated personal material, accept an optional --reviewed-exclusions JSON file selected by the evaluator/operator. Bind it to the exact packet SHA-256 and individual statement hashes, require named reviewer and reasons, and require selected statements to appear only in Section 12. Never infer approval from a card's placement, a source anchor or an unsolicited adjacent file.

Treat invalid, stale, duplicate, unknown-ID or incompatible review records as errors, apply no exclusions, and retain conservative warnings. Reject reviewed exclusion of statements with explicit procurement cues, including mixed genuine/personal statements. This guard is conservative, not a complete semantic verifier. Review records are explicit trust inputs, not independent proof of correct relevance decisions or authenticated human approval. Test records are evaluator-authored and must be labeled as such.

## Frozen acceptance checks

1. Supplemental N1 defective real-deadline card with misleading unrelated anchor: warn for S002 without review records. Original should warn; historical rebuild should miss it; repaired candidate must warn.
2. Original feedback Q8 contained A: suppress personal hints only with valid selected personal-exclusion decisions; report those applied decisions. Genuine deadline remains operational.
3. Original feedback Q8 missed-deadline A: with the same personal decisions, still warn for real S002.
4. Supplemental N2 contained F with neutral anchors: valid selected personal decisions suppress its false date warning; without them the conservative warning remains and is disclosed.
5. Misleading-anchor N1 with a valid empty review file: still warn for S002.
6. A stale packet hash, wrong statement hash, unknown source ID, duplicate decision ID, blank reviewer/reason, unsupported schema version or malformed JSON: nonzero validation, no applied exclusions, original date warnings retained. Preserve every individual case.
7. A selected statement also placed in an operational section: reject exclusion rather than suppress the routing concern.
8. An explicit procurement deadline or indivisible mixed requirement cannot be approved for exclusion under the conservative procurement-cue guard, even with matching hashes.
9. All ten first-pass model cards, all 32 supplemental model cards and four shipped reference cards continue to pass structural/quotation/coverage checks under the repaired validator with no review file. Warnings may differ and must be retained; do not alter outputs to improve tests.
10. Six model knowledge files remain byte-identical to historical rebuild, so no new model-routing claims or model reruns are needed for this validator-only repair.

Run the original, historical rebuild and repaired validator on the same fixed Q8/N1/N2 inputs and save exact commands, stdout, stderr and exit codes. Preserve existing tool scores; publish repair results separately. Review-file generation is evaluator adjudication, not a model run or owner approval. Report the new review burden, conservative default warnings, unsupported ambiguous decisions and remaining whole-statement limitation. No publication in this stage.
