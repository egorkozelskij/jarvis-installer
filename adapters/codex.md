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
