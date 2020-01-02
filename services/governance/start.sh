#!/bin/sh
java -jar /app/spline-web-0.3.9-exec-war.jar \
        -Dspline.mongodb.url=mongodb://mongo/spline \
        -Dspline.persistence.factory=za.co.absa.spline.persistence.mongo.MongoPersistenceFactory
