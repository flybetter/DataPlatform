FROM flybetter/dataplatform:v9
MAINTAINER flybetter@163.com

COPY . /app
WORKDIR /app
#
#RUN apt-get  update
#RUN apt-get install -y apt-transport-https vim iproute2 net-tools ca-certificates curl wget software-properties-common
#RUN apt-get install -q -y openjdk-8-jdk python3-pip libsnappy-dev language-pack-en supervisor vim
#RUN apt-get update && apt-get install -y python3.5-dev python-dev python-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev

ENV active="production"
RUN pip3 install -r requirements.txt
CMD ["python3","-u","./startup.py"]

#sudo docker run -p 7999:5000 --env active='develop' flybetter/dataplatform:v10



#http://202.102.74.62:8000/v1/houses/index?phone=5f5fb63deaea1811af93a7516305f75a&city=南京&secret_key=a405d6792529144fe8bd7e340b3a7e37&source=1&source_id=8906443&nsukey=X1hXZzbEZ2YyQBlskJEE8ls6sipt%2FT2xz9aWGtC0YhS5hfdEnp7%2Fbo1TH3%2BocXetn6L8%2BLrjylfIXtfNu0J31aJ8TIC%2B35uCnORHmy9YIJOpiM01lfVucliKd7Wp1jagkN%2FKCzQb2Hu83HcquFPbKxPabVbH27Fg6mBWBpNON9fkmqA403oUOlPReJpb7%2FYlfUhw59J%2BSo4wjL2fBCqWVg%3D%3D



#http://127.0.0.1:5000/v1/houses/index?phone=5f5fb63deaea1811af93a7516305f75a&city=南京&secret_key=a405d6792529144fe8bd7e340b3a7e37&source=1&source_id=8906443&nsukey=X1hXZzbEZ2YyQBlskJEE8ls6sipt%2FT2xz9aWGtC0YhS5hfdEnp7%2Fbo1TH3%2BocXetn6L8%2BLrjylfIXtfNu0J31aJ8TIC%2B35uCnORHmy9YIJOpiM01lfVucliKd7Wp1jagkN%2FKCzQb2Hu83HcquFPbKxPabVbH27Fg6mBWBpNON9fkmqA403oUOlPReJpb7%2FYlfUhw59J%2BSo4wjL2fBCqWVg%3D%3D


#http://192.168.10.221:7999/v1/houses/index?phone=5f5fb63deaea1811af93a7516305f75a&city=南京&secret_key=a405d6792529144fe8bd7e340b3a7e37&source=1&source_id=8906443&nsukey=X1hXZzbEZ2YyQBlskJEE8ls6sipt%2FT2xz9aWGtC0YhS5hfdEnp7%2Fbo1TH3%2BocXetn6L8%2BLrjylfIXtfNu0J31aJ8TIC%2B35uCnORHmy9YIJOpiM01lfVucliKd7Wp1jagkN%2FKCzQb2Hu83HcquFPbKxPabVbH27Fg6mBWBpNON9fkmqA403oUOlPReJpb7%2FYlfUhw59J%2BSo4wjL2fBCqWVg%3D%3D