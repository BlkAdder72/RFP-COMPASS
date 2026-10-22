# Judge-oriented red-team review

October 22, 2026. Target: packaged commit `7f3317caf52d49089cae88703aadc0c5578969c0`. **Recommendation: hold publication pending one feedback-closure decision and two runner fixes.** This is a spec-based risk assessment, not a claim that a judge has disqualified the entry.

The existing package passes its local preservation audit. That does not prove every named feedback fix wins under the frozen test. This review used the brief first, then exact Q8 executions and a sandbox reproduction of runner behavior. It made no model calls, changed no rebuild code, and did not rewrite prior scores or sealed artifacts.

## Findings, ranked

### 1. High: final default Q8 does not improve on the original

The brief requires the same test on the two versions and visible closure of both fixes. Frozen questions.md:16 requires no Section 6 REVIEW for personal S004–S007 in the correctly contained card, while still warning for missing real S002 in the defective card.

I executed the identical source/card inputs against both default validators:

| Frozen Q8 component | Original default | Final rebuild default |
|---|---|---|
| Contained personal S004 produces no date hint | Fail: S004 warning emitted | Fail: same S004 warning emitted |
| Misplaced genuine deadline S002 still warned | Pass | Pass |
| Q8 verdict under the frozen default invocation | Partial | Partial — tie |

With an additional selected review record, the final version meets both outcomes. That assisted workflow is disclosed honestly and the hashes improve its auditability, but it changes the inputs/operator work from the frozen default test. It is not evidence that the unchanged default Q8 now wins. The final root audit also emits the false S004 warning in packaging/final-checks/first-rebuild-A-stapled-thread.stdout.txt while recording local PASS, because structural validity and integrity are what that step checks.

**Judging risk:** the feedback expressly asks to drop those validator hints. A strict judge can find that this part of Fix 1 remains unresolved in the default submitted workflow. I would not call rejection certain: the spec does not explicitly prohibit operator review records, and judges might accept the declared assisted workflow. But that acceptance is uncertain and should not carry a would-be winning entry.

**Required action:** choose and demonstrate one final, explicit workflow. Either resolve the false-hint requirement in the default path without reintroducing missed-deadline suppression, or make the assisted workflow part of a separately frozen, symmetric rerun protocol and disclose the added review inputs/work in both arms. Publish a final Q1–Q8 scorecard distinguishing default Q8 partial from assisted Q8 pass. Do not edit the old questions or retroactively replace earlier runs. Adding human adjudication may be acceptable engineering, but acceptance by this competition must not be assumed.

Sources: questions.md:16; rebuild/tools/validate_packet.py:97–100 and 229–244; results.md:9–17. Reproduction: evidence/original-contained-default/stdout.txt, evidence/rebuild-contained-default/stdout.txt and the corresponding missed-deadline/additional-review runs.

### 2. Medium: a refused rerun overwrites existing environment evidence

tools/run_arm.py:20 writes run-ARM/environment.json before checking whether the first trial already exists at lines 22–24. The advertised refusal therefore protects trial files but not the environment record describing the earlier trial set.

I copied the unchanged runner and knowledge into an isolated sandbox, created an existing first trial and a sentinel environment.json, then invoked the runner. It exited with the expected refusal and made no model call, but replaced the sentinel environment file. The before/after hashes and bytes are preserved under evidence/. The actual package's environment files were not touched.

**Why it matters here:** a moderator or future owner can damage the provenance of existing results by attempting the obvious rerun. Fresh-session metadata must not silently replace the settings/date record associated with saved raw transcripts. This undermines the receipt the competition asks the repository to preserve.

**Required action:** preflight every destination before any write; use a new explicit run directory for each experiment; create metadata once with exclusive creation; and test that every byte remains unchanged on refusal. Ensure the supplemental/repair runner paths are similarly explicit about new-versus-existing runs. Keep historical scripts intact in the snapshot; fix the current supported entry point.

Source: tools/run_arm.py:20–24. Reproduction: evidence/runner-refusal/, runner-environment-before.bin, runner-environment-after.bin and results.json.

### 3. Medium: the fresh model rerun path remains tied to the original machine

The supported README correctly discloses that runner paths need adapting. However, tools/run_arm.py:12 pins a versioned executable inside this user's Windows profile, and line 36 selects ROOT/.run-work without creating it. The verified clean clone does not contain that ignored directory. The recorded experiment therefore is not directly rerunnable using this script from an ordinary fresh checkout, even though offline evidence verification works.

The brief says the mods clone and rerun both arms. It does not require a one-command model harness or a particular platform, so this is a reproducibility/usability risk rather than a proven automatic disqualification. Reading old commands and adapting the installation/workspace is avoidable reviewer work.

**Required action:** accept or discover the CLI executable, create an isolated working directory, validate model/auth prerequisites before writing evidence, and supply one exact command sequence to run both arms into new destinations. Keep the recorded model/settings, avoid loading the feedback/answers into translation sessions, and provide a manual equivalent if the moderator uses another supported environment. Treat another model as a new experiment, not an identical reproduction.

Sources: README.md:29, questions.md:24 and tools/run_arm.py:12,36. Static evidence: the delivered clean clone has no .run-work directory. This finding is based on the supplied path/workspace requirements, not a failed model API attempt on another operating system.

## What held up under review

- The judged original and exact feedback are preserved; the actual judged Git commit is retained by tag.
- Eight feedback-derived questions and the original baseline precede the first rebuild in Git.
- The routing change, narrow S133 trigger and script-built sample disclosure directly answer the feedback rather than polishing unrelated strengths.
- Raw prompts/results, ties, the earlier warning regression and the explicit repair tradeoff remain visible.
- Clear personal material without explicit unrelated anchors and separate statements in a mixed thread improved in both supplemental repeats.
- The indivisible mixed-statement limit is admitted rather than hidden by source deletion or paraphrasing.

No separate disqualification is inferred from synthetic fixtures, using Codex instead of Claude, reporting ties, keeping extra evidence folders or lacking a statistical estimate: the brief does not prohibit those. Host variation and small/known fixtures limit the strength of the performance claim, as already disclosed. Membership eligibility is unverified, but it is an external entry gate rather than a newly found rebuild defect.

## Suggested priority before publication

1. Resolve the exact Q8 workflow/closure question and produce a final per-question scorecard.
2. Repair runner preservation and portability, retaining the demonstrated failing behavior and old scripts.
3. Freeze any changed protocol before new trials. Rerun the same questions symmetrically; preserve all old runs and any new losses.
4. Repeat the package/fresh-clone checks and regenerate delivery artifacts only after the final evidence and report are committed.

The strongest story remains the real one: feedback named contamination, the routing repair demonstrated containment, adversarial testing found a warning regression, and a revised checker made its review dependency explicit. The weak point is treating conditional assisted closure as though it settled the originally frozen default test.

## Audit preservation

All 2,713 tracked package files remained unchanged during these reproductions. The sealed bundle SHA-256 remains a0280a2c40b031797d316447e5f1164fa85de38b22747867480aba809cfcdb5e; the sealed ZIP remains 3e72bb39199ad8796ea5f7cad3fcde946b56143a4715f05b0cdf8f57ef1fc9a2. New audit files live only under red-team/. No fixes, public pushes, posts or submissions were made.
