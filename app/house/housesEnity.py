from app.house import *
from functools import wraps
from urllib import parse
from app.tools.IDInformation import IDInformation


def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            traceback.print_exc()
            raise ValueError(func.__name__ + ' has something wrong')

    return wrapper


class HOUSES(object):
    def __init__(self):
        self._phone = None
        self.real_phone = None
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
        self.city_images = dict()
        self.sex = None
        self.age = None
        self.show_phone = None

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, phone_number):
        try:
            self._phone = phone_number
            pc = PrpCrypt()
            e = pc.decrypt(self.phone)
            self.real_phone = e
            self.show_phone = self.real_phone.replace(self.real_phone[3:7], '****')
        except Exception as e:
            raise ValueError('house365 error: the phone encryption is error')

    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, city_name):
        try:
            self._city = parse.unquote(city_name)
        except Exception as e:
            raise ValueError('house365 error: the city URL encode is error')

    @property
    def days(self):
        return self._days

    @days.setter
    def days(self, days_num):
        self._days = days_num

    @property
    def secret_key(self):
        return self._secret_key

    @secret_key.setter
    def secret_key(self, secret_key_value):
        m = hashlib.new('md5', (self.real_phone + 'house365').encode('utf-8')).hexdigest()
        if secret_key_value != m:
            raise ValueError(" house365 error: the secret key is error ")
        self._secret_key = secret_key_value

    @property
    def sorted_key(self):
        return self._sorted_key

    @sorted_key.setter
    def sorted_key(self, sorted_key_value):
        self._sorted_key = sorted_key_value

    def begin(self):
        result = dict()
        self.redis_images_read()
        self.redis_devices_read()
        self.redis_data_read()
        self.house_action()
        self.get_price()
        result['phone'] = self.phone
        result['phone_show'] = self.show_phone
        result['count'] = self.get_count()
        result['cities'] = self.get_cities()
        result['min_price'] = self.min_price
        result['max_price'] = self.max_price
        result['secret_key'] = self.secret_key
        result['newhouses_scatter_diagram'] = self.get_scatter_diagram()
        result['newhouses'] = self.get_item_detail()
        result['sex'] = self.sex
        result['age'] = self.age
        result.update(self.city_images)
        return result

    @decorator
    def decrytion(self):
        pc = PrpCrypt()
        e = pc.dncrypt(self.phone)
        self.real_phone = e

    def redis_images_read(self):
        city_images = self.crm_r.hget(REDIS_CRM_PREFIX + self.real_phone, self.city)
        if city_images is not None:
            self.city_images = json.loads(city_images.decode('utf-8').replace("'", "\"").replace("nan", "null"))
            if self.city_images['IDCard'] is not None:
                self.sex = IDInformation(self.city_images['IDCard']).get_sex()
                self.age = IDInformation(self.city_images['IDCard']).get_age()

    def redis_data_read(self):
        for deviceid in self.deviceIds:
            datas = self.office_r.lrange(REDIS_NEWHOUSE_PREFIX + deviceid.decode('utf-8'), 0, self.days)
            for data in datas:
                self.data.extend(json.loads(data.decode('utf-8')))
        if len(self.data) == 0:
            raise ValueError(" house365 error: this phone number has no record ")

    def redis_devices_read(self):
        self.deviceIds = self.office_r.smembers(REDIS_PHONEDEVICE_PREFIX + self.real_phone)
        if len(self.deviceIds) == 0:
            raise ValueError(" house365 error: this phone number has no corresponding device number ")

    def house_action(self):
        newhouse_json = json.dumps(self.data, ensure_ascii=False)
        self.df = pd.read_json(newhouse_json, orient='records').dropna(subset=['B_LAT', 'B_LNG', 'PRJ_ITEMNAME'])

    @decorator
    def get_cities(self):
        cities = list(self.df['CITY_NAME'].unique())
        return cities

    def get_price(self):
        df = self.df[self.df['CITY_NAME'] == self.city]
        df_price = df[df['PRICE_SHOW'].str.contains('元/㎡', na=False)]
        if len(df_price) > 0:
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
