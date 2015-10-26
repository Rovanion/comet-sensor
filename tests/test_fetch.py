import sys
sys.path.append("..")
import os
import glob
import time
import shutil
import codecs
import httpretty
from click.testing import CliRunner
from comet.main import cli
from comet.csvio import loadOne

FIRST_URL = 'http://export'
SECOND_URL = 'http://export.1'
DATA_FOLDER = os.path.join(os.path.dirname(__file__), 'data/')
TEMP_FOLDER = './temp/'


@httpretty.activate
def test_fetch_one():
    """Test whether one fetch results in one file."""
    with codecs.open(os.path.join(DATA_FOLDER, 'export.csv'), encoding='latin1') as f:
        body = f.read()
        httpretty.register_uri(httpretty.GET, FIRST_URL + '/export.csv', body=body)
    runner = CliRunner()
    with runner.isolated_filesystem():
        try:
            os.makedirs(TEMP_FOLDER)
            result = runner.invoke(cli, ['-v', '-d', TEMP_FOLDER, 'fetch', FIRST_URL])
            assert result.exit_code == 0
            assert len(glob.glob(TEMP_FOLDER + '*.csv')) == 1
        except AssertionError:
            print(result.output)
            raise
        finally:
            shutil.rmtree(TEMP_FOLDER)


@httpretty.activate
def test_fetch_twice_on_the_same_minute():
    """
    Here we want to make sure that the data deduplication of fetch is working all
    right, that no additional file is added if fetch is called within the same minute.
    """
    with codecs.open(os.path.join(DATA_FOLDER, 'export.csv'), encoding='latin1') as f:
        body = f.read()
        httpretty.register_uri(httpretty.GET, FIRST_URL + '/export.csv', body=body)
    runner = CliRunner()
    with runner.isolated_filesystem():
        try:
            os.makedirs(TEMP_FOLDER)
            result = runner.invoke(cli, ['-v', '-d', TEMP_FOLDER, 'fetch', FIRST_URL])
            assert result.exit_code == 0
            assert len(glob.glob(TEMP_FOLDER + '*.csv')) == 1
            result2 = runner.invoke(cli, ['-v', '-d', TEMP_FOLDER, 'fetch', FIRST_URL])
            assert result2.exit_code == 0
            assert len(glob.glob(TEMP_FOLDER + '*.csv')) == 1
        except AssertionError:
            print(result.output)
            raise
        finally:
            shutil.rmtree(TEMP_FOLDER)


@httpretty.activate
def test_fetch_twice_separated():
    """
    Here we want to make sure that the data deduplication of fetch is working all
    right, that no additional file is added if fetch is called within the same minute.
    """
    with codecs.open(os.path.join(DATA_FOLDER, 'export.csv'), encoding='latin1') as f:
        body = f.read()
        httpretty.register_uri(httpretty.GET, FIRST_URL + '/export.csv', body=body)
    with codecs.open(os.path.join(DATA_FOLDER, 'export.csv.1'), encoding='latin1') as f:
        body = f.read()
        httpretty.register_uri(httpretty.GET, SECOND_URL + '/export.csv', body=body)
    runner = CliRunner()
    with runner.isolated_filesystem():
        try:
            os.makedirs(TEMP_FOLDER)
            result = runner.invoke(cli, ['-v', '-d', TEMP_FOLDER, 'fetch', FIRST_URL])
            assert result.exit_code == 0
            assert len(glob.glob(TEMP_FOLDER + '*.csv')) == 1
            time.sleep(1)
            result2 = runner.invoke(cli, ['-v', '-d', TEMP_FOLDER, 'fetch', SECOND_URL])
            assert result2.exit_code == 0
            assert len(glob.glob(TEMP_FOLDER + '*.csv')) == 2
            # There are 134 new datapoints in the second file, so 866 should be removed.
            assert len(loadOne(glob.glob(TEMP_FOLDER + '*.csv')[1])) == 134
        except AssertionError:
            print(result.output)
            raise
        finally:
            shutil.rmtree(TEMP_FOLDER)
