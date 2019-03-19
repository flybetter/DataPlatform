from . import newhouses
import pandas as pd
from io import StringIO
import numpy as np
from flask import render_template
import os

# demo
@newhouses.route("/")
def index():
    newhouses_map = get_house_map()
    return render_template("/newhouse_demo/newhouse_map.html", newhouses_map=newhouses_map)


def get_house_map():
    with open(os.path.dirname(os.path.abspath(__file__)) + os.sep + 'newHouse.txt') as f:
        colName = ["PRJ_LISTID", "CHANNEL", "CITY", "CITY_NAME", "PRJ_ITEMNAME", "PRJ_LOC", "PRJ_DECORATE", "PRJ_VIEWS",
                   "B_LNG", "B_LAT", "PRICE_AVG", "PRICE_SHOW"]
        df = pd.read_csv(StringIO(f.read()), names=colName, header=None, delimiter="\t",
                         dtype={'B_LNG': np.str, 'B_LAT': np.str, 'PRJ_LISTID': np.int64})
        df = df[df["CITY"] == 'nj']
    return df.to_json(orient='records', force_ascii=False)


if __name__ == '__main__':
    print(os.getcwd())
