FROM python:slim-buster

COPY backend/requirements.txt .
RUN pip3 install -r requirements.txt

RUN apt-get update && apt-get install -y git make build-essential \
    && git clone https://github.com/hzeller/rpi-rgb-led-matrix.git \
    && cd rpi-rgb-led-matrix \
    && make build-python PYTHON=$(which python3) \
    && make install-python PYTHON=$(which python3) 

WORKDIR /backend