# Hand off

Long work stops: a session ends, a budget runs out, another agent takes over.
The handoff lets the next agent continue without repeating checked work or
inheriting a wrong conclusion. Use `modules/engineering/templates/handoff.md`.

## Content

- the question being answered;
- baseline and candidate revisions (commit, build or file hash);
- what was checked and the result, including negative results;
- rejected options and why;
- separate states: correctness, performance, consumers, merge, release;
- what was not run;
- the open question and the next action with its reason;
- where large logs, traces and raw data live (paths, not contents).

Write it so the reader understands the result without opening raw data.
Failed and unfinished attempts stay next to successful ones; otherwise the next
agent sees a biased picture and repeats them.

## Parallel work

Before splitting hypotheses between agents or worktrees, fix the base revision,
the scenarios, the checks and the result format. Results produced from
different bases or scenarios cannot be compared in one table.

A separate worktree isolates files only. CPU, memory and disk stay shared, so
timing results from parallel agents on one machine are not confirmation.

## Budget

A small hypothesis and a multi-day investigation are different assignments.
Record the budget in the handoff. Re-running the same question under a new
name does not reset it; a new attempt needs a new reason.
