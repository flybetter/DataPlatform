import redis
import re
import pandas as pd
import os
import json
import numpy as np

elastic_server = '202.102.83.162'

michael_server = '192.168.10.221'

phone_device_all = '/home/michael/datax_data/phone_device_all/'

r = redis.Redis(host=elastic_server, db=1)


def remove_second_house():
    keys = list()
    for key in r.scan_iter(match='NHCRM\^*', count=5000):
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


def map_device_count():
    keys = list()
    for key in r.scan_iter(match='NHLOG\^*', count=5000):
        # print(re.match("NHLOG\^(.+)", key.decode('utf-8')).group(1))
        keys.append(re.match("NHLOG\^(.+)", key.decode('utf-8')).group(1))

    print(len(keys))

    for path in os.listdir(phone_device_all):
        df = pd.read_csv(phone_device_all + path, names=['PHONE', 'DEVICE_ID'], header=None,
                         index_col=False, low_memory=False, dtype={'PHONE': object, 'DEVICE_ID': np.str}
                         )

    final_df = df[df['DEVICE_ID'].isin(keys)]
    print(len(final_df))


if __name__ == '__main__':
    map_device_count()
    # remove_second_house()
