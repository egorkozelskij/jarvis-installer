---
name: jarvis-memory
description: Remember, correct, recall or forget durable owner facts and communication preferences in an installed Jarvis instance. Apply the configured memory mode and scope; do not treat temporary task instructions or guesses as facts.
---

Read `core/memory.md`, `core/scopes.md`, and `config/instance.json` from the
instance root. Use the installed CLI at `bootstrap/scripts/jarvis.py`.

The general communication style, memory mode and exclusions are canonical in
`config/instance.json`. Reconfigure them through bootstrap; do not duplicate
them as personal notes. Other facts and preferences use scoped note IDs.

Determine personal versus `project:ID` before writing. Search for an existing
fact, reuse its stable ID when correcting it, and cite the user's statement
and date. `note` replaces the current record and preserves a correction trail.
One-response requests are task-local. Never infer a diagnosis or personality
trait from conversational tone. Explicit user correction needs no extra request
to remember when auto memory is enabled. Explain briefly if memory is disabled;
do not claim a write that did not happen. `on-request` requires an explicit
request to remember (`--explicit`). `off` prevents personal note writes.

Examples:
`note --root ROOT --scope personal --id reading-format --kind preference --text
"Prefer printed books" --source "Owner, current conversation"`.
`note --root ROOT --scope project:atlas --id package-manager --kind decision
--text "Use pnpm" --source "Owner correction, current conversation"`.

Use `forget --root ROOT --scope SCOPE --id ID --explicit` for a requested
deletion from active notes and their correction trail. Check archives and
snapshots separately; do not promise erasure of older remote backups. If a
topic is excluded, do not store it under a disguised name or in session logs.
