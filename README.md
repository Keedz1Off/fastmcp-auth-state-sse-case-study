# FastMCP: authentication, state and SSE failure analysis

**Question:** do authorization decisions, client errors and shared OAuth state preserve their intended boundaries?

**Main result:** the owned server correctly denied a revoked synthetic credential with HTTP 401, while an SSE client RPC remained pending at a two-second observation bound. An explicit 0.5-second RPC deadline produced MCPError in approximately 0.52 seconds. This is a confirmed client/dependency **error-propagation defect**, not a demonstrated authorization bypass or application-wide DoS.

Assessed: PrefectHQ FastMCP source snapshot `4359485`. The SSE controls used MCP SDK **2.3.0 and 2.2.0**, with exact dependency fingerprints retained. Snapshot build metadata is not a public FastMCP release number.

## Upstream fix verification — 25 October 2026

Independently compared SDK PR #3278 at exact base `a4f4ccd` and head `66a9285`, with installed mcp 2.3.0 as a release control. Nine fresh local cases checked prompt error delivery, an explicit RPC deadline, and reuse after reauthorization of the same synthetic client.

**Result:** the tested PR head fixed the selected SSE HTTP 401 waiting behavior. All three desired-behavior criteria held on the head; none held on the base or release control. Server denial and the independent healthy-client controls held across all nine cases.

[Before/after verification](PR-3278-VERIFICATION.md) · [Measurements](evidence/pr3278-verification.json) · [Published upstream confirmation](https://github.com/modelcontextprotocol/python-sdk/pull/3278#issuecomment-6401226641)

## Work performed

- Mapped MCP transports, configured server authorization, OAuth token state and client/session lifecycles.
- Examined JWT/OAuth, PKCE/JWKS, SSE/STDIO, callback/refresh, persistence and selected storage-isolation controls.
- Classified concurrent-refresh, interrupted-write, revocation-compatibility and Windows deployment-policy observations separately.
- Used independent healthy-client and event-loop controls to challenge the DoS interpretation.
- Traced a real consumer's supported SSE path and deadline wiring by source, without running that application.
- Ran and triaged the original upstream suite; it remained red, rather than being replaced by successful diagnostics.

## Read in order

1. [Reading guide and file map](READING-GUIDE.md)
2. [Architecture and failure flows](FLOW.md)
3. [Case study and observations](CASE-STUDY.md)
4. [Evidence and result accounting](RESULTS.md)
5. [Upstream fix verification](PR-3278-VERIFICATION.md)
6. [Source pins](evidence/source-pins.json) · [offline verification](VERIFY.md)

Independent, AI-assisted, scoped assessment. No confirmed exploitable security vulnerability, CVE, accepted bounty, shipped fix or full-audit claim. Original package prepared 23 October 2026. The 25 October update adds separately recorded local PR verification; it does not replace the earlier upstream-suite results or claim a full rerun.
