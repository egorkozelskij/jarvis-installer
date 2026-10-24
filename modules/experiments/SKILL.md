---
name: jarvis-experiments
description: Plan, run and report performance or comparative measurements for an engineering project within a stated budget. Check correctness before timing, fix the matrix in advance, and never keep measuring until a desired win appears.
---

Read `modules/engineering/SKILL.md` and the project's rules first. A project
rule may set its own budgets, tools and machines; it overrides the defaults
below only for its stated scope.

## Choose the mode

| Mode | Default | Budget |
|---|---|---|
| Ordinary change | Project checks; no benchmark added automatically | Part of acceptance |
| Hypothesis | Paired baseline vs candidate, 1–3 related scenarios, 1–2 sizes | about 5 minutes |
| Final check | Predefined matrix of correctness, regressions and needed metrics | about 60 minutes |
| Extended research | Multi-hour comparison, competitors, many environments | Only on explicit owner request |

A request to "make it faster" or "beat competitors" does not by itself allow a
multi-hour run. Normal cycle: baseline → narrow hypotheses → one candidate →
one final check.

## Before running

Write the plan from `modules/experiments/templates/experiment-plan.md`: the question, baseline and
candidate identifiers, environment, scenarios and sizes, expected correct
output, acceptance criterion, warm-up, rounds, run order, and the budget.
Decide the criterion before seeing numbers.

## Running

1. Check that each variant produces the correct result before timing it. A
   faster wrong result is a failure, not a speed-up.
2. Alternate or randomize variant order; use fresh processes where state or
   JIT warm-up can leak between runs.
3. When a small difference matters, run baseline against itself (A/A) to see
   how much the measurement moves with no code change.
4. Keep every planned cell in the results, including failed and noisy ones.
5. Record other load on the machine. Builds, installs, browsers or other
   agents on the same machine make timing exploratory, not confirmation. Use a
   quiet dedicated machine for confirming runs when the project has one.
6. Retries count against the same budget. A new folder or run name does not
   reset it; repeat only with a concrete new reason.

Then decide with `modules/experiments/references/stop-table.md` and report with
`modules/experiments/references/report.md`. "No difference established" is a valid result.
