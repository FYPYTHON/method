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
from tornado.web import stream_request_body
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

from tornado.options import define, options
define("port", default=8081, help="run on the given port", type=int)
dpath = 'upfile'
time1 = 10
buf_size = 4096
MAX_SINGLE = 1024 * 1024 * 10
MAX_STREAMED_SIZE = 1024 * 1024 * 1024
BASE_DIR = os.path.join(os.path.abspath('.'), dpath)


class TestHandler(tornado.web.RequestHandler):
    def get(self):
        print("go test", self.request.remote_ip)
        return self.write("test ok %s" % self.request.request_time())


class DownloadHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(4)

    @tornado.gen.coroutine
    def get(self):
        filename = self.get_argument('filename', None)
        smd5 = self.get_argument('smd5', '0')
        fsize = int(self.get_argument('fsize', '0'))   # 客户端文件大小

        fpath = os.path.join(BASE_DIR, filename)
        print(fpath)
        gsize = os.path.getsize(fpath)

        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=' + filename)
        self.set_header('Gsize', gsize)
        self.set_header('Dmode', '0')

        if not os.path.exists(fpath):
            return self.write(json.dumps({'msg': 'error download file not exist.', 'code': 1}))
        else:
            if fsize > gsize:
                return self.write(json.dumps({'msg': 'file exist but size less than client.', 'code': 0}))

        yield self.read_data(fpath, fsize, smd5)
        self.finish()


    @run_on_executor
    def read_data(self, fpath, flen, smd5):
        with open(fpath, 'rb') as f:

            myhash = hashlib.md5()
            current_read = 0
            while current_read < flen:
                if current_read + 4096 < flen:
                    check_data = f.read(4096)
                else:
                    check_data = f.read(flen - current_read)
                myhash.update(check_data)
                current_read += 4096

            if myhash.hexdigest() != smd5 or flen == 0:
                self.set_header('Dmode', '0')
            else:
                self.set_header('Dmode', '1')
            print('the same ? ', myhash.hexdigest(), smd5, myhash.hexdigest() == smd5)
        self.write(json.dumps({"msg": "success", "code": 0}))

    @tornado.gen.coroutine
    def post(self):
        filename = self.get_argument('filename', None)
        brange = int(self.get_argument('brange', '0'))
        fpath = os.path.join(BASE_DIR, filename)
        print(fpath)
        if not os.path.exists(fpath):
            return self.write(json.dumps({'msg': 'error download', 'count': -1}))
        print(brange)

        yield self.send_data(fpath, brange)
        self.finish()

    @run_on_executor
    def send_data(self, fpath, pos):
        with open(fpath, 'rb') as f:
            f.seek(pos)
            has_read = 0
            while has_read < MAX_SINGLE:
                data = f.read(4096)
                if not data:
                    return
                self.write(data)
                has_read += 4096


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
                print(self.fpath, self.count, len(data))
                ff.write(data)
                self.count += 1
        return True


if __name__ == "__main__":
    if not os.path.exists(BASE_DIR):
        os.mkdir(BASE_DIR)
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[
            (r"/test", TestHandler),
            (r"/upload", UploadHandler),
            (r"/download", DownloadHandler),
    ])

    http_server = tornado.httpserver.HTTPServer(app, max_buffer_size=4 * MAX_STREAMED_SIZE)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

