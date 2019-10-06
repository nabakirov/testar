FROM python:alpine


RUN set -ex && mkdir /app && mkdir /data
WORKDIR /app
COPY . /app
RUN apk add --no-cache --virtual .build-deps \
    ca-certificates gcc postgresql-dev linux-headers musl-dev \
    libffi-dev jpeg-dev zlib-dev

RUN pip3 install pipenv
RUN set -ex && pipenv install --deploy --system

