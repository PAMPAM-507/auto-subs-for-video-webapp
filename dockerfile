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

# RUN apt-get install "linux-headers-$(uname -r)" "linux-modules-extra-$(uname -r)"
# RUN usermod -a -G render,video $LOGNAME
# RUN wget https://repo.radeon.com/amdgpu-install/6.2/ubuntu/noble/amdgpu-install_6.2.60200-1_all.deb
# RUN add-apt-repository -y -s deb http://security.ubuntu.com/ubuntu jammy main universe
# RUN aptget install ./amdgpu-install_6.2.60200-1_all.deb
# RUN apt-get update
# RUN apt-get install amdgpu-dkms rocm



RUN pip install --upgrade pip
# RUN pip install pytorch-triton-rocm
# RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.1
RUN pip install -r requirements3.11.3.txt


COPY . /subs/


