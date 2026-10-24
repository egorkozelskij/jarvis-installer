# Структура и владение

`AGENTS.md` is a short entrypoint, not the whole manual. `config/instance.json`
records owner choices, scopes, consent and installed capabilities. It contains
no credentials. `config/installation.json` records managed file hashes and the
distribution version; it is a receipt, not user knowledge.

Distribution: `bootstrap`, `core`, `modules`, `presets`, `adapters`, `templates`.
Instance: the same relevant components plus user-owned data as needed:

- `knowledge/personal`: owner facts, preferences, life areas, goals, contacts.
- `projects/<stable-id>`: project description, governance, decisions, assets.
- `assets`: shared attachments, not credentials.
- `archive/conversations`: optional imported conversation sources.
- `inbox`: untrusted incoming material, outside automatic skill discovery.
- `vault`: optional encrypted payloads; encryption setup is not implemented yet.
- `local`: device-specific state, indexes, secrets and caches; always ignored.
- `.agents/skills`: generated discovery copies; edit canonical module sources.

Create a folder when it has a consumer, not a folder for every imaginable topic.
Knowledge and project documents have one canonical location; navigation links
refer there. Do not place project rules in personal preferences or duplicate a
whole source tree in the assistant. Project source paths are optional bindings.

The installer only writes inside its explicit target. "Shared" means one
owner's instance used by selected projects, not a system-wide installation.
It does not edit other projects' AGENTS.md or any global configuration.
