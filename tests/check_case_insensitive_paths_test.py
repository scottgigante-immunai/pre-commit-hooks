import contextlib
import os
import tempfile

import pytest

from pre_commit_hooks.check_case_insensitive_paths import main
from testing.util import get_resource_path


def is_fs_case_insensitive():
    # Force case with the prefix
    with tempfile.NamedTemporaryFile(
        dir=os.path.abspath('.'), prefix='TmP',
    ) as tmp_file:
        return os.path.exists(tmp_file.name.lower())


@contextlib.contextmanager
def create_tempdir(dirname):
    if os.path.exists(dirname):
        yield
        return
    os.mkdir(dirname)
    try:
        yield
    finally:
        os.rmdir(dirname)


@contextlib.contextmanager
def create_tempfile(filename):
    if os.path.exists(filename):
        yield
        return

    with create_tempdir(os.path.dirname(filename)):
        with open(filename, 'w') as handle:
            handle.write('\n')
        try:
            yield
        finally:
            os.unlink(filename)


@pytest.mark.parametrize(
    ('filename', 'capitalize', 'expected_retval'),
    (
        ('case_sensitive/goodfile.txt', False, 0),
        ('case_sensitive/goodfile.txt', 'basename', 1),
        ('case_sensitive/goodfile.txt', 'dirname', 1),
    ),
)
def test_main(capsys, filename, capitalize, expected_retval):
    pytest.mark.skipif(is_fs_case_insensitive())
    filename = get_resource_path(filename)
    if capitalize == 'basename':
        filename = os.path.join(
            os.path.dirname(filename), os.path.basename(filename).upper(),
        )
    elif capitalize == 'dirname':
        dirname = os.path.dirname(filename)
        filename = os.path.join(
            os.path.dirname(dirname),
            os.path.basename(dirname).upper(),
            os.path.basename(filename),
        )

    print(filename)
    with create_tempfile(filename):
        ret = main([filename])
    assert ret == expected_retval
    if expected_retval == 1:
        stdout, _ = capsys.readouterr()
        assert str(filename) in stdout
        assert str(filename).lower() in stdout
