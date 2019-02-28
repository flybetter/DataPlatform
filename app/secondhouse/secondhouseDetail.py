import pandas as pd
import json
import traceback
import re


class secondhouseDetail:
    def __init__(self, df, city='南京', sort_key=0):
        """
        :param df:
        :param city:
        :param sort_key: 0 是按点击次数排序 1 是按时间顺序排序
        """
        self.df = df
        self.city = city
        self.sort_key = int(sort_key)

    def get_cities(self):
        try:
            cities = self.df['CITY'].unique()
            return cities
        except Exception:
            print(traceback.format_exc())
            return list()

    def get_price(self):
        try:
            df = self.df[self.df['CITY'] == self.city]
            min_price = min(df['AVERPRICE_x'])
            max_price = max(df['AVERPRICE_x'])
            return min_price, max_price
        except Exception:
            print(traceback.format_exc())
            return 0, 0

    def get_result(self):
        try:
            df = self.df[self.df['CITY'] == self.city]
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
        return len(self.df)

    def get_avg_price(self):
        try:
            return self.df['AVERPRICE_x'].mean()
        except Exception:
            print(traceback.format_exc())
            return 0

    def get_area(self):
        try:
            return self.df['BUILDAREA'].mean()
        except Exception:
            print(traceback.format_exc())
            return 0

    def get_sum_price(self):
        try:
            return pd.to_numeric(
                self.df['PRICE'].astype(str).map(lambda x: re.sub(u'[\u4E00-\u9FA5]', '', x)),
                errors='coerce').mean()
        except Exception:
            print(traceback.format_exc())
            return 0

    def get_toilet(self):
        return self.df['TOILET'].mean()

    def get_bedroom(self):
        return self.df['ROOM'].mean()

    def get_livingroom(self):
        return self.df['HALL'].mean()

    def get_kitchen(self):
        return self.df['KITCHEN'].mean()

    def get_click_frequency_diagram(self):
        count_df = self.df.groupby("DATA_DATE").size().reset_index(name='counts')
        return count_df.to_json(orient='values', index=True)

    def get_avg_price_histogram(self):
        self.df['avg_price_range'] = pd.cut(self.df['AVERPRICE_x'], bins=20, right=False, duplicates='drop')
        value_df = self.df.groupby("avg_price_range").size().reset_index(name='counts')
        return (value_df['avg_price_range'].astype('str').to_json(orient='values', index=True),
                value_df['counts'].to_json(orient='values', index=True))

    def get_area_histogram(self):
        try:
            self.df['BUILDAREA'] = pd.cut(self.df['BUILDAREA'], bins=10, right=False, duplicates='drop')
            value_df = self.df.groupby("BUILDAREA").size().reset_index(name='counts')
            return (value_df['BUILDAREA'].astype('str').to_json(orient='values', index=True),
                    value_df['counts'].to_json(orient='values', index=True))
        except Exception:
            return ('null', 'null')

    def get_sum_price_histogram(self):
        try:
            self.df['PRICE'] = pd.cut(pd.to_numeric(
                self.df['PRICE'].astype(str).map(lambda x: re.sub(u'[\u4E00-\u9FA5]', '', x)),
                errors='coerce'), bins=20, right=False, duplicates='drop')
            value_df = self.df.groupby("PRICE").size().reset_index(name='counts')
            return (value_df['PRICE'].astype('str').to_json(orient='values', index=True),
                    value_df['counts'].to_json(orient='values', index=True))
        except Exception:
            return ('null', 'null')

    def get_toilet_pie(self):
        try:
            temp = pd.DataFrame(
                {'Percentage': self.df.groupby("KITCHEN").size() / len(
                    self.df['KITCHEN'].dropna())}).reset_index().rename(
                columns={'KITCHEN': 'name', 'Percentage': 'y'})
            temp['name'] = temp['name'].astype(str).map(lambda x: x.replace('.0', '间'))
            return temp.to_json(orient='records', index=True)
        except Exception:
            return 'null'

    def get_bedroom_pie(self):
        try:
            temp = pd.DataFrame(
                {'Percentage': self.df.groupby("PIC_TYPE").size() / len(self.df['PIC_TYPE'].dropna())}).reset_index().rename(
                columns={'PIC_TYPE': 'name', 'Percentage': 'y'})
            temp['name'] = temp['name'].astype(str).map(lambda x: x.replace('.0', '室'))
            return temp.to_json(orient='records', index=True)
        except Exception:
            return 'null'

    def get_livingroom_pie(self):
        try:
            temp = pd.DataFrame(
                {'Percentage': self.df.groupby("PIC_TING").size() / len(
                    self.df['PIC_TING'].dropna())}).reset_index().rename(
                columns={'PIC_TING': 'name', 'Percentage': 'y'})
            temp['name'] = temp['name'].astype(str).map(lambda x: x.replace('.0', '间'))
            return temp.to_json(orient='records', index=True)
        except Exception:
            return 'null'

    def get_kitchen_pie(self):
        try:
            temp = pd.DataFrame(
                {'Percentage': self.df.groupby("PIC_CHU").size() / len(
                    self.df['PIC_CHU'].dropna())}).reset_index().rename(
                columns={'PIC_CHU': 'name', 'Percentage': 'y'})
            temp['name'] = temp['name'].astype(str).map(lambda x: x.replace('.0', '间'))
            return temp.to_json(orient='records', index=True)
        except Exception:
            return 'null'
