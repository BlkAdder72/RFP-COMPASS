# Audit execution notes

The completed original baseline was staged for commit `ee50476`. The shell returned a running-session ID rather than a completed commit; the fix/control scripts were initially launched before that pending Git command was observed complete. All model baseline runs had already finished, and only original raw evidence/new scripts were staged, so no candidate changes entered the baseline commit.

The three candidate files were restored byte-for-byte from the pre-fix snapshots while the baseline operation completed. After confirming the baseline commit succeeded, the same deterministic fix was reapplied and committed before any rebuilt model call. The first 137-control run is retained unchanged; it tested the same repaired code. This was a command-wait sequencing correction, not a model retry, selected output, revised expectation or evidence deletion.

The packaged full-run copy inherited rebuild/.gitattributes line-ending normalization. Commit c85d78c warned that its README and two derived validation files would be normalized; the original raw run and working-copy bytes remained intact. A local `* -text` rule was added to the new packaged-copy directory, and its original working-copy bytes were restaged without conversion before sealing. The intermediate commit is retained. This corrects packaging bytes, not model output or validation results.
