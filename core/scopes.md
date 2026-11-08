# Контекст и применимость

Before reading personal information or modifying files, determine the task and
its scope: instance, personal, or a registered project. Use the current user
request and bindings in `config/instance.json`; cwd alone is insufficient.

Order: host permissions and current user instructions, applicable system
contracts, then the selected domain/project rules and narrower rules.
Narrowing a durable rule must identify the original and exact scope. Never
silently resolve contradictory rules by copying one into global settings.

Load common applicable rules and the chosen branch, not every document in the
instance. A coding task does not authorize reading health or family records.
Cross-domain retrieval needs relevance and permission. If consequential scope
is ambiguous, ask; otherwise choose the narrowest reasonable scope.

## Resolving a project

Read core/projects.md. For schema 2 use the card's stable identity, sources, parent chain and per-section storage. The instance location_mode does not force project knowledge local or global. Resolve addresses through config/project-roots.json; no root.json is needed. Read project.md and notes/working-context.md when present, then only relevant topics and rules. Missing roots never trigger fallback writes.

For legacy schema 1 keep explicit source_root/entrypoint until an authorized migration. Project hierarchy and storage are independent; cwd is evidence, not identity. Do not inherit sibling rules or copy knowledge to make navigation easier. Explicit common-document imports are permitted by core/projects.md; importing one document does not import its owner's entire profile. Select direction and stack from the task and project entrypoint, preserving each rule's original scope. User permissions and current task scope govern edits and external actions.

## Instance, personal and project

Instance maintenance concerns this installation's own core, config, modules,
catalog and tools. Personal knowledge follows core/memory.md and the selected
personal module. Project engineering follows the registered card and the
project's local rules. Do not invent a project card for instance/personal work
or borrow a sibling project's rules. An unregistered source repository follows
its own entrypoint; registration and adding local files are separate actions.

Load common rules before narrower target rules. Writing uses the selected
writing module in any scope; it does not implicitly enable engineering.
