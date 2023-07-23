FROM ubuntu:20.04

WORKDIR /workdir

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Berlin
RUN apt-get update && apt-get install -y --no-install-recommends python3-pip python3-venv python3-tk git
RUN python3 -m venv .venv
ENV PATH="/workdir/.venv/bin:$PATH"


COPY requirements.txt requirements.txt
RUN pip install -U pip
RUN pip install -r requirements.txt
RUN pip install opencv-python-headless

COPY train.py train.py
RUN mkdir "baseline_logs"
RUN mkdir "baseline_checkpoints"
ENTRYPOINT ["python3", "-u" , "train.py"]