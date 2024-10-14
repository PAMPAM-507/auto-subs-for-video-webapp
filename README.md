# Information system automatically making subtitles, over original video with possibility voicing persons 

## Description
Information system based on Whisper-AI, which can transcription audio, video. User can upload a video after sign up, then maked transcription by whisper. After that google translator translating text. If user check the special box on uploading video form, system will make voicing. Also in system realized most of the standard functions like reset password, change password, authentication by social. User can download video, watch one on system. For correct position subtitles using fuzzy model which develepment by author. That fuzzy model contains two input parameters, one output parameter. For deffazificasii using method of height, rule base implication - prod, rule base aggregation - max. Also the second fuzzy model using for putting voice. The both models use the same methods. Voicing made by gTTS model.

## Short scheme  work
1. System get video from client
2. System handle the video
   1) The first is transcription by whisper
   2) The secodn is Thraslation
   3) Then making voicing if user wanted that
   4) After that go randering
3. User can download and watch video online

![alt text](2024-10-08-20-54-01.gif)

## Using guide

### 1. Creating .env
You need to create .env with constants below
You should put .env in project's root directory

EMAIL_HOST_PASSWORD='...'  
SECRET_KEY='...'  
EMAIL_HOST_USER='...'  

SOCIAL_AUTH_GITHUB_KEY='...'  
SOCIAL_AUTH_GITHUB_SECRET='...'  

SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET='...'  
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY='...'  

Or you can fill in constants in docker-compose.yml

Application will open on 127.0.0.1:8000 or localhost:8000

If you have installed django you can generate SECRET_KEY by this command
```
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 2. Use Docker and Docker-compose
```
docker-compose up
```

### 3. Local installing
First you need to install imagemagick, ffmpeg, python 3.11.3 for linux. If you get some errors related to ffmpeg you'll need to fix them yourself. In docker containers I fixed problems with ffmpeg and imagemagick but in container you can't use GPU for calculating.
Before install requirements it is better to make python virtualenv. I use ROCm for AMD GPU in this project. If you have Nvidia GPU you should go and download torch for your system (https://pytorch.org/). You can use my requirements for cpu even if you don't have AMD GPU. System will work on CPU.
```
python3.11 -m venv venv
```
activate virtual environment
```
. ./venv/bin/activate
```
install requirements for linux
```
pip3 install -r requirements3.11.3rocm.txt
```
After installing requirements you need to start django server, celery, redis. For redis I used docker (REDIS_HOST = 'localhost'
REDIS_PORT = '6380', you can change them in setting.py). You must use commands below in directory with manage.py.
django server
```
python manage.py runserver
```
celery
```
celery -A auto_subs worker --loglevel=info
```

