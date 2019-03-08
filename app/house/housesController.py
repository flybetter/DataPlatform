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
        traceback.print_exc()
        result['result'] = 0
        result['msg'] = str(e)

    return jsonify(result)


if __name__ == '__main__':
    pass

    # md5
    # m = hashlib.new('md5', ('18652058969house365').encode('utf-8')).hexdigest()
    # print(m)
