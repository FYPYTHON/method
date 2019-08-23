# coding=utf-8


import os
COMMAND1 = 'celery -A task worker --loglevel=info -P eventlet'
os.system(COMMAND1)