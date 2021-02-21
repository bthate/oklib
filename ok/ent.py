from .dbs import find
from .obj import Object

class Log(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""

class Todo(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""

def dne(event):
    if not event.args:
        return
    selector = {"txt": event.args[0]}
    for fn, o in find("ok.ent.Todo", selector):
        o._deleted = True
        o.save()
        event.reply("ok")
        break

def log(event):
    if not event.rest:
        return
    l = Log()
    l.txt = event.rest
    l.save()
    event.reply("ok")

def tdo(event):
    if not event.rest:
        return
    o = Todo()
    o.txt = event.rest
    o.save()
    event.reply("ok")
