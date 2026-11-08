---
name: jarvis-engineering
description: Explore, change, review, accept or hand off code work in a registered engineering project using its scoped rules. Classify the assignment first; a request to explore or review grants no right to edit, commit, publish or deploy.
---

Read `core/scopes.md` and `core/projects.md`, resolve the card's sources, parent
chain and section storage. Instance location_mode does not choose project storage.
Read ancestor/common rules and the target's resolved rules entrypoint, then relevant
specs; legacy cards retain their explicit binding until authorized migration.
Never use a reference project's rules as governing rules for the current project.
Report consequential code/document conflicts before propagating them.

Always read `modules/engineering/references/workflow.md` and
`modules/engineering/references/specifications.md`. Before permitted checks read
`modules/engineering/references/testing-and-benchmarks.md`; for long work read
`core/long-running-agent-work.md`; before an authorized commit read
`modules/engineering/references/commits.md`. Local profiles retain their commands,
versions, paths, permissions and explicit scoped overrides.

Classify the assignment before acting and read only its reference:

| Assignment | Result | Reference |
|---|---|---|
| Explore | Explanation of the real structure; no edits | `modules/engineering/references/context-map.md` |
| Change | A scoped change with stated evidence | `modules/engineering/references/change.md` |
| Review | Verdicts with evidence; no edits unless asked | `modules/engineering/references/review.md` |
| Accept / verify | What was proven, what was not run | `modules/engineering/references/acceptance.md` |
| Pause / pass on | A short state another agent can resume | `modules/engineering/references/handoff.md` |
| Add or change a rule | A rule with ID, scope and evidence | `modules/engineering/references/rules.md` |
| Claim it is faster/smaller | Use `jarvis-experiments` if installed | `modules/experiments/SKILL.md` |

Each result authorizes only itself. Exploring does not authorize editing; a
change does not authorize commit; commit does not authorize push, tag, package
release or deployment. Ask for each step the owner has not explicitly granted.

For non-trivial work, write the task card from `modules/engineering/templates/task-card.md` before
the first edit: goal, behavior to keep, check order and expected result. Name
observable behavior explicitly (ordering, errors, resource release, public API,
memory limits); these are the properties tests most often miss.

Never report one word "done". Report separate states: behavior changed, checks
run, measurements, consumers checked, merged, released. Unrun steps stay open.
A summary from another agent is a lead, not evidence; read the patch and the
saved results yourself before relying on them.
