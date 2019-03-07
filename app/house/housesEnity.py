from app.house import *
from functools import wraps
import traceback


def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            traceback.print_exc()
            raise ValueError(func.__name__ + ' has something wronge')

    return wrapper


class HOUSES:
    def __init__(self):
        self._phone = None
        self._city = None
        self._days = None
        self._secret_key = None
        self._sorted_key = None
        self.deviceIds = None
        self.data = list()
        self.office_r = Redis(host=REDIS_HOST, db=REDIS_DB)
        self.crm_r = Redis(host=REDIS_HOST, db=REDIS_CRM_DB)
        self.df = None
        self.max_price = None
        self.min_price = None

    @property
    def phone(self):
        return self._phone

    @decorator
    @phone.setter
    def phone(self, phone_number):
        # prpcrypt = PrpCrypt()
        # self._phone = prpcrypt.decrypt(phone_number.encode('utf-8')).decode
        self._phone = phone_number

    @property
    def city(self):
        return self._city

    @decorator
    @city.setter
    def city(self, city_name):
        self._city = parse(city_name)

    @property
    def days(self):
        return self._days

    @decorator
    @days.setter
    def days(self, days_num):
        self._days = days_num

    @property
    def secret_key(self):
        return self._secret_key

    @decorator
    @secret_key.setter
    def secret_key(self, secret_key_value):
        m = hashlib.new('md5', (self._phone + 'house365').encode('utf-8')).hexdigest()
        if secret_key_value != m:
            raise ValueError(" secret_key is wrong")
        self._secret_key = secret_key_value

    @property
    def sorted_key(self):
        return self._sorted_key

    @decorator
    @sorted_key.setter
    def sorted_key(self, sorted_key_value):
        self._sorted_key = sorted_key_value

    def begin(self):
        result = dict()
        result['phone'] = self.phone
        # TODO
        result['phone_show'] = self.phone.replace(self.phone[3:7], '****')
        # images = self.redis_images_read()
        # result.extend(json.loads(images))
        self.redis_devices_read()
        self.redis_data_read()
        self.house_action()
        self.get_price()
        result['count'] = self.get_count()
        result['cities'] = self.get_cities()
        result['min_price'] = self.min_price
        result['max_price'] = self.max_price
        result['secret_key'] = self.secret_key
        result['newhouses_scatter_diagram'] = self.get_scatter_diagram()
        result['newhouses'] = self.get_item_detail()
        return result

    @decorator
    def redis_images_read(self):
        city_images = self.crm_r.hget(REDIS_CRM_PREFIX + self.phone, self.city)
        return city_images

    def redis_data_read(self):
        for deviceid in self.deviceIds:
            datas = self.office_r.lrange(REDIS_NEWHOUSE_PREFIX + deviceid.decode('utf-8'), 0, self.days)
            for data in datas:
                self.data.extend(json.loads(data.decode('utf-8')))

    def redis_devices_read(self):
        self.deviceIds = self.office_r.smembers(REDIS_PHONEDEVICE_PREFIX + self.phone)

    def house_action(self):
        newhouse_json = json.dumps(self.data, ensure_ascii=False)
        self.df = pd.read_json(newhouse_json, orient='records')

    @decorator
    def get_cities(self):
        cities = list(self.df['CITY_NAME'].unique())
        return cities

    def get_price(self):
        df = self.df[self.df['CITY_NAME'] == self.city]
        df_price = df[df['PRICE_SHOW'].str.contains('元/㎡', na=False)]
        self.min_price = min(df_price['PRICE_AVG'])
        self.max_price = max(df_price['PRICE_AVG'])

    @decorator
    def get_item_detail(self):
        df = self.df[self.df['CITY_NAME'] == self.city]
        df_result = df.sort_values(by='START_TIME', ascending=False)
        df_count = df_result.groupby('CONTEXT_ID').size().reset_index(name='COUNT')
        df_order = df_result.groupby('CONTEXT_ID').nth(0)
        datas = df_order.merge(df_count, how='left', on='CONTEXT_ID')
        if self.sorted_key == 0:
            datas.sort_values(by='COUNT', ascending=False, inplace=True)
        elif self.sorted_key == 1:
            datas.sort_values(by='COUNT', inplace=True)
        elif self.sorted_key == 2:
            datas.sort_values(by='START_TIME', ascending=False, inplace=True)
        elif self.sorted_key == 3:
            datas.sort_values(by='START_TIME', inplace=True)
        data = datas[['B_LNG', 'B_LAT', 'START_TIME', 'COUNT', 'PRJ_ITEMNAME', 'PRICE_SHOW']].to_json(orient="records",
                                                                                                      force_ascii=False)
        return data

    @decorator
    def get_count(self):
        return len(self.df)

    @decorator
    def get_scatter_diagram(self):
        df = self.df.dropna(subset=['PIC_HX_TOTALPRICE'])
        df['PIC_HX_TOTALPRICE'] = df['PIC_HX_TOTALPRICE'].astype(str).map(
            lambda x: re.sub(u'[\u4E00-\u9FA5]', '', x))
        return df[['PIC_HX_TOTALPRICE', 'START_TIME']].to_json(orient="records",
                                                               force_ascii=False)
