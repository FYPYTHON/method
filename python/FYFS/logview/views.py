from django.shortcuts import render
from logview.models import UserLog
from rest_framework.views import APIView
from rest_framework.response import Response
from django import db
from math import ceil
from common.comfunc import str_to_datetime, datatime_to_str
from common.rep_msg import ResMsg
# Create your views here.
import logging
logger = logging.getLogger('ldfs')


class UserLogView(APIView):

    def get(self, request):
        request_parmas = request.query_params.dict()
        start_time = request_parmas.get("st", None)   # start time
        end_time = request_parmas.get("et", None)     # end time
        content = request_parmas.get("content", "")
        key = request_parmas.get("key", "")
        ip = request_parmas.get("ip", "")
        page = int(request_parmas.get("page", 1))
        # print(start_time, end_time, ip, key, content)

        resp = ResMsg()
        if start_time is not None and end_time is not None:
            start_time = str_to_datetime(start_time)
            end_time = str_to_datetime(end_time)
        else:
            resp.code = 1
            resp.msg = u"时间范围输入错误"
            return Response(data=resp.to_dict())
        offset_start = (page - 1) * 20
        offset_end = page * 20
        data = UserLog.objects.filter(key__contains=content, content__contains=key, ip__contains=ip,
                                      created__gte=start_time, created__lte=end_time).all().order_by('-created'
                                      )[offset_start: offset_end]
        total = data.count()
        result = []
        for item in data:
            log_dict = dict()
            log_dict['user'] = item.user
            log_dict['id'] = item.id
            log_dict['key'] = item.key
            log_dict['content'] = item.content
            log_dict['created'] = datatime_to_str(item.created)
            log_dict['ip'] = item.ip
            result.append(log_dict)
            pass

        db.connections.close_all()
        resp.data = result
        total = ceil(total / 20)
        total = total if total > 0 else 1
        return Response(data={"data": resp.to_dict(), "total": total})

    def post(self, request):
        request_param = request.data
        # print(request_param)
        # print(request.META)
        key = request_param.get('key')
        content = request_param.get('content')
        user = request_param.get('user')
        ip = request.META.get('REMOTE_ADDR')
        resp = ResMsg()
        if not self.add_log(key, content, user, ip):
            resp.code = 1
            resp.msg = u"添加失败"
        else:
            resp.msg = u"添加成功"
        return Response(data=resp.to_dict())

    @classmethod
    def add_log(cls, key, content, user, ip):
        logger.info("post add log data.key:{}.content:{},user:{},ip:{}".format(key, content, user, ip))
        data = UserLog()
        data.key = key
        data.content = content
        data.user = user
        data.ip = ip
        try:
            data.save()
            return True
        except Exception as e:
            logging.error("add log error.{}".format(e))
            return False

