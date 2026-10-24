"""Run three staged, explicitly requested synthetic agent trials.

Each MODEL directory needs ownership.json and phaseN.txt; contains its own
distribution and instance. Run logs stay there, outside the distribution.
This is an opt-in integration test requiring authenticated Codex CLI access.
It does not run as part of unittest discovery. Human review of files and answers
is required; process success alone is not behavioral acceptance.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess

MODELS = ['gpt-5.6-luna', 'gpt-6-luna', 'gpt-6.1-sol']


def run(base, phase, cli, models):
    def one(model):
        folder = base / model
        marker = json.loads((folder / 'ownership.json').read_text())
        if marker != {'purpose': 'synthetic Jarvis installer trial', 'model': model}:
            raise ValueError('Invalid ownership marker')
        prompt = (folder / f'phase{phase}.txt').read_text()
        command = [cli, 'exec', '--ignore-user-config', '--ignore-rules', '--ephemeral',
                   '--skip-git-repo-check', '-s', 'workspace-write',
                   '-c', 'project_doc_max_bytes=0', '-c', 'model_reasoning_effort="medium"',
                   '-c', 'sandbox_workspace_write.network_access=false',
                   '-c', 'sandbox_workspace_write.exclude_tmpdir_env_var=true',
                   '-c', 'sandbox_workspace_write.exclude_slash_tmp=true',
                   '-c', 'approval_policy="never"',
                   '-m', model, '-C', str(folder), '--json',
                   '-o', str(folder / f'phase{phase}.answer.txt'), '-']
        env = os.environ.copy()
        env.pop('CODEX_THREAD_ID', None)
        try:
            proc = subprocess.run(command, input=prompt, text=True, capture_output=True,
                                  timeout=300, env=env)
            (folder / f'phase{phase}.events.jsonl').write_text(proc.stdout)
            (folder / f'phase{phase}.stderr.txt').write_text(proc.stderr)
            result = dict(model=model, phase=phase, exit_code=proc.returncode)
        except subprocess.TimeoutExpired as exc:
            # subprocess.run kills and waits for the direct child on timeout.
            result = dict(model=model, phase=phase, error='300 second timeout')
            for stream, value in [('events.jsonl',exc.stdout),('stderr.txt',exc.stderr)]:
                (folder / f'phase{phase}.{stream}').write_bytes(value if isinstance(value,bytes) else (value or '').encode())
        (folder / f'phase{phase}.result.json').write_text(json.dumps(result))
        print(json.dumps(result), flush=True)
    with ThreadPoolExecutor(max_workers=3) as pool:
        list(pool.map(one, models))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base',type=Path,required=True)
    parser.add_argument('--phase',type=int,required=True)
    parser.add_argument('--cli',required=True)
    parser.add_argument('--model',choices=MODELS,action='append')
    args = parser.parse_args()
    run(args.base.resolve(),args.phase,args.cli,args.model or MODELS)
