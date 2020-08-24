# OLIB - the object library !
#
# handler

import importlib, importlib.util, os, queue, threading, _thread

from olib import Default, Object, locked, update
from ok.utl import direct, find_cmds, launch, get_exception

def __dir__():
    return ("Event", "Handler")

dispatchlock = _thread.allocate_lock()

class Event(Default):

    def __init__(self):
        super().__init__()
        self.ready = threading.Event()
        self.result = []
        self.thrs = []
        self.txt = ""

    def parse(self):
        args = self.txt.split()
        if args:
            self.cmd = args[0]
        if len(args) >= 2:
            self.args = args[1:]
            self.rest = " ".join(args[1:])

    def reply(self, txt):
        if not self.result:
            self.result = []
        self.result.append(txt)

    def show(self):
        for txt in self.result:
            print(txt)

    def wait(self):
        self.ready.wait()
        res = []
        for thr in self.thrs:
            res.append(thr.join())
        return res

class Handler(Object):

    def __init__(self):
        super().__init__()
        self.cmds = Object()
        self.queue = queue.Queue()
        self.speed = "fast"
        self.stopped = False

    def cmd(self, txt):
        e = Event()
        e.txt = txt
        self.dispatch(e)
        return e

    @locked(dispatchlock)
    def dispatch(self, e):
        e.parse()
        if e.cmd in self.cmds:
            try:
                self.cmds[e.cmd](e)
            except Exception as ex:
                print(get_exception())
        e.show()
        e.ready.set()

    def handler(self):
        while not self.stopped:
            event = self.queue.get()
            if not event:
                break
            if not event.orig:
                event.orig = repr(self)
            event.speed = self.speed
            launch(self.dispatch, event)

    def load_mod(self, name):
        mod = direct(name)
        self.scan(mod)
        return mod

    def scan(self, mod):
        cmds = find_cmds(mod)
        update(self.cmds, cmds)

    def start(self):
        launch(self.handler)

    def stop(self):
        self.stopped = True
        self.queue.put(None)

    def walk(self, name):
        mods = []
        spec = importlib.util.find_spec(name)
        if not spec:
            return mods
        pkg = importlib.util.module_from_spec(spec)
        pn = pkg.__path__[0]
        for fn in os.listdir(pn):
            if fn.startswith("_") or not fn.endswith(".py"):
                continue
            mn = "%s.%s" % (name, fn[:-3])
            module = self.load_mod(mn)
            mods.append(module)
        return mods
