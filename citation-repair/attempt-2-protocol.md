# Second prospective repair attempt — 2026-10-23

The first opaque-anchor instruction repair failed: both new full-length cards still omit a qualifier from S072 twice. Preserve that entire pair, its knowledge, core scores and exact validators before the next change. Its failures remain part of the report, not superseded into successes.

Add a general worked example with two identical disclosure-form statements whose anchors differ by a layout suffix, plus explicit treatment of layout words such as bullet/row/paragraph as literal anchor data. This addresses source-ID binding versus reconstructed/canonicalized anchors. Use a different fictitious source and no S072, TBRPC anchor, expected full-card output or actual test answer in new model knowledge. No tool postprocessing or validation change.

Run original and rebuild again in new citation-repair-v2-core and citation-repair-v2-full directories, same A–E order and same unchanged 221-statement packet, gpt-6-astra/medium, same wrappers and continuation protocol. Start original baseline before the next edit; commit its core baseline before updating examples. Commit the second repair before rebuilt trials. No retries within a trial, best-of selection or editing raw cards. Report both attempts side by side; this is a second version change after a disclosed failure, not an independent holdout or first-try success.

Current full results must pass the unchanged exact validator on every citation, not merely S072. Old failed cards must still fail. Frozen questions, full input and expected checks do not change. The existing pre-repair snapshot of examples.md is byte-preserved; examples.md is an additional editable path for this second repair, documented separately without modifying the first preservation manifest.
