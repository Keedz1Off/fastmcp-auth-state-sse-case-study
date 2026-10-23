# Results without score inflation

All results below are historical. Preparing this documentation on 23 October 2026 added zero target tests and zero model calls. Cohorts overlap and **must not be summed** as one test suite.

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
