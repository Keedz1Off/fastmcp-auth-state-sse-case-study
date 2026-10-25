# Results without score inflation

## PR #3278 verification — 25 October 2026

The same three bounded SSE scenarios were measured on installed mcp 2.3.0, the PR's exact base, and its exact head: nine separate local cases in total.

| Source variant | Fixture controls | Desired behavior criteria |
| --- | ---: | ---: |
| Installed mcp 2.3.0 | 3/3 | 0/3 |
| PR base `a4f4ccd` | 3/3 | 0/3 |
| PR head `66a9285` | 3/3 | 3/3 |

Before the fix, the no-deadline call remained pending at the observation bound and the deadline control returned a timeout. At the head, the rejected call received a correlated transport error, and the same client completed a later call on its existing connection after normal reauthorization.

These are measurement cases: baseline processes completed normally while recording defective behavior. A 0/3 result is not a crashed runner. The full upstream suite was not rerun.

[Verification and limits](PR-3278-VERIFICATION.md) · [Actual measurements](evidence/pr3278-verification.json)

## Historical cohorts documented on 23 October 2026

The earlier documentation preparation added zero target tests and zero model calls. These cohorts overlap and **must not be summed** with one another or with the later PR verification as one test suite.

| Evidence cohort | Recorded result | Interpretation |
| --- | --- | --- |
| SSE error-feedback checks | 4 passed / 0 failed | The tests successfully observed/compared the defect and deadline control |
| Liveness checks | 2 passed / 0 failed | Independent authorized call and heartbeat completed while original call was pending |
| Multi-cycle OAuth matrix | 4 cases, then a repeat of the same 4 | One initial two-process refresh refusal/reauthorization per transport; later different pairs refreshed independently |
| Full upstream selection | 9,744 passed; 19 unsuccessful; 77 skipped; 16 xfailed | 9,856 items, exit 1; not green |
| Windows ACL controls | 10 passed; 2 failed; 1 skipped | Owner-only deployment-policy failures retained; actual second-user case untested |
| EpicStaff consumer follow-up | Static only | Supported SSE path and deadline/cancellation wiring; no application execution |

## Upstream failure triage

Fourteen unsuccessful nodes failed before their intended checks because Windows denied symlink creation. Other outcomes concerned a transient native-import policy block, performance worker/deadline behavior, cancellation before startup obtained a PID, bare npx launch and initialization recovery.

The original JUnit distinguishes 18 failure reports and one worker-error report within the 19 unsuccessful outcomes. Focused reruns and an explicit Windows adapter do not replace the original red run.

Selected format/type/lint/secret checks passed. Overall static pipeline did not: the main-branch guard failed and direct loq confirmed 36 size-budget violations. The loq hook's nominal pass was non-enforcing.

## Read the selected records

- [SSE feedback measurements](evidence/sse-feedback.json)
- [Concurrent liveness measurements](evidence/liveness.json)
- [Upstream result summary](evidence/upstream.json)
- [Observation classifications](evidence/observations.json)
- [Pinned source and dependency identifiers](evidence/source-pins.json)

These are selected sanitized summaries, not complete raw logs or a portable full-stand reproducer. No evidence of unauthorized tool execution, whole-app outage or proven infinite wait is claimed.
