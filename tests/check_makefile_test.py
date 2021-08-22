import pytest

from pre_commit_hooks.check_makefile import fix_file
from pre_commit_hooks.check_makefile import main
from testing.util import get_resource_path


@pytest.mark.parametrize(
    ('filename', 'expected_retval'),
    (
        ('bad_makefile.notmakefile', 1),
        ('fixable_makefile_spaces_not_tabs.notmakefile', 1),
        ('ok_makefile.makefile', 0),
    ),
)
def test_main(tmpdir, capsys, filename, expected_retval):
    temp_file = tmpdir.join('t.makefile')
    with open(get_resource_path(filename)) as in_handle, open(
        temp_file, 'w',
    ) as out_handle:
        out_handle.write(in_handle.read())
    ret = main([str(temp_file)])
    assert ret == expected_retval
    if expected_retval == 1:
        stdout, _ = capsys.readouterr()
        assert str(temp_file) in stdout


@pytest.mark.parametrize(
    ('filename', 'expected_retval'),
    (
        ('bad_makefile.notmakefile', 1),
        ('fixable_makefile_spaces_not_tabs.notmakefile', 1),
        ('fixed_makefile_spaces_not_tabs.makefile', 1),
        ('ok_makefile.makefile', 0),
    ),
)
def test_main_with_targets(tmpdir, capsys, filename, expected_retval):
    temp_file = tmpdir.join('t.makefile')
    with open(get_resource_path(filename)) as in_handle, open(
        temp_file, 'w',
    ) as out_handle:
        out_handle.write(in_handle.read())
    ret = main([str(temp_file), '--target', 'all', '--target', 'baz'])
    assert ret == expected_retval
    if expected_retval == 1:
        stdout, _ = capsys.readouterr()
        assert str(temp_file) in stdout


@pytest.mark.parametrize(
    ('input_filename', 'output_filename', 'expected_retval'),
    (
        (
            'fixable_makefile_spaces_not_tabs.notmakefile',
            'fixed_makefile_spaces_not_tabs.makefile',
            1,
        ),
        ('bad_makefile.notmakefile', 'bad_makefile.notmakefile', 0),
    ),
)
def test_fix_file(tmpdir, input_filename, output_filename, expected_retval):
    temp_file = tmpdir.join('t.makefile')
    with open(get_resource_path(input_filename)) as in_handle, open(
        temp_file, 'w',
    ) as out_handle:
        out_handle.write(in_handle.read())
    with open(get_resource_path(output_filename)) as handle:
        expected_output = handle.read()
    ret = fix_file(temp_file)
    with open(temp_file) as handle:
        output = handle.read()
    assert output == expected_output
    assert ret == expected_retval
