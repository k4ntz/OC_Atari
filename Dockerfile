FROM nvcr.io/nvidia/pytorch:23.04-py3
MAINTAINER "Jannis Blüml"

RUN apt-get update -y 

# install ROMs
RUN pip install "autorom[accept-rom-license]" \
&& pip install ale_py \
&& mkdir /root/roms/ \
&& AutoROM --install-dir /root/roms -y \
&& ale-import-roms /root/roms/

RUN cd /root/ \ 
&& git clone https://github.com/k4ntz/OC_Atari.git oc_atari

WORKDIR /root/oc_atari

# install it
RUN cd /root/oc_atari/ \ 
&& pip install -r requirements.txt \
&& python setup.py develop




