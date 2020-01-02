FROM alpine:3.10

RUN apk update
RUN apk add vim
RUN apk add curl
RUN apk add --update nodejs nodejs-npm

RUN mkdir /app
COPY package.json /app/package.json
COPY package-lock.json /app/package-lock.json
COPY server.js /app/server.js
COPY resources /app/resources

WORKDIR /app

RUN npm install fastify
RUN npm install --save fastify-static

CMD ["node", "server.js"]
