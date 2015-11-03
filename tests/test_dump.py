import glob
from support import *


@isolated_filesystem
def test_dump_nothing_stored(runner):
    print(runner)
    result = runner.invoke(cli, ['-v', '-d', './', 'dump'])
    assert result.exit_code == 4


@register_uris
@isolated_filesystem
def test_dump_one_data_file(runner, freezer):
    freezer.freeze(TEST_O_CLOCK)
    result = runner.invoke(cli, ['-v', '-d', TEMP_FOLDER, 'fetch', FIRST_URL])
    assert result.exit_code == 0
    freezer.delta(minutes=1)
    result2 = runner.invoke(cli, ['-v', '-d', TEMP_FOLDER, 'fetch', SECOND_URL])
    assert result2.exit_code == 0
    result3 = runner.invoke(cli, ['-v', '-d', TEMP_FOLDER, 'dump', '-o', 'all_data.csv'])
    assert result3.exit_code == 0
    assert len(glob.glob('./all_data.csv')) == 1
