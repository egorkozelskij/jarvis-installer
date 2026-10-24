# Сопровождение, обновление и восстановление

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
local snapshot, not GitLab sync or an encrypted backup. Ciphertext export and
real Git/cloud providers require separately configured and verified tools.
Do not claim success if a provider is unavailable. Never force push or silently
overwrite a conflict; preserve local changes for recovery.

One writer owns an installation operation; use the provided lock. Concurrent
modifications must fail or be retried after reading the latest version. Atomic
file writes prevent truncated files, not multi-file crash rollback. Before an
upgrade preserve a recoverable copy and inspect proposed changes. Do not run
automatic destructive cleanup or uninstall the instance based on its pathname.

Remote mode is a future service with server-side identity, scope enforcement,
document revisions and one authoritative storage owner. The phone requires a
compatible client. An MCP connection is not a local skill install or permission
to operate a home computer. Current release does not deploy this service.
