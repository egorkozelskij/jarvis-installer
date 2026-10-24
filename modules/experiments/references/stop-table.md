# When to stop

| Result | Next action |
|---|---|
| Correctness broken | Fix or reject the candidate; make no speed claim |
| Regression found | Find the cause or reject the candidate |
| Promising signal | Confirm the chosen variant in a separate run |
| No difference established | Record the uncertainty; a new run needs a new question or conditions |
| Conditions too noisy | Stop measuring there; keep the diagnostic data |
| Budget exhausted | Stop, keep partial data, list what was not checked |

Before repeating an expensive run, name the reason: a bug was fixed, the
conditions changed, or the new data could change the decision. "To be sure"
is not a reason.

## Example: same code, different verdict

A wrapper overhead criterion required a median ratio at or below 1.15 and at
least five of six rounds within it. The first run gave a median of 1.117 with
three of six rounds inside the limit and failed. A later run of the same hot
path gave 1.035 with five of six and passed. The code had not changed; the
second run was taken without parallel load. The environment is a likely
explanation, but without a control experiment the cause is unproven, and the
pair of runs shows no speed-up of the code.
