# coding=utf-8
"""
create:2019/9/24 11:01
author:feiying
describe: this function run only in window, in linux please use script start.sh
django-admin startproject FeiYing
python3 manage.py startapp HomeManage
db:
python3 manage.py makemigrations
python3 manage.py migrate
"""
import socket
import os
if __name__ == "__main__":
    # myname = socket.getfqdn(socket.gethostname())  # get name
    # myaddr = socket.gethostbyname(myname)          # get ip
    myaddr = '0.0.0.0'
    command = "python3 manage.py runserver {}:8019".format(myaddr)
    os.system(command)