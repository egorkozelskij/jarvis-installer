#!/usr/bin/env python3
"""Resolve canonical Jarvis skills and reconcile derived discovery links."""
import argparse
import json
import os
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / 'config/skill-bindings.json'
ID = re.compile(r'^[a-z][a-z0-9-]{0,63}$')


def data():
    return json.loads(REGISTRY.read_text()) if REGISTRY.exists() else {'schema_version': 1, 'skills': {}}


def roots():
    path = ROOT / 'config/project-roots.json'
    config = json.loads(path.read_text()) if path.exists() else {'roots': {}}
    return {'jarvis': ROOT, 'home': Path.home(), **{k: Path(v['path']) for k, v in config['roots'].items()}}


def resolve(binding):
    known = roots()
    if binding['root'] not in known:
        raise ValueError('Unknown root: ' + binding['root'])
    rel = Path(binding['path'])
    if rel.is_absolute() or '..' in rel.parts:
        raise ValueError('Use a relative path without ..')
    base = known[binding['root']].resolve()
    if not base.is_dir():
        raise ValueError('Unavailable root: ' + binding['root'])
    path = (base / rel).resolve(strict=False)
    if not path.is_relative_to(base):
        raise ValueError('Path leaves root')
    return path


def link_location(binding):
    known = roots()
    if binding['root'] not in known:
        raise ValueError('Unknown root: ' + binding['root'])
    rel = Path(binding['path'])
    if rel.is_absolute() or '..' in rel.parts:
        raise ValueError('Use a relative path without ..')
    base = known[binding['root']].resolve()
    if not base.is_dir():
        raise ValueError('Unavailable root: ' + binding['root'])
    path = base / rel
    if not path.parent.resolve().is_relative_to(base):
        raise ValueError('Link parent leaves root')
    return path


def check_entry(name, entry):
    if not ID.fullmatch(name):
        raise ValueError('Invalid skill ID: ' + name)
    owner = entry['owner']
    if owner != 'jarvis':
        card = ROOT / 'projects' / owner / 'project.json'
        if not card.is_file():
            raise ValueError('Unknown project/group owner: ' + owner)
    source = resolve(entry['source'])
    if not (source / 'SKILL.md').is_file():
        raise ValueError('Missing original SKILL.md: ' + str(source))
    locations = [link_location(binding) for binding in entry.get('links', [])]
    if len(locations) != len(set(locations)):
        raise ValueError('Repeated discovery location: ' + name)
    return source, locations


def check_unique(skills):
    sources = {}
    links = {}
    for name, entry in skills.items():
        source, locations = check_entry(name, entry)
        if source in sources:
            raise ValueError(f'Shared original: {sources[source]} and {name}: {source}')
        sources[source] = name
        for location in locations:
            if location in links:
                raise ValueError(f'Shared discovery link: {links[location]} and {name}: {location}')
            links[location] = name


def configure(root):
    global ROOT, REGISTRY
    ROOT = Path(root).expanduser().resolve()
    REGISTRY = ROOT / 'config/skill-bindings.json'


def audit():
    doc = data()
    issues = []
    try:
        check_unique(doc['skills'])
    except (KeyError, ValueError, OSError) as exc:
        return {'skills': len(doc.get('skills', {})), 'issues': [str(exc)]}
    for name, entry in sorted(doc['skills'].items()):
        source, locations = check_entry(name, entry)
        for destination in locations:
            if destination == source:
                continue
            if entry.get('discovery') == 'copy':
                def contents(folder):
                    return {str(p.relative_to(folder)): p.read_bytes()
                            for p in folder.rglob('*') if p.is_file()
                            and '__pycache__' not in p.parts and p.suffix != '.pyc'}
                if destination.is_symlink() or not destination.is_dir() or contents(source) != contents(destination):
                    issues.append(name + ': managed discovery copy differs: ' + str(destination))
            elif not destination.is_symlink() or destination.resolve() != source:
                issues.append(name + ': missing or conflicting link: ' + str(destination))
    return {'skills': len(doc['skills']), 'issues': issues}


def _main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', default=str(ROOT))
    sub = parser.add_subparsers(dest='command', required=True)
    for command in ('register', 'update'):
        s = sub.add_parser(command)
        for field in ('id', 'owner', 'source-root', 'source-path'):
            s.add_argument('--' + field, required=True)
        s.add_argument('--link', action='append', default=[], help='ROOT:relative/path; repeat for each discovery location')
    sub.add_parser('sync')
    sub.add_parser('audit')
    args = parser.parse_args(argv)
    configure(args.root)
    from jarvis import config
    config(ROOT)
    if args.command == 'audit':
        return execute(args)
    from jarvis import locked
    with locked(ROOT):
        return execute(args)


def execute(args):
    doc = data()
    if args.command in ('register', 'update'):
        if (args.id in doc['skills']) != (args.command == 'update'):
            raise ValueError('Use update for an existing skill and register for a new skill')
        if args.id in doc['skills'] and doc['skills'][args.id].get('managed_module'):
            raise ValueError('Managed module bindings are maintained by the installer')
        links = []
        for raw in args.link:
            root, separator, path = raw.partition(':')
            if not separator:
                raise ValueError('Link must be ROOT:relative/path')
            links.append({'root': root, 'path': path})
        entry = {'owner': args.owner, 'source': {'root': args.source_root, 'path': args.source_path}, 'links': links}
        updated = {**doc['skills'], args.id: entry}
        check_unique(updated)
        if args.command == 'update':
            previous_source, previous_links = check_entry(args.id, doc['skills'][args.id])
            new_source, new_links = check_entry(args.id, entry)
            for destination in new_links:
                if destination in previous_links:
                    if not destination.is_symlink() or destination.resolve() != previous_source:
                        raise ValueError('Discovery link changed; inspect it before update: ' + str(destination))
                    continue
                if destination == new_source:
                    continue
                if destination.exists() or destination.is_symlink():
                    raise ValueError('New discovery location occupied: ' + str(destination))
            for destination in previous_links:
                if destination not in new_links and (not destination.is_symlink() or destination.resolve() != previous_source):
                    raise ValueError('Old discovery link changed; inspect it before update: ' + str(destination))
            for destination in previous_links:
                if destination not in new_links:
                    destination.unlink()
            for destination in new_links:
                if destination in previous_links and destination.is_symlink() and destination.resolve() == previous_source:
                    destination.unlink()
                    destination.symlink_to(new_source, target_is_directory=True)
            for destination in new_links:
                if destination not in previous_links and destination != new_source:
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    destination.symlink_to(new_source, target_is_directory=True)
        doc['skills'] = updated
        from jarvis import atomic
        atomic(ROOT, 'config/skill-bindings.json', json.dumps(doc, ensure_ascii=False, indent=2) + '\n')
        print(json.dumps({'id': args.id, 'operation': args.command}, ensure_ascii=False))
        return
    check_unique(doc['skills'])
    issues = []
    for name, entry in sorted(doc['skills'].items()):
        if entry.get('managed_module'):
            continue
        try:
            source, locations = check_entry(name, entry)
            for destination in locations:
                if destination == source:
                    continue
                if destination.is_symlink() and destination.resolve() == source:
                    continue
                if destination.exists() or destination.is_symlink():
                    issues.append('Collision: ' + str(destination))
                    continue
                if args.command == 'sync':
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    destination.symlink_to(source, target_is_directory=True)
                else:
                    issues.append('Missing link: ' + str(destination))
        except (KeyError, ValueError) as exc:
            issues.append(name + ': ' + str(exc))
    result = audit()
    result['issues'] = list(dict.fromkeys(issues + result['issues']))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return bool(result['issues'])


def main(argv=None):
    try:
        return _main(argv)
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
