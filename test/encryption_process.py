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
    phone = '13611572818'
    city = '南京'
    v1 = md5_algorithm(phone)
    v2 = AES_algorithm_encryption(phone).decode('utf-8')
    v3 = URL_encode_encryption(city)
    print(md5_algorithm(phone))
    print(AES_algorithm_encryption(phone).decode('utf-8'))
    print(URL_encode_encryption(city))
    print(
        "http://127.0.0.1:5000/v1/houses/api?phone={0}&city={1}&days=30&secret_key={2}&sorted_key=1".format(v2, v3, v1))

    print("http://127.0.0.1:5000/houses/{0}/南京/30?secret={1}".format(phone, v1))

    print("http://127.0.0.1:5000/v1/houses/index?phone={0}&city={1}&secret_key={2}".format(v2, v3, v1))
