from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from math import ceil
from common.gfs_command import gfs_pool_list, gfs_volume_all, gfs_peer_probe, gfs_peer_detach, gfs_volume_info, \
    gfs_volume_start, gfs_volume_stop
from common.rep_msg import ResMsg
# Create your views here.


class GfsStateView(APIView):
    def get(self, request):
        data = gfs_pool_list()
        total = len(data)
        total = ceil(total / 20)
        total = total if total > 0 else 1
        total = total if total > 0 else 1
        return Response(data={"data": data, "total": total})

    def post(self, request):
        request_data = request.data
        hostname = request_data.get('hostname',None)
        print(request_data)
        print("add peer:", hostname)

        resp = ResMsg()
        code, result = gfs_peer_probe(hostname)
        if code:
            resp.msg = u"添加成功"
        else:
            resp.code = 1
            resp.msg = u"添加失败," + result
        return Response(data=resp.to_dict())

    def delete(self, request):
        request_data = request.data
        hostname = request_data.get('hostname', None)
        print(hostname)

        resp = ResMsg()
        code, result = gfs_peer_detach(hostname)
        if code:
            resp.msg = u"删除成功"
        else:
            resp.code = 1
            resp.msg = u"删除失败," + result
        return Response(data=resp.to_dict())


class GfsVolumeView(APIView):
    def get(self, request):
        request_parmas = request.query_params.dict()
        # gvol = request_parmas.get("gvol", 'all')  # start time

        vol_list = gfs_volume_all()
        total = len(vol_list)
        total = ceil(total / 20)
        total = total if total > 0 else 1
        total = total if total > 0 else 1

        data = []
        for vol in vol_list:
            vol_info = gfs_volume_info(vol)
            data.append(vol_info)

        return Response(data={"data": data, "total": total})

    def post(self, request):
        "gluster volume remove-brick gvol replica 2 gfs-224:/opt/gfs/bk3 gfs-223:/opt/gfs/bk3 force"
        request_data = request.data
        volname = request_data.get("volname", None)
        stripe = request_data.get("stripe", 0)
        replica = request_data.get("replica", 0)
        bricks = request_data.get("bricks", [])
        print(request_data)
        print("volname:", volname, replica, stripe)
        print("brikcs:", bricks)
        resp = ResMsg()
        resp.data = bricks
        return Response(data=resp.to_dict())

    def delete(self, request):
        request_data = request.data
        vol = request_data.get('volname', None)
        resp = ResMsg()
        if vol is None:
            resp.code = 1
            resp.msg = u"卷获取失败，卷名为空"
        else:
            code, result = gfs_volume_stop(vol)
            print("delete vol : code:{}, {}".format(code, result))
            if code:
                resp.msg = u"停用成功"
            else:
                resp.code = 1
                resp.msg = result
        return Response(data=resp.to_dict())

    def put(self, request):
        request_data = request.data
        vol = request_data.get('volname', None)
        print("put ", vol)
        resp = ResMsg()
        if vol is None:
            resp.code = 1
            resp.msg = u"卷获取失败，卷名为空"
        else:
            code, result = gfs_volume_start(vol)
            if code:
                resp.msg = u"启用成功"
            else:
                resp.code = 1
                resp.msg = result

        return Response(data=resp.to_dict())

