from multiprocessing import Process, Queue, Pool
import pymysql
from app.config import get_config


class BuriedPoint(object):

    @staticmethod
    def save_sql(phone, city, soure, source_id, result):
        host = get_config('CRM_MYSQL_HOST')
        user = get_config('CRM_MYSQL_USER')
        password = get_config('CRM_MYSQL_PASSWORD')
        db = get_config('CRM_MYSQL_DB')
        conn = pymysql.connect(host=host, port=3306, user=user, password=password, db=db)
        sql = "insert into phone_profile_log (PHONE,CITY,SOURCE,SOURCE_ID,BEDROOM,AVG_PRICE,SUM_PRICE,KITCHEN,TOLIET,LIVINGROOM,AREA)values (%s,'%s',%s,%s,%s,%s,%s,%s,%s,%s,%s)" % (
            phone, city, soure, source_id, BuriedPoint.get_default(result['bedroom']),
            BuriedPoint.get_default(result['avg_price']),
            BuriedPoint.get_default(result['sum_price']), BuriedPoint.get_default(result['kitchen']),
            BuriedPoint.get_default(result['toliet']), BuriedPoint.get_default(result['livingroom']),
            BuriedPoint.get_default(result['area']))
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()

    @staticmethod
    def get_default(value):
        return value if value is not None else 'null'

    @staticmethod
    def begin(*args):
        p = Process(target=BuriedPoint.save_sql, args=args)
        p.start()
        # p.join()


if __name__ == '__main__':
    bp = BuriedPoint()
