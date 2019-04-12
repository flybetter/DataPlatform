from redis import Redis
import json
import pandas as pd
from sqlalchemy import create_engine


def newhouse_handle(datas):
    df = pd.read_json(datas, orient='records')
    print(df['CITY_NAME'])
    print(df['CITY_NAME'].unique())  # 城市
    df = df[df['CITY_NAME'] == '合肥']
    print(df.loc[:, ['CONTEXT_ID', 'START_TIME']])
    # 均价
    df = df.sort_values(by='START_TIME', ascending=False)
    print(df.loc[:, ['CONTEXT_ID', 'START_TIME']])

    df_count = df.groupby('CONTEXT_ID').size().reset_index(name='COUNT').copy()
    df_order = df.groupby('CONTEXT_ID').nth(0).copy()
    datas = df_order.merge(df_count, how='left', on='CONTEXT_ID')
    print(datas.sort_values(by='START_TIME', ascending=False, inplace=True))
    print(datas.head(100))
    #
    # df = df[df['PRICE_SHOW'].str.contains('元/㎡', na=False)]
    # print(max(df['PRICE_AVG']))
    # print(min(df['PRICE_AVG']))
    # print(df['PRICE_SHOW'])


if __name__ == '__main__':
    NEWHOUSELOG_PREFIX = "NHLOG^"
    PHONEDEVICE_PREFIX = "PD^"
    r = Redis(host='192.168.10.221', port=6379, db=4)

    keys = r.keys('NHLOG^*')
    for key in keys:
        result = []
        print(key)
        datas = r.lrange(key, 0, 30)
        print(len(datas))
        if len(datas) > 0:
            for data in datas:
                result.extend(json.loads(data.decode('utf-8')))
            df = pd.read_json(json.dumps(result, ensure_ascii=False), orient='records')
            engine = create_engine('mysql+pymysql://root:idontcare@192.168.10.221/demo')
            con = engine.connect()
            df.to_sql('behaviors_demo', con=engine, if_exists='append', index=False)


    # df.to_csv("data.txt", index=False)
    # df = pd.read_json(datas, orient='records')
    # object = newhouse_demo(df, '合肥')
    # cities = object.get_cities()
    # min_price, max_price = object.get_price()
    # datas = object.get_result()
    # datas = datas.to_json(orient="records", force_ascii=False)
    # print(datas)
