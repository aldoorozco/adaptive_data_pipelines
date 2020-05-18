FROM python:3.7-alpine

RUN apk update && \
    apk add bash vim curl wget maven openssh-keygen && \
    apk fetch openjdk8 && \
    apk add openjdk8 && \
    echo "Downloading.." && \
    wget -O spark.tgz https://downloads.apache.org/spark/spark-2.4.5/spark-2.4.5-bin-hadoop2.7.tgz && \
    echo "Unzipping.." && \
    tar -zxf spark.tgz && \
    mkdir -p /opt && \
    echo "Moving.." && \
    mv spark-2.4.5-bin-hadoop2.7 /opt/spark

ENV SPARK_HOME=/opt/spark
ENV JAVA_HOME=/usr
ENV PYTHONUNBUFFERED=1
ENV PATH="${SPARK_HOME}/bin:${PATH}"

RUN apk add --no-cache alpine-sdk libffi-dev && \
    pip3 install --no-cache --upgrade pip setuptools wheel && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi

RUN mkdir /app

COPY backend /app/backend
RUN cd /app/backend && pip3 install -r requirements.txt

WORKDIR /app/backend

CMD ["python3", "entrypoint.py"]
