# FastMCP: server rejected a call, client kept waiting

**Status:** client/dependency error-handling bug; no authorization bypass demonstrated.

The application made a protected tool call over an open legacy SSE connection after its token was revoked.

- **Expected:** server denies access; the application promptly receives an error.
- **Observed:** HTTP 401 blocked the tool, but the client call stayed pending at the two-second test bound. A configured deadline produced a timeout instead.
- **Impact:** the calling application waited unnecessarily. Independent work continued; an application-wide outage was not demonstrated.
- **Fix verification:** upstream SDK PR #3278 head `66a9285` returned an error promptly and passed the selected reauthorization control, unlike base `a4f4ccd`. This is scoped verification, not a shipped-release claim.

**Flow:** Application → FastMCP / SDK → server 401 → waiting client call.

## Matrices

| Boundary | JSON |
| --- | --- |
| Credential denial / revocation compatibility | [AUTH](matrices/AUTH.json) |
| Error propagation, deadline and recovery | [SSE](matrices/SSE.json) |
| Refresh coordination and crash consistency | [OAUTH-STORAGE](matrices/OAUTH-STORAGE.json) |
| Chosen owner-only deployment policy | [OS-ISOLATION](matrices/OS-ISOLATION.json) |

Read each row as: **invariant → scenario → oracle → observation → status → evidence → limit**.

[Detailed report, tests, logs and source pins](https://github.com/Keedz1Off/fastmcp-auth-state-sse-case-study/tree/291534dd73ebc992db23b9e1834dc9ed151c3246) are preserved in the pinned evidence snapshot. Matrix links open the exact supporting records.

FastMCP 4359485; selected MCP SDK environments and PR #3278 base/head. Independent, AI-assisted work. Documentation reorganisation only; no new target tests. [File inventory](package-manifest.json).
