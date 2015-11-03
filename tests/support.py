"""
Support module with shared code repeated in most of the tests.
"""
import os
import sys
import shutil
import codecs
import pytest
import datetime
import httpretty
sys.path.append("..")
from comet.main import cli
from functools import wraps
from click.testing import CliRunner



TEST_O_CLOCK = datetime.datetime(2010, 12, 24, 17, 0, 0)
FIRST_URL = 'http://export'
SECOND_URL = 'http://export.1'
EXISTING_DATA_FOLDER = os.path.join(os.path.dirname(__file__), 'data/')
TEMP_FOLDER = './temp/'


def register_uris(func):
    """
    Set up mock http requests for two pieces of data fetched from a real
    Comet Web Sensor T6540.
    """
    @wraps(func)
    @httpretty.activate
    def inner(*args, **kwargs):
        with codecs.open(os.path.join(EXISTING_DATA_FOLDER,
                                      'export.csv'), encoding='latin1') as data:
            body = data.read()
            httpretty.register_uri(httpretty.GET, FIRST_URL + '/export.csv', body=body)
        with codecs.open(os.path.join(EXISTING_DATA_FOLDER,
                                      'export.csv.1'), encoding='latin1') as data:
            body = data.read()
            httpretty.register_uri(httpretty.GET, SECOND_URL + '/export.csv', body=body)
        return func(*args, **kwargs)
    return inner


def isolated_filesystem(func):
    """
    Creates temporary folders in an isolated filesystem, also passes on a PrintRunner.
    """
    @wraps(func)
    def inner(*args, **kwargs):
        r = runner()
        with r.isolated_filesystem():
            try:
                os.makedirs(TEMP_FOLDER)
                func(*args, **kwargs)
            finally:
                shutil.rmtree(TEMP_FOLDER)
    return inner


@pytest.fixture
def runner():
    class PrintRunner(CliRunner):
        def invoke(self, *args, **kwargs):
            result = super(PrintRunner, self).invoke(*args, **kwargs)
            print(result.output)
            return result
    return PrintRunner()


@pytest.fixture
def freezer(monkeypatch):
    """
    Monkeypatches datetime.datetime.now so that it's a fixed value
    which can be adjusted with the delta function.
    """
    original = datetime.datetime

    class FreezeMeta(type):
        def __instancecheck__(self, instance):
            if type(instance) == original or type(instance) == Freeze:
                return True

    class Freeze(datetime.datetime):
        __metaclass__ = FreezeMeta

        @classmethod
        def freeze(cls, val):
            cls.frozen = val

        @classmethod
        def now(cls):
            return cls.frozen

        @classmethod
        def delta(cls, timedelta=None, **kwargs):
            """ Moves time fwd/bwd by the delta"""
            from datetime import timedelta as td
            if not timedelta:
                timedelta = td(**kwargs)
            cls.frozen += timedelta

    monkeypatch.setattr(datetime, 'datetime', Freeze)
    Freeze.freeze(original.now())
    return Freeze
