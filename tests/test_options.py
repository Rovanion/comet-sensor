# -*- coding: utf-8 -*-
"""Test the configuration management part of the program."""


from support import *
from comet.main import cli


@isolated_filesystem
def test_data_folder_not_existing(runner):
    result = runner.invoke(cli, ['-v', '-d', 'doesnt_exist', 'dump'])
    assert result.exit_code == 2
    assert result.output == ('Usage: cli [OPTIONS] COMMAND [ARGS]...\n\n'
                             + 'Error: Invalid value for "-d" / "--data-folder"'
                             + ': Path "doesnt_exist" does not exist.\n')


@isolated_filesystem
def test_data_folder_exists(runner):
    result = runner.invoke(cli, ['-d', TEMP_FOLDER, 'dump'])
    assert result.exit_code == 4
    assert result.output == ('No csv files found in '
                             + TEMP_FOLDER + ', nothing to do.\n')
