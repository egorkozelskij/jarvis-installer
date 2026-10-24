# Change

Make the requested change completely, but do not widen it into unrelated
cleanup, release or deployment.

## Before editing

1. Read the applicable rules and the task card. If no card exists for a
   non-trivial task, write one from `modules/engineering/templates/task-card.md`.
2. Check the state of every repository you will touch. Preserve the owner's
   uncommitted work; never discard or reformat it.
3. Identify the entrypoint, the state owner, the public contract and the
   smallest scope that solves the task.
4. List behavior that must stay the same, including order of callbacks and
   cleanup, error shape, resource release and memory limits.
5. If code contradicts a rule, tell the owner before copying the pattern.

## While editing

- Reuse existing owners and modules when they match the rules.
- Do not add an abstraction, registry or config layer without a current user.
- Change the source of truth, not a derived copy.
- Keep each repository's change self-contained. A library patch and a consumer
  patch may belong to one task but remain two results.

## Finishing

Run only checks that are allowed and proportional, then report as described in
`modules/engineering/references/acceptance.md`. When several repositories are involved, state which version
or build of the library the consumer actually used; a passing library check
does not prove the consumer runs that build.

Commit, push, tag, publish and deploy each need an explicit request.
