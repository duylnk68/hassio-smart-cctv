#ARG BUILD_FROM
FROM debian:latest

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Avoid tzdata asks for "Geographic area" and "Time zone"
ARG DEBIAN_FRONTEND=noninteractive

# Initialize package
RUN apt-get update && apt-get install -y openssh-server screen nano python3-pip \
                                         libxml2-dev libxslt-dev \ 
                                         libatlas3-base libopenexr-dev libilmbase-dev \
                                         libjpeg62 libopenjp2-7 libtiff-dev

RUN python3 -m pip install --upgrade pip
RUN echo "[global]" > /etc/pip.conf \
    && echo "extra-index-url=https://www.piwheels.org/simple" >> /etc/pip.conf

RUN pip3 install https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp37-cp37m-linux_armv7l.whl \
                 onvif_zeep \
                 xmltodict \
                 pyyaml

# Initialize OpenSSH
RUN mkdir /var/run/sshd
RUN echo 'root:root' | chpasswd
RUN sed -ri 's/^#?PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

# Copy src to $HOME
ADD src /root
ADD start.sh /root

EXPOSE 22
RUN chmod +x /root/start.sh
CMD ["/root/start.sh"]
