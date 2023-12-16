#coding=utf-8
import tornado.httpserver
import tornado.web
import tornado.ioloop
import tornado.escape
import asyncio
import sys
from tornado.options import define, options
from config import settings
from handlers.home.home_urls import MyHandlers
#from back_process_thread import MyThreadHandler
import multiprocessing
from multiprocessing.pool import Pool

# set defalt
define("port", default=988, help="run port",type=int)
define("start", default=False, help="start server", type=bool)

define("funds", default=0.3, help="percentage", type=float)#max stcok occupation

if __name__ == "__main__":
    options.parse_command_line()

    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    #if options.start:
    app = tornado.web.Application(handlers=MyHandlers, **settings) #creat app
    http_server = tornado.httpserver.HTTPServer(app) #create server
    http_server.listen(options.port) #listining to server
    print('start server...')
    #http_server.start(num_processes=2)
    #tornado.ioloop.PeriodicCallback(MyThreadHandler.check_backprocess, 1000)

    #tasks = asyncio.create_task(ods.start_fetch())
    #tornado.ioloop.run_until_complete(ods.start_fetch())
    loop = asyncio.get_event_loop()
    #loop.run_until_complete(ods.start_fetch())
    #loop.close()

    tornado.ioloop.IOLoop.instance().start()
    () #start

