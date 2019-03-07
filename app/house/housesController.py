from app.house import *
from app.house.housesEnity import HOUSES


@houses_v1.route("/api", methods=['GET'])
def houses_api():
    secret_key = request.args.get("secret_key")
    sorted_key = request.args.get("sorted_key")
    phone = request.args.get("phone")
    city = request.args.get("city")
    days = request.args.get("days")
    result = dict()
    try:
        houses_entity = HOUSES()
        houses_entity.phone = phone
        houses_entity.city = city
        houses_entity.days = days
        houses_entity.sorted_key = sorted_key
        houses_entity.secret_key = secret_key
        data = houses_entity.begin()
        result['result'] = int(1)
        result['data'] = data
    except Exception as e:
        result['result'] = 0
        result['msg'] = str(e)

    return json.dumps(result, ensure_ascii=False)


# m = hashlib.new('md5', (phone + 'house365').encode('utf-8')).hexdigest()
# if m != secret:
#     return "the secret key is wrong"
# else:
#     pc = PrpCrypt()
#     phone = pc.decrypt(phone)
#     deviceids = r.smembers(REDIS_PHONEDEVICE_PREFIX + phone)
#     result = list()
#     for deviceid in deviceids:
#         datas = r.lrange(REDIS_NEWHOUSE_PREFIX + deviceid.decode('utf-8'), 0, days)
#         for data in datas:
#             result.extend(json.loads(data.decode('utf-8')))
#
#     newhouse_json = json.dumps(result, ensure_ascii=False)
#     df = pd.read_json(newhouse_json, orient='records')
#     object = newhouse.newhouse(df, city, sort_key)
#     cities = object.get_cities()
#     min_price, max_price = object.get_price()
#     newhouses = object.get_item_detail()
#     newhouses_count = object.get_count()
#     newhouses_scatter_diagram = object.get_scatter_diagram()
#
#     return render_template("house/house.html", newhouses=newhouses, userId=phone, days=days, cities=cities,
#                            min_price=min_price, max_price=max_price, newhouses_count=newhouses_count,
#                            secret=secret,
#                            newhouses_scatter_diagram=newhouses_scatter_diagram)

if __name__ == '__main__':
    pass

    # md5
    # m = hashlib.new('md5', ('18652058969house365').encode('utf-8')).hexdigest()
    # print(m)
