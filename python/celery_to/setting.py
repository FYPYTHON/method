# coding=utf-8

BROKER_URL = 'redis://:feiying@127.0.0.1:6379/'

CELERY_RESULT_BACKEND = 'redis://:feiying@127.0.0.1:6379/'

CELERY_TASK_RESULT_EXPIRES = 30 * 60    # 结果保留时间

CELERY_TASK_SERIALIZER = 'json'

CELERY_RESULT_SERIALIZER = 'json'

CELERY_ACCEPT_CONTENT = ['json']

CELERY_TIMEZONE = 'Asia/Shanghai'

CELERY_ENABLE_UTC = True

CELERYD_CONCURRENCY = 3  # worker数量

CELERYD_HIJACK_ROOT_LOGGER = False  # 如果True则会移除所有的root logger下的handler。


CELERY_ACKS_LATE = False

CELERYD_PREFETCH_MULTIPLIER = 1  # 每一个worker服务的task数量