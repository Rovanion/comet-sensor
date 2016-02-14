# -*- coding: utf-8 -*-
"""Test the data fetching mechanims."""


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
    # There are 135 new datapoints in the second file, so 866 should be removed.
    assert len(loadOne(glob.glob(TEMP_FOLDER + '*:30:00.csv')[0])) == 135


@register_uris
def test_data_folder_without_trailing_slash(runner, freezer):
    """
    There were issues with fetch due to the data directory not being terminated
    with a slash.
    """
    with runner.isolated_filesystem():
        try:
            os.makedirs('./no_slash')
            freezer.freeze(TEST_O_CLOCK)
            result = runner.invoke(cli, ['-d', './no_slash', 'fetch', FIRST_URL])
            assert result.exit_code == 0
            freezer.delta(minutes=30)
            result2 = runner.invoke(cli, ['-d', './no_slash', 'fetch', SECOND_URL])
            assert result2.exit_code == 0
            assert len(loadOne(glob.glob('./no_slash/*:30:00.csv')[0])) == 135
        finally:
            shutil.rmtree('./no_slash')
