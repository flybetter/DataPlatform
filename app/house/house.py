from . import houses
from flask import render_template
from redis import Redis
import json

r = Redis(host='192.168.10.221', port=6379, db=1)

NEWHOUSELOG_PREFIX = "NHLOG^"
PHONEDEVICE_PREFIX = "PD^"


@houses.route("/<string:phone>/<int:num>", methods=['GET'])
def index(phone, num):
    deviceids = r.smembers(PHONEDEVICE_PREFIX + phone)
    result = list()
    for deviceid in deviceids:
        datas = r.lrange(NEWHOUSELOG_PREFIX + deviceid.decode('utf-8'), 0, num)
        for data in datas:
            result.extend(json.loads(data.decode('utf-8')))

    return render_template("house/house.html", newhouses=json.dumps(result, ensure_ascii=False), userId=phone, num=num)
