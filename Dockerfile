FROM nvidia/cuda:9.2-base-ubuntu18.04

ENV TZ=Europe/Vienna
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && \
    apt-get install -y sudo wget bash zip git rsync build-essential software-properties-common ca-certificates xvfb vim

RUN apt-get install -y python3.6-venv python3.6-dev python3-pip

RUN apt-get install -y libsm6 libxrender1 libfontconfig1 libpython3.6-dev libopenblas-dev

RUN apt-get install -y meshlab

RUN python3.6 -m pip install numpy \
                             scipy \
                             matplotlib \
                             tensorboardX==1.4 \
                             scikit-learn \
                             cython \
                             trimesh \
							 scikit-image \
							 future \
                             tqdm \
                             opencv-python==3.3.1.11 \
                             yacs

RUN python3.6 -m pip install torch==0.4.1 torchvision==0.2.1

# ==================================================================
# config & cleanup
# ------------------------------------------------------------------

RUN ldconfig && \
    apt-get clean && \
    apt-get autoremove && \
    rm -rf /var/lib/apt/lists/* /tmp/* ~/*
