import argparse
import os
import pathlib
import subprocess
from functools import lru_cache
from typing import Optional
from typing import Sequence


def git_base_dir(filename: str) -> str:
    with subprocess.Popen(
        ['git', 'rev-parse', '--show-toplevel'],
        stdout=subprocess.PIPE,
        cwd=os.path.dirname(filename),
    ) as process:
        stdout, _ = process.communicate()
    return os.path.abspath(stdout.decode().strip())


def list_files(base_dir: str) -> Sequence[str]:
    return tuple(dir.as_posix() for dir in pathlib.Path(base_dir).iterdir())


@lru_cache(None)
def check_file(
    filename: str,
    file_list: Sequence[str],
    base_dir: str,
) -> Optional[str]:
    assert filename.startswith(base_dir)
    for other_file in file_list:
        # exact file match
        if other_file != filename and other_file.lower() == filename.lower():
            return other_file
    # base case
    if filename == base_dir:
        return None
    # recurse
    return check_file(os.path.dirname(filename), file_list, base_dir)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)
    filenames = [os.path.abspath(filename) for filename in args.filenames]

    base_dir = git_base_dir(filenames[0])
    file_list = list_files(base_dir)
    retval = 0
    for filename in filenames:
        match = check_file(filename, file_list, base_dir)
        if match:
            print(
                f'file {filename} conflicts with file {match} '
                'in case-insensitive filesystems',
            )
            retval = 1
    return retval


if __name__ == '__main__':
    exit(main())
