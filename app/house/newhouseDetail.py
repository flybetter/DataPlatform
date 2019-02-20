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

    def get_avg_price_histogram(self):
        self.fiter_df['avg_price_range'] = pd.cut(self.fiter_df['PRICE_AVG'], bins=20, right=False)
        value_df = self.fiter_df.groupby("avg_price_range").size().reset_index(name='counts')
        return (value_df['avg_price_range'].astype('str').to_json(orient='values', index=True),
                value_df['counts'].to_json(orient='values', index=True))

    def get_area_histogram(self):
        self.df['PIC_AREA'] = pd.cut(self.df['PIC_AREA'], bins=10, right=False)
        value_df = self.df.groupby("PIC_AREA").size().reset_index(name='counts')
        return (value_df['PIC_AREA'].astype('str').to_json(orient='values', index=True),
                value_df['counts'].to_json(orient='values', index=True))

    def get_sum_price_histogram(self):
        self.df['PIC_HX_TOTALPRICE'] = pd.cut(self.df['PIC_HX_TOTALPRICE'], bins=20, right=False)
        value_df = self.df.groupby("PIC_HX_TOTALPRICE").size().reset_index(name='counts')
        return (value_df['PIC_HX_TOTALPRICE'].astype('str').to_json(orient='values', index=True),
                value_df['counts'].to_json(orient='values', index=True))

    def get_toilet_pie(self):
        temp = pd.DataFrame(
            {'Percentage': self.df.groupby("PIC_WEI").size() / len(self.df['PIC_WEI'].dropna())}).reset_index().rename(
            columns={'PIC_WEI': 'name', 'Percentage': 'y'})
        temp['name'] = temp['name'].astype(str).map(lambda x: x.replace('.0', '间'))
        return temp.to_json(orient='records', index=True)

    def get_bedroom_pie(self):
        di = {8: 1, 9: 2, 10: 3, 11: 4, 21: 5, 22: 6}
        df = self.df.replace({"PIC_TYPE": di})
        temp = pd.DataFrame(
            {'Percentage': df.groupby("PIC_TYPE").size() / len(df['PIC_TYPE'].dropna())}).reset_index().rename(
            columns={'PIC_TYPE': 'name', 'Percentage': 'y'})
        temp['name'] = temp['name'].astype(str).map(lambda x: x.replace('.0', '室'))
        return temp.to_json(orient='records', index=True)

    def get_livingroom_pie(self):
        temp = pd.DataFrame(
            {'Percentage': self.df.groupby("PIC_TING").size() / len(self.df['PIC_TING'].dropna())}).reset_index().rename(
            columns={'PIC_TING': 'name', 'Percentage': 'y'})
        temp['name'] = temp['name'].astype(str).map(lambda x: x.replace('.0', '间'))
        return temp.to_json(orient='records', index=True)

    def get_kitchen_pie(self):
        temp = pd.DataFrame(
            {'Percentage': self.df.groupby("PIC_CHU").size() / len(self.df['PIC_CHU'].dropna())}).reset_index().rename(
            columns={'PIC_CHU': 'name', 'Percentage': 'y'})
        temp['name'] = temp['name'].astype(str).map(lambda x: x.replace('.0', '间'))
        return temp.to_json(orient='records', index=True)
