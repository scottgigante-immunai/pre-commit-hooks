import argparse
import os
import pathlib
import subprocess
from typing import Optional
from typing import Sequence


def list_files(filename: str) -> Sequence[str]:
    with subprocess.Popen(
        ['git', 'rev-parse', '--show-toplevel'],
        stdout=subprocess.PIPE,
        cwd=os.path.dirname(filename),
    ) as process:
        stdout, _ = process.communicate()
    git_dir = pathlib.Path(stdout.decode().strip()).resolve()
    return [dir.as_posix() for dir in git_dir.iterdir()]


def check_file(filename: str, file_list: Sequence[str]) -> Optional[str]:
    for other_file in file_list:
        if other_file != filename and other_file.lower() == filename.lower():
            return other_file
    return None


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)
    filenames = [os.path.abspath(filename) for filename in args.filenames]

    file_list = list_files(filenames[0])
    retval = 0
    for filename in filenames:
        match = check_file(filename, file_list)
        if match:
            print(
                f'file {filename} matches file {match} '
                'in case-insensitive filesystems',
            )
            retval = 1
    return retval


if __name__ == '__main__':
    exit(main())
