from multiprocessing import Pool, Process, Queue
import urllib.request as request
import time


def baidu_url():
    response = request.urlopen(
        "http://192.168.10.221:5000/v1/houses/api?phone=1e527645419a904de346bc7981a8935c&city=%E5%8D%97%E4%BA%AC&days=30&secret_key=920a3bfab8649eb377713afbae265b50&sorted_key=1")
    print(response)


def test(key):
    for i in range(100000):
        baidu_url()
        print(key + ":" + str(i))


if __name__ == '__main__':
    p1 = Process(target=test, args=("one",))
    p2 = Process(target=test, args=('two',))
    p3 = Process(target=test, args=('three',))

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()
