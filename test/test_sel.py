import unittest

from ok.obj import cfg
from ok.sel import Select

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
