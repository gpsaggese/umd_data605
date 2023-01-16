#!/bin/bash -xe

IMAGE_NAME=umd_data605_postgres
REPO_NAME=gpsaggese

CONTAINER_NAME=$IMAGE_NAME
CONTAINER_ID=$(docker container ls | grep $IMAGE_NAME | awk '{print $1}')
docker exec -it $CONTAINER_ID bash
