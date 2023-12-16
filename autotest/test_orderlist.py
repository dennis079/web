from tornado.test.util import unittest
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application

from handlers.home.djsvc_handler import FetchOrderListHandler
#TestHandler is the model to be tested

class BaseTest(AsyncHTTPTestCase):
    def setUp(self):
        pass
        super(BaseTest, self).setUp()


class WebHandlerTest(BaseTest):

    def get_app(self):
        return Application([
            ('/fetchorders/', FetchOrderListHandler),
        ])

    def test_sub(self):
        body = ""
        response = self.fetch('/fetchorders/', method='GET', body=body)
        self.assertEqual(response.code, 200)


if __name__ == '__main__':
    unittest.main()
