# coding=utf-8
from datetime import datetime


def str_to_datetime(strt):
    dt = datetime.strptime(strt, "%Y-%m-%d %H:%M:%S")
    return dt


def datatime_to_str(dt):
    st = datetime.strftime(dt, "%Y-%m-%d %H:%M:%S")
    return st

if __name__ == "__main__":
    st = '2019-09-02 12:13:14'
    d = str_to_datetime(st)
    print(d, type(d))
    print(datatime_to_str(datetime.now()))