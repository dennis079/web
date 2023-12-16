#coding=utf-8


import tornado.escape
from libs.pycket.session import SessionMixin
from libs.db.dbsession import dbSession
from libs.redis_conn.redis_conn import conn
from models.account.account_user_model import YYUser

users = {
    'user': YYUser
}

class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def initialize(self):  #initial connection  db is the instance of mysql  conn is instance of redis
        self.db=dbSession
        self.conn=conn
        self.uid = 0
        self.uname = ""

    def get_current_user(self):  #rewrite if need to use authenticated method
        """get present user"""

        uid = self.get_secure_cookie("uid")
        if not uid:
            self.redirect('/auth/user_login')
            return None

        #user = dbSession.query(YYUser).filter(YYUser.uid == uid).first()
        #if not user:
        #    self.redirect('/auth/user_login')
        #    return None

        #username = self.session.get("uname")
        self.uid = 1#user.uid
        self.uname = 'tester'#user.uname
        self.nickname = 'tester'#user.nickname

        return uid

    def on_finish(self):  #clean date in progress
        self.db.close()


