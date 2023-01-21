#!/bin/bash -xe

IMAGE_NAME=umd_data605_mongodb

docker login --username gpsaggese --password-stdin <~/.docker/passwd.gpsaggese.txt

docker images $IMAGE_NAME
docker push docker.io/gpsaggese/$IMAGE_NAME
