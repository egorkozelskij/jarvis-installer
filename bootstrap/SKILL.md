---
name: jarvis-bootstrap
description: Install or reconfigure an owner-controlled Jarvis knowledge base from this distribution. Use for first-run profiling, module selection, installation checks, and project links. Does not migrate existing assistants or configure external accounts automatically.
---

# Jarvis bootstrap

1. Read `../core/README.md`, then layout, permissions and maintenance. Read the
   module catalog from `../modules/registry.json`; do not invent capabilities.
2. Explain: this creates files and instructions; it does not create a running
   background assistant. Shared installation means one folder reused by the
   owner's projects. Never modify global agent settings or another project.
3. Run `python3 scripts/jarvis.py questions --language ru` (paths here are relative
   to this skill). Ask in small groups. Use the host's native multi-select for
   modules and single-select for modes when a real input tool is available and
   confirms that it displayed the questions. Never refer to an invisible form.
   Otherwise include numbered questions in your reply and accept a list of
   numbers; Markdown boxes are not interactive.
   Ask free text only for a path, name and optional preferences. Do not read
   other personal directories to profile the user. Do not repeat answered items.
4. Core questions: folder/shared location and exact path; name and language;
   selected modules; memory mode and excluded topics if memory is selected;
   autonomy and communication style. Explain memory modes before choosing.
   No personal memory by default: offer `on-request` as the initial choice.
5. Conditional questions concern ONLY selected optional modules: archive sources,
   local snapshot destination/provider, intended recipients, OS/control tools,
   secret storage and encrypted backup consent, remote hosting. These are setup
   preferences, not credentials or blanket permission. Record them under
   `module_options`; external services remain `unconfigured`. Do not ask for a
   password/token in chat. Remote access is planned, not installable in v1.
6. Create an answer JSON using `../templates/answers.example.json`. Run `plan`
   and show the exact target, modules/dependencies, deferred items and data
   boundaries. Within the user's already authorized installation, proceed;
   ask for missing choices, not repeated approval. If a path is nonempty and
   not an existing Jarvis instance, stop; propose a dedicated child folder.
7. Run `install --target ABSOLUTE_PATH --answers ANSWERS_JSON`, then `doctor
   --root ABSOLUTE_PATH`. Do not claim success on a nonzero exit.
8. Explain how to start: read the installed `AGENTS.md` in a new session or use
   the owner's explicit project link. Offer the snippet; edit an existing
   project's AGENTS only when asked. `.agents/skills` discovery depends on the
   host; manually reading a skill does not prove automatic discovery.

For reconfiguration, read `config/instance.json` first, preserve unspecified
choices and use the original full distribution as the source. The installer
refuses edited managed files; resolve that conflict with the owner. Do not
delete user data or enable new permissions to make a check pass.
