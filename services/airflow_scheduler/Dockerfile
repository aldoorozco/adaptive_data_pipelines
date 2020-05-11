FROM puckel/docker-airflow:1.10.4

USER root

COPY requirements.txt /root/requirements.txt

RUN apt update -y && \
    apt install -y python3 python3-pip && \
    cd /root && pip3 install -r requirements.txt

USER airflow
