# coding=utf-8
"""
Time  : 2019/3/9 9:01
Author: wangguoqiang@kedacom.com

"""
import logging
import subprocess
from threading import Timer
import psutil
import re
import os
DN = 3
SPACE_TOPPATH = "/opt/data/region"
TIMEOUT = 60
EXE_PATH = '.' + os.getcwd()
DISK_TYPE = ['part', 'disk']
ROOT_DISK = '/dev/sda'
logger = logging.getLogger('ldfs')


def psutil_shell(arg, timeout):
    # print('arg:', arg)
    if arg != 'cat /etc/redhat-release':
        logger.info("psutil shell cmd:{}".format(arg))
    child = psutil.Popen(arg, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    timer = Timer(timeout, lambda process: process.kill(), [child])
    try:
        timer.start()
        stdout, stderr = child.communicate()
        return_code = child.returncode
        # print('stdout:', stdout)
        # print('stderr:', stderr, '\n', stderr.decode(chardet.detect(stderr)['encoding']))
        if 0 != return_code:
            logger.error("cmd:%s.error code is %d, output is %s", arg, return_code, stderr)
            return return_code, stderr.decode('utf-8')
        else:
            return return_code, stdout.decode('utf-8')
    finally:
        timer.cancel()


def bytes2human(n):
    """
    2199023255552 byte --> 2.0T
    :param n: memory size transfer to pretty
    :return:
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n


def str2num_disk_size(disk_size_str):
    """
    smallest unit is  M,all size transfer to M show in web page
    :param disk_size_str: eg:'100G'
    :return: eg:100 * 1024
    """
    disk_size = 0
    symbol = ('M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    if isinstance(disk_size_str, str):
        level = disk_size_str[-1]
        if level in symbol:
            index = symbol.index(level)
            disk_size = int(disk_size_str[0:-1]) * (1 << index * 10)
    return disk_size


def byte_from_str(size, unit):
    """
    :param size: 3.6
    :param unit: T / TB
    :return:
    """
    unit = unit.upper()
    try:
        size = float(size)
    except:
        size = float(size[:-1])
    if unit == 'T' or unit == 'TB':
        return size * 1024 * 1024 * 1024 * 1024
    elif unit == 'G' or unit == "GB":
        return size * 1024 * 1024 * 1024
    elif unit == 'M' or unit == "MB":
        return size * 1024 * 1024
    elif unit == 'K' or unit == "KB":
        return size * 1024
    else:
        return size


def unifrom_size(size, unit, flag=0):
    unit = unit.upper()
    size = float(size)
    if unit == 'T' or unit == 'TB':
        size = (size)
    if unit == 'G' or unit == "GB":
        size = (size) / 1024
    if unit == 'M' or unit == "MB":
        size = (size) / 1024 / 1024
    if unit == "K" or unit == "KB":
        size = (size) / 1024 / 1024 / 1024
    if unit == "B" or unit == "Byte":
        size = (size) / 1024 / 1024 /1024 /1024
    size = round(size, DN)
    if flag == 0:
        return size
    else:
        return str(size) + 'TB'

def disk_to_mountname(disk_name):
    """
    /dev/sdb --> /dev/sdb1
    :param disk_name:
    :return:
    """
    return disk_name + '1'

def disk_to_hdname(disk_name):
    """
    /dev/sdb --> B
    :param disk_name:
    :return:
    """
    return disk_name[-1].upper()

def get_mountdisk():
    """
    mount -l | grep /dev/sd
    :return:
    """
    result = psutil_shell('mount -l', TIMEOUT)
    logger.info("get mount disk. result:{}".format(result))
    if result is None:
        return None
    device_list = list()
    for res in result.split('\n'):
        device_dict = dict()
        devices = res.split(' ')
        if len(devices) > 2:
            device_dict['device'] = devices[0]
            device_dict['mount'] = devices[2]
            device_list.append(device_dict)
    return device_list


def get_lsblk():
    """
    lsblk -lpb | grep disk
    lsblk -pbo NAME,SIZE,TYPE | grep disk   #select item to output
    :p fullpath b:byte o:output list
    :return:
    """
    cmd = 'lsblk -pbo NAME,SIZE,TYPE,UUID | grep disk'
    code, result = psutil_shell(cmd, TIMEOUT)
    if code != 0:
        return None
    blk_list = list()
    for blk_info in result.split('\n'):
        # print(blk_info)
        if blk_info.startswith('NAME'):
            continue
        blk_dict = dict()
        info_list = list(filter(None, blk_info.split(' ')))
        if len(info_list) < 3:
            continue
        if info_list[0] != ROOT_DISK:
            blk_dict['device_name'] = info_list[0]
            # blk_dict['type'] = info_list[2]
            blk_dict['device_size'] = info_list[1]
            blk_list.append(blk_dict)
    # import operator
    # blk_list_sorted = sorted(blk_list, key=operator.itemgetter('device'))  # blk list sort
    blk_list_sorted = sorted(blk_list, key=lambda x: x['device_name'])
    return blk_list_sorted


def check_dev_name(dev_name):

    rer = r'/dev/sd[a-z]'
    pattern = re.compile(rer, re.IGNORECASE)
    disks = pattern.findall(dev_name)
    if len(disks) > 0:
        return True
    else:
        return False


def get_disk_id(disk_name):
    """
    ls -l /dev/disk/by-id | grep sda | awk 'NR==1{print $9,$11}'
    :return:
    """
    # output:name uuid
    disk_suff = disk_name[5:8]
    cmd = "ls -l /dev/disk/by-id | grep %s | awk 'NR==1{print $9}'" % disk_suff
    code, result = psutil_shell(cmd, TIMEOUT)
    if code == 0:
        if result == '':
            return False
        return result
    else:
        return False


def get_disk_size_by_slot(disk_slot):
    cmd = "lsblk -pbo SIZE,NAME | grep %s | awk '{print $1}'" % disk_slot
    code, result = psutil_shell(cmd, TIMEOUT)
    if code == 0:
        if result == '':
            return False
        return result
    else:
        return False


def get_slot_from_id(disk_id):
    """
    ls -l /dev/disk/by-id | grep K7HBUPAL
    ls -l /dev/disk/by-id | grep K7HBUPAL | awk '{print $11}'
    :param sn: K7HBUPAL
    :return:
    """
    cmd = "ls -l /dev/disk/by-id | grep %s | awk '{print $11}'" % disk_id
    code, result = psutil_shell(cmd, TIMEOUT)

    if code == 0:
        res = result.strip().split('/')[-1]
        # print(res)
        if len(res) < 1:
            return False
        return '/dev/' + res
    else:
        logger.error('shell,get slot name form sn fail.{}.{}'.format(cmd, result))
        return False


def get_disk_identifier(disk_name):
    """
    fdisk -l /dev/sdi | grep 'Disk identifier' | awk '{print $3}'
    disk_name: /dev/sdi
    :return:
    """
    # output:name uuid
    cmd = "fdisk -l %s | grep 'Disk identifier' | awk 'END {print $3}'" % disk_name
    code, result = psutil_shell(cmd, TIMEOUT)

    if code == 0:
        return result
    else:
        return None


def get_disk_usage(disk):
    """
    df /dev/sdc1 or df /opt/data/hd/hd2
    size:Kb
    :param disk: disk_name or mountpoint
    :return:
    """
    disk = disk.strip("\n")
    print("df %s | awk 'END {print $1,$2,$3,$4,$5,$6}'" % disk)
    code, result = psutil_shell("df %s | awk 'END {print $1,$2,$3,$4,$5,$6}'" % disk, TIMEOUT)
    print(code, result)
    if code != 0:
        return None
    # print(disk, "used:", result)
    disk_dict = dict()
    result = result.split(" ")
    disk_dict["device_name"] = result[0]
    disk_dict["device_size"] = result[1]
    disk_dict["used_size"] = result[2]
    disk_dict["available_size"] = result[3]
    disk_dict["used_percent"] = result[4]
    return disk_dict


def get_dir_usage(dir):
    """
    du -sh /opt/data/region/meetingData
    :return:

    """
    code, result = psutil_shell('du -sh %s | awk \'{print $1}\'' % dir, TIMEOUT)
    if code != 0:
        return None
    logger.info("dir usage:dir:{}, result:{}".format(dir, result))
    return result


def get_region_usage(region):
    """
    du -csh /opt/data/region/meetingData/*
    :param region:meetingData
    :return:
    """
    region_path = os.path.join(SPACE_TOPPATH, region)
    # full_path = os.path.join(region_path, '*')
    code, result = psutil_shell('du -bcsh %s | awk \'END {print $1}\'' % region_path, TIMEOUT)
    if code != 0:
        return None
    result = result.strip()
    size = result[0:-1]
    unit = result[-1]
    # print("\n get rgion us:", size, unit, "\n")
    used = byte_from_str(size, unit)
    # print("get_region_usage:", size, unit, 'used:', used)
    logger.info('region used:region:{}, used:{}'.format(region, used))
    return used


def generate_hd_name(dev_name):
    flag = dev_name[-1]
    hd_name = "hd" + str(ord(flag) - 97)
    return hd_name


def psutil_shell_create_disk(disk_name, hd_name, size):
    # psutil_shell_create_disk('./shells/fdisk_create.sh', '/dev/sdb', '2', '+1G')
    shell_name = 'common/shells/create.sh'
    if not isinstance(size, int):
        size = int(size)
    size = '+' + str(size) + 'K'
    cmd = list()
    cmd.append(shell_name)
    cmd.append(disk_name)
    cmd.append(hd_name)
    cmd.append(size)
    cmd_ = ' '.join(cmd)
    code, result = psutil_shell(cmd_, TIMEOUT)
    if code == 0:
        logger.info('create {} / {} success ,size is {}.'.format(disk_name, hd_name, size))
    else:
        logger.info('create fail.{}'.format(result))
    # print(cmd_)
    return code, result


def psutil_shell_mount_all(disk_list, hd_list):
    shell_name = './shells/mount.sh'
    cmdstr = "{} \'{}\' \'{}\'".format(shell_name, ','.join(disk_list), ','.join(hd_list))
    code, result = psutil_shell(cmdstr, 10)
    if code == 0:
        logger.info('mount disk success.cmd:{}'.format(cmdstr))
    else:
        logger.error('mount disk fail.{}'.format(result))
    return result


def psutil_shell_add_disk(disk_name, hd_name):
    """
    gdisk_create.sh /dev/sdb hd1
    :param disk_name: /dev/sdb
    :param hd_name: hd1
    :return:
    """
    cmd = list()
    shell_name = 'shells/gdisk_create.sh'
    cmd.append(shell_name)
    cmd.append(disk_name)
    cmd.append(hd_name)
    cdm_ = ' '.join(cmd)
    code, result = psutil_shell(cdm_, TIMEOUT)
    if code == 0:
        logger.info('add {} success.'.format(hd_name))
    else:
        logger.info('add fail.{}'.format(result))
    return code, result


def psutil_shell_delete_disk(disk_name, hd_name):
    """
    gdisk_delete.sh /dev/sdb hd1
    :param disk_name: /dev/sdb
    :param hd_name: hd1
    :return:
    """
    cmd = list()
    shell_name = 'shells/gdisk_delete.sh'

    cmd.append(shell_name)
    cmd.append(disk_name)
    cmd.append(hd_name)
    cdm_ = ' '.join(cmd)
    code, result = psutil_shell(cdm_, TIMEOUT)
    if code == 0:
        logger.info('delete {} success.'.format(hd_name))
    else:
        logger.error('delete fail.{}'.format(result))
    return code, result


def psutil_shell_quota_new_disk(hd_name_list, region_list, quota_list, hd_size_list):
    """
    size:byte
    :param hd_name_list: [hd1,hd2]
    :param region_list:  [meetingData,Aidata...]
    :param quota_list:   [20,20,...]
    :param hd_size_list: [1024,1024]
    :return:
    """
    shell_name = '/opt/midware/kdfs/stsps/common/shells/quota_new_disk.sh'
    logger.info('quota new disk........{} {} {} {}'.format(hd_name_list, region_list, quota_list, hd_size_list))
    cmdstr = "{} \'{}\' \'{}\' \'{}\' \'{}\'".format(
               shell_name, ','.join(hd_name_list), ','.join(region_list), ','.join(quota_list), ','.join(hd_size_list))
    code, result = psutil_shell(cmdstr, 10)
    if code == 0:
        logger.info('quota {} success.'.format(','.join(hd_name_list)))
    else:
        logger.error('quota fail.{}'.format(result))
    return code, result


def psutil_shell_quota_disk(hd_name_list, region_list, quota_list, hd_size_list):
    """
    size:byte
    :param hd_name_list: [hd1,hd2]
    :param region_list:  [meetingData,Aidata...]
    :param quota_list:   [20,20,...]
    :param hd_size_list: [1024,1024]
    :return:
    """
    shell_name = '/opt/midware/kdfs/stsps/common/shells/quota.sh'
    logger.info('quota all disk........{} {} {} {}'.format(hd_name_list, region_list, quota_list, hd_size_list))
    cmdstr = "{} \'{}\' \'{}\' \'{}\' \'{}\'".format(
               shell_name, ','.join(hd_name_list), ','.join(region_list), ','.join(quota_list), ','.join(hd_size_list))
    code, result = psutil_shell(cmdstr, 10)
    if code == 0:
        logger.info('quota {} success.'.format(','.join(hd_name_list)))
    else:
        logger.error('quota fail.{}'.format(result))
    return code, result


def psutil_shell_mount_disk(dev_list, hd_list, region_list):
    """
    eg:./mount.sh "/dev/sdb1,/dev/sdc1" "hd1,hd2" "meetingData,AiData..."
    :param hd_name:  [/dev/sdb1,/dev/sdc1]
    :param dir_list: [hd1,hd2]
    :param region_list: [meetingData,...]
    :return:
    """
    shell_name = '/opt/midware/kdfs/stsps/common/shells/mountdisk.sh'
    cmdstr = "{} \'{}\' \'{}\' \'{}\'".format(shell_name, ','.join(dev_list), ','.join(hd_list), ','.join(region_list))
    code, result = psutil_shell(cmdstr, 10)
    if code == 0:
        logger.info('mount disk {} success.'.format(','.join(hd_list)))
    else:
        logger.error('mount disk fail.{}'.format(result))
    return code, result


def psutil_shell_mount_region(hd_list, region_list):
    """
    arg1: hd_name    "hd1,hd2"
    arg2: region list  "meetingData,AiData,mtLog,platformData,platformLog"
    :param hd_list:  [hd1,hd2]
    :param region_list: [meetingData,AiData,mtLog,platformData,platformLog]
    :return:
    """
    shell_name = 'common/shells/mountdisk.sh'
    cmdstr = "{} \'{}\' \'{}\'".format(shell_name, ','.join(hd_list), ','.join(region_list))
    code, result = psutil_shell(cmdstr, 10)
    if code == 0:
        logger.info('mount region {} success.'.format(','.join(region_list)))
    else:
        logger.info('mount region fail.{}'.format(result))
    return code

def psutil_shell_mount_status(dev_name):
    """
    mount -l | grep /dev/sdc1
    :param dev_name: /dev/sdc1 or /opt/data/hd/hd1
    :return: 0=no mount, 1=mount
    """
    cmdstr = "mount -l | grep %s | awk '{print $1}'" % dev_name
    code, result = psutil_shell(cmdstr, TIMEOUT)
    if code == 0:
        # print(result)
        # print(type(result))
        if result == "":
            logger.info("{} not mount".format(dev_name))
            return False
        else:
            logger.info("{} mount".format(dev_name))
            return result
    else:
        logger.error("get mount status error.{}".format(result))
        return False

def pustil_shell_mount_raid(dev_name):
    """
    mdadm -D /dev/md* | grep /dev/sdg | awk '{print $7}'
    :param dev_name: /dev/sdc1 or /opt/data/hd/hd1
    :return: 0= no mount , 1=mount
    """
    cmdstr = "mdadm -D /dev/md* | grep %s | awk '{print $7}'" % dev_name
    code, result = psutil_shell(cmdstr, TIMEOUT)
    if code == 0:
        if result == "":
            logger.info("{} not mount".format(dev_name))
            return False
        else:
            logger.info("{} mount".format(dev_name))
            return result.strip('\n')
    else:
        logger.error("get mount status error.{}".format(result))
        return False


def psutil_shell_mount_point(dev_name):
    """
    mount -l | grep /dev/sdc1
    :param dev_name: /dev/sdc1 or /opt/data/hd/hd1
    :return: 0=no mount, 1=mount
    """
    cmdstr = "mount -l | grep %s | awk '{print $3}'" % dev_name
    code, result = psutil_shell(cmdstr, TIMEOUT)
    if code == 0:
        # print(result)
        # print(type(result))
        if result == "":
            logger.info("{} not mount".format(dev_name))
            return 0
        else:
            logger.info("{} mount point is :{}".format(dev_name, cmdstr))
            if cmdstr in ['/', '/boot', '/dev/mapper/centos-root']:
                return 2
            else:
                return 1
    else:
        logger.error("get mount status error.{}".format(result))
        return 0

def psutil_shell_test():
    proc = psutil_shell('fdisk -l', TIMEOUT)
    # print(proc)


def psutil_sh_args_test():
    file = './shells/array.sh'
    arg1 = 'hd1'
    arg2 = ['meetingData','AiData']
    cmdstr = "{} {} \'{}\'".format(file, arg1, ' '.join(arg2))
    a = psutil_shell(cmdstr, 10)
    # print('result:', a)

def psutil_get_disk_part_max(dev_name):
    """
    lsblk -p | grep /dev/sde | grep part | awk '{print $1}'
    :param dev_name:  /dev/sde
    :return:
    """
    cmdstr = "lsblk -pb | grep %s | grep part | awk '{print $1,$4}'" % dev_name
    code, result = psutil_shell(cmdstr, TIMEOUT)
    if code == 0:
        logger.info('get disk max parted number success.')
    else:
        return None
    part_info = result.strip().split('\n')
    max_size = 0
    max_part = None
    for part in part_info:
        if part != '':
            part, psize = part.split(' ')
            size = int(psize)
            if size > max_size:
                max_size = size
                max_part = part
    return max_part[10:]


if __name__ == "__main__":
    # psutil_shell_mount_status('/dev/sdc1')
    # a = psutil_get_disk_part_max('/dev/sdh')
    # print(a)
    code, res = psutil_shell_create_disk('/dev/sdb', 'hd1', 3905199013.888)
    print(code, res)
