# coding=utf-8
import psutil
import subprocess
from threading import Timer
from common.comoncommand import psutil_shell
TIMEOUT = 10


def get_raid_info_all():
    """
    mdadm -Q /dev/md* |tr ":" " " |awk '{print $1,$2,$3,$4}'
    mdadm -D -Y /dev/md*
    :return:
    """
    cmd = "mdadm -Q /dev/md* |tr \":\" \" \" |awk '{print $1,$2,$3,$4}'"
    code, result = psutil_shell(cmd, 10)
    print(result)
    if code == 0:
        # print('{}. get success.'.format(cmd))
        raid_list = list()
        for blk_info in result.split('\n'):

            raid_dict = dict()
            info_list = list(filter(None, blk_info.split(' ')))
            if len(info_list) < 3:
                continue

            raid_dict['id'] = info_list[0]
            raid_dict['name'] = info_list[0]
            raid_dict['size'] = info_list[1]
            raid_dict['type'] = info_list[2]
            raid_dict['nums'] = info_list[3]
            # blk_dict['type'] = info_list[2]
            raid_list.append(raid_dict)
        # import operator
        # blk_list_sorted = sorted(blk_list, key=operator.itemgetter('device'))  # blk list sort
        blk_list_sorted = sorted(raid_list, key=lambda x: x['id'])
        return blk_list_sorted
    else:
        print('{}. get fail.{}'.format(cmd, result))
        return code, result


def get_raid_disks_by_name(raid_name):
    """
    mdadm -D /dev/md67 | grep /dev/sd | awk '{print $7}' | xargs
    :param raid_name:
    :return:
    """
    cmd = "mdadm -D %s | grep /dev/sd | awk '{print $7}' | xargs" % raid_name
    code, result = psutil_shell(cmd, TIMEOUT)
    # print(result)
    if code == 0:
        return result.strip().split(' ')
    else:
        return None


def get_raid_info_uuid(raid_name):
    """
    :param raid_name: /dev/md0
    :return:
    """
    cmd = "mdadm -D %s | grep UUID | awk '{print $3}'" % raid_name
    code, result = psutil_shell(cmd, TIMEOUT)

    if code == 0:
        return result.strip()
    else:
        return None


def get_raid_info_size(raid_name):
    """
    :param raid_name: /dev/md0
    :return: 20952064   KB
    """
    cmd = "mdadm -D %s | grep 'Array Size' | awk '{print $4}'" % raid_name
    code, result = psutil_shell(cmd, TIMEOUT)

    if code == 0:
        return result.strip()
    else:
        return None


def create_raid(raid_name, raid_level, dev_num, dev_list):
    """
    mdadm -C /dev/md2 -l 5 -n 3 /dev/sdd /dev/sde /dev/sdf -x /dev/sdg  # raid5
    :param raid_name: /dev/md2
    :param raid_level: 5
    :param dev_num: 3
    :param dev_str: /dev/sdd /dev/sde /dev/sdf
    :return:
    """
    shell_name = 'shells/raid_create.sh'
    cmdstr = "{} {} {} {} \'{}\'".format(shell_name, raid_name, raid_level, dev_num, ' '.join(dev_list))
    print(cmdstr)
    code, result = psutil_shell(cmdstr, 10)
    if code == 0:
        print('{}. success.'.format(cmdstr))
    else:
        print('{}. fail.{}'.format(cmdstr, result))
    return code, result


def delete_raid(raid_name):
    """
    mdadm -S /dev/md2
    :param raid_name: /dev/md2
    :return:
    """
    shell_name = 'shells/raid_delete.sh'
    cmdstr = "{} {} ".format(shell_name, raid_name)
    code, result = psutil_shell(cmdstr, 10)
    if code == 0:
        print('{}. success.'.format(cmdstr))
    else:
        print('{}. fail.{}'.format(cmdstr, result))
    return code, result


if __name__ == "__main__":
    uuid = get_raid_info_uuid('/dev/md0')
    size = get_raid_info_size('/dev/md0')
    print(uuid, size)