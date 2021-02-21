import os, unittest

from ok.obj import cfg

from test.run import exec, h

class Test_Cmd(unittest.TestCase):

    def test_cmds(self):
        for x in range(cfg.index or 1):
            for cmd in h.cmds:
                exec(cmd)

