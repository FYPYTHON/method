# coding=utf-8
"""
pip install eventlet
celery -A <mymodule> worker -l info -P eventlet
# celery beat -A celery_demo.worker -l info --pidfile=celery.pid --logfile=celery.log
# celery -A proj control shutdown
# celery multi stop w1 -A celery_demo -l info
# celery multi stopwait w1 -A celery_demo -l info
# ps auxww|grep "celery worker"|grep -v grep|awk '{print $2}'|xargs kill -9
"""
import celery
import time
from datetime import timedelta
import sys

CELERY_DIR = 'D:/project/method/python/celery_py'

sys.path.insert(0, CELERY_DIR)

BROKER_URL = 'redis://:feiying@127.0.0.1:6379/'
BACKEND_URL = 'redis://:feiying@127.0.0.1:6379/'

worker = celery.Celery("demo", backend=BACKEND_URL, broker=BROKER_URL)


class Config:
    CELERYBEAT_SCHEDULE = {
        'update_info': {
            'task': 'celery_demo.hello',
            "schedule": timedelta(seconds=6),
        }
    },
    CELERY_ANNOTATIONS = {
        'tasks.add': {'rate_limit': '10/m'}  # 每分钟10个
    }


worker.config_from_object(Config)


@worker.task
def hello(x, y):
    print("hello,{}".format(time.time()))
    return x + y



if __name__ == '__main__':
    import os
    # command_beat = 'celery beat -A celery_demo.worker -l info'
    # os.system(command_beat)
    # command_worker = 'celery worker -A demo'
    # os.system(command_worker)
    a = hello.delay(1,6)
    print(a.ready())
    print(a.get())
