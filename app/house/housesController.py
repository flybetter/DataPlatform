from app.house import *
from app.house.housesEnity import HOUSES
import urllib
import string


@houses_v1.route("/index", methods=['GET'])
def houses_index():
    secret_key = request.args.get("secret_key")
    phone = request.args.get("phone")
    city = request.args.get("city")
    source = request.args.get("source")
    source_id = request.args.get("source_id")
    session['source'] = source
    session['source_id'] = source_id if source_id is not None else 'null'
    if secret_key is None:
        return "secret_key is missing"
    elif phone is None:
        return "phone is missing"
    elif city is None:
        return "city is missing"
    elif source is None:
        return "source is missing"
    else:
        try:
            houses_entity = HOUSES()
            houses_entity.phone = phone
            houses_entity.city = city
        except Exception as e:
            traceback.print_exc()
        return render_template("house_v1/house.html", secret_key=secret_key, phone=houses_entity.phone,
                               show_phone=houses_entity.show_phone,
                               city=houses_entity.city)


@houses_v1.route("/api", methods=['GET'])
def houses_api():
    secret_key = request.args.get("secret_key")
    sorted_key = request.args.get("sorted_key")
    phone = request.args.get("phone")
    city = request.args.get("city")
    days = request.args.get("days")
    result = dict()
    company = companyHouses(city)
    try:
        houses_entity = HOUSES()
        houses_entity.phone = phone
        houses_entity.company = company
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


def companyHouses(city):
    url = 'http://crm.house365.com/api/directProject/projects?city=' + city
    s = urllib.parse.quote(url, safe=string.printable)
    response = urllib.request.urlopen(s)
    jsonBody = json.loads(response.read().decode(encoding='utf-8'))
    company = list(map(lambda x: x['project_name'], jsonBody))
    return company

    # body = request.urlopen(
    #     "http://crm.house365.com/api/directProject/projects?city={}".format(str(city, encoding='unicode')))
    # print(body)


if __name__ == '__main__':
    companyHouses('南京')

    # md5
    # m = hashlib.new('md5', ('18652058969house365').encode('utf-8')).hexdigest()
    # print(m)
