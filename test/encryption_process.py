import hashlib
from app.tools.prpcrypt import PrpCrypt
from urllib import parse


def md5_algorithm(phone):
    m = hashlib.new('md5', (phone + 'house365').encode('utf-8')).hexdigest()
    return m


def AES_algorithm_encryption(phone):
    pc = PrpCrypt()
    return pc.encrypt(phone)


def URL_encode_encryption(city):
    return parse.quote(city)


if __name__ == '__main__':
    phone = '13057593972'
    city = '南京'
    print(md5_algorithm(phone))
    print(AES_algorithm_encryption(phone).decode('utf-8'))
    print(URL_encode_encryption(city))
