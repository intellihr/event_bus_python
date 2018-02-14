FROM python:3.6-alpine

MAINTAINER Soloman Weng "soloman.weng@intellihr.com.au"
ENV REFRESHED_AT 2018-02-14

RUN apk add --update make && rm -rf /var/cache/apk/*

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ADD ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

ADD . /usr/src/app
