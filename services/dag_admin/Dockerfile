FROM alpine:3.10

RUN apk update && \
    apk add --no-cache openssh-keygen
RUN apk add vim
RUN apk add curl
RUN apk add maven
RUN apk fetch openjdk8
RUN apk add openjdk8

ENV PYTHONUNBUFFERED=1

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
COPY template /app/template
RUN cd /app/template && mvn package

COPY backend /app/backend
RUN cd /app/backend && pip3 install -r requirements.txt

WORKDIR /app/backend

CMD ["python3", "entrypoint.py"]
