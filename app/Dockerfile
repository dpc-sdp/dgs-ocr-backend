FROM python:3.10-alpine3.17
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools wheel
RUN apk add g++ linux-headers libffi-dev # Dependencies for building various Python packages

COPY ./requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

RUN mkdir /app
WORKDIR /app
COPY . /app

CMD ["gunicorn", \
     "-b", "0.0.0.0:5000", \
     "app:app", \
     "--access-logfile", "-", "--reload"]
