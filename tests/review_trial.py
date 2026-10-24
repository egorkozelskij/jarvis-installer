"""Synthetic review trial for the engineering module (opt-in, not unit tests).

A small library passes all 11 tests with and without `candidate.patch`, but the
patch changes the documented disposal order when a neighbour consumer is alive.
Each model reviews the patch twice: in a plain folder and with a Jarvis
instance (engineering preset, project rule CORE-CLEANUP-ORDER-001). The hidden
scenario in `fixtures/review-trial/hidden_scenario.py` is never shown to agents.

    python3 tests/review_trial.py setup --base /absolute/empty/dir
    python3 tests/review_trial.py run --base /absolute/empty/dir --cli /path/to/codex

Requires an authenticated Codex CLI. Read the answers yourself: process success
is not behavioral acceptance.
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
FIXTURE = HERE / 'fixtures/review-trial'
INSTALLER = HERE.parent / 'bootstrap/scripts/jarvis.py'
MODELS = ['gpt-5.6-luna', 'gpt-6-luna', 'gpt-6.1-sol']
CONDITIONS = ['plain', 'jarvis']
PLACEHOLDER = ('None yet. Add rules from `modules/engineering/templates/rule.md` when a real,\n'
               'repeated problem needs one.')


def cli(*args):
    subprocess.run([sys.executable, *map(str, args)], check=True, capture_output=True)


def setup(base, models):
    for cond in CONDITIONS:
        for model in models:
            d = base / cond / model
            d.mkdir(parents=True)
            shutil.copytree(FIXTURE / 'atlas-core', d / 'atlas-core')
            git = ['git', '-C', str(d / 'atlas-core'), '-c', 'user.name=Fixture',
                   '-c', 'user.email=fixture@example.invalid']
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
                cli(d / 'instance/bootstrap/scripts/jarvis.py', 'project', '--root', d / 'instance',
                    '--id', 'atlas', '--title', 'Atlas', '--kind', 'engineering')
                project = d / 'instance/projects/atlas/project.md'
                project.write_text(project.read_text()
                                   .replace('Purpose: to be clarified with owner.', 'Purpose: reactive dependency graph library.')
                                   .replace('Source repository: unbound.', 'Source repository: ../atlas-core (relative to the instance root).'))
                rules = d / 'instance/projects/atlas/governance/README.md'
                text = rules.read_text()
                if PLACEHOLDER not in text:
                    raise ValueError('Unexpected starter rules template')
                rules.write_text(text.replace(PLACEHOLDER, (FIXTURE / 'rule.md').read_text().strip()))


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
    args = parser.parse_args()
    base = args.base.resolve()
    if args.action == 'setup':
        if base.exists() and any(base.iterdir()):
            sys.exit('Base must be a new or empty directory')
        setup(base, args.model or MODELS)
    else:
        if not args.cli:
            sys.exit('--cli is required for run')
        run(base, args.cli, args.model or MODELS)
