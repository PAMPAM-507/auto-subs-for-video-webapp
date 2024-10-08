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

## Using guide
### 1. Use Docker and Docker-compose
```
docker-compose up --build
```

### 2. Local installing
First you need to install imagemagick, ffmpeg, python 3.11.3 for linux. If you get some errors related to ffmpeg you'll need to fix them yourself.
Before install requirements it is better to make python virtualenv.
```
python3.11 -m venv venv
```
```
. ./venv/bin/activate
```
