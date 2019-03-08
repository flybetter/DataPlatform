from app.house import *

r = Redis(host=REDIS_HOST, db=REDIS_DB)


@houses.route("/<string:phone>/<string:city>/<int:num>", methods=['GET'])
def index(phone, num, city):
    secret = request.args.get("secret")
    sort_key = request.args.get("sort_key")
    if sort_key is None:
        sort_key = 0
    m = hashlib.new('md5', (phone + 'house365').encode('utf-8')).hexdigest()
    if m == secret:
        deviceids = r.smembers(REDIS_PHONEDEVICE_PREFIX + phone)
        result = list()
        for deviceid in deviceids:
            datas = r.lrange(REDIS_NEWHOUSE_PREFIX + deviceid.decode('utf-8'), 0, num)
            for data in datas:
                result.extend(json.loads(data.decode('utf-8')))

        newhouse_json = json.dumps(result, ensure_ascii=False)
        df = pd.read_json(newhouse_json, orient='records').dropna(subset=['B_LAT', 'B_LNG', 'PRJ_ITEMNAME'])
        df.to_csv('demo.csv')
        object = newhouse.newhouse(df, city, sort_key)
        cities = object.get_cities()
        min_price, max_price = object.get_price()
        newhouses = object.get_item_detail()
        newhouses_count = object.get_count()
        newhouses_scatter_diagram = object.get_scatter_diagram()

        return render_template("house/house.html", newhouses=newhouses, userId=phone, num=num, cities=cities,
                               min_price=min_price, max_price=max_price, newhouses_count=newhouses_count, secret=secret,
                               newhouses_scatter_diagram=newhouses_scatter_diagram)
    else:
        return "the secret key is wrong"


@houses.route("/<string:phone>/<string:city>/<int:num>/detail", methods=['GET'])
def detail(phone, num, city):
    secret = request.args.get("secret")
    sort_key = request.args.get("sort_key")
    if sort_key is None:
        sort_key = 0
    m = hashlib.new('md5', (phone + 'house365').encode('utf-8')).hexdigest()
    if m == secret:
        deviceids = r.smembers(REDIS_PHONEDEVICE_PREFIX + phone)
        result = list()
        for deviceid in deviceids:
            datas = r.lrange(REDIS_NEWHOUSE_PREFIX + deviceid.decode('utf-8'), 0, num)
            for data in datas:
                result.extend(json.loads(data.decode('utf-8')))

        count, avg_price, area, sum_price, toilet, bedroom, livingroom, kitchen = newhouseDetail_handle(result,
                                                                                                        city,
                                                                                                        sort_key)
        # TODO
        newhouse_json = json.dumps(result, ensure_ascii=False)
        df = pd.read_json(newhouse_json, orient='records')
        object = newhouseDetail.newhouseDetail(df, city, sort_key)
        click_frequency_diagram = object.get_click_frequency_diagram()
        avg_price_histogram = object.get_avg_price_histogram()
        sum_price_histogram = object.get_sum_price_histogram()
        area_histogram = object.get_area_histogram()
        toilet_pie = object.get_toilet_pie()
        bedroom_pie = object.get_bedroom_pie()
        livingroom_pie = object.get_livingroom_pie()
        kitchen_pie = object.get_kitchen_pie()
        return render_template("house/newhouseDetail.html", count=count, avg_price=avg_price, area=area,
                               sum_price=sum_price, toilet=toilet, bedroom=bedroom, livingroom=livingroom,
                               kitchen=kitchen, click_frequency_diagram=click_frequency_diagram,
                               avg_price_histogram=avg_price_histogram, sum_price_histogram=sum_price_histogram,
                               area_histogram=area_histogram, toilet_pie=toilet_pie, bedroom_pie=bedroom_pie,
                               livingroom_pie=livingroom_pie, kitchen_pie=kitchen_pie)
    else:
        return "the secret key is wrong"


def newhouseDetail_handle(newhouse_json, city='南京', sort_key=0):
    try:
        newhouse_json = json.dumps(newhouse_json, ensure_ascii=False)
        df = pd.read_json(newhouse_json, orient='records')
        count = len(df)
        if count == 0:
            return list(), 0, 0, {}, count
        else:
            object = newhouseDetail.newhouseDetail(df, city, sort_key)
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
    pass
