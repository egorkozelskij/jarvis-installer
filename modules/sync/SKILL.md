---
name: jarvis-sync
description: Inspect pending local Jarvis changes, create a local snapshot, and guide explicit external synchronization setup. A local snapshot or queued event is not a remote delivery confirmation.
---

Read `core/maintenance.md` and `core/permissions.md`. `sync-status --root ROOT`
shows pending CLI changes. `snapshot --root ROOT --destination NEW_PATH` creates
a local copy excluding local/, inbox/, caches and plaintext secrets. It does
not push, encrypt, schedule or acknowledge pending changes as remotely delivered.
External edits need explicit inspection; no watcher runs in this release.

For GitLab/GitHub/cloud: ask the provider, private destination, allowed content
and frequency; use official setup tools only after owner authorization. First
check ignore rules and a dry-run file list. Use OS credential storage or
local/secrets; never put a token in a URL or committed Markdown. Keep secrets
excluded. If the owner wants secret backups, configure real encryption with a
separate recovery key before opting in to ciphertext backup. Verify restore
and actual remote receipt before reporting working sync. No force push.
