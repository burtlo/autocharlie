FROM ubuntu:16.04

RUN apt-get update
# NOTE: To provide support for testing sftp locally
# RUN apt-get install openssh-client openssh-server -y
# TODO: In /etc/ssh/sshd_config change 'PermitRootLogin prohibit-password' to 'PermitRootLogin yes'
# RUN echo "Docker!" | passwd --stdin root
RUN apt-get install python2.7 python-pip -y
RUN pip install requests python-dateutil pysftp
RUN apt-get install sox libsox-fmt-all -y

RUN mkdir -p /share
VOLUME ["/share"]
WORKDIR /share
