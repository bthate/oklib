# OLIB - the object library !
#
# handler

import queue, threading, _thread

from olib import Object
from ok.utl import get_exception

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
        try:
            self._result = func(*args)
        except EOFError:
            _thread.interrupt_main()
        except Exception as ex:
            print(get_exception())

    def join(self, timeout=None):
        super().join(timeout)
        return self._result

