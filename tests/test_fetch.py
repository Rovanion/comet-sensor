import glob
import time
from support import *
from comet.main import cli
from comet.csvio import loadOne



@isolated_filesystem
@register_uris
def test_fetch_one(runner):
    """Test whether one fetch results in one file."""
    result = runner.invoke(cli, ['-v', '-d', TEMP_FOLDER, 'fetch', FIRST_URL])
    assert result.exit_code == 0
    assert len(glob.glob(TEMP_FOLDER + '*.csv')) == 1


@register_uris
@isolated_filesystem
def test_fetch_twice_on_the_same_minute(runner, freezer):
    """
    Here we want to make sure that the data deduplication of fetch is working all
    right, that no additional file is added if fetch is called within the same minute.
    """
    freezer.freeze(TEST_O_CLOCK)
    result = runner.invoke(cli, ['-v', '-d', TEMP_FOLDER, 'fetch', FIRST_URL])
    assert result.exit_code == 0
    assert len(glob.glob(TEMP_FOLDER + '*.csv')) == 1
    result2 = runner.invoke(cli, ['-v', '-d', TEMP_FOLDER, 'fetch', FIRST_URL])
    assert result2.exit_code == 0
    assert len(glob.glob(TEMP_FOLDER + '*.csv')) == 1


@register_uris
@isolated_filesystem
def test_fetch_twice_separated(runner, freezer):
    """
    Here we want to make sure that the data deduplication of fetch is working all
    right, that no additional file is added if fetch is called within the same minute.
    """
    freezer.freeze(TEST_O_CLOCK)
    result = runner.invoke(cli, ['-v', '-d', TEMP_FOLDER, 'fetch', FIRST_URL])
    assert result.exit_code == 0
    assert len(glob.glob(TEMP_FOLDER + '*.csv')) == 1
    freezer.delta(minutes=30)
    result2 = runner.invoke(cli, ['-v', '-d', TEMP_FOLDER, 'fetch', SECOND_URL])
    assert result2.exit_code == 0
    assert len(glob.glob(TEMP_FOLDER + '*.csv')) == 2
    # There are 134 new datapoints in the second file, so 866 should be removed.
    assert len(loadOne(glob.glob(TEMP_FOLDER + '*:30:00.csv')[0])) == 134
