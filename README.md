# Information system automatically making subtitles, over original video with possibility voicing persons 

## Description
Information system based on Whisper-AI, which can transcription audio, video. User can upload a video after sign up, then maked transcription by whisper. Ffter that google translator translating text. If user check the special box on uploading video form, system will make voicing. Also in system realized most of the standard functions like reset password, change password, authentication by social. User can download video, watch one on system. For correct position subtitles using fuzzy model which develepment by autor. That fuzzy model contains two input parameters, one output parameter. For deffazificasii using method of height, rule base implication - prod, rule base aggregation - max. Also the second fuzzy model using for putting voice. The both models use the same methods. Voicing made by gTTS model.

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
### 1. Use Docker and Docker-compose
```
docker-compose up --build
```

### 2. Local installing
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

