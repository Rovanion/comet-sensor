"""
Test the functionality of the write_config subcommand.
"""
import sys
sys.path.append("..")
import os
import difflib
from click.testing import CliRunner
from comet.main import cli


def test_write_conf():
    original_file = os.path.join(os.path.dirname(__file__), 'data/basic_conf.ini')
    new_file = './conf.ini'
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ['-v', '-d', './', 'write_conf', new_file])
        assert result.exit_code == 0
        assert difflib.SequenceMatcher(
            None, open(new_file).readlines(),
            open(original_file).readlines()).ratio() == 1.0
