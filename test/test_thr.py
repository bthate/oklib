# OPLIB - Object Programming Library (test_tinder.py)
#
# This file is placed in the Public Domain.

import os, unittest

from op.obj import cfg
from op.thr import launch

from test.run import exec, consume, h

events = []

class Test_Threaded(unittest.TestCase):

    def test_thrs(self):
        thrs = []
        for x in range(cfg.index or 1):
            launch(tests, h)
        consume(events)

def tests(b):
    for cmd in h.cmds:
        events.extend(exec(cmd))
