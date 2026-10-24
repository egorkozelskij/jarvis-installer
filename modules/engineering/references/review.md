# Review

Check a change against the project's rules and observable behavior. A review
is read-only; fix code only when the owner asked for fixes.

## Inputs

Read the patch, the applicable rules and the saved results of checks. The
author's summary helps navigation but can carry a wrong premise; verify it
against the code. A reviewer from a fresh context is preferable for risky work.

## Work

1. List the applicable rule IDs for the touched scope.
2. Trace state owners, dependency direction, side effects, lifecycle and
   public API through the changed paths.
3. Look for behavior a value check does not see: order of callbacks and
   cleanup, the order of aggregated errors, resource release, partial disposal
   while neighbours stay alive, repeated access, concurrency and size limits.
4. For each risky path ask which scenario would expose a mistake. If no test
   covers it, name the missing scenario; a large test count is not coverage of
   that path.
5. Separate problems introduced by this change from pre-existing debt.
6. Say what you ran and what you only read.

## Verdict

For every applicable rule give:

- `verdict`: `pass`, `violation`, `uncertain` or `not-applicable`;
- `evidence`: files, symbols and the traced path;
- `reason`: why the evidence supports the verdict;
- `risk`: the practical consequence;
- `safe path`: the smallest fix.

`uncertain` is not a pass. Do not report taste as a violation without an
invariant. End with the next justified action and what must not yet be
considered finished.
