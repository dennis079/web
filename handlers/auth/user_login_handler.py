# coding=utf-8
import tornado.web
from handlers.base.base_handler import BaseHandler

from libs.db.dbsession import dbSession
from models.account.account_user_model import YYUser

class LoginHandler(BaseHandler):
    def get(self):
        self.write('<html><body><form action="/auth/user_login" method="post">'
                   'Name: <input type="text" name="name">'
                   '<input type="submit" value="Sign in">'
                   '</form></body></html>')
        #self.render('auth/login.html')

    def post(self):
        login_user = self.get_argument("name")
        user = dbSession.query(YYUser).filter(YYUser.uname == login_user).first()
        if not user:
            self.redirect('/auth/register')

        # check is password is correct
        self.set_secure_cookie("uid", str(user.uid), expires_days=1000, path="/")
        self.set_secure_cookie("uname", user.uname, expires_days=1000, path="/")
        self.set_secure_cookie("nickname", user.nickname, expires_days=1000, path="/")

        self.session.set("uid", user.uid)
        self.session.set("uname", user.uname)
        self.session.set("nickname", user.nickname)

        nexturl = self.get_argument('next', '/')
        self.redirect(nexturl)