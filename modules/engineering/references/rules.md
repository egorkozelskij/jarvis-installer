# Project rules

A rule is a durable requirement that must survive the current conversation and
apply to the next agent. Store it once, in the project's resolved rules section; link
to it elsewhere instead of copying it.

## Format

Use `modules/engineering/templates/rule.md`. Every rule has:

- **ID** — stable, e.g. `CORE-CLEANUP-ORDER-001`; never reused for another meaning.
- **Scope** — the exact project branch, package or path it governs.
- **Invariant** — the property that must hold, stated so it can be checked.
- **Safe path** — the normal way to satisfy it.
- **Forbidden** — the tempting shortcut it excludes.
- **Evidence** — how compliance is shown: `hard-static`, `hard-contract`,
  `runtime-evidence`, or `architecture-review`. Legacy aliases `static`,
  `contract`, `runtime`, and `review` retain their corresponding meaning. A rule without an evidence path is a wish.

## Hierarchy

The card's resolved rules entrypoint routes to project-wide rules and branches
such as backend or packages. Sources and instance location_mode do not determine
where rules live. For legacy cards retain the explicit entrypoint. Read the common level, then
only the branch the task touches. A narrower rule may refine a broader one only
by naming the original ID, the exact scope and the reason. Being deeper in the
tree is not permission to cancel what was read above.

## When to add or change a rule

1. Confirm a repeated or costly problem and who owns the affected area.
2. Prefer a check that runs by itself when it can express the rule reliably.
3. Otherwise make it a `review` rule; do not write a custom checker for a
   one-off concern.
4. Do not turn taste, file size or naming preference into a rule without an
   invariant that protects behavior.
5. A single mistake usually needs a test scenario, not a repository-wide ban.

Rules cost attention. When one becomes obsolete or contradicts the code, raise
it with the owner and retire or rewrite it; do not leave two active truths.
Write a new rule only with the owner's agreement unless the project grants it.
