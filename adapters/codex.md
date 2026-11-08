# Codex adapter

The local installer generates `.agents/skills/<name>/SKILL.md` and support files
from canonical installed modules. These are derived discovery copies; the
receipt hashes them to detect drift. Keep the canonical source in `modules/`.
The root AGENTS.md routes to core and selected modules. Validate discovery in a
fresh session of the target client; reading a file is not proof of discovery.

Use native input forms when available: multi-select for modules, single-select
for modes, text only for names/paths. Fall back to numbered options when native
forms cannot represent the question. Do not imitate clickable UI with plain
text checkboxes. Do not edit global skills or config during local installation.

To share one instance across chats, the owner must connect its entrypoint in
each intended client or explicitly request a host-level link. Use the chosen
instance path, never a developer's personal absolute path. Installation itself
does not edit global settings. Already running chats may need to reload rules.

With the owner's `history.capture=available-chats` choice, use available native
chat list/read tools during active work and the history module's incremental
workflow. Missing tools mean capture is unavailable, not that all chats are known.
The agent conducting each conversation saves justified useful context itself.
Memory sharing does not require a heartbeat or periodic scan. Do not create a
schedule as part of enabling memory or copy another instance's account/thread IDs.

Skill ownership and custom discovery follow core/skills.md and the bindings registry. Bundled module copies are derived; custom originals use registered links. Check a new host session separately. No home paths are installed automatically.
