import configparser
import os


# ENV = 'develop'


def get_config(name):
    env = os.getenv('active', 'production')
    con = configparser.ConfigParser()
    con.read(os.path.dirname(os.path.abspath(__file__)) + os.sep + 'settings.ini')
    return con.get(env, name)


if __name__ == '__main__':
    print(get_config("REDIS_HOST"))
