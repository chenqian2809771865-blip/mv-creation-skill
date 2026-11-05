#!/usr/bin/env python3
"""Copy the bundled character runtime into a new project; optionally install deps."""

import argparse
from pathlib import Path
import shutil
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('target', type=Path)
    parser.add_argument('--demo', action='store_true', help='Connect the original demo scene')
    parser.add_argument('--install', action='store_true', help='Run npm ci after copying')
    args = parser.parse_args()
    source = Path(__file__).resolve().parent.parent / 'assets' / 'painted-character'
    target = args.target.expanduser().resolve()
    if not source.is_dir():
        parser.error(f'Bundled runtime missing: {source}')
    if target.exists() and (not target.is_dir() or any(target.iterdir())):
        parser.error(f'Target must be a new or empty directory: {target}')
    shutil.copytree(source, target, dirs_exist_ok=True)
    if not args.demo:
        html = target / 'studio.html'
        html.write_text(html.read_text(encoding='utf-8').replace(
            '<script src="src/scenes/demo.js"></script>',
            '<!-- Add your own scene scripts here; demo.js is an optional example. -->'
        ), encoding='utf-8')
    for path in ('assets', 'out/check'):
        (target / path).mkdir(parents=True, exist_ok=True)
    if args.install:
        npm = shutil.which('npm')
        if not npm:
            parser.exit(1, f'Project copied to {target}; npm unavailable. Install Node/npm, then run npm ci there.\n')
        subprocess.run([npm, 'ci'], cwd=target, check=True)
    print(f'Project ready: {target}')
    if not args.install:
        print('Next: run npm ci in that directory, then add scenes and render a preview.')


if __name__ == '__main__':
    try:
        main()
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f'Error: {exc}', file=sys.stderr)
        sys.exit(1)
