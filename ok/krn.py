# OLIB - the object library !
#
# handler

import olib, os, sys, threading, time

from olib import Default, Object, cdir, get_name
from ok.hdl import Handler
from ok.utl import get_exception, launch, spl

def __dir__():
    return ("Cfg", "Kernel", "bus", "get_kernel", "kernels")

class Cfg(Default):

    def __init__(self):
        super().__init__()
        self.users = False

class Kernel(Handler):

    def __init__(self):
        super().__init__()
        self.ready = threading.Event()
        self.stopped = False
        self.cfg = Cfg()
        kernels.append(self)
        bus.add(self)

    def announce(self, txt):
        pass

    def init(self, mns):
        mods = []
        thrs = []
        for mn in spl(mns):
            ms = "okbot.%s" % mn
            try:
                mod = self.load_mod(ms)
            except ModuleNotFoundError:
                ms = "okmods.%s" % mn
                try:
                    mod = self.load_mod(ms)
                except ModuleNotFoundError:
                    try:
                        mod = self.load_mod(mn)
                    except ModuleNotFoundError:
                        print(get_exception())
                        continue
            mods.append(mod)
            func = getattr(mod, "init", None)
            if func:
                thrs.append(launch(func, self, name=get_name(func)))
        for thr in thrs:
            thr.join()
        return mods

    def say(self, channel, txt):
        print(txt)

    def stop(self):
        self.stopped = True
        self.queue.put(None)

    def sysmods(self):
        mods = []
        assert olib.workdir
        sys.path.insert(0, olib.workdir)
        cdir(olib.workdir)
        cdir(os.path.join(olib.workdir, "okmods", ""))
        for fn in os.listdir(os.path.join(olib.workdir, "okmods")):
            if fn.startswith("_") or not fn.endswith(".py"):
                continue
            mn = "okmods.%s" % fn[:-3]
            module = self.load_mod(mn)
            mods.append(module)
        return mods

    def wait(self):
        while not self.stopped:
            time.sleep(60.0)

class Bus(Object):

    objs = []

    def __iter__(self):
        return iter(Bus.objs)

    def add(self, obj):
        Bus.objs.append(obj)

    def announce(self, txt, skip=None):
        for h in self.objs:
            if skip is not None and isinstance(h, skip):
                continue
            if "announce" in dir(h):
                h.announce(txt)

    def dispatch(self, event):
        for b in Bus.objs:
            if repr(b) == event.orig:
                b.dispatch(event)

    def by_orig(self, orig):
        for o in Bus.objs:
            if repr(o) == orig:
                return o

    def by_cls(self, otype, default=None):
        res = []
        for o in Bus.objs:
            if isinstance(o, otype):
                res.append(o)
        return res

    def by_type(self, otype):
        res = []
        for o in Bus.objs:
            if otype.lower() in str(type(o)).lower():
                res.append(o)
        return res

    def say(self, orig, channel, txt):
        for o in Bus.objs:
            if repr(o) == orig:
                o.say(channel, str(txt))

bus = Bus()
kernels = []

def get_kernel():
    if kernels:
        return kernels[0]
