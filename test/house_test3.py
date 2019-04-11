from redis import Redis
import pandas as pd
import json

if __name__ == '__main__':
    PD_PREFIX = 'PD^'
    NHLOG_PREFIX = 'NHLOG^'
    redis = Redis(host='202.102.83.162', db=1, port=6379)
    results = redis.lrange(NHLOG_PREFIX+'865441036008605', 0, 30)
    data = list()
    for result in results:
        data.extend(json.loads(result.decode('utf-8')))

    df = pd.read_json(json.dumps(data, ensure_ascii=False), orient='records')
    df.to_csv('newhouseLog.csv', index=False)
