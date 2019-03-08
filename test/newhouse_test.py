import pandas as pd
from io import StringIO
import numpy as np
import os
import hashlib
import re
from urllib import parse
import json


def get_all_houses():
    with open('newHouse.txt') as f:
        colName = ["PRJ_LISTID", "CHANNEL", "CITY", "CITY_NAME", "PRJ_ITEMNAME", "PRJ_LOC", "PRJ_DECORATE", "PRJ_VIEWS",
                   "B_LNG", "B_LAT", "PRICE_AVG", "PRICE_SHOW"]
        df = pd.read_csv(StringIO(f.read()), names=colName, header=None, delimiter="\t",
                         dtype={'B_LNG': np.str, 'B_LAT': np.str, 'PRJ_LISTID': np.int64})
        df = df[df["CITY"] == 'nj']
        print(df.loc[:, ['PRJ_ITEMNAME', "CITY", 'B_LNG', 'B_LAT']])


if __name__ == '__main__':
    # print(os.path.dirname(os.path.abspath(__file__)))
    # print(hashlib.new('md5', '13305181837house365'.encode('utf-8')).hexdigest())
    # print(hashlib.new('md5', '13675184898house365'.encode('utf-8')).hexdigest())
    # print(hashlib.new('md5', '18013960786house365'.encode('utf-8')).hexdigest())
    # print(hashlib.new('md5', '19951953059house365'.encode('utf-8')).hexdigest())
    # print(hashlib.new('md5', '15212211618house365'.encode('utf-8')).hexdigest())
    #
    # print(re.sub(u'[\u4E00-\u9FA5]', '', '约149.12万元'))

    cc = dict()
    cc['aaa'] = None
    print(json.dumps(cc))

    aa = "{'kitchen': nan, 'area': nan, 'sum_price': nan, 'IDCard': nan, 'top_item_name': '绿城招商诚园', 'userId': nan, 'toliet': nan, 'livingroom': nan, 'bedroom': nan, 'avg_price': 18350.25}"
    print(json.loads(aa.replace("'", "\"")))
