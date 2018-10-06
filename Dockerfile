FROM ubuntu:14.04
MAINTAINER anyone

RUN sed -i'' 's/archive\.ubuntu\.com/us\.archive\.ubuntu\.com/' /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y build-essential unzip wget libssl-dev libffi-dev curl
RUN apt-get install -y python3-dev python3-setuptools
RUN apt-get install -y libjpeg-dev
RUN apt-get install -y libtiff5-dev
RUN apt-get install -y libjpeg8-dev
RUN apt-get install -y zlib1g-dev
RUN apt-get install -y libfreetype6-dev
RUN apt-get update
RUN apt-get install -y liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk
RUN apt-get install -y software-properties-common && add-apt-repository -y ppa:fkrull/deadsnakes && apt-get update
RUN apt-get install -y python3.5 python3.5-dev libpq-dev libpq-dev
RUN wget https://bootstrap.pypa.io/get-pip.py && sudo python3.5 get-pip.py
RUN apt-get install -y nginx
RUN wget https://releases.hashicorp.com/consul/0.6.4/consul_0.6.4_linux_amd64.zip
RUN unzip *.zip && rm *.zip
RUN pip3 install uwsgi
RUN apt-get install -y postgresql-server-dev-all

ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ADD conf /conf
ADD ContactBook /ContactBook
ADD contact_book /contact_book
ADD manage.py /manage.py

ADD startProcess.sh /startProcess.sh
RUN chmod +x /startProcess.sh
CMD /startProcess.sh
