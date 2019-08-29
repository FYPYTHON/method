# coding=utf-8
import json
import os
import hashlib
import requests
server_local = 'localhost'
server_222 = '172.16.83.222'
url = 'http://{}:8001/upload'.format(server_222)
filename = '1.txt'
# filename = 'test.rpm'


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
    # print(data)
    params = {'filename': filename, "ftime": ftime, "smd5": status}
    # files = {'file': (filename, data)}
    # resp = requests.post(real_url, data=data, headers=headers, stream=True)
    # params = {'filename': filename, "ftime": ftime, "fmd5": fmd5.hexdigest(), 'data': data}
    # print(data)
    print("待上传文件大小：", len(data))
    resp = requests.post(real_url, params=params, headers=headers, data=data)
    print(resp.content)
    return resp



if __name__ == "__main__":
    flen, fmd5 = get_header()
    if flen is not None:
        upload_file(flen, fmd5)
    # upload_file(0)

