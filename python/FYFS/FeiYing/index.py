# coding=utf-8
import os
from django.shortcuts import redirect
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from FeiYing.settings import DEBUG, DJANGO_REST_PATH
from rest_framework.views import APIView
from logview.views import UserLogView
import logging
logger = logging.getLogger('ldfs')

def rest_static(request, filename):
    """
    load js css ttf when use api docs
    :return:
    """
    if DEBUG is False:
        return HttpResponse("must use only in debug mode")
    content_type = filename.split('.')[-1]
    if content_type == 'js':
        content_type = 'application/javascript'
    elif content_type == 'css':
        content_type = 'text/css'
    elif content_type == 'ttf':
        content_type = 'application/x-font-woff'
    else:
        content_type = None
    real_path = os.path.join(DJANGO_REST_PATH, filename)
    if os.path.exists(real_path) and content_type is not None:
        with open(os.path.join(DJANGO_REST_PATH, filename), 'rb') as f:
            js_content = f.read()
        return HttpResponse(content=js_content,
                            content_type=content_type)
    else:
        return HttpResponse("not found %s" % request.path)


class Index(APIView):
    def get(self, request, format=None):
        """visit index page"""
        return redirect('/ldfs/static/index.html')


class LogRecodeMidware(MiddlewareMixin):

    def process_request(self, request):
        if request.method not in ['get', 'GET']:
            ip = request.META.get('REMOTE_ADDR')
            user = 'admin'
            key = request.path.split('/')[-1]
            content = request.path
            try:
                UserLogView.add_log(key, content, user, ip)
            except Exception as e:
                print(e)
                logger.error("add user log error: {}".format(e))

    # def process_response(self, request, response):
    #     return response

    # def process_view(self, request, callback, callback_args, callback_kwargs):
    # pass
    # print("中间件 process view")