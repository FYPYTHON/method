# coding=utf-8

# from app import hello

def redis_celery():
    import redis
    conn = redis.StrictRedis(host='localhost', password='feiying', port='6379')
    print(conn.keys())

    for item in conn.keys():
        conn.delete(item)
    print(conn.keys())
    # print(conn.get('_kombu.binding.celery'))
    # print(conn.get('celery'))

# python3 -m celery -A celery_demo worker
if __name__  == "__main__":
    import os
    # command_beat = 'celery beat -A celery_demo.worker -l info'
    # os.system(command_beat)
    # command_worker = 'celery worker -A celery_demo.worker -l info'
    # os.system(command_worker)
    # a = hello.delay(2,3)
    # a.ready()
    # print(a)
    # print(a.ready())
    # # print(a.get(timeout=1))
    # print(a.get(propagate=False))
    redis_celery()
