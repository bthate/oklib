#!/usr/bin/python3 -u
# OLIB - the object library !
#
# handler

import importlib, importlib.util, inspect, os, queue, sys, threading, traceback

from olib import Default, Object, update

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

class Cfg(Default):

    def __init__(self):
        super().__init__()
        self.users = False

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
        self.names = Object()
        self.queue = queue.Queue()
        self.speed = "fast"
        self.stopped = False

    def cmd(self, txt):
        e = Event()
        e.txt = txt
        self.dispatch(e)
        return e

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
            self.dispatch(event)

    def load_mod(self, name):
        mod = direct(name)
        self.scan(mod)
        return mod

    def scan(self, mod):
        cmds = find_cmds(mod)
        update(self.cmds, cmds)

    def start(self):
        k = get_kernel()
        k.launch(self.handler)

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

class Task(threading.Thread):

    def __init__(self, func, *args, name="noname", daemon=True):
        super().__init__(None, self.run, name, (), {}, daemon=daemon)
        self._name = name
        self._result = None
        self._queue = queue.Queue()
        self._queue.put((func, args))
        self.sleep = None
        self.state = Object()

    def __iter__(self):
        return self

    def __next__(self):
        for k in dir(self):
            yield k

    def run(self):
        func, args = self._queue.get()
        self.setName(self._name)
        self._result = func(*args)

    def join(self, timeout=None):
        super().join(timeout)
        return self._result

class Kernel(Handler):

    def __init__(self):
        super().__init__()
        self.ready = threading.Event()
        self.stopped = False
        self.cfg = Cfg()
        self.bus = Bus()
        self.bus.add(self)
        kernels.append(self)

    def announce(self, txt):
        pass

    def launch(self, func, *args, **kwargs):
        name = kwargs.get("name", func.__name__)
        t = Task(func, *args, name=name, daemon=True)
        t.start()
        return t

    def init(self, mns):
        mods = []
        thrs = []
        for mn in spl(mns):
            ms = "mods.%s" % mn
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
                thrs.append(self.launch(func, self))
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
        cdir(os.path.join(olib.workdir, "mods", ""))
        for fn in os.listdir(os.path.join(olib.workdir, "mods")):
            if fn.startswith("_") or not fn.endswith(".py"):
                continue
            mn = "mods.%s" % fn[:-3]
            module = self.load_mod(mn)
            mods.append(module)
        return mods

    def wait(self):
        while not self.stopped:
            time.sleep(60.0)

def direct(name):
    return importlib.import_module(name)

def find_cmds(mod):
    cmds = {}
    for key, o in inspect.getmembers(mod, inspect.isfunction):
        if "event" in o.__code__.co_varnames:
            if o.__code__.co_argcount == 1:
                cmds[key] = o
    return cmds

def get_exception(txt="", sep=" "):
    exctype, excvalue, tb = sys.exc_info()
    trace = traceback.extract_tb(tb)
    result = []
    for elem in trace:
        fname = elem[0]
        linenr = elem[1]
        func = elem[2]
        if fname.endswith(".py"):
            plugfile = fname[:-3].split(os.sep)
        else:
            plugfile = fname.split(os.sep)
        mod = []
        for element in plugfile[::-1]:
            mod.append(element)
            if "o" in element:
                break
        ownname = ".".join(mod[::-1])
        if "o" not in ownname:
            continue
        result.append("%s:%s" % (ownname, linenr))
    res = "%s %s: %s %s" % (sep.join(result), exctype, excvalue, str(txt))
    del trace
    return res

def spl(txt):
    return iter([x for x in txt.split(",") if x])

kernels = []

def get_kernel():
    if kernels:
        return kernels[0]
