FROM python:3.9.9

RUN apt-get update -y
RUN apt-get upgrade -y

WORKDIR /subs

COPY ./subs/tasks.py ./subs
COPY ./subs/translator.py ./subs
COPY ./subs/subs.py ./subs
COPY ./subs/requirements.txt ./subs
