import pandas as pd
import json
import traceback


class newhouse:
    def __init__(self, df, city='南京'):
        self.df = df
        self.city = city

    def get_cities(self):
        try:
            cities = self.df['CITY_NAME'].unique()
            return cities
        except Exception:
            print(traceback.format_exc())
            return list()

    def get_price(self):
        try:
            df = self.df[self.df['CITY_NAME'] == self.city]
            df_price = df[df['PRICE_SHOW'].str.contains('元/㎡', na=False)]
            min_price = min(df_price['PRICE_AVG'])
            max_price = max(df_price['PRICE_AVG'])
            return min_price, max_price
        except Exception:
            print(traceback.format_exc())
            return 0, 0

    def get_result(self):
        try:
            df = self.df[self.df['CITY_NAME'] == self.city]
            df_result = df.sort_values(by='START_TIME', ascending=False)
            df_count = df_result.groupby('CONTEXT_ID').size().reset_index(name='COUNT')
            df_order = df.groupby('CONTEXT_ID').nth(0)
            datas = df_order.merge(df_count, how='left', on='CONTEXT_ID')
            datas.sort_values(by='COUNT', ascending=False, inplace=True)
            return datas
        except Exception:
            print(traceback.format_exc())
            return {}
