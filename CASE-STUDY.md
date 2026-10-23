# FastMCP case study

## Executive Summary

In the owned SSE stand, a server rejection and a client wait coexisted: HTTP 401 prevented the revoked client's tool body from executing again, but the waiting RPC did not promptly receive the transport error. Without an RPC deadline it was still pending at the two-second harness bound and was cancelled. With a 0.5-second deadline it failed with MCPError in 0.515/0.516 seconds.

The result is an error-propagation/reliability defect in the inspected dependency path, **not evidence that revocation failed**. Independent client work and an event-loop heartbeat completed while the original call was still pending. No infinite wait, application-wide outage or resource exhaustion was demonstrated.

This report consolidates retained measurements and source checks, not a new reproduction. It assesses FastMCP snapshot `4359485` with MCP SDK 2.3.0 and 2.2.0 for the bounded SSE controls. No affected release range or first/fixed release has been established.

## Background

FastMCP provides MCP clients and servers; MCP is a protocol, not the LLM. Applications choose transports, credentials, tools and authorization rules. Legacy SSE separates a server-to-client event stream from client-to-server message POSTs.

In the stand, a synthetic credential had previously succeeded and was then revoked. A marker counted actual tool executions. Server responses and counters, not client success messages, established whether access survived.

## Vulnerability Details

No report-ready security vulnerability is claimed. The observed sequence was:

1. The client sent an ordinary tool RPC on its already-open SSE connection.
2. Server authorization rejected the POST with HTTP 401; the denied tool body did not re-enter.
3. The SDK's POST writer logged the transport exception. The independent reader/session remained active and the RPC waiter was not directly notified.
4. [Client._await_with_session_monitoring](https://github.com/PrefectHQ/fastmcp/blob/435948521d40a2d4b9b13b7f76ccfaa6a54a72c6/fastmcp_slim/fastmcp/client/client.py) monitors the session task, but an internally logged writer failure need not finish that task.
5. An explicit request deadline bounded the response wait. It mitigated waiting; it did not repair error propagation or prove the same connection reusable.

The retained SDK SSE files have the same SHA256 in both tested environments. That establishes inspected file equality, not a general affected-version range.

## Exploitability Analysis

| Observation | Classification and limit |
| --- | --- |
| POST error not promptly delivered to pending RPC | Confirmed bounded reliability defect; no authorization bypass |
| Two already-open OAuth contexts refresh against shared storage | Coordination limitation; sharing a database does not share their per-context lock or live token state |
| Controlled exit between token-pair and expiry writes | Crash-consistency limitation; new pair/old expiry observed, SQLite still valid; explicit retry repaired the test state |
| Public-client revocation returned invalid_request in an earlier SDK combination | Compatibility defect in that tested flow; confidential-client revocation worked; no access-control bypass proved |
| Additional modeled Windows SIDs had cache-file permissions | Failure of the chosen owner-only deployment policy; actual second-user logon, key access and plaintext-token disclosure not established |

The source [TokenStorageAdapter.set_tokens](https://github.com/PrefectHQ/fastmcp/blob/435948521d40a2d4b9b13b7f76ccfaa6a54a72c6/fastmcp_slim/fastmcp/client/auth/oauth.py#L148) performs token and expiry storage operations separately. The observed controlled interruption does not establish a naturally occurring exploit. Cross-process refresh results used an owned rotating-token provider, not every production IdP or token-family reuse policy.

A healthy independent call and heartbeat succeeded during the pending SSE RPC in both environments. This counters a claim that one occurrence necessarily disabled the stand; it does not prove every real consumer safe.

### Real consumer: EpicStaff

Static review of EpicStaff snapshot `7923b1d` found a Redis worker → Prefect FastMCP Client → supported legacy SSE path. Its lock specifies fastmcp/fastmcp-slim 3.4.7 and mcp 1.30.0, **different from the runtime stand**.

The factory passes a default 30-second request deadline and separate 10-second initialize deadline. Locked dependency source shows the response deadline reaches ClientSession. Cancellation forwarding and bounded disconnect logic are present. The worker drains in-flight tasks during shutdown rather than immediately cancelling them.

This is counterevidence to transferring the no-RPC-deadline condition unchanged. It is not a runtime result, a 30-second total-job SLA, proof of remote cancellation, or confirmation of this app being affected. Its full checkout failed on Windows path length; analysis used downloaded pinned Git objects and verified locked wheels.

## Proof of Concept

This documentation package contains selected sanitized JSON measurements, not an exploit runner or the complete raw traces. All runtime observations came from prior owned local checks.

- SSE error-feedback controls: four cases passed, two per SDK. Passing means the observation assertions held, **not that the product defect was fixed**.
- Concurrent-liveness controls: two cases passed. At most one failing RPC existed in each bounded stand.
- Historical multi-cycle refresh matrix: four cases, then a repeat of those same four. Do not count the repeat as eight independently covered behaviors.
- Original full upstream run: 9,856 collected; 9,744 passed, 19 unsuccessful, 77 skipped, 16 xfailed; exit 1.
- Historical Windows ACL run: 10 passed, two failed, one skipped. A real second OS-account process was not tested.

See [results and qualifications](RESULTS.md). No load, saturation, production-target or new application execution was performed for this packaging update.

## Remediation

No upstream fix was submitted or verified. The narrow SSE recommendation is to communicate writer/transport failure to pending RPCs or terminate the associated session coherently, while preserving cancellation and cleanup.

Explicit RPC deadlines are a tested mitigation of waiting, not a substitute for correct failure delivery. Shared refresh coordination and atomic token/expiry persistence should be designed and verified when an application requires those guarantees. An owner-only cache policy also requires validating OS identities, parent-directory trust and key access.

## Summary

The strongest finding is an evidenced client/dependency error-propagation defect. The other observations concern shared-state coordination, crash consistency, interoperability and deployment policy. None was upgraded into a confirmed exploitable vulnerability.

Remaining limits include real two-user OS isolation, production IdPs/TLS/deployments, consumer runtime behavior, an untrusted trigger with meaningful shared impact, release-history bounds and exhaustive source coverage.
