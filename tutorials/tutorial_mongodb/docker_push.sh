#!/bin/bash -xe

REPO_NAME=gpsaggese
IMAGE_NAME=umd_data605_mongodb
FULL_IMAGE_NAME=$REPO_NAME/$IMAGE_NAME

docker login --username $REPO_NAME --password-stdin <~/.docker/passwd.$REPO_NAME.txt

docker images $FULL_IMAGE_NAME
docker push $FULL_IMAGE_NAME
