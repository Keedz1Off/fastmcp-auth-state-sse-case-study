# Independent verification of the legacy SSE fix in PR #3278

**Result:** the tested PR revision fixes the selected HTTP 401 error-propagation case in the local FastMCP fixture. This is verification of a known reliability fix.

## Sources and method

- Before: `a4f4ccd091138771535e17191123f20b30fda68e`.
- After: `66a928547c160e4aca20a558d28aa50c08151426`.
- Additional release control: installed mcp 2.3.0.
- Unchanged FastMCP client/server: `435948521d40a2d4b9b13b7f76ccfaa6a54a72c6`.
- Windows, Python 3.12.10; recorded on 25 October 2026.

The complete pinned SDK and matching mcp-types sources were imported for the base/head comparison, with the same existing dependency environment. Installed distribution metadata still reports 2.3.0 under a source override; the full revisions and recorded module hashes identify the code actually tested.

Each fresh owned loopback fixture first completed healthy calls, then revoked one synthetic client's credential and made one rejected protected call. The original fixed-bearer scenarios were preserved. A separate recovery control used a newly authorized token for the same registered client through the normal HTTP authentication interface.

## Before and after

| Check | Release 2.3.0 / PR base | PR head |
| --- | --- | --- |
| Rejected call, no RPC deadline | Pending at the approximately 2-second observation bound; cancelled by harness | MCPError -32603 in approximately 0.016 seconds |
| Rejected call, 0.5-second deadline | MCPError -32001, request timeout, in approximately 0.5 seconds | MCPError -32603 in approximately 0.016 seconds |
| Same client, new valid token, existing connection | Follow-up reported Connection closed | Follow-up succeeded |

Three scenarios per variant produced nine measurement cases. All nine retained server HTTP 401 denial, no re-entry of the revoked client's protected tool, a working independent client, and closed listeners during cleanup.

The baseline recovery observation includes cancellation of the earlier pending call by the harness; it is not isolated evidence about HTTP 401 alone. Timings are descriptive, with Windows timer granularity, not performance guarantees.

## What changed

Before the patch, the SDK writer logged the POST failure while the RPC continued waiting. The PR returns an error correlated to that request and preserves the selected valid-token follow-up path.

Server authorization denied the revoked credential before and after. This is not a demonstrated authorization bypass. The returned error is generic; preservation of the HTTP status in structured error data was not asserted by this check.

## Scope and evidence

The nine local cases do not certify the entire PR, all transports or all deployments. No full upstream rerun, load test, exhaustion claim or exploitable outage is represented. The immutable source modules were checked unchanged after execution. Python-level network audit recorded no non-loopback events; that is not comprehensive native-process confinement.

- [Sanitized measurements and source fingerprints](evidence/pr3278-verification.json).
- [Our published confirmation](https://github.com/modelcontextprotocol/python-sdk/pull/3278#issuecomment-6401226641).
- [Upstream PR](https://github.com/modelcontextprotocol/python-sdk/pull/3278).

This verifies a proposed fix at the stated revision; it does not claim the patch is included in a published release. AI assisted the source review, local testing, analysis and write-up.
