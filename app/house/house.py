from . import houses
from flask import render_template
from redis import Redis
import json
import pandas as pd

# TODO 调试的用的redis
r = Redis(host='192.168.10.221', port=6379, db=1)
r2 = Redis(host='192.168.10.221', port=6379, db=2)

NEWHOUSELOG_PREFIX = "NHLOG^"
PHONEDEVICE_PREFIX = "PD^"


@houses.route("/<string:phone>/<string:city>/<int:num>", methods=['GET'])
def index(phone, num, city):
    deviceids = r.smembers(PHONEDEVICE_PREFIX + phone)
    result = list()
    for deviceid in deviceids:
        datas = r2.lrange(NEWHOUSELOG_PREFIX + deviceid.decode('utf-8'), 0, num)
        for data in datas:
            result.extend(json.loads(data.decode('utf-8')))

    cities, min_price, max_price, newhouses, newhouses_count = newhouse_handle(result, city)

    return render_template("house/house.html", newhouses=newhouses, userId=phone, num=num, cities=cities,
                           min_price=min_price, max_price=max_price, newhouses_count=newhouses_count)


def newhouse_handle(newhouse_json, city='南京'):
    newhouse_json = json.dumps(newhouse_json, ensure_ascii=False)
    df = pd.read_json(newhouse_json, orient='records')
    count = len(df)
    cities = df['CITY_NAME'].unique()
    df = df[df['CITY_NAME'] == city]
    print(df.loc[:, ['CONTEXT_ID', 'START_TIME']])
    min_price = min(df['PRICE_AVG'])
    max_price = max(df['PRICE_AVG'])
    df = df.sort_values(by='START_TIME', ascending=False)
    df_count = df.groupby('CONTEXT_ID').size().reset_index(name='COUNT')
    print(df_count.head(100))
    df_order = df.groupby('CONTEXT_ID').nth(0).copy()
    print(df_order.head(100))
    datas = df_order.merge(df_count, how='left', on='CONTEXT_ID')
    print(datas.head(100))
    datas.sort_values(by='COUNT', ascending=False, inplace=True)
    print(datas.head(100))
    datas = datas.to_json(orient="records", force_ascii=False)
    return cities, min_price, max_price, datas, count


if __name__ == '__main__':
    deviceids = r.smembers('PD^13851729904')
    result = list()
    for deviceid in deviceids:
        datas = r2.lrange(NEWHOUSELOG_PREFIX + deviceid.decode('utf-8'), 0, 30)
        for data in datas:
            result.extend(json.loads(data.decode('utf-8')))

    print(len(result))
