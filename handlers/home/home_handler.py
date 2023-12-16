# coding=utf-8
import tornado.web
from handlers.base.base_handler import BaseHandler


class HomeHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self):
        uid = self.get_secure_cookie("uid")
        username = self.get_secure_cookie("uname")
        self.render('index.html', uid=uid, uname=username)

class OrderListHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self):
        uid = self.get_secure_cookie("uid")
        username = self.get_secure_cookie("uname")
        self.render('index.html', uid=uid, uname=username)

