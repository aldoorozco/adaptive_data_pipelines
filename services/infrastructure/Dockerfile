FROM python:3.7-alpine

RUN apk update && \
    apk add openssh-keygen vim curl openssh

ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache alpine-sdk libffi-dev && \
    pip3 install --no-cache --upgrade pip setuptools wheel && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi

RUN apk add terraform

RUN mkdir /app
COPY terraform /app/terraform
COPY backend /app/backend

RUN cd /app/backend && pip3 install -r requirements.txt

RUN cd /app/terraform/AWS && \
    rm -rf .terraform deploy* && \
    cat /dev/zero | ssh-keygen -q -N "" -f deploy

WORKDIR /app/backend

CMD ["python3", "entrypoint.py"]
