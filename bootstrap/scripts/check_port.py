#!/usr/bin/env python3
"""Read-only check of an explicitly supplied source Jarvis and the port manifest."""
import argparse
import hashlib
import json
from pathlib import Path


def fingerprint(root, name):
    path = root / name
    if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
        raise ValueError('Invalid port path: ' + name)
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True)
    args = parser.parse_args()
    source = Path(args.source).expanduser().resolve()
    distribution = Path(__file__).resolve().parents[2]
    manifest = json.loads((distribution / 'bootstrap/port-manifest.json').read_text())
    issues = []
    for entry in manifest['files']:
        if fingerprint(source, entry['source']) != entry['source_sha256']:
            issues.append({'path': entry['source'], 'side': 'source', 'reason': 'changed or missing since port'})
        if fingerprint(distribution, entry['destination']) != entry['distribution_sha256']:
            issues.append({'path': entry['destination'], 'side': 'distribution', 'reason': 'changed or missing since port'})
    print(json.dumps({'ok': not issues, 'files': len(manifest['files']), 'issues': issues}, ensure_ascii=False, indent=2))
    return bool(issues)


if __name__ == '__main__':
    raise SystemExit(main())
