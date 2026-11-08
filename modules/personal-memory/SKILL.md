---
name: jarvis-memory
description: Retain, recall, correct or forget significant owner facts, preferences and current work in an installed Jarvis instance, including routine updates when auto memory is explicitly enabled. Apply the configured scope and exclusions; keep guesses separate from facts.
---

Read `core/memory.md`, `core/scopes.md`, and `config/instance.json` from the
instance root. Use the installed CLI at `bootstrap/scripts/jarvis.py`.

The general communication style, memory mode and exclusions are canonical in
`config/instance.json`. Reconfigure them through bootstrap; do not duplicate
them as personal notes. Other facts and preferences use scoped note IDs.

When this module is enabled, read `knowledge/personal/context/active.md` at task
start and open only relevant topics. With `memory_mode=auto`, the communicating
agent itself retains new information and work state when it can justify their
value for future conversation or work, without waiting for "remember this".
If nothing useful changed, do not write merely because a reply ended. Do not
create a timer or background scan as a substitute for this judgment and write.
`autonomy=ask` still governs unrelated actions.
With `on-request`, wait for an explicit personal-memory request; with `off`,
do not collect personal knowledge. Check existing records before asking the
owner to repeat known information.

Determine personal versus `project:ID` before writing. Search for an existing
fact, reuse its stable ID when correcting it, and cite the user's statement
and date. `note` replaces the current record and preserves a correction trail.
Use `--section` to choose profile, preferences, areas, vectors, events, my-notes,
context or inbox. Omitted sections retain the old `notes` location. A record's
identity is its scope, section and ID; correction trails remain separate.
Keep one main record per fact, link related topics, and preserve important
previous states as history. Split oversized topics instead of creating one
large memory file. Re-read before replacing a record to retain concurrent work.
One-response requests are task-local. Never infer a diagnosis or personality
trait from conversational tone. Explicit user correction needs no extra request
to remember when auto memory is enabled. Explain briefly if memory is disabled;
do not claim a write that did not happen. `on-request` requires an explicit
request to remember (`--explicit`). `off` prevents personal note writes.

Examples:
`note --root ROOT --scope personal --section preferences --id reading-format --kind preference --text
"Prefer printed books" --source "Owner, current conversation"`.
`note --root ROOT --scope project:atlas --id package-manager --kind decision
--text "Use pnpm" --source "Owner correction, current conversation"`.

For a current-work topic use `--section context --kind state`. Record the goal,
verified result, decisions, open questions and next step with the source ID and
date. Keep `context/active.md` a short index of topic links; project details
belong at the project's local entrypoint. `event`, `hypothesis` and `question`
are available kinds when the material is not a confirmed fact or decision.

Use `forget --root ROOT --scope SCOPE --section SECTION --id ID --explicit` for a requested
deletion from active notes and their correction trail. Check archives and
snapshots separately; do not promise erasure of older remote backups. If a
topic is excluded, do not store it under a disguised name or in session logs.
Forgetting without `--section` continues to target legacy `notes` records.
Archives use the separate history module and owner choice, not memory mode alone.
