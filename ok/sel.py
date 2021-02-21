import selectors, time

from .hdl import Event, Handler
from .thr import launch
from .utl import get_name

class EDISCONNECT(Exception):

    pass

class Select(Handler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._select = selectors.DefaultSelector()

    def select(self, once=False):
        while not self.stopped:
            try:
                sel = self._select.select(1.0)
            except OSError:
                if once:
                    break
                continue
            for key, mask in sel:
                e = self.poll()
                self.put(e)
                e.wait()
            if once:
                break

    def poll(self):
        e = Event()
        e.txt = time.ctime(time.time())
        return e

    def register_fd(self, fd):
        try:
            fd = fd.fileno()
        except AttributeError:
            fd = fd
        self._select.register(fd, selectors.EVENT_READ|selectors.EVENT_WRITE)
        return fd

    def stop(self):
        self._select.close()
        super().stop()

    def start(self):
        launch(self.select, name="%s.select" % get_name(self), daemon=True)
        super().start()
