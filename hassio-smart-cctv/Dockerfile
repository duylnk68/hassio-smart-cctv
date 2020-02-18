#ARG BUILD_FROM
FROM debian:latest

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Avoid tzdata asks for "Geographic area" and "Time zone"
ARG DEBIAN_FRONTEND=noninteractive

# Initialize package
#ARG BUILD_ARCH=amd64
RUN apt-get update && apt-get install -y openssh-server
RUN apt-get install -y python3-pip python3-opencv libxml2-dev libxslt-dev
RUN python3 -m pip install --upgrade pip
#RUN apt-get install -y libtiff5 libpango-1.0-0 libavcodec-dev libgdk-pixbuf2.0-0 libjasper1-dev libqt4-test libpangocairo-1.0-0 libswscale5-dev libilmbase23-dev libatk1.0-0 libgtk-3-0 libqtcore4 libcairo2 libwebp6 libavutil56-dev libcairo-gobject2 libopenexr23-dev libqtgui4 libavformat58-dev
#RUN pip3 install opencv-contrib-python
#RUN pip3 install onvif_zeep
#RUN pip3 install xmltodict
#RUN pip3 install pyyaml

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
ADD src $HOME

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
