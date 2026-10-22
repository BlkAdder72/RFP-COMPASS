# Judge-oriented red team

Target: packaged commit 7f3317caf52d49089cae88703aadc0c5578969c0 and its unpublished delivery artifacts. No edits to the rebuild, existing evidence, scores or sealed artifacts in this audit.

Test the brief's actual acceptance conditions, not just the package's integrity assertions:

1. Rerun frozen Q8 on the identical contained/missed-deadline cards with each version's default validator invocation. Then test the final version with the extra review input, separately labeled. Check whether the final-default workflow wins on the precommitted expected answer.
2. Exercise the shipped runner's refusal-to-overwrite behavior in an isolated minimal sandbox. A refused run should not change an existing environment record. Ensure the first trial already exists, so the test cannot launch a model.
3. Inspect fresh-run portability: platform paths, CLI flags, workspace creation and documented manual alternatives. Distinguish offline evidence checking from actually rerunning the model experiment.
4. Check whether the repaired root card set still generates the false warning during the package's green audit, without modifying that audit's records.
5. Verify all tracked target files and local delivery hashes remain unchanged. Record exact commands/stdout/stderr/exit codes for new tests only.

This is an adversarial review, not a repair or a new model evaluation. Existing stage limitations are not automatically disqualifying; grade confirmed behavior separately from judging risk and recommendations.
