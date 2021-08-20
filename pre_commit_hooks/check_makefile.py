import argparse
import re
import subprocess
from typing import Optional
from typing import Sequence


def fix_file(filename: str) -> int:
    """Fix formatting of makefiles.

    Currently, all this does is replaces spaces with tabs.
    """
    with open(filename) as handle:
        contents = handle.read()
    pattern = re.compile(r'^  ')
    contents_fixed = '\n'.join(
        pattern.sub('\t', line) for line in contents.split('\n')
    )
    if contents_fixed != contents:
        with open(filename, 'w') as handle:
            handle.write(contents_fixed)
        return 1

    return 0


def parse_makefile(filename: str) -> None:
    process = subprocess.Popen(
        ['make', '-f', filename, '--dry-run'],
        stderr=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
    )
    _, stderr = process.communicate()
    if process.returncode != 0:
        raise ValueError(stderr.decode())


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)

    retval = 0
    for filename in args.filenames:
        changed = fix_file(filename)
        if changed:
            print(f'reformatted {filename}')
            retval = 1
        try:
            parse_makefile(filename)
        except ValueError as exc:
            print(
                f'{filename}: Failed to parse with `make --dry-run`\n({exc})',
            )
            retval = 1
    return retval


if __name__ == '__main__':
    exit(main())
