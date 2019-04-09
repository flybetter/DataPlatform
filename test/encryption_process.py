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
    # phone = '13236527011'

    phones = list()
    phones.append('13002593669')
    phones.append('13003423756')
    phones.append('13016972890')
    phones.append('13148493156')
    phones.append('18005151618')
    phones.append('13301596858')
    # 异常数据
    phones.append('13337813226')
    phones.append('18652058969')
    phones.append('13404162426')
    phones.append('18652058969')
    phones.append('18652058969')
    phones.append('13500000001')


    temp_url = "192.168.10.221:5000"
    # temp_url = "202.102.83.162:8000"
    # temp_url = "192.168.10.221:8000"
    # temp_url = "127.0.0.1:5000"

    for simple in phones:
        city = '南京'
        print(simple)
        # print(type(simple))
        v1 = md5_algorithm(simple)
        v2 = AES_algorithm_encryption(simple).decode('utf-8')
        v3 = URL_encode_encryption(city)

        # print(parse.unquote(v3))
        # print(md5_algorithm(simple))
        # print(AES_algorithm_encryption(simple).decode('utf-8'))
        # print(URL_encode_encryption(city))
        # print(
        #     "http://" + temp_url + "/v1/houses/api?phone={0}&city={1}&days=30&secret_key={2}&sorted_key=1&source=1&source_id=3232".format(
        #         v2, v3,
        #         v1))
        # print("http://" + temp_url + "/houses/{0}/{1}/30?secret={2}".format(simple, v3, v1))

        print(
            "http://" + temp_url + "/v1/houses/index?phone={0}&city={1}&secret_key={2}&source=1&source_id=3232".format(
                v2, v3, v1))

        print("")
