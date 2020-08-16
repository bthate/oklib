# OLIB - the object library !
#
# oper

import inspect, olib, os

from olib import Object, cdir, get, save
from ok.hdl import get_kernel

class Log(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""

class Todo(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""

def find_modules(pkgs, skip=None):
    mods = []
    for pkg in pkgs.split(","):
        if skip is not None and skip not in pkg:
            continue
        try:
            p = direct(pkg)
        except ModuleNotFoundError:
            continue
        for key, m in inspect.getmembers(p, inspect.ismodule):
            if m not in mods:
                mods.append(m)
    return mods

def find_shorts(mn):
    shorts = Ol()
    for mod in find_modules(mn):
        for key, o in inspect.getmembers(mod, inspect.isclass):
            if issubclass(o, Object):
                t = "%s.%s" % (o.__module__, o.__name__)
                shorts.append(o.__name__.lower(), t)
    return shorts

def list_files(wd):
    path = os.path.join(wd, "store")
    if not os.path.exists(path):
        return ""
    return "|".join(os.listdir(path))

def cmd(event):
    k = get_kernel()
    event.reply(",".join(k.cmds))

def dne(event):
    if not event.args:
        return
    selector = {"txt": event.args[0]}
    db = Db()
    for o in db.find("__main__.Todo", selector):
        o._deleted = True
        save(o)
        event.reply("ok")
        break

def edt(event):
    if not event.args:
        event.reply(list_files(olib.workdir) or "no files yet")
        return
    cn = event.args[0]
    shorts = find_shorts(__name__)
    if shorts:
        cn = shorts[0]
    db = Db()
    l = db.last(cn)
    if not l:
        try:
            c = get_cls(cn)
            l = c()
            event.reply("created %s" % cn)
        except ENOCLASS:
            event.reply(list_files(olib.workdir) or "no files yet")
            return
    if len(event.args) == 1:
        event.reply(l)
        return
    if len(event.args) == 2:
        setter = {event.args[1]: ""}
    else:
        setter = {event.args[1]: event.args[2]}
    edit(l, setter)
    save(l)
    event.reply("ok")

def fnd(event):
    if not event.args:
        wd = os.path.join(olib.workdir, "store", "")
        cdir(wd)
        fns = os.listdir(wd)
        fns = sorted({x.split(os.sep)[0] for x in fns})
        if fns:
            event.reply("|".join(fns))
        return
    parse(event, event.txt)
    db = Db()
    otype = event.args[0]
    shorts = find_shorts(__name__)
    otypes = get(shorts, otype, [otype,])
    args = list(keys(event.gets))
    try:
        arg = event.args[1:]
    except ValueError:
        arg = []
    args.extend(arg)
    nr = -1
    for otype in otypes:
        for o in db.find(otype, event.gets, event.index, event.timed):
            nr += 1
            if "f" in event.opts:
                pure = False
            else:
                pure = True
            txt = "%s %s" % (str(nr), format(o, args, pure))
            if "t" in event.opts:
                txt += " %s" % (elapsed(time.time() - fntime(o.__stamp__)))
            event.reply(txt)
    if nr == -1:
        event.reply("no matching objects found.")

def krn(event):
    k = get_kernel()
    event.reply(k)

def log(event):
    if not event.rest:
        return
    l = Log()
    l.txt = event.rest
    save(l)
    event.reply("ok")

def tdo(event):
    if not event.rest:
        return
    o = Todo()
    o.txt = event.rest
    save(o)
    event.reply("ok")

def tsk(event):
    psformat = "%-8s %-50s"
    result = []
    for thr in sorted(threading.enumerate(), key=lambda x: x.getName()):
        if str(thr).startswith("<_"):
            continue
        d = vars(thr)
        o = o.Object()
        update(o, d)
        if get(o, "sleep", None):
            up = o.sleep - int(time.time() - o.state.latest)
        else:
            up = int(time.time() - starttime)
        result.append((up, thr.getName(), o))
    nr = -1
    for up, thrname, o in sorted(result, key=lambda x: x[0]):
        nr += 1
        res = "%s %s" % (nr, psformat % (elapsed(up), thrname[:60]))
        if res:
            event.reply(res.rstrip())

def ver(event):
    k = get_kernel()
    event.reply("OSH %s" % __version__)
    for mod in k.walk("mods"):
        try:
            event.reply("%s %s" % (mod.__name__, mod.__version__))
        except AttributeError:
            continue

def wd(event):
    event.reply(olib.workdir)
