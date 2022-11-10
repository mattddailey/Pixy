FROM python:slim-buster

COPY backend/requirements.txt .
RUN pip3 install -r requirements.txt

WORKDIR /backend