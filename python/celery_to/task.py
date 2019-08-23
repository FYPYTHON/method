#!/usr/bin/env python
# encoding: utf-8

import time
from celery import Celery, platforms

platforms.C_FORCE_ROOT = True  # linux use root

BROKER_URL = 'redis://:feiying@127.0.0.1:6379/'
BACKEND_URL = 'redis://:feiying@127.0.0.1:6379/'
# celery = Celery("tasks", broker=BROKER_URL, backend=BACKEND_URL)


# celery.conf.CELERY_RESULT_BACKEND = "redis"
celery = Celery()
celery.config_from_object('setting')


@celery.task
def sleep(seconds, name):
    time.sleep(float(seconds))
    return "I go over," + name


@celery.task(name="longtime")
def celery_do_longtime_task(some_param):

    """

    这里我们模拟一个耗时操作，然后返回一个value



    :param some_param:  某些参数，这里模拟一个大数据如 999999999

    :return: 某一个值

    """
    ret = 1
    for i in range(some_param):
        ret += i
    print("ret=%s" % ret)

    return ret


if __name__ == "__main__":
    celery.start()