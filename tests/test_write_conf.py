# -*- coding: utf-8 -*-
"""
Test the functionality of the write_config subcommand.
"""
import os
import difflib
from support import *
from click.testing import CliRunner
from comet.main import cli

@isolated_filesystem
def test_write_conf(runner):
    original_file = os.path.join(EXISTING_DATA_FOLDER, 'basic_conf.ini')
    new_file = './conf.ini'
    result = runner.invoke(cli, ['-v', '-d', './', 'write_conf', new_file])
    assert result.exit_code == 0
    assert difflib.SequenceMatcher(
        None, open(new_file).readlines(),
        open(original_file).readlines()).ratio() == 1.0
