# -*- coding: utf-8 -*-
"""
Seriously, we're testing the test code here. Absolutely ridiculous.
"""
from support import *

def test_freeze(freezer):
    freezer.freeze(TEST_O_CLOCK)
    assert datetime.datetime.now() == TEST_O_CLOCK
    freezer.delta(minutes=2)
    assert datetime.datetime.now() == TEST_O_CLOCK + datetime.timedelta(minutes=2)
