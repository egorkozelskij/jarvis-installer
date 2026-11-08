# Jarvis Installer

[Русский](README.md)

A local instruction, memory and project base for an AI agent. Choose modules,
answer a few questions, and let the agent create a dedicated directory. One
owner can use it for personal matters, engineering and design, with separate
contexts and permissions.

**Version 0.4.0 is a local installer.** It is neither a model nor an always-on
service. An attached agent maintains the base during active sessions. Installation
does not change global agent settings, existing projects or connected accounts.

The agent classifies significant memories into thematic sections and maintains
separate current-work topics. `note --section` writes to the chosen section;
omitting it retains the legacy `knowledge/personal/notes/` location. Classification
is performed by the agent under the rules, not by a separate background service.
The project registry stores addresses and
entrypoints; existing projects are not migrated automatically.
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
  projects/<id>/             cards; folder mode also keeps local rules/knowledge
  assets/                    ordinary attachments
  inbox/                     untrusted incoming files, excluded from Git
  local/                     pending changes, correction trail, local secrets
```

Selected text imports or accessible-chat captures create `archive/conversations/` or, for embedded folder projects,
`projects/<id>/archive/`. Schema 2 archives use the resolved assets/conversations section. Legacy records retain their explicit location.
An optional `vault/` requires separately configured encryption; this installer
does not implement it. It generates no fictional biography or unused domain tree.

The distribution has the same six source directories (bootstrap, core, modules,
presets, adapters, templates), plus tests and reports. It contains all module
sources. An installed base contains only selected modules and owner data. Use
the full distribution to add a previously absent module.

## Central and project-local installations

`location_mode` describes instance placement. Schema 2 project/group cards independently choose global, local or per-section storage. Source folders are optional.

```sh
python3 bootstrap/scripts/jarvis.py projects --root /absolute/path/my-jarvis create --id project-a --title "Project A" --kind project --purpose "Project purpose" --storage jarvis
python3 bootstrap/scripts/jarvis.py projects --root /absolute/path/my-jarvis resolve --id project-a --section specs --create
python3 bootstrap/scripts/jarvis.py projects --root /absolute/path/my-jarvis rules --id project-a
```

The card owns parent and storage bindings; project.md provides navigation. Register an existing root before binding local sections. Use move-section for existing data, repair links and finalize the transfer. Missing roots never trigger fallback writes. No root.json is installed. Legacy schema 1 needs an explicit migration. Reading another project does not grant editing permission. Central snapshots do not include external stores.

Snapshots preserve selected file bytes and a checksum manifest. They do not
verify preservation of filesystem metadata, permissions, timestamps, empty
directories or link relationships, or transactional consistency of running
databases. Required metadata, current state and external stores need a
separately configured backup workflow with verified recovery.

Pre-0.3 project records with governance/README.md are retained and locate-project
marks them legacy. Changing location mode with existing projects requires an
explicit migration. Verify skill discovery in a fresh host session; manual
reading is not automatic discovery.

## Memory, archive and search

Memory holds current facts with source and date. Corrections replace the current
record, keeping a local correction trail. “Be brief for this reply” does not change
a general response preference. Explicitly choose `auto` to retain significant
facts, preferences, decisions and current work when the communicating agent
finds justified value for future conversation or work, without repeated save
requests. Each new utterance or completed reply does not itself require a write.
The initial choice remains `on-request`; `off` disables personal note collection.
Permission to maintain memory does not authorize unrelated actions under
`autonomy=ask`. Installation configuration and
technical project decisions are separate from personal memory.

Personal sections include profile, preferences, areas, vectors, events, my-notes,
context and inbox under `knowledge/personal/`. A section is created on first
write. Selecting personal memory seeds an empty `context/active.md` once: a short
index of topics, their state and links. Facts, topic details and history remain
separate. The index is owner data preserved on update and module removal. The
general response style stays in `config/instance.json.communication_style`.

```sh
python3 bootstrap/scripts/jarvis.py note --root /absolute/path/my-jarvis --scope personal --section preferences --id reading-format --kind preference --text "Prefer printed books" --source "Owner, current conversation" --explicit
```

Correct a record using the same scope, section and ID; use `forget` with the
same identity and `--explicit` to remove it. Existing notes are not moved
automatically. The kinds state, event, hypothesis and question distinguish work
state, events and uncertain material from confirmed facts.

Archives preserve source text for later verification, not governing instructions
or necessarily current facts. History has a choice separate from personal memory:
`module_options.history.capture=provided-only` stores supplied texts;
`available-chats` authorizes capture from conversations actually readable through
the current host's tools. Legacy textual history options keep supplied-file
behavior. Input is UTF-8 `.md`/`.txt` up to 2 MiB.

After selecting `available-chats`, save a new exported source chunk with:

```sh
python3 bootstrap/scripts/jarvis.py archive --root /absolute/path/my-jarvis --scope personal --file /absolute/path/chat-chunk.md --source-id codex --chat-id example-chat --date 2026-01-01
```

Sources are stored separately by provider, chat, date and content hash. The agent
selects unprocessed message IDs and maintains coverage/continuation indexes;
the CLI deduplicates identical text chunks, not individual messages. Partial
exports stay marked partial. Installation does not connect accounts, guarantee
account-wide history access or create a background collector. Another chat must
load the same instance entrypoint; global links require separate owner setup.
The communicating agent handles justified memory writes itself; no hourly run
or background all-chat scan is created for this work.

Search is scoped text search, not semantic RAG. Markdown remains the source of
truth; a rebuildable index can be added later. The agent must respect excluded
topics: CLI word checks are not a semantic privacy classifier.

## Engineering work with agents

Core rules cover communication, critical decisions, documentation hierarchy,
knowledge-route maintenance and handoff for long work in the selected scope.
They do not themselves authorize tests, delegation or publication. An optional
experimental `writing` module supports Russian technical articles and editing;
its examples do not define a new owner's voice. Article work does not implicitly
enable engineering rules.

The `engineering` module (requires `projects`) defines how an agent works on
code in a registered project. It first classifies the assignment: explore,
change, review, accept or hand off. Each assignment authorizes only its own
result: exploring does not allow edits, a change does not allow a commit, a
commit does not allow push or release. A project rule has a stable ID, scope,
invariant and evidence path. For non-trivial work the agent writes a task card:
what to improve, which observable behavior to keep and how to check it. Review
gives a verdict per rule with evidence and looks for behavior tests often miss:
cleanup order, error order, resource release. The final report keeps "fixed",
"measured", "consumers checked", "merged" and "released" apart instead of one
word "done".

The `experiments` module covers measurements: a hypothesis mode (about 5
minutes), a final check (about an hour) and extended research only on explicit
request. Correctness is checked before timing, the criterion is set before the
run, inconvenient cells are kept, and repeats need a new reason. "No difference
established" is a valid result. The `engineering` preset selects `projects`,
`search`, `engineering` and `experiments`. Registration uses `projects create` with explicit storage; it creates the card
and navigation, not source rules. Author rules only under an authorized request,
at the address returned by `projects resolve --section rules`. location_mode
never chooses rule storage. The common workflow, spec updates, verification
budgets and commit contract live in modules/engineering/references/.


A queue to dedicated machines for confirming measurements and a coordinator
(`machine-queue`) are planned and not installed.

## Capability status

Canonical IDs, statuses and dependencies: [modules/registry.json](modules/registry.json).

| Capability | Status |
|---|---|
| Installation, module selection, integrity checks | Local commands |
| Memory, corrections, deleting an active record | Local commands and agent rules |
| Thematic records and current-work topics | Local storage; classification and maintenance by the agent |
| Technical writing and editing | Optional experimental module |
| Engineering/design projects and rule hierarchy | Local commands and agent rules |
| Engineering work: assignments, review, acceptance, handoff | Agent rules and templates |
| Measurements and experiments within a budget | Agent rules and templates |
| Search and text archives | Local commands; accessible-chat capture is an opted-in workflow requiring host tools |
| Local snapshots and pending-change queue | Local commands; no network delivery |
| GitLab/GitHub/cloud sync | Separate setup guidance |
| Skill exchange, computer control, secret storage | Optional guides; services unconfigured |
| Machine queue for measurements and coordinator | Planned, not implemented |
| Remote MCP access from other devices | Planned, not implemented |

Installer and legacy CLI operations record pending events; project and skill commands retain current state in cards and registries. No watcher, background push or server runs.
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

## Project and group catalogue

Schema 2 project/group cards share a standard section layout and have one parent. Source folders and section storage are independent. Use `python3 bootstrap/scripts/jarvis.py projects --root ROOT --help`. Storage defaults to the explicitly chosen location, with per-section overrides. Missing roots never cause fallback writes. No root.json is installed. See core/projects.md and modules/projects/SKILL.md. Legacy cards require an explicit migration.

## Skill ownership and automations

`core/skills.md` defines one owner and original per skill.
`config/skill-bindings.json` records sources and derived discovery locations.
Bundled modules use installer-managed copies; owner skills use registered links
through `skills --root ROOT register|update|sync|audit`. The optional
`skill-management` module depends on projects and provides the lifecycle workflow.
Installation changes no home discovery or client settings without authorization.

`doctor` checks managed hashes, project cards, assigned root availability and
registered discovery. It cannot prove rule semantics or model skill selection;
verify discovery in a new client session. Snapshot skips registered derived
links and retains the registry; run `skills --root ROOT sync` after restoring.
External originals and section stores require their own backup.

`core/automations.md` defines portable task/state ownership and one executor
binding, with templates under templates. No empty task tree, service, schedule,
account connection or previous owner's tasks are installed.

`bootstrap/port-manifest.json` records the current Jarvis source contracts and
intentional portable adaptations. Source-instance paths, data, Git permissions
and machine configuration are excluded. Current release validation is in
[the report](reports/2026-11-08-publication/README.md); historical model trials
retain their original coverage.

## Connecting and routing the base

After installation, connect the new base's `AGENTS.md` to the instructions of
the intended client or project. Bootstrap offers the link; existing instructions
change only when requested. A new session must actually load this entrypoint;
installation alone does not provide automatic discovery.

Routers may explicitly import common documents from another owner while
preserving each document's Scope; this does not inherit the owner's entire
profile. `projects rules` lists parent entrypoints and `validate` checks
structure, so the agent still checks the complete effective route separately.
Meeting and work-discussion materials use the selected owner's
`notes/discussions/` and `assets/discussions/` under the
[discussion convention](core/discussions.md). Shared
[browser resource](core/browser-and-servers.md) and [access](core/access.md)
contracts import no other owner's settings or credentials.
