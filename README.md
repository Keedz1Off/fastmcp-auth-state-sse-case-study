# FastMCP SSE error handling

The server denied a protected tool call after token revocation, but the application never received the denial during the two-second observation window. A proposed MCP SDK fix delivered the error promptly in the same test.

## What the local test showed

| Check | Result |
| --- | --- |
| Server | Returned HTTP 401 and kept the protected tool from running |
| Client on the baseline SDK | Call stayed pending at the test deadline |
| Client with the proposed fix | Received the error promptly and passed the selected reauthorization check |

The result identifies a client error-handling issue. The server enforced authorization in the tested cases, and the fix comparison covers specific SDK revisions.

## Evidence

- [Recorded SDK comparison](evidence/pr3278-verification.json)
- [Boundary matrix index](matrices/boundaries.json)
- [SSE and recovery](matrices/SSE.json) · [Authorization](matrices/AUTH.json) · [OAuth storage](matrices/OAUTH-STORAGE.json) · [Deployment isolation](matrices/OS-ISOLATION.json)

## Run the checks

[Open Case study checks in GitHub Actions](https://github.com/Keedz1Off/fastmcp-auth-state-sse-case-study/actions/workflows/checks.yml) and select **Run workflow**. CI runs two offline tests against the saved server and client results.

The run saves `check-results`. Select **CD demo** to also package the passing log, commit SHA and checksum as `verified-delivery`.

Run locally with Python 3.10 or later:

```sh
python -B -m unittest discover -s tests -v
```
