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
                                         libjpeg62 libwebp-dev libtiff-dev \
                                         libavcodec-dev libavformat-dev libswscale-dev \
                                         libqtgui4 libqt4-test libqtcore4 \
                                         libgstreamer1.0-dev \
                                         git cmake

RUN python3 -m pip install --upgrade pip
RUN echo "[global]" > /etc/pip.conf \
    && echo "extra-index-url=https://www.piwheels.org/simple" >> /etc/pip.conf

RUN pip3 install opencv-python==4.1.0.25 \
                 opencv-contrib-python==4.1.0.25 \
                 onvif_zeep \
                 xmltodict \
                 pyyaml

RUN cd /tmp \
    && git clone https://github.com/mdadams/jasper \
    && cd jasper \
    && cmake . -DALLOW_IN_SOURCE_BUILD=1 \
    && make && make install \
    && rm -rf jasper \
    && ln -s /usr/local/lib/libjasper.so.4 /usr/lib/libjasper.so.1

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
