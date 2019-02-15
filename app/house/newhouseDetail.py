import pandas as pd
import json
import traceback


class newhouseDetail:
    def __init__(self, df, city='南京', sort_key=0):
        """
        :param df:
        :param city:
        :param sort_key: 0 是按点击次数排序 1 是按时间顺序排序
        """
        self.df = df
        self.city = city
        self.sort_key = int(sort_key)
        self.fiter_df = df[df['PRICE_SHOW'].str.contains('元/㎡', na=False)]

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
            df_order = df_result.groupby('CONTEXT_ID').nth(0)
            datas = df_order.merge(df_count, how='left', on='CONTEXT_ID')
            if self.sort_key == 0:
                datas.sort_values(by='COUNT', ascending=False, inplace=True)
            elif self.sort_key == 1:
                datas.sort_values(by='START_TIME', ascending=False, inplace=True)
            return datas
        except Exception:
            print(traceback.format_exc())
            return {}

    def get_sum_count(self):
        return len(self.fiter_df)

    def get_avg_price(self):
        try:
            return self.fiter_df['PRICE_AVG'].mean()
        except Exception:
            print(traceback.format_exc())
            return 0

    def get_area(self):
        try:
            return self.df['PIC_AREA'].mean()
        except Exception:
            print(traceback.format_exc())
            return 0

    def get_sum_price(self):
        try:
            # TODO  有点情况下，没有总价， 需要均价*面积得到总价。目前用最简单的
            return self.df['PIC_HX_TOTALPRICE'].mean()
        except Exception:
            print(traceback.format_exc())
            return 0

    def get_toilet(self):
        return self.df['PIC_WEI'].mean()

    def get_bedroom(self):
        di = {8: 1, 9: 2, 10: 3, 11: 4, 21: 5, 22: 6}
        df = self.df.replace({"PIC_TYPE": di})
        return df['PIC_TYPE'].mean()

    def get_livingroom(self):
        return self.df['PIC_TING'].mean()

    def get_kitchen(self):
        return self.df['PIC_CHU'].mean()

    def get_click_frequency_diagram(self):
        count_df = self.df.groupby("DATA_DATE").size().reset_index(name='counts')
        return count_df.to_json(orient='values', index=True)