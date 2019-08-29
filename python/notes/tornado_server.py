#!/usr/bin/env python
# encoding: utf-8
import os
import json
import time
import hashlib
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.gen
import tornado.httpclient
# import tornado.web.stream_request_body
from tornado.web import stream_request_body
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

from tornado.options import define, options
define("port", default=8001, help="run on the given port", type=int)
dpath = 'upfile'
time1 = 10
MAX_STREAMED_SIZE = 1024 * 1024 * 1024
BASE_DIR = os.path.join(os.path.abspath('.'), dpath)
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


@stream_request_body
class UploadHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(4)

    def _initialize(self):
        self.fpath = ''
        self.mode = 'wb'

    def prepare(self):

        filename = self.get_argument('filename', None)
        self.count = 0
        self.fpath = os.path.join(BASE_DIR, filename)
        self.mode = 'wb'
        print(self.request.method)
        if self.request.method == 'POST':
            smd5 = int(self.get_argument('smd5', '0'))

            if os.path.exists(self.fpath) and smd5 == 0:
                print('remove ...', self.fpath)
                os.remove(self.fpath)
            else:
                print('not exist...', self.fpath, smd5)


    @tornado.gen.coroutine
    def get(self):
        filename = self.get_argument('filename', None)
        print('go get', filename)
        if filename is None:
            return self.write(json.dumps({'msg': 'error', 'len': -1}))
        self.fpath = os.path.join(os.path.join(os.path.abspath('.'), dpath), filename)
        myhash = None
        flen = 0
        if os.path.exists(self.fpath):
            flen = os.path.getsize(self.fpath)
            print("已存在文件大小：", flen, self.fpath)
            if flen > 0:
                myhash = hashlib.md5()
                f = open(self.fpath, 'rb')
                while True:
                    b = f.read(1024)
                    if not b:
                        break
                    myhash.update(b)
                myhash = myhash.hexdigest()
                f.close()

        return self.write(json.dumps({'msg': 'success', 'len': flen, 'fmd5': myhash}))



    @tornado.gen.coroutine
    def post(self):
        print('go post')

        filename = self.get_argument('filename', None)

        if filename is None:
            print('file none')
            return self.write(json.dumps({'msg': 'error', 'count': -1}))

        if self.request.body == b'':
            print('request.body none')
            return self.write(json.dumps({'msg': 'error', 'count': self.count, 'flen': os.path.getsize(self.fpath)}))

        print('post', self.fpath)

        res = yield self.data_received(self.request.body)

        return self.write(json.dumps({'msg': 'success', 'count': self.count, 'flen': os.path.getsize(self.fpath)}))


    @run_on_executor
    def data_received(self, data):
        # print("data:")
        if data is None or data == '':
            return False
        else:
            with open(self.fpath, 'ab') as ff:
                # print(data)
                print(self.fpath, self.count, len(data))
                ff.write(data)
                self.count += 1
        # self.f.write(data)
        # self.count += 1

        return True


if __name__ == "__main__":
    if not os.path.exists(BASE_DIR):
        os.mkdir(BASE_DIR)
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[
            (r"/sleep", SleepHandler),
            # (r"/down/(.*)", UploadHandler),
            (r"/upload", UploadHandler),
    ])

    http_server = tornado.httpserver.HTTPServer(app, max_buffer_size=4 * MAX_STREAMED_SIZE)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

