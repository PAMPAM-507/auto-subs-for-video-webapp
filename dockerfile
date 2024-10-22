FROM python:3.11.3-bullseye

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y ffmpeg libpng-dev libjpeg-dev \
    libtiff-dev libmagickwand-dev imagemagick \
    libmagick++-dev vim \
    && apt-get install libpq-dev

RUN apt remove "*imagemagick*" --purge -y && apt autoremove --purge -y

RUN apt-get -qq update && apt-get -qq install -y ffmpeg build-essential

RUN git clone https://github.com/SoftCreatR/imei && \
cd imei && \
chmod +x imei.sh && \
./imei.sh


WORKDIR /subs

COPY . /subs/

RUN pip install --upgrade pip
RUN pip install -r requirements3.11.3.txt

RUN chmod +x /subs/wait-for-postgres.sh


CMD /subs/wait-for-postgres.sh \
    # && python3 ./auto_subs/manage.py migrate \
    && python3 ./auto_subs/manage.py makemigrations \
    && python3 ./auto_subs/manage.py migrate \
    # && python3 ./auto_subs/manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='root').exists() or User.objects.create_superuser('root', 'root@example.com', 'root')" \
    # && python3 ./auto_subs/manage.py loaddata ./auto_subs/fixtures/initialize_db.json \
    && cd ./auto_subs \
    && gunicorn auto_subs.wsgi:application --bind 0.0.0.0:8000 --log-level info


