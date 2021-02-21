import urllib

from .clk import Repeater
from .dbs import all, find, last, last_match
from .obj import Cfg, Default, Object, cfg
from .hdl import Bus
from .thr import launch
from .utl import get_tinyurl, get_url, strip_html, unescape

from urllib.error import HTTPError, URLError

try:
    import feedparser
    gotparser = True
except ModuleNotFoundError:
    gotparser = False

def init(hdl):
    f = Fetcher()
    return launch(f.start)

class Cfg(Cfg):

    def __init__(self):
        super().__init__()
        self.dosave = True

class Feed(Default):

    pass

class Rss(Object):

    def __init__(self):
        super().__init__()
        self.rss = ""

class Seen(Object):

    def __init__(self):
        super().__init__()
        self.urls = []

class Fetcher(Object):

    cfg = Cfg()
    seen = Seen()

    def display(self, o):
        result = ""
        dl = []
        try:
            dl = o.display_list.split(",")
        except AttributeError:
            pass
        if not dl:
            dl = self.cfg.display_list.split(",")
        if not dl or not dl[0]:
            dl = ["title", "link"]
        for key in dl:
            if not key:
                continue
            data = get(o, key, None)
            if not data:
                continue
            if key == "link" and self.cfg.tinyurl:
                datatmp = get_tinyurl(data)
                if datatmp:
                    data = datatmp[0]
            data = data.replace("\n", " ")
            data = strip_html(data.rstrip())
            data = unescape(data)
            result += data.rstrip()
            result += " - "
        return result[:-2].rstrip()

    def fetch(self, rssobj):
        counter = 0
        objs = []
        if not rssobj.rss:
            return 0
        for o in reversed(list(get_feed(rssobj.rss))):
            if not o:
                continue
            f = Feed()
            f.update(rssobj)
            f.update(Object(o))
            u = urllib.parse.urlparse(f.link)
            if u.path and not u.path == "/":
                url = "%s://%s/%s" % (u.scheme, u.netloc, u.path)
            else:
                url = f.link
            if url in Fetcher.seen.urls:
                continue
            Fetcher.seen.urls.append(url)
            counter += 1
            objs.append(f)
            if self.cfg.dosave:
                f.save()
        if objs:
            Fetcher.seen.save()
        for o in objs:
            txt = self.display(o)
            Bus.announce(txt)
        return counter

    def run(self):
        thrs = []
        for fn, o in all("ok.rss.Rss"):
            #d = Default(o)
            thrs.append(launch(self.fetch, o))
        return thrs

    def start(self, repeat=True):
        last(Fetcher.cfg)
        last(Fetcher.seen)
        if repeat:
            repeater = Repeater(300.0, self.run)
            repeater.start()

    def stop(self):
        self.seen.save()

def get_feed(url):
    if cfg.debug:
        return [Object(), Object()]
    try:
        result = get_url(url)
    except (HTTPError, URLError):
        return [Object(), Object()]
    if gotparser:
        result = feedparser.parse(result.data)
        if "entries" in result:
            for entry in result["entries"]:
                yield entry
    else:
        return [Object(), Object()]

def dpl(event):
    if len(event.args) < 2:
        return
    setter = {"display_list": event.args[1]}
    for fn, o in last_match("ok.rss.Rss", {"rss": event.args[0]}):
        o.edit(setter)
        o.save()
        event.reply("ok")

def ftc(event):
    res = []
    thrs = []
    fetcher = Fetcher()
    fetcher.start(False)
    thrs = fetcher.run()
    for thr in thrs:
        res.append(thr.join() or 0)
    if res:
        event.reply("fetched %s" % ",".join([str(x) for x in res]))
        return

def rem(event):
    if not event.args:
        return
    selector = {"rss": event.args[0]}
    nr = 0
    got = []
    for fn, o in find("ok.rss.Rss", selector):
        nr += 1
        o._deleted = True
        got.append(o)
    for o in got:
        o.save()
    event.reply("ok")

def rss(event):
    if not event.args:
        return
    url = event.args[0]
    res = list(find("ok.rss.Rss", {"rss": url}))
    if res:
        return
    o = Rss()
    o.rss = event.args[0]
    o.save()
    event.reply("ok")
