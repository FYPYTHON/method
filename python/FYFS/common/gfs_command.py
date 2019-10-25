# coding=utf-8
"""
本地脚本在远程服务器上执行
ssh gfs-224 'bash -s' < sshlog.sh 123
远程执行远程服务器上的脚本
ssh gfs-224  /root/test.sh 123

设置配额
gluster volume quota gcvol limit-usage /C 5GB
/C: /mnt/gfs下的目录
查看
gluster volume quota gcvol list
解除限额
gluster volume quota gcvol remove /A
"""
try:
    from common.comoncommand import psutil_shell
except:
    from comoncommand import psutil_shell


def gfs_pool_list():
    cmd = "gluster pool list | awk '{if (NR>1) {print $1,$2,$3}}'"

    code, result = psutil_shell(cmd, 30)
    pool = []
    if code != 0:
        return False
    result = result.strip('\n').split('\n')
    for item in result:
        info = item.split(' ')
        pool_dict = dict()
        pool_dict['hostname'] = info[1]
        pool_dict['uuid'] = info[0]
        pool_dict['state'] = info[2]
        pool.append(pool_dict)
    return pool


def gfs_peer_probe(hostname):
    cmd = "gluster peer probe %s" % hostname
    code, result = psutil_shell(cmd, 30)
    if code != 0:
        print(hostname, result)
        return False, result
    else:
        return True, result


def gfs_peer_detach(hostname):
    cmd = "echo y | gluster peer detach %s force" % hostname
    code, result = psutil_shell(cmd, 30)
    print(result)
    if code != 0:
        print(hostname, result)
        return False, result
    else:
        return True, result


def gfs_volume_all():
    cmd = "gluster volume list"
    code, result = psutil_shell(cmd, 30)

    if code != 0:
        return False
    result = result.strip('\n').split('\n')
    return result


def gfs_volume_info(gvol):
    cmd = "gluster volume info %s" % gvol
    code, result = psutil_shell(cmd, 30)
    if code != 0:
        return False
    result = result.strip('\n').split('\n')
    info_list = []
    info_dict = dict()
    info_dict['bricks'] = []
    for item in result:
        if item == ' ':
            continue
        key, value = item.split(":", 1)
        if value == '':
            continue

        if key.startswith("Brick"):
            info_dict['bricks'].append(value.strip(' '))
        else:
            if key == 'Number of Bricks':
                info_dict[key.replace(' ', '')] = value.split('=')[-1]
            else:
                info_dict[key.replace(' ', '')] = value.strip(' ')
    # print(info_dict)
    return info_dict


def gfs_volume_start(vol):
    cmd = "gluster volume start %s force" % vol
    code, result = psutil_shell(cmd, 30)
    print(result)
    if code != 0:
        print(vol, result)
        return False, result
    else:
        return True, result


def gfs_volume_stop(vol):
    cmd = "echo y | gluster volume stop %s force" % vol
    code, result = psutil_shell(cmd, 30)
    # print(result)
    if code != 0:
        # print(vol, result)
        return False, result
    else:
        return True, result


if __name__ == "__main__":
    r = gfs_volume_info('gvol')
    # print(r)
    # gfs_peer_detach('gfs-224')