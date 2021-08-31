import argparse
import os
import re
import subprocess
from typing import List
from typing import Optional
from typing import Sequence


def fix_file(filename: str) -> int:
    """Fix formatting of makefiles.

    Currently, all this does is replaces leading spaces with tabs.
    """
    with open(filename) as handle:
        contents = handle.read()
    pattern = re.compile(r'^ +')
    contents_fixed = '\n'.join(
        pattern.sub('\t', line) for line in contents.split('\n')
    )
    if contents_fixed != contents:
        with open(filename, 'w') as handle:
            handle.write(contents_fixed)
        return 1

    return 0


def parse_makefile(filename: str, targets: Optional[List[str]]) -> None:
    filename = os.path.abspath(filename)
    workdir = os.path.dirname(filename)
    args = ['make', '-f', filename, '--dry-run']
    if targets:
        args.extend(targets)
    process = subprocess.Popen(
        args, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL, cwd=workdir,
    )
    _, stderr = process.communicate()
    if process.returncode != 0:
        raise ValueError(stderr.decode())


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    parser.add_argument(
        '--target', action='append', help='Make targets to check.',
    )
    args = parser.parse_args(argv)

    retval = 0
    for filename in args.filenames:
        changed = fix_file(filename)
        if changed:
            print(f'reformatted {filename}')
            retval = 1
        try:
            parse_makefile(filename, targets=args.target)
        except ValueError as exc:
            print(
                f'{filename}: Failed to parse with `make --dry-run`\n({exc})',
            )
            retval = 1
    return retval


if __name__ == '__main__':
    exit(main())
