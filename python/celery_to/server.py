#!/usr/bin/env python
# encoding: utf-8
# pip install celery
# pip install redis
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.gen
import tornado.httpclient

import time
from celery import Celery

import task
import torncelery


from tornado.options import define, options
define("port", default=8001, help="run on the given port", type=int)

time1 = 10


class SleepHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        # tornado.gen.Task的参数是:要执行的函数, 参数
        # res = task.sleep.apply_async(args=[time1])
        res = yield torncelery.async(task.sleep, time1, 'SleepHandler')
        # task.sleep.apply_async(args=[time1])
        print(res)
        # print(res.get())
        # yield res.get()
        self.write("when i sleep %ds. %s" % (time1, res))
        self.finish()


class JustNowHandler(tornado.web.RequestHandler):
    # @tornado.gen.coroutine
    def get(self):
        # yield time.sleep(time1)
        task.sleep.apply_async(args=[time1, 'JustNowHandler'])
        self.write("i hope just now see you")


class LongTimeHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        res = yield torncelery.async(task.celery_do_longtime_task, 999999999)
        # task.celery_do_longtime_task.apply_async(args=[999999999])
        self.write("celery_do_longtime_task is over, ret=%s" % res)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[
            (r"/sleep", SleepHandler),
            (r"/justnow", JustNowHandler),
            (r'/longtime', LongTimeHandler)])

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()