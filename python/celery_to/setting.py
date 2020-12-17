# coding=utf-8
# /opt/midware/python3.8/bin/python3 -m celery --version
# celery=5.0.2


# broker_url = 'redis://:fy123456@127.0.0.1:6379/'
# result_backend = 'redis://:fy123456@127.0.0.1:6379/'
# task_result_expires = 30
# task_serializer = 'json'
# result_serializer = 'json'
# accept_content = ['json']
# timezone = 'Asia/Shanghai'
# enable_utc = True
# work_concurrency = 3  # worker number
# hijack_root_logger = False  # 如果True则会移除所有的root logger下的handler。
# prefetch_multiplier = 1  # 每一个worker服务的task数量
# acks_late = False

# sqlite
broker_url = 'sqla+sqlite:///tc.db'
# result_backend = 'sqla+sqlite:///tc.db'
