# Audit corrections, not model retries

The first combined audit stopped on the full-length model card's S072 anchor failures because its initial assertion expected an entirely passing card. The final audit records and verifies the structural regression rather than relabeling the raw card a pass. The two actual failed citation validations and first-pass reports remain preserved.

A later preservation audit detected a snapshot naming collision: the first-pass root README had been copied to `full-first-pass/README.md`, then the snapshot description was written at that same path. Its unchanged source bytes were already committed at the first-pass Git commit. `repair_snapshot_note.py` verifies those bytes against the previously recorded SHA-256 before restoring them, and preserves the descriptive note as `AUDIT-NOTE.md`. No hash expectation or original model evidence changes. This recovery is deliberately recorded; the failed integrity assertion was not bypassed.
