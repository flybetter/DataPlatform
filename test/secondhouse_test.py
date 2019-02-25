import redis
import pandas as pd
import json

if __name__ == '__main__':

    r = redis.Redis(host='202.102.83.162', port=6379, db='1')
    keys = r.keys('SHLOG^*')
    result = list()
    for key in keys:
        datas = r.lrange(key, 0, 30)
        for data in datas:
            result.extend(json.loads(data.decode('utf-8')))
    df = pd.read_json(json.dumps(result, ensure_ascii=False), orient='records')
    df.to_json('secondhouseDemo.csv')
