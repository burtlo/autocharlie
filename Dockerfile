FROM ubuntu:16.04

RUN apt-get update

# Local Development
#
#   To provide support for testing sftp locally the openssh-server is required
#   and it needs to be configured to allow root to login with a password
#   and to ensure that the root user has a password that is known
#
#   NOTE: `service ssh start` still needs to be executed upon entrance
#
RUN apt-get install openssh-server -y
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN echo "root:ubuntu" | chpasswd

# Application Dependencies
RUN apt-get install openssh-client 
RUN apt-get install python2.7 python-pip -y
RUN pip install requests python-dateutil pysftp
RUN apt-get install sox libsox-fmt-all -y

# Local Developmnet
#
#    Create a path in the image, declare it as a volume, and then make it
#    the default place to work.
#
RUN mkdir -p /share
VOLUME ["/share"]
WORKDIR /share
