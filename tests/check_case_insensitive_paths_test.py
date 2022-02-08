import os

import pytest

from pre_commit_hooks.check_case_insensitive_paths import main
from testing.util import get_resource_path


@pytest.mark.parametrize(
    ('filename', 'capitalize', 'expected_retval'),
    (('ok_makefile.makefile', False, 0), ('ok_makefile.makefile', True, 0)),
)
def test_main(capsys, filename, capitalize, expected_retval):
    filename = get_resource_path(filename)
    if capitalize:
        filename = os.path.join(
            os.path.dirname(filename), os.path.basename(filename).upper(),
        )
    ret = main([filename])
    assert ret == expected_retval
    if expected_retval == 1:
        stdout, _ = capsys.readouterr()
        assert str(filename) in stdout
        assert str(filename).lower() in stdout
