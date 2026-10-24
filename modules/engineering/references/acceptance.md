# Accept and verify

Acceptance answers one question: what has actually been shown about this
change, and what has not.

## What each check proves

| Check | Shows | Does not show |
|---|---|---|
| diff, whitespace check | Which files changed | That behavior is right |
| Type checker | Static contracts | Runtime behavior |
| Linter | Only the enabled rules | Anything else |
| Unit / contract / integration tests | The covered scenarios | Uncovered paths, however many tests pass |
| Browser or live run | That flow in that environment | CI, other environments, production |
| Local success | The local run | CI, deployment or release |
| Review | Traced reasoning | That commands were executed |

## Rules

- Decide the checks before running them; do not pick checks after seeing
  which ones pass.
- For a change to complex behavior, add or require a scenario that drives the
  changed path (reordered reads, partial disposal, error paths) before
  accepting. Count of passing tests is not an argument by itself.
- Use statuses `pass`, `fail`, `not-run`, `blocked`, `not-available`,
  `excluded`. A build that skips type checking does not make types `pass`.
- Separate failures that existed before the change from regressions.
- A flaky test may be retried up to three times; do not rewrite it unless the
  change is proven to affect it.
- Run tests only when the owner or a project rule asks for them.

## Final report

- what changed in behavior;
- entrypoint and source of truth;
- key files and versions;
- invariants kept;
- checks run and what each proves;
- checks not run;
- remaining risks and rule conflicts;
- rules or templates added or changed.

Keep the states apart: fixed, measured, consumers checked, merged, released.
