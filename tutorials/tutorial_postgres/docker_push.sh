#!/bin/bash -xe

docker login --username gpsaggese --password-stdin <~/.docker/passwd.gpsaggese.txt

IMAGE_NAME=umd_data605_postgres
docker images $IMAGE_NAME
docker push docker.io/gpsaggese/$IMAGE_NAME
