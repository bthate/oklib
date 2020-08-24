# OKLIB - the ok library !
#
# console

import atexit, olib, os, readline, sys, termios, time, threading

from olib import Object, update
from ok.hdl import Event
from ok.krn import get_kernel
from ok.prs import parse
from ok.utl import launch

def __dir__():
    return ("Console", "execute", "parse_cli", "starttime")

cmds = []
resume = {}
starttime = time.time()

class Console(Object):

    def __init__(self):
        super().__init__()
        self.ready = threading.Event()

    def announce(self, txt):
        pass

    def input(self):
        k = get_kernel()
        while 1:
            try:
                event = self.poll()
            except EOFError:
                print("")
                continue
            event.orig = repr(self)
            k.queue.put(event)
            event.wait()
        self.ready.set()

    def poll(self):
        e = Event()
        e.speed = "fast"
        e.txt = input("> ")
        return e

    def raw(self, txt):
        print(txt.rstrip())

    def say(self, channel, txt):
        self.raw(txt)

    def start(self):
        k = get_kernel()
        setcompleter(k.cmds)
        launch(self.input)

    def wait(self):
        self.ready.wait()

def complete(text, state):
    matches = []
    if text:
        matches = [s for s in cmds if s and s.startswith(text)]
    else:
        matches = cmds[:]
    try:
        return matches[state]
    except IndexError:
        return None

def execute(main):
    termsave()
    try:
        main()
    except KeyboardInterrupt:
        print("")
    except PermissionError:
        print("you need root permissions.")
    finally:
        termreset()

def get_completer():
    return readline.get_completer()

def parse_cli(name="ok"):
    from ok.krn import Cfg
    cfg = Cfg()
    parse(cfg, " ".join(sys.argv[1:]))
    if cfg.wd:
        p = cfg.wd
    if root():
        p = "/var/lib/%s/" % name
        cfg.root = True
    else:
        p = os.path.expanduser("~/.%s" % name)
        cfg.root = False
    olib.workdir = p
    if len(sys.argv) <= 1:
        c = Cfg()
        parse(c, "")
        return c
    k = get_kernel()
    update(k.cfg, cfg)
    return cfg

def root():
    if os.geteuid() != 0:
        return False
    return True

def setcompleter(commands):
    cmds.extend(commands)
    readline.set_completer(complete)
    readline.parse_and_bind("tab: complete")
    atexit.register(lambda: readline.set_completer(None))

def termsetup(fd):
    return termios.tcgetattr(fd)

def termreset():
    if "old" in resume:
        termios.tcsetattr(resume["fd"], termios.TCSADRAIN, resume["old"])

def termsave():
    try:
        resume["fd"] = sys.stdin.fileno()
        resume["old"] = termsetup(sys.stdin.fileno())
        atexit.register(termreset)
    except termios.error:
        pass

def touch(fname):
    try:
        fd = os.open(fname, os.O_RDWR | os.O_CREAT)
        os.close(fd)
    except (IsADirectoryError, TypeError):
        pass
