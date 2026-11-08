# Правила Jarvis / Jarvis contracts

Версия формата установки: **1**. Общая установка обслуживает разные области,
не объединяя их данные и разрешения.

Read only the route needed for the task:

- Before any task read [communication](agent-communication.md), [critical decisions](decisions.md), [documentation hierarchy](documentation.md), [maintenance](maintenance.md) and [browser and temporary server resources](browser-and-servers.md).
- [Структура и владельцы](layout.md): installation, paths, updates.
- [Контекст и приоритет](scopes.md): personal/project routing, conflicts.
- [Память](memory.md): durable facts, corrections, source boundaries.
- [Разрешения и входящие](permissions.md): trust, secrets, packages.
- [Доступы к ресурсам](access.md): select an owner-configured credential profile independently of cwd; no credentials or accounts are bundled.
- [Рабочие обсуждения](discussions.md): dated project/group records, immutable originals and explicit source boundaries.
- [Сопровождение](maintenance.md): updates, sync, recovery.
- [Оригиналы навыков](skills.md): owners, registry and derived discovery.
- [Автоматизации](automations.md): task/state ownership, executor and schedule boundaries.
- For long tasks read [work waves and handoff](long-running-agent-work.md).
- For articles use `modules/writing/SKILL.md` only if the owner selected `writing`; article work alone does not require engineering rules.

When `personal-memory` is enabled, read the short `knowledge/personal/context/active.md`
and only the relevant topic. Follow the configured memory and archive choices:
automatic memory is an explicit owner choice, not a default permission.

`modules/registry.json` is the sole module catalog. A copied guide is not proof
that an external integration works. Never promote `setup-guide` or `planned`
to verified functionality without actual evidence.

## Каталог проектов и ПО

Прочитать [Проекты и группы](projects.md) при выборе проектной области или управлении каталогом. Для schema 2 этот контракт заменяет прежнее требование shared-хранения только локально: действуют storage-привязки карточки. Проектные материалы могут целиком находиться в Jarvis, локально или по разделам.
