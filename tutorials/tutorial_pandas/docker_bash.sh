#!/bin/bash -xe

IMAGE_NAME=umd_data605_spring2023_pandas
CONTAINER_NAME=$IMAGE_NAME
docker run --rm -ti --name $CONTAINER_NAME -p 8888:8888 -p 5432:5432 -v $(pwd):/data $IMAGE_NAME
