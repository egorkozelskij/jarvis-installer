# Jarvis Installer

Read `core/README.md` before changing the installer. This is an independent local
project. Do not import instructions, accounts, histories or permissions from a
different user's assistant. Do not modify global agent configuration.

Source of truth: `modules/registry.json` for capabilities, `core/` for contracts,
and `bootstrap/scripts/jarvis.py` for local filesystem operations. Keep Russian
and English user guides consistent. Existing user data belongs to the instance,
not to the distribution. Tests use synthetic data in disposable directories.

No commit, push, deployment, real-account setup or migration unless requested.

Publishing this development repository requires an explicit owner instruction
for each push. Do not push automatically after implementation, documentation
updates or knowledge maintenance. Public release commits use
`chore(release): v<SemVer>`, matching `VERSION` in `bootstrap/scripts/jarvis.py`.
Source publication does not imply permission to create release tags, GitHub
Releases, registry packages or deployments.
