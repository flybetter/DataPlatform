import configparser
import os

ENV = 'development'


def get_config(name):
    con = configparser.ConfigParser()
    con.read(os.path.dirname(os.path.abspath(__file__)) + os.sep + 'settings.ini')
    return con.get(ENV, name)


if __name__ == '__main__':
    print(get_config("REDIS_HOST"))
