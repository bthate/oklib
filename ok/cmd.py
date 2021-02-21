from .hdl import Bus

def cmd(event):
    bot = Bus.by_orig(event.orig)
    if bot:
        c = sorted(bot.cmds.keys())
        if c:
            event.reply(",".join(c))
