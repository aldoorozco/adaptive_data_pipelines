#!/bin/sh

ip=$(curl -s https://api.ipify.org)
sed -i "s/{fastifyIp}/$ip/g" /app/resources/js/main.js
