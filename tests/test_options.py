import sys
sys.path.append("..")
import os
from click.testing import CliRunner
from comet.main import cli


DATA_FOLDER = './test-folder/'


def test_data_folder_not_existing():
    runner = CliRunner()
    result = runner.invoke(cli, ['-v', '-d', DATA_FOLDER, 'dump'])
    assert result.exit_code == 2


def test_data_folder_exists():
    runner = CliRunner()
    with runner.isolated_filesystem():
        try:
            os.makedirs(DATA_FOLDER)
            result = runner.invoke(cli, ['-d', DATA_FOLDER, 'dump'])
            assert result.exit_code == 4
            assert result.output == ('No csv files found in '
                                     + DATA_FOLDER + ', nothing to do.\n')

        finally:
            os.removedirs(DATA_FOLDER)
