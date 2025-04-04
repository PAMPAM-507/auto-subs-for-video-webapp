FROM python:3.11.3-bullseye
# FROM python:3.11.3-alpine
# FROM python:3.11.3-slim

WORKDIR /subs

COPY . /subs/

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y \
        ffmpeg \
        libpng-dev \
        libjpeg-dev \
        libtiff-dev \
        libmagickwand-dev \
        imagemagick \
        libmagick++-dev \
        vim \
        libpq-dev \
        build-essential \
    && apt-get remove -y "*imagemagick*" --purge \
    && apt-get autoremove -y --purge \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/* &&\
    pip install --upgrade pip && \
    pip install -r requirements3.11.3.txt && \
    chmod +x /subs/wait-for-postgres.sh && \
    git clone https://github.com/SoftCreatR/imei && \
    cd imei && \
    chmod +x imei.sh && \
    ./imei.sh

# RUN pip install --upgrade pip && \
#     pip install -r requirements3.11.3.txt && \
#     chmod +x /subs/wait-for-postgres.sh && \
#     git clone https://github.com/SoftCreatR/imei && \
#     cd imei && \
#     chmod +x imei.sh && \
#     ./imei.sh

ENV IMAGEMAGICK_BINARY=/usr/bin/convert


CMD /subs/wait-for-postgres.sh && \
    python3 ./proj/manage.py migrate && \
    python3 ./auto_subs/manage.py makemigrations && \
    python3 ./auto_subs/manage.py migrate && \
    python3 ./auto_subs/manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='root').exists() or User.objects.create_superuser('root', 'root@root.ru', 'root')" && \
    python3 ./auto_subs/manage.py loaddata /subs/initialize_db.json && \
    celery --workdir=./auto_subs -A auto_subs worker --loglevel=INFO & \
    cd ./auto_subs && \
    gunicorn auto_subs.wsgi:application --bind 0.0.0.0:8000 --log-level info


