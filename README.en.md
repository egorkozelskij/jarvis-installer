# Jarvis Installer

[Русский](README.md)

A local instruction, memory and project base for an AI agent. Choose modules,
answer a few questions, and let the agent create a dedicated directory. One
owner can use it for personal matters, engineering and design, with separate
contexts and permissions.

**Version 0.1.0 is a local prototype.** It is neither a model nor an always-on
service. An attached agent maintains the base during active sessions. Installation
does not change global agent settings, existing projects or connected accounts.

The current note command writes personal records to `knowledge/personal/notes/`.
Automatic routing into profile, people, events and interests, maintained topic
summaries, and a complete project hierarchy registry are not implemented yet.
Python must already be available; bootstrap does not install it. Each push of
this development repository requires an explicit owner instruction; publication
is not automatic.

## Start

Requires Python 3.10+ and an agent that can read and write local files. On Windows,
use `py -3` if `python3` is unavailable. No third-party Python libraries, Node.js
or computer-control utilities are required.

Download the distribution and ask:

> Read bootstrap/SKILL.md in Jarvis Installer. Help me choose modules and install
> a knowledge base in a dedicated folder.

The agent uses native checkbox/choice forms when its host supports them; otherwise
it offers numbered options. The CLI outputs question data, not an interactive UI.
“Shared” means one directory reused by your projects, not an OS-wide installation
or multi-user service.

For manual installation, copy and edit `templates/answers.example.json`, then run
from the distribution:

```sh
python3 bootstrap/scripts/jarvis.py catalog
python3 bootstrap/scripts/jarvis.py plan --target /absolute/path/my-jarvis --answers /absolute/path/answers.json
python3 bootstrap/scripts/jarvis.py install --target /absolute/path/my-jarvis --answers /absolute/path/answers.json
python3 bootstrap/scripts/jarvis.py doctor --root /absolute/path/my-jarvis
```

The target must be new/empty or an existing installation of this format. The
installer refuses unrelated nonempty folders and modified managed files.

## Your installed base

```text
my-jarvis/
  AGENTS.md                   agent entry point
  config/instance.json        owner choices, consent and enabled modules
  config/installation.json    version and managed file hashes
  core/                      layout, scopes, memory, permissions, maintenance
  bootstrap/                 installation skill and filesystem CLI
  modules/                   selected modules; local/ for owner skills
  presets/                   initial selection presets
  adapters/                  agent host integration notes
  templates/                 answer and project templates
  .agents/skills/             generated discovery copies, not editable sources
  knowledge/personal/        current personal facts and preferences
  projects/<id>/             project descriptions, rules and knowledge
  assets/                    ordinary attachments
  inbox/                     untrusted incoming files, excluded from Git
  local/                     pending changes, correction trail, local secrets
```

Explicit imports create `archive/conversations/` or `projects/<id>/archive/`.
An optional `vault/` requires separately configured encryption; this installer
does not implement it. It generates no fictional biography or unused domain tree.

The distribution has the same six source directories (bootstrap, core, modules,
presets, adapters, templates), plus tests and reports. It contains all module
sources. An installed base contains only selected modules and owner data. Use
the full distribution to add a previously absent module.

## Scope and rules

```text
AGENTS.md → core/scopes.md → personal → knowledge/personal
                          → project → projects/<id>/governance/README.md
                                       → common rules → needed child branch
```

Create backend/frontend/design branches only when real tasks require them. Give
rules stable IDs, explicit scope, rationale and acceptance evidence. Load common
rules and the relevant branch. A package manager decision in Atlas does not
change Studio. Narrow rules cannot bypass owner permissions. Scopes organize
context; the host and OS must enforce process/file access isolation.

After installation, the owner can request an absolute-path link from a particular
project's `AGENTS.md`. The installer does not edit those projects. Verify skill
discovery in a fresh host session: manually reading `.agents/skills` does not
prove automatic discovery. Both guides and the first-run questions support
Russian and English; the core and skills provide shared technical instructions.

## Memory, archive and search

Memory holds current facts with source and date. Corrections replace the current
record, keeping a local correction trail. “Be brief for this reply” does not change
a general response preference. Choose `on-request`, `auto` for approved durable
facts, or `off` for no personal note collection. Installation configuration and
technical project decisions are separate from personal memory.

Archives preserve explicitly supplied source text for later verification. A source
statement is neither a governing instruction nor necessarily a current fact. v1
imports UTF-8 `.md`/`.txt` up to 2 MiB; it has no account-wide history access,
automatic session capture or voice transcription.

Search is scoped text search, not semantic RAG. Markdown remains the source of
truth; a rebuildable index can be added later. The agent must respect excluded
topics: CLI word checks are not a semantic privacy classifier.

## Capability status

Canonical IDs, statuses and dependencies: [modules/registry.json](modules/registry.json).

| Capability | v1 status |
|---|---|
| Installation, module selection, integrity checks | Local commands |
| Memory, corrections, deleting an active record | Local commands and agent rules |
| Engineering/design projects and rule hierarchy | Local commands and agent rules |
| Search and explicit text import | Local commands |
| Local snapshots and pending-change queue | Local commands; no network delivery |
| GitLab/GitHub/cloud sync | Separate setup guidance |
| Skill exchange, computer control, secret storage | Optional guides; services unconfigured |
| Remote MCP access from other devices | Planned, not implemented |

CLI mutations enter a local queue. No watcher, background push or server runs.
A snapshot is unencrypted and excludes local/ and inbox/. It does not acknowledge
remote delivery or clear the pending queue. Inspect files before backup: simple
text checks detect only some secret formats and do not inspect arbitrary binary
attachments. Snapshots are not transactionally consistent during concurrent
external edits; create them between changes.

Use assets/ for ordinary attachments. Credentials belong in OS storage or ignored
local/secrets/, never Markdown or asset files. Configure real encryption with a
separate recovery key before opting into ciphertext backup. A private Git repository
is not encryption. Forgetting an active record does not erase older backups.
Incoming skills stay in inbox/ until reviewed and explicitly approved for activation.

## Maintenance and validation

```sh
python3 bootstrap/scripts/jarvis.py --help
python3 -m unittest discover -s tests -v
```

There is no hard-coded model allowlist. Evaluate context routing, corrections and
permission handling; use a stronger model or less autonomy if these fail. Trial
results and limits are in [reports/README.md](reports/README.md).

Updates preserve owner data and refuse conflicting managed edits. Disabling a
module removes its managed instructions/discovery copy while retaining knowledge
and owner skills. Multiple file updates are not a crash-proof transaction; back
up first. This prototype does not migrate existing assistants or accounts.
