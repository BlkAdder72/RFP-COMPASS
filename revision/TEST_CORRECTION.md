# Preserved test assertion correction

The first checker suite recorded 50/51 passing expectations in default-results.json. The remaining case, missing-heading, correctly produced structural FAIL and no personal exclusion, but the test also required a downstream date REVIEW. The existing validator returns early when the headings cannot be parsed, in both old and current designs; a routing hint is not meaningful at that point.

No validator code was changed in response. The corrected criterion is structural failure, no applied personal filter and no downstream routing requirement. The correction is limited to this new adversarial test, not the frozen questions or any source fixture. The original failed assertion, raw outputs and code hash remain preserved. The complete corrected suite runs into default-tests-v2/ and default-tests-v2-results.json, never overwriting the initial record.
