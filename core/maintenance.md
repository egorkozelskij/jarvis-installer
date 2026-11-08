# Сопровождение, обновление и восстановление

## JARVIS-MAINTENANCE-001 — Changes keep the affected knowledge routes current

- Scope: authorized changes to this instance or a selected project, within its permissions.
- Invariant: update affected links, indexes, catalog entries and specifications in the same task. A fact and rule each have one canonical owner; project IDs remain stable.
- Safe path: link a new document from its owner, fix incoming links after a move, keep project-specific content at the section address resolved from its card, and mark unavailable routes pending. Routine path repairs within the task need no repeated permission.
- Do not: reorganize unrelated branches, create duplicate rule copies, change a topic's identity or merge distinct topics without authorization, or treat a working link as proof of correct content.
- Evidence: scoped path/link inspection and review against the current implementation. This rule is not a background watcher.

## Installation and recovery

Preserve data, local skills and owner choices during reconfiguration. The
installer preflights managed files and refuses to overwrite local modifications.
Resolve a conflict explicitly; never replace the whole installation to get past
it. Module removal disables discovery but retains user knowledge. User-created
skills belong to `modules/local`; do not overwrite them with distribution files.

Knowledge operations through the CLI record pending sync events. They do not
imply network delivery. `sync-status` distinguishes pending changes from an
actual confirmed snapshot. External edits require an explicit scan/workflow;
no watcher or scheduler is installed automatically.

The local snapshot provider includes managed components, config and user data,
excluding local state, plaintext secrets, inbox and generated indexes. It is a
local snapshot, not GitLab sync or an encrypted backup. In shared mode a snapshot
includes project cards, not the linked repositories or their local knowledge.
Back up each project through its own storage workflow; a central snapshot does
not prove those external sources were backed up. Ciphertext export and
real Git/cloud providers require separately configured and verified tools.
Do not claim success if a provider is unavailable. Never force push or silently
overwrite a conflict; preserve local changes for recovery.


Snapshots preserve selected file bytes and a checksum manifest. They do not
verify preservation of filesystem metadata, permissions, timestamps, empty
directories or link relationships, and do not establish transactional
consistency of running databases. Preserve required metadata and live state
with a separately configured backup workflow and verify recovery. External
stores and linked repositories need their own verified backups.

One writer owns an installation operation; use the provided lock. Concurrent
modifications must fail or be retried after reading the latest version. Atomic
file writes prevent truncated files, not multi-file crash rollback. Before an
upgrade preserve a recoverable copy and inspect proposed changes. Do not run
automatic destructive cleanup or uninstall the instance based on its pathname.

Remote mode is a future service with server-side identity, scope enforcement,
document revisions and one authoritative storage owner. The phone requires a
compatible client. An MCP connection is not a local skill install or permission
to operate a home computer. Current release does not deploy this service.
