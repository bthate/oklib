from op.hdl import Command, Test
from op.itr import walk
from op.obj import cfg

from test.prm import param

events = []

def consume(elems):
    fixed = []
    res = []
    for e in elems:
        r = e.wait()
        res.append(r)
        fixed.append(e)
    for f in fixed:
        try:
            elems.remove(f)
        except ValueError:
            continue
    return res

def exec(cmd):
    exs = param.get(cmd, [""])
    e = list(exs)
    events = []
    nr = 0
    for ex in e:
        nr += 1
        txt = cmd + " " + ex
        e = Command(txt)
        h.put(e)
        events.append(e)
    return events

h = Test()
h.walk("mod,ok")
h.start()

for e in exec("rss https://www.reddit.com/r/python/.rss"):
    e.wait()
