import pandas as pd
import json
import traceback
from functools import wraps
import re


def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            print(func.__name__)
            traceback.print_exc()
            result = None
        return result

    return wrapper


class newhouse:
    def __init__(self, df, city='南京', sort_key=0):
        """
        :param df:
        :param city:
        :param sort_key: 0 是按点击次数排序 1 是按时间顺序排序
        """
        self.df = df
        self.city = city
        self.sort_key = int(sort_key)

    @decorator
    def get_cities(self):
        cities = self.df['CITY_NAME'].unique()
        return cities

    @decorator
    def get_price(self):
        df = self.df[self.df['CITY_NAME'] == self.city]
        df_price = df[df['PRICE_SHOW'].str.contains('元/㎡', na=False)]
        min_price = min(df_price['PRICE_AVG'])
        max_price = max(df_price['PRICE_AVG'])
        return min_price, max_price

    @decorator
    def get_item_detail(self):
        df = self.df[self.df['CITY_NAME'] == self.city]
        df_result = df.sort_values(by='START_TIME', ascending=False)
        df_count = df_result.groupby('CONTEXT_ID').size().reset_index(name='COUNT')
        df_order = df_result.groupby('CONTEXT_ID').nth(0)
        datas = df_order.merge(df_count, how='left', on='CONTEXT_ID')
        if self.sort_key == 0:
            datas.sort_values(by='COUNT', ascending=False, inplace=True)
        elif self.sort_key == 1:
            datas.sort_values(by='START_TIME', ascending=False, inplace=True)
        newhouses = datas.to_json(orient="records", force_ascii=False)
        return newhouses

    @decorator
    def get_count(self):
        return len(self.df)

    @decorator
    def get_scatter_diagram(self):
        pd.to_numeric(
            self.df['PIC_HX_TOTALPRICE'].astype(str).map(lambda x: re.sub(u'[\u4E00-\u9FA5]', '', x)),
            errors='coerce')
        return



