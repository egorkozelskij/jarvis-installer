---
name: jarvis-secrets-guide
description: Guide local credential storage and optional encrypted backup for a Jarvis owner. No vault encryption or credential connector is implemented by this skill alone.
---

Read `core/permissions.md`. Prefer the OS credential manager; an explicit
local/secrets fallback must be ignored by version control and access-restricted.
Never ask the owner to paste a token in chat or echo its value. assets/ is for
ordinary attachments, not a credential store. A private Git repository is not
encryption. Even if the owner requests synchronization, do not add plaintext
credentials: offer an established encryption tool and separate recovery key.
Only after encryption and restore are verified may the owner opt in to backing
up ciphertext in vault/. This installer merely creates the boundary.
