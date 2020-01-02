FROM alpine:3.10

RUN apk update
RUN apk fetch openjdk8
RUN apk add openjdk8

RUN mkdir /app
COPY ./spline-web-0.3.9-exec-war.jar /app/spline-web-0.3.9-exec-war.jar
COPY ./start.sh /app/start.sh

RUN chmod 777 /app/start.sh

CMD /app/start.sh
