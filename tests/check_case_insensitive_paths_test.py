import os
import tempfile

import pytest

from pre_commit_hooks.check_case_insensitive_paths import main
from testing.util import get_resource_path


def is_fs_case_insensitive(*args):
    # Force case with the prefix
    with tempfile.NamedTemporaryFile(prefix='TmP') as tmp_file:
        return os.path.exists(tmp_file.name.lower())


@pytest.mark.parametrize(
    ('filename', 'capitalize', 'expected_retval'),
    (
        ('ok_makefile.makefile', False, 0),
        ('ok_makefile.makefile', 'basename', 1),
        ('thisfiledoesnot.exist', 'dirname', 1),
    ),
)
@pytest.mark.skipif(is_fs_case_insensitive)
def test_main(capsys, filename, capitalize, expected_retval):
    filename = get_resource_path(filename)
    if capitalize == 'basename':
        filename = os.path.join(
            os.path.dirname(filename), os.path.basename(filename).upper(),
        )
    elif capitalize == 'dirname':
        filename = os.path.join(
            os.path.dirname(filename).upper(), os.path.basename(filename),
        )
    ret = main([filename])
    assert ret == expected_retval
    if expected_retval == 1:
        stdout, _ = capsys.readouterr()
        assert str(filename) in stdout
        assert str(filename).lower() in stdout
