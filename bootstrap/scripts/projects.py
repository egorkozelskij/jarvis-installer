#!/usr/bin/env python3
"""Project/group catalogue and section storage. No services or filesystem markers."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
import uuid

SECTIONS = ('rules', 'skills', 'specs', 'test-specs', 'notes', 'assets', 'reports', 'software')
ID = re.compile(r'^[a-z][a-z0-9.-]{0,127}$')


def stamp():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2) + '\n'
    fd, tmp = tempfile.mkstemp(prefix='.jarvis-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(text)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


@contextmanager
def locked(root):
    path = root / 'local/projects.lock'
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    try:
        os.write(fd, str(os.getpid()).encode())
        os.close(fd)
        yield
    finally:
        path.unlink()


def identifier(value):
    if not isinstance(value, str) or not ID.fullmatch(value):
        raise ValueError('Invalid stable project/root ID')
    return value


def relative(value):
    p = Path(value)
    if p.is_absolute() or '..' in p.parts:
        raise ValueError('Use a path relative to the registered storage root')
    return p


def card_path(root, pid):
    return root / 'projects' / identifier(pid) / 'project.json'


def cards(root):
    result = {}
    for p in sorted((root / 'projects').glob('*/project.json')):
        c = read(p)
        if c.get('schema_version') == 2:
            if c.get('id') != p.parent.name:
                raise ValueError('Card ID differs from directory: ' + str(p))
            result[c['id']] = c
    return result


def card(root, pid):
    c = read(card_path(root, pid))
    if c.get('schema_version') != 2 or c.get('id') != pid:
        raise ValueError('Legacy/inconsistent card: explicit migration required')
    return c


def roots(root):
    p = root / 'config/project-roots.json'
    return read(p) if p.exists() else {'schema_version': 1, 'roots': {}}


def root_path(root, rid, require=True):
    if rid == 'jarvis':
        return root
    entries = roots(root)['roots']
    if rid not in entries:
        raise ValueError('Unknown storage root: ' + rid)
    p = Path(entries[rid]['path']).expanduser()
    if not p.is_absolute():
        raise ValueError('Storage root must be absolute')
    if require and not p.is_dir():
        raise ValueError('Storage unavailable; repair binding, do not create fallback: ' + str(p))
    return p.resolve()


def address(root, binding, require=True):
    base = root_path(root, binding['root'], require)
    p = (base / relative(binding['path'])).resolve()
    if not p.is_relative_to(base):
        raise ValueError('Resolved address escapes registered root')
    return p


def section_binding(c, name):
    if name not in SECTIONS:
        raise ValueError('Unknown standard section: ' + name)
    storage = c['storage']
    return storage.get('sections', {}).get(name, {
        'root': storage['default']['root'],
        'path': str(relative(storage['default']['path']) / name),
    })


def section(root, c, name):
    return address(root, section_binding(c, name))


def chain(root, pid, catalogue=None):
    catalogue = cards(root) if catalogue is None else catalogue
    result, seen = [], set()
    while pid is not None:
        if pid in seen:
            raise ValueError('Parent cycle: ' + pid)
        if pid not in catalogue:
            raise ValueError('Unknown parent: ' + pid)
        seen.add(pid)
        c = catalogue[pid]
        result.append(c)
        pid = c['parent_id']
    return list(reversed(result))


def validate(root, catalogue=None):
    catalogue = cards(root) if catalogue is None else catalogue
    errors, locations, scope_ids = [], {}, {}
    for pid, c in catalogue.items():
        try:
            identifier(pid)
            if not isinstance(c.get('title'), str) or not c['title'].strip():
                raise ValueError('Non-empty title required')
            if not isinstance(c.get('purpose'), str) or not c['purpose'].strip():
                raise ValueError('Non-empty purpose required')
            unknown = set(c['storage'].get('sections', {})) - set(SECTIONS)
            if unknown:
                raise ValueError('Unknown section overrides: ' + ', '.join(sorted(unknown)))
            scope_id = c.get('scope_id', pid)
            if scope_id in scope_ids:
                raise ValueError('Duplicate historical scope ID: ' + scope_id)
            scope_ids[scope_id] = pid
            if c['kind'] not in ('project', 'group') or c['status'] not in ('active', 'archived'):
                raise ValueError('Invalid kind/status')
            lineage = chain(root, pid, catalogue)
            if c['status'] == 'active' and any(x['status'] != 'active' for x in lineage):
                raise ValueError('Active record below archived parent')
            for name in SECTIONS:
                p = address(root, section_binding(c, name), require=False)
                if p.exists() and not p.is_dir():
                    raise ValueError('Section is not directory: ' + str(p))
                key = str(p)
                if c['status'] == 'active' and key in locations:
                    raise ValueError('Duplicate section owner: ' + key)
                if c['status'] == 'active':
                    locations[key] = (pid, name)
            for b in c.get('sources', []):
                address(root, b, require=False)
        except (ValueError, KeyError, TypeError) as e:
            errors.append({'id': pid, 'error': str(e)})
    return {'ok': not errors, 'projects': len(catalogue), 'errors': errors}


def index(root):
    cs = cards(root)
    lines = ['# Каталог проектов и групп', '', 'Карточки и привязки — источник структуры; названия не заменяют ID.', '',
             '| ID | Тип | Родитель | Название | Статус |', '| --- | --- | --- | --- | --- |']
    for pid, c in sorted(cs.items()):
        lines.append(f"| [{pid}]({pid}/project.md) | {c['kind']} | {c['parent_id'] or '—'} | {c['title'].replace('|', '/')} | {c['status']} |")
    write(root / 'projects/README.md', '\n'.join(lines) + '\n')


def save_card(root, c, event):
    candidate = cards(root)
    candidate[c['id']] = c
    result = validate(root, candidate)
    if not result['ok']:
        raise ValueError(json.dumps(result['errors'], ensure_ascii=False))
    c['updated_at'] = stamp()
    c.setdefault('history', []).append({'at': c['updated_at'], **event})
    write(card_path(root, c['id']), c)
    navigation = card_path(root, c['id']).with_name('project.md')
    if navigation.is_file():
        text = navigation.read_text()
        first, sep, rest = text.partition('\n')
        if first.startswith('# '):
            write(navigation, '# ' + c['title'] + sep + rest)
    index(root)


def hashes(folder):
    result = {}
    if not folder.exists():
        return result
    for p in sorted(folder.rglob('*')):
        if p.is_symlink():
            result[p.relative_to(folder).as_posix()] = 'link:' + os.readlink(p)
        elif p.is_file():
            h = hashlib.sha256()
            with p.open('rb') as f:
                for chunk in iter(lambda: f.read(1024 * 1024), b''):
                    h.update(chunk)
            result[p.relative_to(folder).as_posix()] = h.hexdigest()
    return result


def project_note(root, cfg, a):
    """Legacy note/forget CLI, resolved through the v2 notes section."""
    if 'projects' not in cfg.get('modules', []):
        raise ValueError('Projects module is disabled')
    c = card(root, a.scope.split(':', 1)[1])
    if c['status'] != 'active':
        raise ValueError('Archived project is read-only')
    mode = cfg.get('memory_mode', 'on-request')
    if a.command == 'note' and (mode == 'off' or (mode == 'on-request' and not a.explicit)):
        raise ValueError('Memory policy does not allow this write')
    if getattr(a, 'task_only', False):
        return {'written': False, 'reason': 'Task-local preference'}
    identifier(a.id)
    target = section(root, c, 'notes') / (a.id + '.md')
    if target.is_symlink():
        raise ValueError('Note is a navigation link; edit its canonical owner instead')
    with locked(root):
        if a.command == 'forget':
            if not a.explicit or not target.is_file():
                raise ValueError('Forgetting requires explicit request and existing note')
            target.unlink()
            return {'forgotten': str(target), 'limitation': 'Archives and Git history are separate'}
        text = a.text.strip()
        if not text:
            raise ValueError('Note must not be empty')
        if target.exists():
            old = target.read_text()
            if text in old and a.source in old:
                return {'written': False, 'reason': 'Already recorded', 'path': str(target)}
            trail = root / 'local/corrections' / ('project-' + c['id']) / (a.id + '.jsonl')
            history = trail.read_text() if trail.exists() else ''
            write(trail, history + json.dumps({'replaced_at': stamp(), 'previous': old}, ensure_ascii=False) + '\n')
        text = f'# {a.id}\n\nSource: {a.source}\nKind: {a.kind}\nUpdated: {stamp()}\n\n{text}\n'
        write(target, text)
    return {'written': True, 'path': str(target)}


def move_section(root, c, name, binding, confirm):
    src, dst = section(root, c, name), address(root, binding)
    if src == dst:
        return {'changed': False, 'path': str(src)}
    if src.is_relative_to(dst) or dst.is_relative_to(src):
        raise ValueError('Source/destination overlap')
    result = {'project': c['id'], 'section': name, 'source': str(src), 'destination': str(dst)}
    if not confirm:
        return {**result, 'plan_only': True}
    if dst.exists():
        raise ValueError('Destination exists; explicit merge required')
    if not src.is_dir():
        raise ValueError('Source section does not exist; use bind for an empty/new section')
    before = hashes(src)
    pending = dict(result, phase='copying', started_at=stamp())
    journal = root / 'local/transfers' / (str(uuid.uuid4()) + '.json')
    write(journal, pending)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dst, symlinks=True)
    if before != hashes(dst) or before != hashes(src):
        write(journal, {**pending, 'phase': 'conflict'})
        raise ValueError('Source changed or copy mismatch; source retained, see transfer journal')
    # Links to moved documents must be repaired by the agent before finalization.
    c['storage'].setdefault('sections', {})[name] = binding
    save_card(root, c, {'operation': 'move-section', 'section': name, 'from': str(src), 'to': str(dst)})
    write(journal, {**pending, 'phase': 'bound-source-retained', 'hashes': before})
    return {**result, 'journal': str(journal), 'phase': 'bound-source-retained', 'next': 'Repair incoming links, then finalize-transfer'}


def execute(root, a):
    if a.command == 'software':
        sid = identifier(a.software_id)
        base = section(root, card(root, a.id), 'software') if a.id else root / 'software'
        target = base / sid
        if target.exists():
            raise ValueError('Software already registered; edit its existing card')
        data = {'schema_version': 1, 'id': sid, 'title': a.title, 'owner': a.id or 'instance',
                'origin': a.origin, 'components': {}, 'created_at': stamp()}
        if a.source:
            source = Path(a.source).expanduser().resolve()
            if not source.exists():
                raise ValueError('Software source/install address does not exist')
            data['components']['source' if a.origin == 'developed' else 'install'] = str(source)
        write(target / 'software.json', data)
        write(target / 'README.md', f'# {a.title}\n\nВладелец: {data["owner"]}. Адреса компонентов: [software.json](software.json).\n\nУстановка, запуск и внешние действия выполняются по актуальному поручению пользователя.\n')
        return {'registered': str(target), 'executed': False}
    if a.command == 'list':
        return {'projects': list(cards(root).values())}
    if a.command == 'validate':
        return validate(root)
    if a.command == 'root':
        db = roots(root)
        identifier(a.id)
        if a.id == 'jarvis':
            raise ValueError('Reserved root ID')
        p = Path(a.path).expanduser().resolve()
        if not p.is_dir():
            raise ValueError('Register an existing root, no root.json is created')
        old = db['roots'].get(a.id)
        if old and old['path'] != str(p) and not a.confirm:
            return {'plan_only': True, 'old': old['path'], 'new': str(p)}
        previous = list(old.get('previous_paths', [])) if old else []
        if old and old['path'] != str(p):
            previous.append(old['path'])
        db['roots'][a.id] = {'path': str(p), 'previous_paths': list(dict.fromkeys(previous)), 'updated_at': stamp()}
        write(root / 'config/project-roots.json', db)
        return {'registered': a.id, 'path': str(p)}
    if a.command == 'create':
        pid = identifier(a.id)
        if (root / 'projects' / pid).exists():
            raise ValueError('Project already exists; inspect it instead of duplicating')
        if list((root / 'local/deleted-projects').glob(pid + '-*')):
            raise ValueError('Deleted ID is reserved; restore it instead of reusing')
        if a.storage == 'jarvis':
            default = {'root': 'jarvis', 'path': 'projects/' + pid}
        else:
            if not a.storage_root or a.path is None:
                raise ValueError('Local storage requires --storage-root and --path')
            default = {'root': a.storage_root, 'path': a.path}
        c = {'schema_version': 2, 'id': pid, 'title': a.title, 'kind': a.kind,
             'parent_id': a.parent, 'status': 'active', 'purpose': a.purpose,
             'sources': [], 'storage': {'default': default, 'sections': {}}}
        save_card(root, c, {'operation': 'create', 'storage_choice': a.storage})
        folder = root / 'projects' / pid
        write(folder / 'project.md', f"# {a.title}\n\nID: `{pid}`. Тип и связи указаны в карточке.\n\n{a.purpose}\n\nПривязки: [project.json](project.json). Разделы разрешаются через CLI `resolve`; отсутствие локальной папки не меняет назначение.\n")
        return {'created': pid}
    if a.command == 'match':
        target = Path(a.path).expanduser().resolve()
        candidates = []
        for c in cards(root).values():
            if c['status'] != 'active':
                continue
            for b in c.get('sources', []):
                try:
                    p = address(root, b)
                except ValueError:
                    continue
                if target == p or target.is_relative_to(p):
                    candidates.append({'id': c['id'], 'source': str(p), 'depth': len(p.parts)})
        candidates.sort(key=lambda c: -c['depth'])
        return {'candidates': candidates, 'note': 'Use task context; equally specific matches require clarification'}
    if a.command == 'repair':
        entry = roots(root)['roots'].get(a.id)
        if entry is None:
            raise ValueError('Unknown root')
        old = Path(entry['path'])
        search = [old, *(Path(p) for p in entry.get('previous_paths', []))]
        if old.parent.is_dir():
            search.extend(p for p in old.parent.iterdir() if p.is_dir())
        search.extend(Path(p).expanduser() for p in a.candidate)
        found = []
        for p in dict.fromkeys(search):
            if not p.is_dir():
                continue
            bound = [b['path'] for c in cards(root).values() for b in c.get('sources', []) if b['root'] == a.id]
            if bound and all((p / relative(s)).exists() for s in bound):
                found.append(str(p.resolve()))
        return {'root': a.id, 'old': str(old), 'candidates': sorted(set(found)),
                'updated': False, 'next': 'Inspect identity/Git evidence, then root --confirm; names/remotes alone are insufficient'}
    if a.command == 'finalize-transfer':
        path = Path(a.journal).resolve()
        if not path.is_relative_to(root / 'local/transfers'):
            raise ValueError('Use a transfer journal in this instance')
        j = read(path)
        if j['phase'] != 'bound-source-retained' or not a.confirm:
            raise ValueError('Confirm repaired incoming links and pending transfer')
        c = card(root, j['project'])
        if str(section(root, c, j['section'])) != j['destination']:
            raise ValueError('Binding changed since transfer')
        src, dst = Path(j['source']), Path(j['destination'])
        if hashes(src) != j['hashes'] or hashes(dst) != j['hashes']:
            raise ValueError('Source/destination changed; manual reconciliation required')
        shutil.rmtree(src)
        write(path, {**j, 'phase': 'completed', 'completed_at': stamp()})
        return {'completed': str(path)}
    c = card(root, a.id)
    if a.command == 'show':
        return c
    if a.command == 'resolve':
        p = section(root, c, a.section)
        if a.create:
            if c['status'] != 'active':
                raise ValueError('Archived project is read-only')
            p.mkdir(parents=True, exist_ok=True)
        return {'id': c['id'], 'section': a.section, 'path': str(p), 'exists': p.is_dir()}
    if a.command == 'rules':
        result = []
        for parent in chain(root, c['id']):
            p = section(root, parent, 'rules')
            entry = parent.get('rules_entry', 'README.md')
            result.append({'id': parent['id'], 'entrypoint': str(p / relative(entry)), 'exists': (p / entry).is_file()})
        return {'core': str(root / 'core/README.md'), 'chain': result}
    if a.command == 'update':
        if a.title:
            c['title'] = a.title
        if a.kind:
            c['kind'] = a.kind
        if a.parent is not None:
            c['parent_id'] = None if a.parent == '-' else identifier(a.parent)
        if a.purpose is not None:
            c['purpose'] = a.purpose
        before = [x['id'] for x in chain(root, a.id)]
        proposed = cards(root)
        proposed[c['id']] = c
        after = [x['id'] for x in chain(root, a.id, proposed)]
        if before != after and not a.confirm:
            return {'plan_only': True, 'old_rule_chain': before, 'new_rule_chain': after}
        save_card(root, c, {'operation': 'update', 'old_rule_chain': before, 'new_rule_chain': after})
        return {'updated': c['id']}
    if a.command == 'bind':
        b = {'root': a.storage_root, 'path': a.path}
        dst = address(root, b)
        src = section(root, c, a.section)
        if src != dst and src.exists():
            raise ValueError('Existing section has data; use move-section, not address-only replacement')
        c['storage'].setdefault('sections', {})[a.section] = b
        save_card(root, c, {'operation': 'bind', 'section': a.section, 'destination': str(dst)})
        return {'bound': str(dst)}
    if a.command == 'source':
        b = {'root': a.storage_root, 'path': a.path}
        if a.remove:
            c['sources'] = [x for x in c['sources'] if x != b]
            save_card(root, c, {'operation': 'remove-source', 'binding': b})
            return {'sources': c['sources']}
        if not address(root, b).exists():
            raise ValueError('Source must exist')
        if b not in c['sources']:
            c['sources'].append(b)
        save_card(root, c, {'operation': 'source', 'binding': b})
        return {'sources': c['sources']}
    if a.command == 'move-section':
        return move_section(root, c, a.section, {'root': a.storage_root, 'path': a.path}, a.confirm)
    if a.command == 'move-project':
        default = {'root': a.storage_root, 'path': a.path}
        address(root, default)
        inherited = [n for n in SECTIONS if n not in c['storage'].get('sections', {})]
        plan, bindings = [], {}
        for name in inherited:
            binding = {'root': default['root'], 'path': str(relative(default['path']) / name)}
            src, dst = section(root, c, name), address(root, binding)
            if src != dst and (src.is_relative_to(dst) or dst.is_relative_to(src)):
                raise ValueError('Overlapping section addresses')
            if src != dst and src.exists() and dst.exists():
                raise ValueError('Destination exists; explicit merge required: ' + str(dst))
            bindings[name] = binding
            plan.append({'section': name, 'source': str(src), 'destination': str(dst), 'has_data': src.exists()})
        if not a.confirm:
            return {'plan_only': True, 'sections': plan, 'retained_overrides': list(c['storage'].get('sections', {}))}
        transfers = []
        for item in plan:
            if item['has_data']:
                result = move_section(root, c, item['section'], bindings[item['section']], True)
                if result.get('changed') is not False:
                    transfers.append(result)
        c['storage']['default'] = default
        for name in inherited:
            c['storage'].get('sections', {}).pop(name, None)
        save_card(root, c, {'operation': 'move-project', 'default': default, 'transfer_count': len(transfers)})
        return {'id': c['id'], 'storage_default': default, 'transfers': transfers,
                'next': 'Repair all incoming links and software paths, finalize each transfer journal'}
    if a.command in ('archive', 'restore'):
        c['status'] = 'archived' if a.command == 'archive' else 'active'
        save_card(root, c, {'operation': a.command})
        return {'id': c['id'], 'status': c['status']}
    if a.command == 'delete':
        children = [x['id'] for x in cards(root).values() if x['parent_id'] == c['id']]
        if children:
            raise ValueError('Reparent/delete children first: ' + ', '.join(children))
        if not a.confirm or c['status'] != 'archived':
            raise ValueError('Archive first; permanent deletion requires --confirm')
        for name in SECTIONS:
            p = section(root, c, name)
            if p.exists() and not p.is_relative_to(root / 'projects' / c['id']):
                raise ValueError('External data retained; relocate or explicitly handle it before deleting card')
        tomb = root / 'local/deleted-projects' / (c['id'] + '-' + str(uuid.uuid4()))
        tomb.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(root / 'projects' / c['id']), tomb)
        index(root)
        return {'deleted_from_catalogue': c['id'], 'recovery_copy': str(tomb), 'historical_git_data_removed': False}
    raise ValueError('Unknown command')


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', required=True)
    sub = p.add_subparsers(dest='command', required=True)
    for name in ('list', 'validate'):
        sub.add_parser(name)
    s = sub.add_parser('create')
    s.add_argument('--id', required=True); s.add_argument('--title', required=True)
    s.add_argument('--kind', choices=['project', 'group'], default='project'); s.add_argument('--parent')
    s.add_argument('--purpose', required=True); s.add_argument('--storage', choices=['jarvis', 'local'], required=True)
    s.add_argument('--storage-root'); s.add_argument('--path')
    s = sub.add_parser('root'); s.add_argument('--id', required=True); s.add_argument('--path', required=True); s.add_argument('--confirm', action='store_true')
    s = sub.add_parser('repair'); s.add_argument('--id', required=True); s.add_argument('--candidate', action='append', default=[])
    s = sub.add_parser('match'); s.add_argument('--path', required=True)
    s = sub.add_parser('software'); s.add_argument('--id'); s.add_argument('--software-id', required=True)
    s.add_argument('--title', required=True); s.add_argument('--origin', choices=['installed', 'developed'], required=True); s.add_argument('--source')
    s = sub.add_parser('finalize-transfer'); s.add_argument('--journal', required=True); s.add_argument('--confirm', action='store_true')
    for name in ('show', 'rules', 'update', 'archive', 'restore', 'delete', 'resolve', 'bind', 'source', 'move-section', 'move-project'):
        s = sub.add_parser(name); s.add_argument('--id', required=True)
        if name in ('update', 'delete', 'move-section', 'move-project'):
            s.add_argument('--confirm', action='store_true')
        if name == 'update':
            s.add_argument('--title'); s.add_argument('--kind', choices=['project', 'group']); s.add_argument('--parent'); s.add_argument('--purpose')
        if name in ('resolve', 'bind', 'move-section'):
            s.add_argument('--section', choices=SECTIONS, required=True)
        if name == 'resolve':
            s.add_argument('--create', action='store_true')
        if name in ('bind', 'source', 'move-section', 'move-project'):
            s.add_argument('--storage-root', required=True); s.add_argument('--path', required=True)
        if name == 'source':
            s.add_argument('--remove', action='store_true')
    a = p.parse_args(argv)
    root = Path(a.root).expanduser().resolve()
    try:
        cfg = read(root / 'config/instance.json')
        if 'projects' not in cfg['modules']:
            raise ValueError('Projects module is disabled')
        readonly = a.command in ('list', 'show', 'validate', 'rules', 'match', 'repair') or (a.command == 'resolve' and not a.create)
        if readonly:
            result = execute(root, a)
        else:
            with locked(root):
                result = execute(root, a)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if result.get('ok') is False else 0
    except (ValueError, OSError, KeyError, TypeError) as e:
        print(json.dumps({'error': str(e)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
