# FastMCP: reading guide

## Where to start

Read README.md for the summary, FLOW.md for the architecture, CASE-STUDY.md for the reasoning, and RESULTS.md for the result accounting. Consult evidence/ only when you want the exact measurements or source pins.

| File or directory | Purpose |
| --- | --- |
| [README.md](README.md) | Scope, main result, assessed snapshot, and navigation links. |
| [FLOW.md](FLOW.md) | Client/server, authorization, OAuth state, and SSE failure paths. |
| [CASE-STUDY.md](CASE-STUDY.md) | Main analysis: observations, impact, counterevidence, limits, and recommendations. |
| [RESULTS.md](RESULTS.md) | Test accounting and what passing or failing checks actually mean. |
| [PR-3278-VERIFICATION.md](PR-3278-VERIFICATION.md) | Later independent before/after check of the proposed SSE fix. |
| [evidence/pr3278-verification.json](evidence/pr3278-verification.json) | Nine local measurement cases across release, exact PR base and exact PR head. |
| evidence/ | Selected sanitized JSON measurements, not executable tests. |
| [evidence/sse-feedback.json](evidence/sse-feedback.json) | Server rejection, pending RPC, and deadline observations. |
| [evidence/liveness.json](evidence/liveness.json) | Independent healthy-client and event-loop controls. |
| [evidence/observations.json](evidence/observations.json) | Shared-state, interrupted-write, compatibility, and deployment observations. |
| [evidence/upstream.json](evidence/upstream.json) | Original upstream run accounting and failure qualifications. |
| [evidence/source-pins.json](evidence/source-pins.json) | Source revisions and dependency/evidence fingerprints. |
| [VERIFY.md](VERIFY.md) | How to check this documentation package offline. |
| [verify_package.py](verify_package.py) | Checks hashes, sizes, and local links; does not run FastMCP. |
| [MANIFEST.json](MANIFEST.json) | Expected file sizes and SHA256 hashes used by the verifier. |
| [NOTICE.md](NOTICE.md) | Attribution, AI assistance, and assessment limits. |

## One-minute explanation

The study examined authorization, SSE sessions, and persisted OAuth state. In the main local case, the server correctly returned HTTP 401 after a test credential was revoked, and the tool did not execute again. The client RPC nevertheless kept waiting: the transport logged an error without delivering it promptly to the waiter.

The controls compared behavior without an RPC deadline and with an explicit deadline, then checked an independent client and the event loop. The result is an error-propagation defect, not a demonstrated authorization bypass or application-wide DoS.

The work used AI-assisted analysis and tools; it is not presented as entirely manual review.

The 25 October update also [verified the proposed upstream fix](PR-3278-VERIFICATION.md): the exact PR head delivered the error promptly and supported a later valid call on the same client's existing connection. The historical behavior described below remains preserved as baseline evidence.

## Normal flow

The host or agent selects a tool. FastMCP Client sends a request over the chosen transport. The MCP server applies configured authentication and application authorization before invoking the tool and backend.

MCP is the communication protocol; FastMCP is a client/server library. An LLM may choose an action, but it does not replace server-side permission checks.

Legacy SSE uses a server-to-client event stream alongside client-to-server HTTP POSTs. A POST failure and the event stream's lifetime are different states.

## Why the client waited

An RPC is a request expecting a response. A background writer sent it; the server correctly denied the action with 401. The writer logged the error, but the waiting RPC was not directly notified while the reader and session task remained active.

Without an RPC deadline, the call was still pending at the two-second observation bound and was then cancelled by the stand. This does not establish an infinite hang. With a 0.5-second deadline, MCPError arrived in about 0.52 seconds.

An independent client and event-loop heartbeat completed while the first call waited. One pending request therefore does not establish that the entire application stopped working.

## Four additional observations

**Concurrent refresh.** Two processes used shared storage but separate OAuthContext instances and locks. A shared database does not make those locks shared. With rotating refresh tokens, an initial refresh was rejected, followed by reauthorization. Later, the processes refreshed different token pairs; this did not prove coordinated exactly-once refresh.

**Interrupted writes.** The new token pair and absolute expiry were stored separately. A controlled exit between those writes left a new pair with the old expiry. SQLite remained valid. An explicit retry repaired the tested state; automatic recovery was not established.

**Public-client revocation.** In an earlier tested SDK combination, revocation without client_secret returned invalid_request. The confidential-client flow worked. This is a compatibility observation, not a demonstrated authorization bypass. The separate SSE server-denial case is a different check.

**Windows ACLs.** Inherited permissions gave additional modeled SIDs cache-file rights contrary to the selected owner-only policy. A real second-user logon was not exercised. Key access and plaintext-token disclosure were not demonstrated.

## What the EpicStaff source review establishes

A real Redis worker supported a PrefectHQ Client-to-SSE path. It used different dependency versions and already configured a 30-second response deadline plus a separate 10-second initialize deadline. Source tracing showed the response deadline reaching the response wait.

This was static analysis; the application was not run. Thirty seconds is not a bound on the entire job, which may include connection setup, several RPCs, model work, and cleanup. The worker drains in-flight tasks on normal shutdown. Cancelling a local wait does not guarantee that a remote action stops.

## Questions a reviewer may ask

**Is this an authorization bypass?** No. The server returned 401, and the denied tool body did not run again.

**Is it DoS?** Not established. A pending RPC was observed, but shared availability impact was not demonstrated.

**Why use a healthy control?** To test the alternative explanation that the whole event loop or server had stopped working.

**Why do tests pass if a bug remains?** An observation test can correctly assert defective behavior. Passed does not mean the product was fixed.

**Was the full upstream suite run?** The pinned snapshot's full default selection collected 9,856 items and remained red with 19 unsuccessful outcomes. This does not cover every environment or opt-in test selection.

**What is the main contribution?** Tracing server rejection through client transport and session state to the pending waiter, checking independent signals, and calibrating the impact to the evidence.
