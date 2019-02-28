from . import secondhouses
from flask import render_template, request
from redis import Redis
import json
import pandas as pd
import traceback
from . import secondhouse
from . import secondhouseDetail
import hashlib
from ..config import get_config

r = Redis(host=get_config("REDIS_HOST"), port=6379, db=get_config("REDIS_DB"))
# r2 = Redis(host='192.168.10.221', port=6379, db=2)

SECONDHOUSELOG_PREFIX = get_config("SECONDHOUSELOG_PREFIX")
PHONEDEVICE_PREFIX = get_config("PHONEDEVICE_PREFIX")


# @houses.route("/<string:phone>/<string:city>/<int:num>", methods=['GET'])
# def index(phone, num, city):
#     deviceids = r.smembers(PHONEDEVICE_PREFIX + phone)
#     result = list()
#     for deviceid in deviceids:
#         datas = r.lrange(SECONDHOUSELOG_PREFIX + deviceid.decode('utf-8'), 0, num)
#         for data in datas:
#             result.extend(json.loads(data.decode('utf-8')))
#
#     cities, min_price, max_price, newhouses, newhouses_count = newhouse_handle(result, city)
#     return render_template("newhouse/newhouse.html", newhouses=newhouses, userId=phone, num=num, cities=cities,
#                            min_price=min_price, max_price=max_price, newhouses_count=newhouses_count)

@secondhouses.route("/select", methods=['GET'])
def select():
    phone = request.args.get("phone")
    m = hashlib.new('md5', (phone + 'house365').encode('utf-8')).hexdigest()
    return m


@secondhouses.route("/<string:phone>/<string:city>/<int:num>", methods=['GET'])
def index(phone, num, city):
    secret = request.args.get("secret")
    sort_key = request.args.get("sort_key")
    if sort_key is None:
        sort_key = 0
    m = hashlib.new('md5', (phone + 'house365').encode('utf-8')).hexdigest()
    if m == secret:
        deviceids = r.smembers(PHONEDEVICE_PREFIX + phone)
        result = list()
        for deviceid in deviceids:
            datas = r.lrange(SECONDHOUSELOG_PREFIX + deviceid.decode('utf-8'), 0, num)
            for data in datas:
                result.extend(json.loads(data.decode('utf-8')))

        cities, min_price, max_price, newhouses, newhouses_count = newhouse_handle(result, city, sort_key)
        return render_template("newhouse/newhouse.html", newhouses=newhouses, userId=phone, num=num, cities=cities,
                               min_price=min_price, max_price=max_price, newhouses_count=newhouses_count, secret=secret)
    else:
        return "the secret key is wrong"


@secondhouses.route("/<string:phone>/<string:city>/<int:num>/detail", methods=['GET'])
def detail(phone, num, city):
    secret = request.args.get("secret")
    sort_key = request.args.get("sort_key")
    if sort_key is None:
        sort_key = 0
    m = hashlib.new('md5', (phone + 'house365').encode('utf-8')).hexdigest()
    if m == secret:
        deviceids = r.smembers(PHONEDEVICE_PREFIX + phone)
        result = list()
        for deviceid in deviceids:
            datas = r.lrange(SECONDHOUSELOG_PREFIX + deviceid.decode('utf-8'), 0, num)
            for data in datas:
                result.extend(json.loads(data.decode('utf-8')))

        count, avg_price, area, sum_price, toilet, bedroom, livingroom, kitchen = secondhouseDetail_handle(result,
                                                                                                        city,
                                                                                                        sort_key)
        # TODO
        newhouse_json = json.dumps(result, ensure_ascii=False)
        df = pd.read_json(newhouse_json, orient='records')
        object = secondhouseDetail.secondhouseDetail(df, city, sort_key)
        click_frequency_diagram = object.get_click_frequency_diagram()
        avg_price_histogram = object.get_avg_price_histogram()
        sum_price_histogram = object.get_sum_price_histogram()
        area_histogram = object.get_area_histogram()
        toilet_pie = object.get_toilet_pie()
        bedroom_pie = object.get_bedroom_pie()
        livingroom_pie = object.get_livingroom_pie()
        kitchen_pie = object.get_kitchen_pie()
        return render_template("newhouse/secondhouseDetail.html", count=count, avg_price=avg_price, area=area,
                               sum_price=sum_price, toilet=toilet, bedroom=bedroom, livingroom=livingroom,
                               kitchen=kitchen, click_frequency_diagram=click_frequency_diagram,
                               avg_price_histogram=avg_price_histogram, sum_price_histogram=sum_price_histogram,
                               area_histogram=area_histogram, toilet_pie=toilet_pie, bedroom_pie=bedroom_pie,
                               livingroom_pie=livingroom_pie, kitchen_pie=kitchen_pie)
    else:
        return "the secret key is wrong"


def newhouse_handle(newhouse_json, city='南京', sort_key=0):
    try:
        newhouse_json = json.dumps(newhouse_json, ensure_ascii=False)
        df = pd.read_json(newhouse_json, orient='records')
        count = len(df)
        if count == 0:
            return list(), 0, 0, {}, count
        else:
            object = secondhouse.newhouse(df, city, sort_key)
            cities = object.get_cities()
            min_price, max_price = object.get_price()
            datas = object.get_result()
            datas = datas.to_json(orient="records", force_ascii=False)
        return cities, min_price, max_price, datas, count
    except Exception:
        print(traceback.format_exc())
        return list(), 0, 0, {}, count


def secondhouseDetail_handle(newhouse_json, city='南京', sort_key=0):
    try:
        newhouse_json = json.dumps(newhouse_json, ensure_ascii=False)
        df = pd.read_json(newhouse_json, orient='records')
        count = len(df)
        if count == 0:
            return list(), 0, 0, {}, count
        else:
            object = secondhouseDetail.secondhouseDetail(df, city, sort_key)
            count = object.get_sum_count()
            avg_price = object.get_avg_price()
            area = object.get_area()
            sum_price = object.get_sum_price()
            toilet = object.get_toilet()
            bedroom = object.get_bedroom()
            livingroom = object.get_livingroom()
            kitchen = object.get_kitchen()
        return count, avg_price, area, sum_price, toilet, bedroom, livingroom, kitchen
    except Exception:
        print(traceback.format_exc())
        return list(), 0, 0, {}, count


if __name__ == '__main__':
    deviceids = r.smembers('PD^15298383419')
    result = list()
    for deviceid in deviceids:
        datas = r.lrange(SECONDHOUSELOG_PREFIX + deviceid.decode('utf-8'), 0, 30)
        for data in datas:
            result.extend(json.loads(data.decode('utf-8')))
    print(json.dump(result))

    # md5
    # m = hashlib.new('md5', ('18652058969house365').encode('utf-8')).hexdigest()
    # print(m)
