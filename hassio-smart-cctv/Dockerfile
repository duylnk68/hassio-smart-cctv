ARG BUILD_FROM
FROM ${BUILD_FROM}

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Avoid tzdata asks for "Geographic area" and "Time zone"
ARG DEBIAN_FRONTEND=noninteractive

# Initialize package
RUN apt-get update && apt-get install -y openssh-server python3-pip python3-opencv
RUN pip3 install opencv-contrib-python
RUN pip3 install onvif_zeep
RUN pip3 install xmltodict

# Initialize OpenSSH
RUN mkdir /var/run/sshd
RUN echo 'root:root' | chpasswd
RUN sed -ri 's/^#?PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

CMD ["/usr/sbin/sshd", "-D"]
