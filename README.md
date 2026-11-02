# FastMCP: server rejected a call, client kept waiting

**Status:** client/dependency error-handling bug; no authorization bypass demonstrated.

The application made a protected tool call over an open legacy SSE connection after its token was revoked.

- **Expected:** server denies access; the application promptly receives an error.
- **Observed:** HTTP 401 blocked the tool, but the client call stayed pending at the two-second test bound. A configured deadline produced a timeout instead.
- **Impact:** the calling application waited unnecessarily. Independent work continued; an application-wide outage was not demonstrated.
- **Fix verification:** upstream SDK PR #3278 head `66a9285` returned an error promptly and passed the selected reauthorization control, unlike base `a4f4ccd`. This is scoped verification, not a shipped-release claim.

## Evidence and details

[Before/after results](PR-3278-VERIFICATION.md) · [Boundary matrix](matrices/boundaries.json) · [Flow](FLOW.md) · [Measurements](evidence/pr3278-verification.json)

FastMCP snapshot: `4359485`. [Technical assessment](CASE-STUDY.md) · [Other results](RESULTS.md) · [File map](READING-GUIDE.md) · [Package check](VERIFY.md) · [Attribution / AI assistance](NOTICE.md).

Historical results; no new target execution in this documentation edit.
