# BOTLIB - the bot library !
#
#

import threading, time

from olib import Object
from .hdl import get_kernel

def __dir__():
    return ("Repeater", "Timer")

k = get_kernel()

class Timer(Object):

    def __init__(self, sleep, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.sleep = sleep
        self.args = args
        self.name = kwargs.get("name", "")
        self.kwargs = kwargs
        self.state = Object()
        self.timer = None

    def run(self, *args, **kwargs):
        self.state.latest = time.time()
        k.launch(self.func, *self.args, **self.kwargs)

    def start(self):
        if not self.name:
            self.name = self.func.__name__
        timer = threading.Timer(self.sleep, self.run, self.args, self.kwargs)
        timer.setName(self.name)
        timer.setDaemon(True)
        timer.sleep = self.sleep
        timer.state = self.state
        timer.state.starttime = time.time()
        timer.state.latest = time.time()
        timer.func = self.func
        timer.start()
        self.timer = timer
        return timer

    def stop(self):
        if self.timer:
            self.timer.cancel()

class Repeater(Timer):

    def run(self, *args, **kwargs):
        thr = launch(self.start)
        super().run(*args, **kwargs)
        return thr
