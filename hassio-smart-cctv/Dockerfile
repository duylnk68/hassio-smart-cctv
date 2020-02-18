#ARG BUILD_FROM
FROM debian:latest

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Avoid tzdata asks for "Geographic area" and "Time zone"
ARG DEBIAN_FRONTEND=noninteractive

# Initialize package
RUN apt-get update && apt-get install -y openssh-server
RUN apt-get install -y python3-pip python3-opencv libxml2-dev libxslt-dev
RUN python3 -m pip install --upgrade pip
RUN echo "[global]" >> /etc/pip.conf
RUN echo "extra-index-url=https://www.piwheels.org/simple" >> /etc/profile
RUN pip3 install opencv-contrib-python
RUN pip3 install onvif_zeep
RUN pip3 install xmltodict
RUN pip3 install pyyaml

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
