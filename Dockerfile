FROM ubuntu:latest

ARG remote_destination
ENV remote_destination_env=${remote_destination}

ADD ingestion.py /root/
ADD config.toml /root/
ADD python_dependencies.txt /root/
ADD runner.sh /root/

RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt install openssh-server git python3-pip rsync -y
RUN apt upgrade -y

RUN mkdir /root/ingest
RUN mkdir /root/.ssh

RUN pip3 install -r /root/python_dependencies.txt

RUN chmod +x /root/runner.sh
ENTRYPOINT /root/runner.sh $remote_destination_env