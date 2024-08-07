FROM python:3.11-slim

RUN apt-get update -y
RUN apt-get upgrade -y

WORKDIR /subs
COPY . /subs/

RUN pip install -r requirements.txt
