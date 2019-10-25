# coding=utf-8
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from FeiYing.settings import DEBUG
from common.comoncommand import get_lsblk, get_disk_usage, get_mountdisk, psutil_shell_mount_status, \
    pustil_shell_mount_raid, byte_from_str, check_dev_name, get_disk_id, get_slot_from_id, get_disk_size_by_slot, \
    generate_hd_name, psutil_shell_add_disk, psutil_shell_mount_disk, psutil_shell_delete_disk
from common.raid_command import create_raid, delete_raid, get_raid_info_all, get_raid_disks_by_name
from common.rep_msg import ResMsg, APPLY, NOAPPLY
# Create your views here.
import logging
logger = logging.getLogger('ldfs')


class CommonMethodMixin(object):
    def get_service_ip(self, request):
        if 'HTTP_HOST' in request.META:
            ip = request.META.get('HTTP_HOST').split(":")[0]
        else:
            ip = 'localhost'
        return ip

    def get_disk_info(self):
        simple_info = get_lsblk()
        if simple_info is None:
            return None
        return simple_info

    def get_raid_info(self):
        raid_info = get_raid_info_all()

        return raid_info


    def gene_diskdata_resp(self, request, lsblk_info):
        """
        lsblk_info  list
        :param lsblk_info:
        :return:
        """
        resp_data = []
        raid_list = get_raid_info_all()
        for item in lsblk_info:
            if not check_dev_name(item['device_name']):
                continue
            disk_dict = dict()
            disk_id = get_disk_id(item['device_name'])
            disk_dict['id'] = disk_id
            disk_dict['ip'] = self.get_service_ip(request)
            disk_dict['slot'] = item['device_name']
            if not disk_id and DEBUG:
                disk_dict['id'] = item['device_name']
            disk_dict['name'] = generate_hd_name(item['device_name'])
            disk_dict['total_size'] = item['device_size']
            disk_mount = psutil_shell_mount_status(item['device_name'])
            if disk_mount:
                used_info = get_disk_usage(disk_mount)
                if used_info is None:
                    disk_dict['free_size'] = "--"
                else:
                    disk_dict['free_size'] = byte_from_str(used_info['available_size'], 'KB')
                disk_dict['status'] = APPLY
            else:
                disk_dict['free_size'] = item['device_size']
                disk_dict['status'] = NOAPPLY
            raid = pustil_shell_mount_raid(item['device_name'])
            print(raid)
            if raid:
                disk_dict['raid'] = u'已配置'
                for md in raid_list:
                    disks = get_raid_disks_by_name(md['id'])
                    if str(raid) in disks:
                        disk_dict['raid'] = md['type']
            else:
                disk_dict['raid'] = ' --'

            resp_data.append(disk_dict)
        return resp_data

    def gene_raiddata_resp(self, request, raid_info):
        resp_data = []
        for item in raid_info:
            raid_dict = dict()
            raid_dict['id'] = item['id']
            raid_dict['type'] = item['type']
            disks = get_raid_disks_by_name(item['id'])
            raid_dict['disks'] = disks
            resp_data.append(raid_dict)
        return resp_data


class DiskManageView(APIView, CommonMethodMixin):
    """disk manage """
    def get(self, request, format=None):
        disk_info = self.get_disk_info()
        resp = ResMsg()
        if disk_info is None:
            resp.code = 1
            resp.msg = u"获取磁盘信息失败"
            return Response(data=resp.to_dict())

        disk_data = self.gene_diskdata_resp(request, disk_info)
        resp.data = disk_data
        resp.msg = u"查询成功"
        return Response(data=resp.to_dict(), status=status.HTTP_200_OK)

    def post(self, request, format=None):
        print(self.request.data)
        print(request.data)
        request_params = request.data
        disk_id = request_params.get("id", None)
        disk_slot = request_params.get("slot", None)
        print("post params:", disk_id, disk_slot)

        if disk_id:
            return self.add_disk_by_id(disk_id)
        else:
            return self.add_disk_by_slot(disk_slot)

    def delete(self, request, format=None):
        request_params = request.data
        disk_id = request_params.get("id", None)
        disk_slot = request_params.get("slot", None)

        if disk_id and not DEBUG:
            return self.del_disk_by_id(disk_id)
        else:
            return self.del_disk_by_slot(disk_slot)

    def add_disk_by_id(self, disk_id):
        resp = ResMsg()
        slot = get_slot_from_id(disk_id)
        if DEBUG:
            slot = disk_id
        if slot:
            return self.add_disk_by_slot(slot)
        else:
            resp.code = 1
            resp.msg = u"未获取到磁盘ID"
            return Response(data=resp.to_dict(), status=status.HTTP_200_OK)

    def add_disk_by_slot(self, disk_slot):
        resp = ResMsg()
        disk_size = get_disk_size_by_slot(disk_slot)
        if disk_size:
            hd_name = generate_hd_name(disk_slot)
            code, result = psutil_shell_add_disk(disk_slot, hd_name)
            if code == 0:
                resp.msg = u"添加成功"
            else:
                resp.code = 1
                resp.msg = u"添加磁盘失败" + result
                print("add disk error. {}".format(result))
        return Response(data=resp.to_dict(), status=status.HTTP_200_OK)

    def del_disk_by_id(self, disk_id):
        resp = ResMsg()
        slot = get_slot_from_id(disk_id)
        print("del:", disk_id, slot)
        if slot:
            return self.del_disk_by_slot(slot)
        else:
            resp.code = 1
            resp.msg = u"未获取到磁盘ID"
            return Response(data=resp.to_dict(), status=status.HTTP_200_OK)

    def del_disk_by_slot(self, disk_slot):
        print("del:", disk_slot)
        resp = ResMsg()
        disk_size = get_disk_size_by_slot(disk_slot)
        if disk_size:
            hd_name = generate_hd_name(disk_slot)
            code, result = psutil_shell_delete_disk(disk_slot, hd_name)
            print("del", hd_name, disk_size)
            if code == 0:
                resp.msg = u"删除成功"
            else:
                resp.code = 1
                resp.msg = u"删除磁盘失败" + result
                print("add disk error. {}".format(result))
        return Response(data=resp.to_dict(), status=status.HTTP_200_OK)


class RaidManageView(APIView, CommonMethodMixin):
    """raid manage """

    def get(self, request, format=None):
        disk_info = self.get_raid_info()
        resp = ResMsg()
        if disk_info is None:
            resp.code = 1
            resp.msg = u"获取磁盘信息失败"
            return Response(data=resp.to_dict())

        disk_data = self.gene_raiddata_resp(request, disk_info)
        resp.data = disk_data
        resp.msg = u"查询RAID成功"
        return Response(data=resp.to_dict(), status=status.HTTP_200_OK)

    def post(self, request, format=None):
        print(self.request.data)
        print(request.data)
        request_params = request.data
        raid_type = request_params.get('type')  # 'raid0
        raid_disk = request_params.get('disks')  # []
        # print(raid_type, raid_disk)
        raid_type_num = raid_type[4:]
        logger.info("raid type:{}, disk:{}".format(raid_type, raid_disk))
        check_param = True
        disk_num = len(raid_disk)
        if raid_type_num == '0' or raid_type_num == '1':
            if disk_num != 2:
                check_param = False
        if raid_type_num == '5':
            if disk_num != 3:
                check_param = False
        if raid_type_num == '10':
            if disk_num != 4:
                check_param = False
        resp = ResMsg()
        if check_param is False:

            resp.code = 1
            resp.msg = u"磁盘数量不正确"
            return Response(data=resp.to_dict(), status=status.HTTP_200_OK)

        for disk_id in raid_disk:
            disk = get_slot_from_id(disk_id)

            if DEBUG:
                disk = disk_id
            if not disk:
                resp.code = 1
                resp.msg = u"磁盘id={}未找到".format(disk_id)
                return Response(data=resp.to_dict(), status=status.HTTP_200_OK)
            # print("disk_info:", disk_info)
            raid = pustil_shell_mount_raid(disk)
            print('is raid:', raid)
            if raid:
                resp.code = 1
                resp.msg = u"磁盘{}已配置RAID".format(disk)
                return Response(data=resp.to_dict(), status=status.HTTP_200_OK)
            disk_mount = psutil_shell_mount_status(disk)
            if disk_mount:
                resp.code = 1
                resp.msg = u"磁盘{}使用中,不能配置RAID".format(disk)
                return Response(data=resp.to_dict(), status=status.HTTP_200_OK)

        raid_name = "/dev/md"
        for item in raid_disk:
            raid_name += str(ord(item[7]) - ord('a'))
        code, result = create_raid(raid_name, raid_type_num, disk_num, raid_disk)
        if code == 0:
            resp.msg = u"RAID配置成功"
        else:
            resp.code = 1
            resp.msg = u"RAID配置失败" + result
        return Response(data=resp.to_dict(), status=status.HTTP_200_OK)

    def delete(self, request, format=None):
        request_params = request.data
        raid_id = request_params.get("id", None)
        resp = ResMsg()
        if not raid_id:
            resp.code = 1
            resp.msg = u"获取RAID失败"
            return Response(data=resp.to_dict(), status=status.HTTP_200_OK)
        else:
            code, result = delete_raid(raid_id)
            if code == 0:
                resp.msg = u"RAID删除成功"
            else:
                resp.code = 1
                resp.msg = u"RAID:{}删除失败".format(raid_id)
            return Response(data=resp.to_dict(), status=status.HTTP_200_OK)

