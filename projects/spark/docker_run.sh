#!/bin/bash -xe

IMAGE_NAME=umd_data05_spring2023_spark
CONTAINER_NAME=umd_data05_spring2023_spark
docker run --rm -ti --name $CONTAINER_NAME -p 8888:8888 -v $(pwd):/data $IMAGE_NAME
