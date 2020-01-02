FROM alpine:3.10

RUN apk update && \
    apk add bash vim curl wget maven openssh-keygen && \
    apk fetch openjdk8 && \
    apk add openjdk8 && \
    echo "Downloading.." && \
    wget -O spark.tgz https://www-us.apache.org/dist/spark/spark-2.4.4/spark-2.4.4-bin-hadoop2.7.tgz &> /dev/null && \
    echo "Unzipping.." && \
    tar -zxf spark.tgz && \
    mkdir -p /opt && \
    echo "Moving.." && \
    mv spark-2.4.4-bin-hadoop2.7 /opt/spark

ENV SPARK_HOME=/opt/spark
ENV JAVA_HOME=/usr
ENV PYTHONUNBUFFERED=1
ENV PATH="${SPARK_HOME}/bin:${PATH}"

RUN echo "**** Install Python ****" && \
    apk add --no-cache python3 python3-dev alpine-sdk libffi-dev && \
    if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \
    \
    echo "**** Install pip ****" && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    apk add build-base && \
    pip3 install --no-cache --upgrade pip setuptools wheel && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi

RUN mkdir /app

COPY backend /app/backend
COPY ../credentials /root/.aws/credentials
RUN cd /app/backend && pip3 install -r requirements.txt

WORKDIR /app/backend

CMD ["python3", "entrypoint.py"]
