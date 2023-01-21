#!/bin/bash -x

REPO_NAME=gpsaggese
IMAGE_NAME=umd_data605_mongodb
FULL_IMAGE_NAME=$REPO_NAME/$IMAGE_NAME

docker image ls | grep $FULL_IMAGE_IMAGE_NAME
docker image ls | grep $FULL_IMAGE_IMAGE_NAME | awk '{print $1}' | xargs -n 1 -t docker image rm -f
docker image ls
