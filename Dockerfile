FROM flybetter/dataplatform:v7
MAINTAINER flybetter@163.com

COPY . /app
WORKDIR /app
#
#RUN apt-get  update
#RUN apt-get install -y apt-transport-https vim iproute2 net-tools ca-certificates curl wget software-properties-common
#RUN apt-get install -q -y openjdk-8-jdk python3-pip libsnappy-dev language-pack-en supervisor vim
#RUN apt-get update && apt-get install -y python3.5-dev python-dev python-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev
RUN pip3 install -r requirements.txt
CMD ["python3","-u","./startup.py"]




