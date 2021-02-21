# This file is placed in the Public Domain.

import unittest

from op.obj import cfg
from op.sel import Select

from test.run import exec

class Test_Select(unittest.TestCase):

    def test_sel(self):
        for x in range(cfg.index or 1):
            tests(t)

def tests(t):
    for cmd in t.cmds:
        exec(t, cmd)

t = Select()
t.start()
