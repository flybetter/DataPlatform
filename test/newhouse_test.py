import pandas as pd
from io import StringIO
import numpy as np
import os
import hashlib


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
    print(hashlib.new('md5', '13305181837house365'.encode('utf-8')).hexdigest())
