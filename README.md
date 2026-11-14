# FastMCP: server rejected a call, client kept waiting

**Status:** client/dependency error-handling bug; no authorization bypass demonstrated.

FastMCP connects applications to MCP tools. We tested a protected call over an open legacy SSE connection after its token was revoked.

- **Expected:** server denies access; the application promptly receives an error.
- **Observed:** HTTP 401 blocked the tool, but the client call stayed pending at the two-second test bound. A configured deadline produced a timeout instead.
- **Impact:** the calling application waited unnecessarily. Independent work continued; an application-wide outage was not demonstrated.
- **Fix verification:** upstream SDK PR #3278 head `66a9285` returned an error promptly and passed the selected reauthorization control, unlike base `a4f4ccd`. This is scoped verification, not a shipped-release claim.

## Boundaries, tests and evidence

Open the [boundary index](matrices/boundaries.json) and the [recorded SDK comparison](evidence/pr3278-verification.json). [Python tests](tests/test_recorded_evidence.py) check the saved server-denial and error-delivery results. The original local FastMCP harness is not in the public snapshot.

Run the offline evidence checks from the repository root with Python 3.10 or later.

```sh
python -B -m unittest discover -s tests -v
```

These checks read saved files and do not launch the assessed application.

## Flow

```mermaid
flowchart LR
    A["Application call"] --> C["FastMCP / SDK, open legacy SSE"]
    C --> P["HTTP POST with revoked token"]
    P --> S["Server: 401, protected tool not run"]
    S --> T["SDK transport receives rejection"]
    T --> W["Baseline: caller pending at 2 seconds"]
    T --> F["Tested PR head: caller gets prompt error"]
```

## JSON matrices

| Boundary checked | JSON matrix |
| --- | --- |
| Credential denial / revocation compatibility | [AUTH](matrices/AUTH.json) |
| Error propagation, deadline and recovery | [SSE](matrices/SSE.json) |
| Refresh coordination and crash consistency | [OAUTH-STORAGE](matrices/OAUTH-STORAGE.json) |
| Chosen owner-only deployment policy | [OS-ISOLATION](matrices/OS-ISOLATION.json) |

## How to read

Read the summary and flow, then choose a JSON matrix above. Expand **Technical details** for field guidance, supporting records and exact versions.

<details>
<summary>Technical details: reading guide and evidence</summary>

1. Read the summary and flow to separate server denial from client error delivery.
2. Open [SSE](matrices/SSE.json), row `FM-ERROR`, for the base/head comparison; then [AUTH](matrices/AUTH.json) for access controls. `invariant` is the required rule, `oracle` the measurement, and `observed` the result.
3. Follow `evidence[].url`; a `pointer`, when present, selects a nested JSON entry. Read `status` with `limits`: fix verification applies to the stated scenario and commits.

[Evidence archive: detailed report and recorded results](https://github.com/Keedz1Off/fastmcp-auth-state-sse-case-study/tree/291534dd73ebc992db23b9e1834dc9ed151c3246) are preserved in the pinned evidence snapshot. Matrix links open the exact supporting records.

FastMCP 4359485; selected MCP SDK environments and PR #3278 base/head. Independent, AI-assisted work. [File inventory](package-manifest.json).

</details>
