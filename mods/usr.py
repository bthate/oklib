# BOTLIB - the bot library !
#
#

import ob

from olib import Db, Object, get, save

class ENOUSER(Exception):

    pass

class User(Object):

    def __init__(self):
        super().__init__()
        self.user = ""
        self.perms = []

class Users(Db):

    userhosts = Object()

    def allowed(self, origin, perm):
        perm = perm.upper()
        origin = get(self.userhosts, origin, origin)
        user = self.get_user(origin)
        if user:
            if perm in user.perms:
                return True
        return False

    def delete(self, origin, perm):
        for user in self.get_users(origin):
            try:
                user.perms.remove(perm)
                save(user)
                return True
            except ValueError:
                pass

    def get_users(self, origin=""):
        s = {"user": origin}
        return self.find("bot.usr.User", s)

    def get_user(self, origin):
        u = list(self.get_users(origin))
        if u:
            return u[-1]

    def meet(self, origin, perms=None):
        user = self.get_user(origin)
        if user:
            return user
        user = User()
        user.user = origin
        user.perms = ["USER", ]
        save(user)
        return user

    def oper(self, origin):
        user = self.get_user(origin)
        if user:
            return user
        user = User()
        user.user = origin
        user.perms = ["OPER", "USER"]
        save(user)
        return user

    def perm(self, origin, permission):
        user = self.get_user(origin)
        if not user:
            raise ENOUSER(origin)
        if permission.upper() not in user.perms:
            user.perms.append(permission.upper())
            save(user)
        return user

def add(event):
    if not event.args:
        event.reply("add <userhost>")
        return
    from .krn import k
    origin = event.args[0]
    origin = get(k.users.userhosts, origin, origin)
    k.users.meet(origin)
    event.reply("ok")
