import sys
sys.path.append("..")
import os
import glob
import shutil
from click.testing import CliRunner
from comet.main import cli


URL = 'http://212.111.6.29'
DATA_FOLDER = './data/'


def test_fetch_one():
    """Test whether one fetch results in one file."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        try:
            os.makedirs(DATA_FOLDER)
            result = runner.invoke(cli, ['-v', '-d', DATA_FOLDER, 'fetch', URL])
            assert result.exit_code == 0
            assert len(glob.glob(DATA_FOLDER + '*.csv')) == 1
        finally:
            shutil.rmtree(DATA_FOLDER)


def test_fetch_twice_on_the_same_minute():
    """
    Here we want to make sure that the data deduplication of fetch is working all
    right, that no additional file is added if fetch is called within the same minute.
    """
    runner = CliRunner()
    with runner.isolated_filesystem():
        try:
            os.makedirs(DATA_FOLDER)
            result = runner.invoke(cli, ['-v', '-d', DATA_FOLDER, 'fetch', URL])
            assert result.exit_code == 0
            assert len(glob.glob(DATA_FOLDER + '*.csv')) == 1
            result2 = runner.invoke(cli, ['-v', '-d', DATA_FOLDER, 'fetch', URL])
            assert result2.exit_code == 0
            assert len(glob.glob(DATA_FOLDER + '*.csv')) == 1
        finally:
            shutil.rmtree(DATA_FOLDER)
