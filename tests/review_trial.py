"""Synthetic review trial for the engineering module (opt-in, not unit tests).

A small library passes all tests with and without `candidate.patch`, but the
patch changes the documented disposal order when a neighbour consumer is alive.
Fixture `review-trial` states the contract at the top of the edited file;
`review-trial-hard` keeps it only in `docs/contracts.md` and hides the change
in a larger diff (rename, new `peek()` and its tests).
Each model reviews the patch twice: in a plain folder and with a Jarvis
instance (engineering preset, project rule CORE-CLEANUP-ORDER-001). The hidden
scenario `hidden_scenario.py` in each fixture is never shown to agents.

    python3 tests/review_trial.py setup --base /absolute/empty/dir [--fixture review-trial-hard]
    python3 tests/review_trial.py run --base /absolute/empty/dir --cli /path/to/codex

Requires an authenticated Codex CLI. Read the answers yourself: process success
is not behavioral acceptance. Setup uses the current distribution and schema 2;
historical trial results refer to their recorded source snapshots.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
FIXTURES = ['review-trial', 'review-trial-hard']
INSTALLER = HERE.parent / 'bootstrap/scripts/jarvis.py'
MODELS = ['gpt-5.6-luna', 'gpt-6-luna', 'gpt-6.1-sol']
CONDITIONS = ['plain', 'jarvis']



def cli(*args):
    subprocess.run([sys.executable, *map(str, args)], check=True, capture_output=True)


def setup(base, models, fixture):
    FIXTURE = HERE / 'fixtures' / fixture
    for cond in CONDITIONS:
        for model in models:
            d = base / cond / model
            d.mkdir(parents=True)
            shutil.copytree(FIXTURE / 'atlas-core', d / 'atlas-core')
            git = ['git', '-C', str(d / 'atlas-core'), '-c', 'user.name=Fixture',
                   '-c', 'user.email=fixture@example.invalid', '-c', 'core.hooksPath=/dev/null']
            subprocess.run(['git', 'init', '-q', '-b', 'main', str(d / 'atlas-core')], check=True)
            subprocess.run(git + ['add', '-A'], check=True)
            subprocess.run(git + ['commit', '-qm', 'feat(core): dependency graph with ordered disposal'], check=True)
            shutil.copy(FIXTURE / 'candidate.patch', d / 'candidate.patch')
            shutil.copy(FIXTURE / f'prompt-{cond}.txt', d / 'prompt.txt')
            (d / 'ownership.json').write_text(json.dumps(
                {'purpose': 'synthetic Jarvis review trial', 'model': model, 'condition': cond}))
            if cond == 'jarvis':
                answers = d / 'answers.json'
                answers.write_text(json.dumps(dict(
                    name='Alex Example', language='ru', location_mode='folder', autonomy='ask',
                    modules=['projects', 'search', 'engineering', 'experiments'])))
                cli(INSTALLER, 'install', '--target', d / 'instance', '--answers', answers)
                answers.unlink()
                installed = d / 'instance/bootstrap/scripts/jarvis.py'
                cli(installed, 'projects', '--root', d / 'instance', 'create',
                    '--id', 'atlas', '--title', 'Atlas', '--kind', 'project',
                    '--purpose', 'Synthetic reactive dependency graph library', '--storage', 'jarvis')
                cli(installed, 'projects', '--root', d / 'instance', 'root',
                    '--id', 'trial-source', '--path', d / 'atlas-core')
                cli(installed, 'projects', '--root', d / 'instance', 'source',
                    '--id', 'atlas', '--storage-root', 'trial-source', '--path', '.')
                cli(installed, 'projects', '--root', d / 'instance', 'resolve',
                    '--id', 'atlas', '--section', 'rules', '--create')
                rules = d / 'instance/projects/atlas/rules/README.md'
                rules.write_text('# Atlas rules\n\nRead modules/engineering/SKILL.md from the instance root.\n\n'
                                 + (FIXTURE / 'rule.md').read_text())



def run(base, codex, models):
    def one(job):
        cond, model = job
        d = base / cond / model
        marker = json.loads((d / 'ownership.json').read_text())
        if marker != {'purpose': 'synthetic Jarvis review trial', 'model': model, 'condition': cond}:
            raise ValueError('Invalid ownership marker')
        command = [codex, 'exec', '--ignore-user-config', '--ignore-rules', '--ephemeral',
                   '--skip-git-repo-check', '-s', 'workspace-write',
                   '-c', 'project_doc_max_bytes=0', '-c', 'model_reasoning_effort="medium"',
                   '-c', 'sandbox_workspace_write.network_access=false',
                   '-c', 'sandbox_workspace_write.exclude_tmpdir_env_var=true',
                   '-c', 'sandbox_workspace_write.exclude_slash_tmp=true',
                   '-c', 'approval_policy="never"',
                   '-m', model, '-C', str(d), '--json', '-o', str(d / 'answer.txt'), '-']
        env = os.environ.copy()
        env.pop('CODEX_THREAD_ID', None)
        try:
            proc = subprocess.run(command, input=(d / 'prompt.txt').read_text(), text=True,
                                  capture_output=True, timeout=900, env=env)
            (d / 'events.jsonl').write_text(proc.stdout)
            (d / 'stderr.txt').write_text(proc.stderr)
            result = dict(condition=cond, model=model, exit_code=proc.returncode)
        except subprocess.TimeoutExpired:
            result = dict(condition=cond, model=model, error='900 second timeout')
        (d / 'result.json').write_text(json.dumps(result))
        print(json.dumps(result), flush=True)
    with ThreadPoolExecutor(max_workers=3) as pool:
        list(pool.map(one, [(c, m) for c in CONDITIONS for m in models]))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('action', choices=['setup', 'run'])
    parser.add_argument('--base', type=Path, required=True)
    parser.add_argument('--cli')
    parser.add_argument('--model', choices=MODELS, action='append')
    parser.add_argument('--fixture', choices=FIXTURES, default='review-trial')
    args = parser.parse_args()
    base = args.base.resolve()
    if args.action == 'setup':
        if base.exists() and any(base.iterdir()):
            sys.exit('Base must be a new or empty directory')
        setup(base, args.model or MODELS, args.fixture)
    else:
        if not args.cli:
            sys.exit('--cli is required for run')
        run(base, args.cli, args.model or MODELS)
