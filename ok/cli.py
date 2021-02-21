import os, shutil

from .dbs import last
from .obj import Object, cfg, edit, format, save
from .prs import parse

def cpy(event):
    md = os.path.join(cfg.wd, "mod")
    if not os.path.exists(md):
        os.mkdir(md)
    fns = []
    nr = 0
    p = os.path.join(os.getcwd(), "mod")
    if not os.path.exists(p):
        event.reply("%s does not exist" % p)
        return
    for fn in os.listdir(p):
        if not fn.endswith("py"):
            continue
        fns.append(fn)
    for fn in fns:
        fnn = os.path.join(md, fn)
        shutil.copy2("mod/%s" % fn, fnn)
        nr += 1
    event.reply("%s copied to %s" % (nr, p))

def set(event):
    if not event.otxt:
        event.reply(format(cfg))
        return
    last(cfg)
    p = Object()
    parse(p, event.rest)
    edit(cfg, p)
    save(cfg)
    event.reply("ok")
