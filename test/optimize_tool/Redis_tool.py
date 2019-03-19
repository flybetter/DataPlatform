import redis

elastic_server = '202.102.83.162'

michael_server = '192.168.10.221'

r = redis.Redis(host=michael_server, db=6)


def remove_second_house():
    keys = list()
    for key in r.scan_iter(match='NHLOG\^*', count=5000):
        print(key.decode('utf-8'))
        keys.append(key.decode('utf-8'))

    with r.pipeline(transaction=False) as pipe:
        for key in keys:
            pipe.delete(key)
        pipe.execute()


def get_CRM_hashmap():
    for key in r.scan_iter(match='NHCRM\^*', count=5000):
        len = r.hlen(key.decode('utf-8'))
        if len > 2:
            print(key.decode('utf-8'))


if __name__ == '__main__':
    get_CRM_hashmap()
