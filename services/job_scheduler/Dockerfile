FROM python:3.7-alpine

RUN apk update && \
    apk add bash vim curl wget maven openssh-keygen

RUN apk add --no-cache alpine-sdk libffi-dev && \
    pip3 install --no-cache --upgrade pip setuptools wheel && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi

RUN mkdir /app

COPY backend /app/backend
RUN cd /app/backend && pip3 install -r requirements.txt

WORKDIR /app/backend

CMD ["python3", "entrypoint.py"]
