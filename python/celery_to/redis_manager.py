# coding=utf-8


def redis_celery():
    import redis
    conn = redis.StrictRedis(host='localhost', password='feiying', port='6379')
    print(conn.keys())
    # return conn
    for key in conn.keys():
        if b'celery-task' in key:
            print(conn.get(key))
            # conn.delete(key)


if __name__ == "__main__":
    redis_celery()