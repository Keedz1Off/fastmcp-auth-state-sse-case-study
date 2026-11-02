# Reading guide

Start with [README](README.md), then [PR-3278-VERIFICATION.md](PR-3278-VERIFICATION.md) for the main result.

| Next question | File |
| --- | --- |
| How do SSE requests and errors travel? | [FLOW.md](FLOW.md) |
| What were the expected and observed results? | [Boundary matrix](matrices/boundaries.json) |
| Where are the before/after measurements? | [pr3278-verification.json](evidence/pr3278-verification.json) |
| Did the server still reject the revoked token? | [sse-feedback.json](evidence/sse-feedback.json) |
| Did other work continue? | [liveness.json](evidence/liveness.json) |
| What about token storage and concurrent refresh? | [CASE-STUDY.md](CASE-STUDY.md) and [observations.json](evidence/observations.json) |
| Did the full upstream suite pass? | [RESULTS.md](RESULTS.md) and [upstream.json](evidence/upstream.json) — the original run remained red |
| Which source and dependencies were tested? | [source-pins.json](evidence/source-pins.json) |
| How do I check file integrity? | [VERIFY.md](VERIFY.md) |

The matrix indexes historical observations, not new executions. Passing a harness assertion can confirm that a defect was reproduced; it does not necessarily mean the product behaved correctly.
