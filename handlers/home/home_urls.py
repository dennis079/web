from handlers.home.home_handler import HomeHandler
from handlers.home.home_handler import OrderListHandler
from handlers.auth.user_login_handler import LoginHandler
from handlers.home.djsvc_handler import FetchInfoHandler
from handlers.home.djsvc_handler import FetchOrderListHandler
from handlers.home.djsvc_handler import AddOrderHandler

MyHandlers = [
    (r'/', HomeHandler),

    # 股票管理网页访问通道
    # stock management visite path
    (r"/orderlist/?", OrderListHandler),
    (r"/fetchinfo/?", FetchInfoHandler),
    (r"/fetchorders/?", FetchOrderListHandler),
    (r"/addorder/([^/?&]*)/([^/?&]*)/([^/?&]*)/([^/?&]*)/([^/?&]*)/([^/?&]*)/??", AddOrderHandler),

    (r'/auth/user_login/?', LoginHandler)
]
