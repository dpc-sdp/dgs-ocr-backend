FROM python:3.10-alpine3.17

ARG modelid
ENV modelid $modelid

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools wheel
RUN apk add g++ linux-headers libffi-dev # Dependencies for building various Python packages

COPY ./requirements.txt /tmp
RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN mkdir /app
WORKDIR /app
COPY . /app

CMD uwsgi --master \
     --workers 8 \
     --threads 100 \
     --protocol http \
     --socket 0.0.0.0:5000 \
     --module app:app
