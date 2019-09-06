# coding=utf-8
import json
import os
import hashlib
import requests
server_local = 'localhost'
server_222 = '172.16.83.226'
server = server_222
url = 'http://{}:80/upload'.format(server)
downurl = 'http://{}:80/download'.format(server)
filename = '1.txt'
# filename = 'test.rpm'
MAX_SINGLE = 1024 * 1024 * 10

def get_header():
    headers = {}
    real_url = url
    params = {'filename': filename}
    resp = requests.get(real_url, params=params, headers=headers)
    print(resp.content)
    if resp.status_code in [200, 201]:
        resp = resp.content.decode('utf-8')
        resp = json.loads(resp)
        flen = resp['len']
        fmd5 = resp['fmd5']
        return flen,  fmd5
    else:
        return None, None


def upload_file(flen, gmd5):
    fsize = os.path.getsize(filename)
    print("待上传文件大小：", fsize, "已上传大小：", flen)
    if flen > 0:
        headers = {'Range': 'bytes=%d-%d' % (flen, fsize)}
    else:
        headers = {}
    real_url = url
    data = ''
    fmd5 = hashlib.md5()
    status = 0
    with open(filename, 'rb') as f:
        if fsize > flen > 0:
            fmd5.update(f.read(flen))
        print(fmd5.hexdigest(), gmd5, fmd5.hexdigest() == gmd5)
        if gmd5 == fmd5.hexdigest():
            status = 1
            f.seek(flen)
            data = f.read()
        else:
            f.seek(0)
            data = f.read(fsize)

    ftime = os.stat(filename).st_mtime
    params = {'filename': filename, "ftime": ftime, "smd5": status}
    print("待上传文件大小：", len(data))
    resp = requests.post(real_url, params=params, headers=headers, data=data)
    print(resp.content)
    return resp


def main_upload():
    flen, fmd5 = get_header()
    if flen is not None:
        upload_file(flen, fmd5)

def get_file_md5(filename):
    fmd5 = hashlib.md5()
    if os.path.exists(filename):
        print(' exist', filename)
        fsize = os.path.getsize(filename)

        fmd5 = hashlib.md5()
        with open(filename, 'rb') as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                fmd5.update(data)
    fmd5 = fmd5.hexdigest()
    return fmd5


def download():
    real_url = downurl
    headers = {}
    filename = '1.bin'

    fsize = 0
    mode = 'wb'

    if os.path.exists(filename):
        fsize = os.path.getsize(filename)

    fmd5 = get_file_md5(filename)

    params = {'filename': filename, "smd5": fmd5, 'fsize': fsize}

    print("已下载文件大小：", fsize)
    print("参数：", params)
    resp = requests.get(real_url, params=params, headers=headers)
    print(resp.headers)
    resp_data = resp.content.decode('utf-8')
    resp_data = json.loads(resp_data)
    error_code = resp_data['code']

    print(resp_data['msg'])
    if error_code == 1:
        return None


    ghed = resp.headers['Dmode']
    gsize = int(resp.headers['Gsize'])
    if ghed == '0' or fsize > gsize:
        if os.path.exists(filename):
            os.remove(filename)
        fsize = 0

    plen = (gsize - fsize)//MAX_SINGLE
    print("分块数：", plen, "待下载大小：", gsize, '已下载大小：', fsize, "是否追加：", ghed)

    for i in range(plen + 1):

        pparams = {'filename': filename, 'brange': fsize + i * MAX_SINGLE}
        pres = requests.post(real_url, params=pparams, headers=headers)

        if pres.status_code not in [200, 201]:
            print("下载文件错误", filename)
            break

        if not resp.content:
            continue
        print('正在下载', i, len(pres.content))
        with open(filename, 'ab') as f:
            # print("write data")
            f.write(pres.content)
    print('下载完成。')


if __name__ == "__main__":

    main_upload()
    # download()

