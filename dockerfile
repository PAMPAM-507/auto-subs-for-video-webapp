FROM python:3.11.3-bullseye

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y ffmpeg libpng-dev libjpeg-dev \
    libtiff-dev libmagickwand-dev imagemagick \
    libmagick++-dev vim

RUN apt remove "*imagemagick*" --purge -y && apt autoremove --purge -y

RUN apt-get -qq update && apt-get -qq install -y ffmpeg build-essential

RUN git clone https://github.com/SoftCreatR/imei && \
cd imei && \
chmod +x imei.sh && \
./imei.sh


WORKDIR /subs

COPY requirements3.11.3.txt .
RUN pip install -r requirements3.11.3rocm.txt

COPY . /subs/


