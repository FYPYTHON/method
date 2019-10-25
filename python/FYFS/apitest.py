# coding=utf-8
import requests

ip = '172.16.83.222'
port = '8019'
api = 'ldfs/api/v1/log'
volapi = 'ldfs/api/v1/gfs/volume'


def getip():
    res = requests.get("http://txt.go.sohu.com/ip/soip")
    import re
    ip = re.findall(r'\d+.\d+.\d+.\d+', res.text)

    print(res)
    print(ip[0])


def get():
    param = {"st": "2019-10-09 00:00:00", "et": "2019-10-09 23:00:00"}
    result = requests.get("http://{}:{}/{}".format(ip, port, api), params=param)
    print(result.content)


def post():
    data = {'user': 'admin', 'key': '日志', 'content': '日志下载'}
    result = requests.post("http://{}:{}/{}".format(ip, port, api), data=data)
    print(result.content)


def volpost():
    data = {"volname": 'gcvol', "bricks": ["bk1", "bk2"], "replica": 0, " stripe": 0}
    result = requests.post("http://{}:{}/{}".format(ip, port, volapi), data=data)
    print(result.content)


if __name__ == "__main__":
    # post()
    # get()
    volpost()