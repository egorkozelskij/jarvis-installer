# Карточка проекта schema 2

Обязательные поля: schema_version=2, id (неизменяем), title, kind=project|group, parent_id (ID или null), status=active|archived, purpose, sources (список {root,path}), storage.default={root,path}, storage.sections (исключения стандартных разделов).

Root jarvis — текущий экземпляр. Другие IDs находятся в config/project-roots.json schema 1, roots: {ID: {path: absolute, previous_paths: [...], updated_at}}. Paths в карточках относительные без '..'; root не создаётся при записи.

Необязательные поля: rules_entry (README.md по умолчанию), history, created_at/updated_at, scope_id/scope_kind/position для сохранённой проекции портала. Источник правил — core/projects.md, этот документ поясняет формат.
