FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y python3-pip python3-dev libglib2.0-0 libsm6 libxrender1 libxext6 \
    && cd /usr/local/bin \
    && ln -s /usr/bin/python3 python \
    && pip3 install --upgrade pip

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/requirements.txt
RUN pip3 install -r requirements.txt