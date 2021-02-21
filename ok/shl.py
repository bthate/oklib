import sys

from .obj import Cfg, cfg
from .hdl import Bused, Command
from .prs import parse as p
from .thr import launch

def init(h):
    shl = Shell()
    shl.clone(h)
    shl.start()
    return shl

class Cfg(Cfg):

    pass

class Shell(Bused):

    def direct(self, txt):
        print(txt)

    def poll(self):
        return Command(input("> "))

    def start(self):
        super().start()
        launch(self.input)

def parse():
    c = Cfg()
    p(c, " ".join(sys.argv[1:]))
    cfg.update(c)
    return c
