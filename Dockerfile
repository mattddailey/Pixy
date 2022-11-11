FROM python:slim-buster

RUN apt-get update && apt-get install -y python3-pil git make build-essential

COPY backend/requirements.txt .
RUN pip3 install -r requirements.txt

RUN $(which python3) -m pip install Pillow \
    && git clone https://github.com/hzeller/rpi-rgb-led-matrix.git \
    && cd rpi-rgb-led-matrix \
    && make build-python PYTHON=$(which python3) \
    && make install-python PYTHON=$(which python3) 

WORKDIR /backend