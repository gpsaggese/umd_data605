#!/bin/bash -xe

IMAGE_NAME=umd_data605_spring2023_example1
CONTAINER_NAME=umd_data605_spring2023_example1
docker run --rm -ti --name $CONTAINER_NAME -p 8888:8888 -p 8881:8881 -p 5432:5432 -v $(pwd):/data $IMAGE_NAME
